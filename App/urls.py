from django.conf.urls import url

from App import views
app_name ='app'
urlpatterns = [
    url(r'index/',views.index,name ='index'),
    url(r'^news/',views.news,name= 'news'),
    url(r'^jokes/',views.jokes,name= 'jokes'),
    url(r'^home/',views.home,name= 'home'),
    url(r'^getphone/', views.getphone, name='getphone'),
    url(r'^getticket/', views.getticket, name='getticket'),
    url(r'^search/', views.search, name='search'),
    url(r'^calc/', views.calc, name='calc'),
    url(r'^login/', views.login, name='login'),
    url(r'^addsts/',views.addsts,name = 'addsts'),
    url(r'^getsts/', views.getsts, name='getsts'),
    url(r'^addstspage/', views.addstspage, name='addstspage'),
    url(r'^getcode/', views.getcode, name='getcode'),
]