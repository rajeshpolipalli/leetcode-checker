from django.conf.urls import url
from . import views


app_name = 'assignments'

urlpatterns = [
    # /assignments/
    url(r'^$', views.index, name='index'),

    # /assignments/homework/
    url(r'^homework/$', views.hw_index, name='hw_index'),

    # /assignments/register/
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /assignments/login_user/
    url(r'^login_user/$', views.user_login, name='login_user'),

    # /assignments/logout_user/
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    # /assignments/7/
    url(r'^(?P<task_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),

    # /assignments/hw/7
    url(r'^hw/(?P<hw_id>[0-9]+)/$', views.hw_detail, name='hw_detail'),

    # /assignments/task/add/
    url(r'task/add/$', views.TaskCreate.as_view(), name='task-add'),

    # /assignments/task/7/
    url(r'task/(?P<pk>[0-9]+)/$', views.TaskUpdate.as_view(), name='task-update'),

    # /assignments/task/7/delete/
    url(r'task/(?P<pk>[0-9]+)/delete/$', views.TaskDelete.as_view(), name='task-delete'),

    # /assignments/7/hw/add/
    url(r'(?P<task_id>[0-9]+)/hw/add/$', views.create_hw, name='hw-add'),

    # /assignments/7/hw/9
    # url(r'(?P<task_id>[0-9]+)/hw/(?P<hw_id>[0-9]+)/$', views.update_hw, name='hw-update'),

    # /assignments/7/hw/9/delete/
    url(r'(?P<task_id>[0-9]+)/hw/(?P<hw_id>[0-9]+)/delete/$', views.delete_hw, name='hw-delete'),

    # /assignments/7/plagdetec/
    url(r'(?P<task_id>[0-9]+)/plagdetec/$', views.plagdetec, name='plagdetec'),

    # /assignments/sim_detail/3/4/
    url(r'^sim_detail/(?P<hw_id1>[0-9]+)/(?P<hw_id2>[0-9]+)/$', views.sim_detail, name='sim_detail'),
]

