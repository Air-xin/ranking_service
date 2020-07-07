import redis
from django.views import View

# r = redis.Redis(host='127.0.0.1', port=6379, db=0, password='123456')



class MyRedisConnect(View):

    def __init__(self, host='127.0.0.1', port=6379, db=0):
        super().__init__()
        self.host = host
        self.port = port
        self.db = db
        self.connect_obj()

    # 创建redis链接对象
    def connect_obj(self):
        self.r = redis.Redis(host=self.host,
                             port=self.port,
                             db=self.db,
                             decode_responses=True)

    # 为有序集合添加元素
    def add_ordered_set(self, key, socre, member):
        try:
            res = self.r.zadd(key, {member: socre})

        except Exception as e:
            print(e)
            return False

        else:
            if res == 1:
                return '信息提交成功'
            elif res == 0:
                return '信息更新成功'

    # 按需获取有序集合元素
    def get_ordered_set(self, key, num1=1, num2=0):
        res = self.r.zrange(key, num1 - 1, num2 - 1, withscores=True,desc=True)
        return res

    # 获取有序集合元素排名
    def get_member_rank(self, key, member):
        res = self.r.zrevrank(key, member)
        return res + 1


if __name__ == '__main__':
    r = MyRedisConnect()
    # print(r.add_ordered_set('test_add', 100, 'e'))
    # print(r.add_ordered_set('test_add', 200, 'f'))

    print(r.get_ordered_set('test_add'))
    # [('f', 200.0), ('d', 200.0), ('b', 200.0), ('e', 100.0), ('c', 100.0), ('a', 100.0)]

    print(r.get_ordered_set('test_add', 1, 111))
    # [('f', 200.0), ('d', 200.0), ('b', 200.0), ('e', 100.0), ('c', 100.0), ('a', 100.0)]

    print(r.get_ordered_set('test_add', 1, 3))
    # [('f', 200.0), ('d', 200.0), ('b', 200.0)]

    print(r.get_ordered_set('test_add', 3, 1))
    # []

    print(r.get_ordered_set('test_add', 30, 30))
    # []

    print(r.get_ordered_set('test_add', 99, 1))
    # []

    print(r.get_ordered_set('test_add', 99, 111))
    # []

    print(r.get_member_rank('test_add', 'f'))
    # 1

    # print(r.get_member_rank('test_add', 'gg'))
    # error