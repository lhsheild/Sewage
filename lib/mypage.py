class Page(object):
    def __init__(self, page, total_count, class_url, per_page=10, max_page=11):
        """
        :param page:当前页面
        :param total_count:对象数量
        :param class_url:url前缀
        :param per_page:每页显示数量
        :param max_page:页码导航条显示的页数
        """
        super(Page, self).__init__()

        self.p = page
        total_page, m = divmod(total_count, per_page)
        if m:
            total_page += 1

        self.total_page = total_page
        try:
            self.p = int(self.p)
            if self.p > total_page:
                self.p = self.total_page
        except Exception as e:
            self.p = 1

        # 当前页面的数据在数据库的取值范围
        self.data_start = (self.p - 1) * per_page
        self.data_end = self.p * per_page

        self.max_page = max_page
        if self.total_page < self.max_page:
            self.max_page = self.total_page

        self.half_max_page = self.max_page // 2

        self.page_start = self.p - self.half_max_page
        self.page_end = self.p + self.half_max_page
        if self.page_start <= 1:
            self.page_start = 1
            self.page_end = self.max_page
        if self.page_end >= self.total_page:
            self.page_end = self.total_page
            self.page_start = self.total_page - self.max_page + 1

        self.url_prefix = class_url

    def page_html(self):
        html_str_list = []  # 后台拼接前端页码控件
        html_str_list.append('<li><a href="/{}/?page=1">首页</a></li>'.format(self.url_prefix))
        if self.p <= 1:
            html_str_list.append('<li class="disabled"><a href="#" aria-label="Previous"><span '
                                 'aria-hidden="true">&laquo;</span></a></li>')
        else:
            html_str_list.append('<li><a href="/{}/?page={}" aria-label="Previous"><span '
                                 'aria-hidden="true">&laquo;</span></a></li>'.format(self.url_prefix, self.p - 1))
        for i in range(self.page_start, self.page_end + 1):
            if i == self.p:
                tmp = '<li class="active"><a href="/{0}/?page={1}">{1}</a></li>'.format(self.url_prefix, i)
            else:
                tmp = '<li><a href="/{0}/?page={1}">{1}</a></li>'.format(self.url_prefix, i)
            html_str_list.append(tmp)

        if self.p >= self.total_page:
            html_str_list.append('<li class="disabled"><a href="#" aria-label="Previous"><span '
                                 'aria-hidden="true">&raquo;</span></a></li>')
        else:
            html_str_list.append('<li><a href="/{}/?page={}" aria-label="Previous"><span '
                                 'aria-hidden="true">&raquo;</span></a></li>'.format(self.url_prefix, self.p + 1))
        html_str_list.append('<li><a href="/{}/?page={}">尾页</a></li>'.format(self.url_prefix,  self.total_page))

        return html_str_list


class Page2(object):
    def __init__(self, page, total_count, class_url, per_page=10, max_page=11):
        super(Page2, self).__init__()

        self.p = page
        total_page, m = divmod(total_count, per_page)
        if m:
            total_page += 1

        self.total_page = total_page
        try:
            self.p = int(self.p)
            if self.p > total_page:
                self.p = self.total_page
        except Exception as e:
            self.p = 1

        # 当前页面的数据在数据库的取值范围
        self.data_start = (self.p - 1) * per_page
        self.data_end = self.p * per_page

        self.max_page = max_page
        if self.total_page < self.max_page:
            self.max_page = self.total_page

        self.half_max_page = self.max_page // 2

        self.page_start = self.p - self.half_max_page
        self.page_end = self.p + self.half_max_page
        if self.page_start <= 1:
            self.page_start = 1
            self.page_end = self.max_page
        if self.page_end >= self.total_page:
            self.page_end = self.total_page
            self.page_start = self.total_page - self.max_page + 1

        self.url_prefix = class_url

    def page_html(self):
        html_str_list = []  # 后台拼接前端页码控件
        html_str_list.append('<li><a href="/{}&page=1">首页</a></li>'.format(self.url_prefix))
        if self.p <= 1:
            html_str_list.append('<li class="disabled"><a href="#" aria-label="Previous"><span '
                                 'aria-hidden="true">&laquo;</span></a></li>')
        else:
            html_str_list.append('<li><a href="/{}&page={}" aria-label="Previous"><span '
                                 'aria-hidden="true">&laquo;</span></a></li>'.format(self.url_prefix, self.p - 1))
        for i in range(self.page_start, self.page_end + 1):
            if i == self.p:
                tmp = '<li class="active"><a href="/{0}&page={1}">{1}</a></li>'.format(self.url_prefix, i)
            else:
                tmp = '<li><a href="/{0}&page={1}">{1}</a></li>'.format(self.url_prefix, i)
            html_str_list.append(tmp)

        if self.p >= self.total_page:
            html_str_list.append('<li class="disabled"><a href="#" aria-label="Previous"><span '
                                 'aria-hidden="true">&raquo;</span></a></li>')
        else:
            html_str_list.append('<li><a href="/{}&page={}" aria-label="Previous"><span '
                                 'aria-hidden="true">&raquo;</span></a></li>'.format(self.url_prefix, self.p + 1))
        html_str_list.append('<li><a href="/{}&page={}">尾页</a></li>'.format(self.url_prefix,  self.total_page))

        return html_str_list