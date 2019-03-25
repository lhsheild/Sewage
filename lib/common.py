def list_decode(list):
    '''
    将列表内元素解码为UTF-8
    :param list:
    :return:
    '''
    new_list = []
    while list:
        temp = list.pop().decode('utf-8')
        new_list.append(temp)
    return new_list