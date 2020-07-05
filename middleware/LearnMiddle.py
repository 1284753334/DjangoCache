import random
import time

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

#Mixin  混合  1. 基类。 多继承一般以Mixin结尾
class HelloMiddle(MiddlewareMixin):
    def process_request(self,request):
        print(request.META.get('REMOTE_ADDR'))
        ip = request.META.get('REMOTE_ADDR')
        # if request.path =="/app/getphone/":
        #     if ip == '127.0.0.1':
        #         q =  random.randrange(100)
        #         if q > 50:
        #             return HttpResponse('恭喜你免费获得小米k30 Pro 8+256版%d'%q)
        #     # 黑名单
        # if request.path =='app/getticket':
        #     if ip.startwith('10.0.122.7'):
        #         return HttpResponse('已抢光')
        #
        # if request.path == '/app/search/':
        #     result = cache.get(ip)
        #     if result:
        #         return  HttpResponse('您的访问过于频繁，请10秒后再次搜索')
        #     cache.set(ip, ip ,timeout = 10)
        # 限制 访问  1 分钟 允许 10 次
        # black_list =[]
        # if ip in black_list:
        #     return  HttpResponse('黑名单用户，凉凉')
        #
        # requests = cache.get(ip,[])
        # while requests and time.time() - requests[-1] > 60:
        #     requests.pop()
        #
        # requests.insert(0, time.time())
        # cache.set(ip, requests, timeout=60)
        # if len(requests) > 30:
        #     black_list.append(ip)
        #     cache.set('black',black_list,timeout = 60*60*24)
        #
        #     return HttpResponse("小爬虫，去小黑屋待着吧")
        # if len(requests) > 9:
        #     return HttpResponse('请求次数过于频繁，小爬虫回家睡觉吧')

    # 出错 重定向
    # def process_exception(self,request,exception):
    #     print(request,exception)
    #     return redirect(reverse('app:index'))

class TwoMiddle(MiddlewareMixin):
    def process_request(self,request):
        print('two middle ware')

