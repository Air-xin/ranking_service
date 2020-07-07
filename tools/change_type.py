def change_type(target):
    try:
        res = int(target)

    except Exception as e:
        print(e)
        return False

    if res == 0:
        return -1

    return res
