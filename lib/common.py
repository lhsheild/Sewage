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


def list_split(list):
    '''
    转换列表内照片的地址
    :param list:
    :return:
    '''
    new_list = []
    while list:
        i = list.pop()
        if i and i != 'null':
            temp = i.split('Sewage')[1]
            new_list.append(temp)
    return new_list


# if __name__ == '__main__':
#     lst = ['E:\\Projects\\Python_Projects\\Sewage\\media\\img\\2019\\03\\21\\T1-1_外景_0.jpg', 'E:\\Projects\\Python_Projects\\Sewage\\media\\img\\2019\\03\\21\\T1-1_外景_0.jpg']
#     lst = list_split(lst)
#     print(lst)