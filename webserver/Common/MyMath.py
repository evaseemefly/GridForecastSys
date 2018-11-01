
def getRundingVal(val ,interval):
    '''
        将传入的浮点类型四舍五入
    :param val:
    :return:
    '''


def getRundingVal(val, interval):
    '''
        将传入的浮点类型四舍五入
    :param val:
    :return:
    '''
    # 17.975,17.233

    finial_index = 0
    # 1 取整数部分 eg:18  eg2:17
    rundingIndex = round(val)

    # 2 四舍五入到小数点后2位 eg:17.98,eg2:17.23
    rundingVal = round(val, 2)

    # 3-1 向上取整
    if rundingIndex > rundingVal:
        # 说明四舍五入后的整数部分大于原值 eg:17.75
        if abs((rundingIndex - interval) - rundingVal) < abs(rundingIndex - rundingVal):
            finial_index = rundingIndex - interval
        else:
            finial_index = rundingIndex
    # 3-2 向下取整 eg2:17.23
    else:
        if abs((rundingIndex + interval) - rundingVal) < abs(rundingIndex - rundingVal):
            finial_index = rundingIndex + interval
        else:
            finial_index = rundingIndex
    return rundingIndex
