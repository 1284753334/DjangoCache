import random
from io import BytesIO
from time import sleep

# from django.core.cache import cache
from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw,Draw

from django.core import paginator
from django.core.cache import caches
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from App.models import Student
from App.utils import generate_code, get_color
from DjangoCache import settings


def index(request):
    return HttpResponse('hello')


# @cache_page(30)
def news(request):
    # 添加两个缓存事件后,新增一行
    cache = caches['redis_backend']
    result = cache.get('news')
    if result:
        HttpResponse(result)
    new_list = []
    for i in range(10):
        new_list.append('最近芯片火热%d' % i)
    sleep(5)
    data = {
        'news_list': new_list
    }
    response = render(request, 'news.html', context=data)
    cache.set('news', response, timeout=60)

    return response


@cache_page(60, cache='default')
def jokes(request):
    sleep(5)
    return HttpResponse('Jokes_list')


def home(request):
    return HttpResponse('home')


def getphone(request):
    a = random.randrange(100)
    print(a)
    if a > 95:
        return HttpResponse('恭喜你抢到新款手机%d' % a)

    return HttpResponse('正在排队%d' % a)


def getticket(request):
    return HttpResponse("还剩余99张票满100-99")


def search(request):
    return HttpResponse("这是你搜索到的种子资源")


def calc(request):
    a = 250
    b = 150
    result = (a + b) / 0

    return HttpResponse(result)


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        receive_code = request.POST.get('verify_code')
        store_code = request.session.get('verify_code')
        # lower()  不区分大小写
        if receive_code.lower() != store_code.lower():
            return redirect(reverse('app:login'))
        return HttpResponse('登录成功')



def addsts(request):
    for i in range(100):
        student = Student()
        student.s_name = 'Tom%d' % i
        student.s_age = i
        student.save()
    return HttpResponse("学生创建成功")


# 分页原生实现
def getsts(request):
    # 原生实现{{
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))

    students = Student.objects.all()[per_page * (page - 1):page * per_page]
    # 原生实现}}

    return render(request, 'sdudents_list.html', context=locals())


# 使用分页器
def addstspage(request):
    # 默认为1
    page = int(request.GET.get('page', 1))
    # 每页默认10条
    per_page = int(request.GET.get('per_page', 10))
    students = Student.objects.all()
    paginator = Paginator(students, per_page)
    # 获取具体的某一页
    page_object = paginator.page(page)
    data = {
        'page_object': page_object,
        'page_range': paginator.page_range
    }

    return render(request, 'sts_page.html', context=data)


# def addstspage(request, type):
#     # 导入的Student模型
#     students = Student.objects.all()
#     p = Paginator(students, 10)  # 分页，10篇文章一页
#     if p.num_pages <= 1:  # 如果文章不足一页
#         students_list = students  # 直接返回所有文章
#         data = ''  # 不需要分页按钮
#     else:
#         page = int(request.GET.get('page', 1))  # 获取请求的文章页码，默认为第一页
#         students_list = p.page(page)  # 返回指定页码的页面
#         left = []  # 当前页左边连续的页码号，初始值为空
#         right = []  # 当前页右边连续的页码号，初始值为空
#         left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
#         right_has_more = False  # 标示最后一页页码前是否需要显示省略号
#         first = False  # 标示是否需要显示第 1 页的页码号。
#         # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
#         # 其它情况下第一页的页码是始终需要显示的。
#         # 初始值为 False
#         last = False  # 标示是否需要显示最后一页的页码号。
#         total_pages = p.num_pages
#         page_range = p.page_range
#         if page == 1:  # 如果请求第1页
#             right = page_range[page:page + 2]  # 获取右边连续号码页
#             if right[-1] < total_pages - 1:  # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
#                 # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
#                 right_has_more = True
#             if right[-1] < total_pages:  # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
#                 # 所以需要显示最后一页的页码号，通过 last 来指示
#                 last = True
#         elif page == total_pages:  # 如果请求最后一页
#             left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
#             if left[0] > 2:
#                 left_has_more = True  # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
#             if left[0] > 1:  # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
#                 first = True
#         else:  # 如果请求的页码既不是第一页也不是最后一页
#             left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 获取左边连续号码页
#             right = page_range[page:page + 2]  # 获取右边连续号码页
#             if left[0] > 2:
#                 left_has_more = True
#             if left[0] > 1:
#                 first = True
#             if right[-1] < total_pages - 1:
#                 right_has_more = True
#             if right[-1] < total_pages:
#                 last = True
#         data = {  # 将数据包含在data字典中
#             'left': left,
#             'right': right,
#             'left_has_more': left_has_more,
#             'right_has_more': right_has_more,
#             'first': first,
#             'last': last,
#             'total_pages': total_pages,
#             'page': page
#         }
#     return render(request, 'sts_page.html', context={'students_list': students_list, 'data': data})
def getcode(request):
    # 初始化画布，画笔
    mode = 'RGB'
    size = (200, 100)
    red = get_color()
    green = get_color()
    blue = get_color()
    # 三个 255 背景白色
    color_bg = (255, 255,255)
    image = Image.new(mode=mode, size=size, color=color_bg)
    imagedraw = ImageDraw(image, mode=mode)

    imagefont= ImageFont.truetype(settings.FONT_PASH,120)

    verify_code = generate_code()
    # 验证码内容存储到服务器
    request.session['verify_code']=verify_code

    for i in range(4):
        fill=(get_color(),get_color(),get_color(),get_color())
        imagedraw.text(xy=(45*i,0), text=verify_code[i],font=imagefont,fill=fill)
    for i in range(1000):
        fill = (get_color(), get_color(), get_color(), get_color())
        xy = (random.randrange(200),random.randrange(100))
        imagedraw.point(xy=xy,fill=fill)
        # imagedraw.line(xy=xy,fill= blue,width=99)

    fp = BytesIO()
    image.save(fp, 'png')


    return HttpResponse(fp.getvalue(),content_type='image/png')




