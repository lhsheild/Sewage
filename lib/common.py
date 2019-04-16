import os


def list_decode(list):
    """
    将列表内元素解码为UTF-8
    :param list:
    :return:
    """
    new_list = []
    while list:
        temp = list.pop().decode('utf-8')
        new_list.append(temp)
    return new_list


def list_split(list):
    """
    转换列表内照片的地址
    :param list:
    :return:
    """
    new_list = []
    while list:
        i = list.pop()
        if i and i != 'null':
            temp = i.split('Sewage')[1]
            print(temp)
            new_list.append(temp)
    return new_list


def file_iterator(file_name, chunk_size=512):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
