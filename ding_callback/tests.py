import requests
import os
import json
import datetime
import itertools

from conf import my_setting


def save_img(list):
    try:
        for i, j in enumerate(list):
            print(i, j)
            r = requests.get(j, stream=True)
            with open(str(i) + '.jpg', 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            r.close()
            print("downloading picture succed!")

    except IOError as e:
        print(e)
    except Exception as e:
        print(e)
    # time.sleep(2)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sewage.settings")
    import django

    django.setup()

    from ding_callback import models
    from lib.common import list_split

    monitor_obj = models.MonitorPoint.objects.filter(id=2).first()
    sample_photo = monitor_obj.sample.all().values_list('sample_photo', flat=True).distinct()
    sample_photo = list(sample_photo)
    lst = []
    for i in sample_photo:
        if i:
            i = json.loads(i)
            lst.extend(i)
    sample_photo = lst
    sample_photo = list_split(sample_photo)
    print(sample_photo)