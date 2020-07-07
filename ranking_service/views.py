import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from tools.change_type import change_type
from tools.my_redis_connect import MyRedisConnect


def server_index(request):
    return render(request, 'ranking.html')


class RankingService(MyRedisConnect):

    def get(self, request):
        user = request.GET.get('user')
        num1_str = request.GET.get('num1')
        num2_str = request.GET.get('num2')

        if num1_str and num2_str:
            num1 = change_type(num1_str)
            num2 = change_type(num2_str)
            if not num1 or not num2:
                return JsonResponse({'code': 2000, 'error': '请输入整数'})

            if num1 > num2 or num1 < 1 or num2 < 2:
                return JsonResponse({'code': 2001, 'error': '范围输入有误'})

        elif num1_str and not num2_str:
            num1 = change_type(num1_str)
            num2 = 10000000
            if not num1:
                return JsonResponse({'code': 2002, 'error': '请输入整数'})
            if num1 < 1:
                return JsonResponse({'code': 2003, 'error': '范围输入有误'})

        elif not num1_str and num2_str:
            num1 = 1
            num2 = change_type(num1_str)
            if not num2:
                return JsonResponse({'code': 2004, 'error': '请输入整数'})
            if num2 < 2:
                return JsonResponse({'code': 2005, 'error': '范围输入有误'})

        else:
            num1 = 1
            num2 = 10000000

        try:
            # 尝试获取客户端号排名
            user_rank = self.get_member_rank(settings.ORDERED_SET_KEY, user)

        except Exception as e:
            print(e)
            return JsonResponse({'code': 2006, 'error': '客户端号不存在'})

        # 获取排行客户端号与分数 -> 降序排列
        res = self.get_ordered_set(settings.ORDERED_SET_KEY, num1, num2)

        if not res:
            return JsonResponse({'code': 2007, 'error': '没有数据'})

        data_list = []
        target_user = {}
        # 获取每个客户端号的排名 并 存储所需信息
        for u in res:
            data_dict = {}
            data_dict['user'] = u[0]
            data_dict['score'] = u[1]
            data_dict['rank'] = self.get_member_rank(settings.ORDERED_SET_KEY, u[0])

            if u[0] == user:
                target_user = data_dict

            data_list.append(data_dict)

        if len(data_list) ==1:
            data_list = {}

        return JsonResponse({'code': 200,
                             'data': data_list,
                             'target_user': target_user})

    def post(self, request):

        ordered_set_key = settings.ORDERED_SET_KEY

        json_obj = json.loads(request.body)
        user = json_obj.get('user')
        score_str = json_obj.get('score')

        score = change_type(score_str)
        if not score:
            return JsonResponse({'code': 1000, 'error': '分数要求整数'})

        if score < 1 or score > 10000000:
            return JsonResponse({'code': 1001, 'error': '分数输入有误'})

        res = self.add_ordered_set(ordered_set_key, score, user)

        if res:
            return JsonResponse({'code': 200, 'msg': res})

        else:

            return JsonResponse({'code': 1002, 'error': '提交失败'})

"""
git remote add origin git@github.com:Air-xin/ranking_service.git
git push -u origin master
"""