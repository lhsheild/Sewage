from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator

from ding_callback import models as monitor_model
from lib.login import check_login


# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user == 'admin' and pwd == 'admin':
            next_url = request.GET.get('next')
            if next_url:
                rep = redirect(next_url)
            else:
                rep = redirect('/index/')
            # rep.set_signed_cookie('is_login', '1', salt='sewage')  # max_age=7*24*60*60（一周）cookie
            # 设置session
            request.session['is_login'] = '1'
            return rep


class Logout(View):
    def get(self, request):
        # rep = redirect('/login/')
        # rep.delete_cookie('is_login')
        request.session.flush()
        return redirect('/login/')

    def post(self, request):
        pass


class MonitorInfo(View):  # 监测点列表查询
    @method_decorator(check_login)
    def get(self, request):
        from lib.mypage import Page
        p = request.GET.get('p')
        monitors = monitor_model.MonitorPoint.objects.all()
        total_count = monitors.count()
        monitor_page = Page(p, total_count, 'monitor')
        monitor_data_start = monitor_page.data_start
        monitor_data_end = monitor_page.data_end
        monitor_page_html = monitor_page.page_html()
        current_page_monitors = monitors[monitor_data_start:monitor_data_end]
        return render(request, 'monitorInfo.html', {'monitors': current_page_monitors, 'total_page': monitor_page_html})

    @method_decorator(check_login)
    def post(self, request):  # 根据条件查询监测点信息
        req_dic = request.POST
        func = req_dic.get('mFunc')
        people = req_dic.get('mPeople')
        date_start = req_dic.get('mDateStart')
        date_end = req_dic.get('mDateEnd')
        if func and people and date_start and date_end:
            monitors = monitor_model.MonitorPoint.objects.filter(work_function=func, people=people, start_time__gte=date_start, start_time__lt=date_end)
        elif func and people and date_start:
            monitors = monitor_model.MonitorPoint.objects.filter(work_function=func, people=people, start_time__gte=date_start)
        else:
            monitors = None
        return render(request, 'monitorInfo.html', {'monitors': monitors})


class SampleInfo(View):  # 样品信息查询
    @method_decorator(check_login)
    def get(self, request):
        id = request.GET.get('id')
        monitor_obj = monitor_model.MonitorPoint.objects.filter(id=id)
        if monitor_obj:
            monitor_obj = monitor_obj.first()
        else:
            monitor_obj = monitor_model.MonitorPoint.objects.all().first()
        sample_objs = monitor_obj.sample.all()
        total_count = sample_objs.count()
        from lib.mypage import Page2
        sample_page = Page2(1, total_count, 'sample/?id={}'.format(monitor_obj.id))
        sample_data_start = sample_page.data_start
        sample_data_end = sample_page.data_end
        sample_page_html = sample_page.page_html()
        current_page_samples = sample_objs[sample_data_start:sample_data_end]
        return render(request, 'sampleInfo.html', {
            'monitor': monitor_obj,
            'samples': current_page_samples,
            'total_page': sample_page_html
        })


class FlowInfo(View):  # 流量信息查询
    @method_decorator(check_login)
    def get(self, request):
        id = request.GET.get('id')
        monitor_obj = monitor_model.MonitorPoint.objects.filter(id=id)
        if monitor_obj:
            monitor_obj = monitor_obj.first()
        else:
            monitor_obj = monitor_model.MonitorPoint.objects.all().first()
        flow_objs = monitor_obj.flow.all()
        total_count = flow_objs.count()
        from lib.mypage import Page2
        flow_page = Page2(1, total_count, 'flow/?id={}'.format(monitor_obj.id))
        flow_data_start = flow_page.data_start
        flow_data_end = flow_page.data_end
        flow_page_html = flow_page.page_html()
        current_page_flows = flow_objs[flow_data_start:flow_data_end]
        return render(request, 'flowInfo.html', {
            'monitor': monitor_obj,
            'flows': current_page_flows,
            'total_page': flow_page_html
        })


class Photo(View):
    @method_decorator(check_login)
    def get(self, request):
        import json
        from lib.common import list_split
        id = request.GET.get('id')
        monitor_obj = monitor_model.MonitorPoint.objects.filter(id=id)

        exterior_photo = []
        water_flow_photo = []
        work_photo = []
        status_photo = []
        probe_photo = []
        machine_photo = []
        setup_photo = []
        if monitor_obj:
            monitor_obj = monitor_obj.first()
        else:
            monitor_obj = monitor_model.MonitorPoint.objects.all().first()

        sample_photo = monitor_obj.sample.all().values_list('sample_photo', flat=True).distinct()
        sample_photo = list(sample_photo)
        lst = []
        for i in sample_photo:
            if i:
                i = json.loads(i)
                lst.extend(i)
        sample_photo = lst

        if monitor_obj.exterior_photo:
            exterior_photo = json.loads(monitor_obj.exterior_photo)
            exterior_photo = list_split(exterior_photo)
            # print('exterior_photo:', exterior_photo)
        if monitor_obj.water_flow_photo:
            water_flow_photo = json.loads(monitor_obj.water_flow_photo)
            water_flow_photo = list_split(water_flow_photo)
            # print('water_flow_photo:', water_flow_photo)
        if monitor_obj.work_photo:
            work_photo = json.loads(monitor_obj.work_photo)
            work_photo = list_split(work_photo)
            # print('work_photo:', work_photo)
        if monitor_obj.status_photo:
            status_photo = json.loads(monitor_obj.status_photo)
            status_photo = list_split(status_photo)
            # print('status_photo:', status_photo)
        if monitor_obj.probe_photo:
            probe_photo = json.loads(monitor_obj.probe_photo)
            probe_photo = list_split(probe_photo)
            # print('probe_photo:', probe_photo)
        if monitor_obj.machine_photo:
            machine_photo = json.loads(monitor_obj.machine_photo)
            machine_photo = list_split(machine_photo)
            # print('machine_photo:', machine_photo)
        if monitor_obj.setup_photo:
            setup_photo = json.loads(monitor_obj.setup_photo)
            setup_photo = list_split(setup_photo)
            # print('setup_photo:', setup_photo)
        if monitor_obj.setup_photo:
            setup_photo = json.loads(monitor_obj.setup_photo)
            setup_photo = list_split(setup_photo)
            # print('setup_photo:', setup_photo)
        if sample_photo:
            sample_photo = list_split(sample_photo)
            # print(sample_photo)
        return render(request, 'pictureInfo.html', {
            'monitor': monitor_obj,
            'exterior_photo': exterior_photo,
            'water_flow_photo': water_flow_photo,
            'work_photo': work_photo,
            'status_photo': status_photo,
            'probe_photo': probe_photo,
            'machine_photo': machine_photo,
            'setup_photo': setup_photo,
            'sample_photo': sample_photo
        })


class Export(View):
    def post(self, request):
        pass