from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View
from .models import Task, Hw
from .forms import UserForm, HwForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.contrib import messages


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'assignments/login.html')
    else:
        all_tasks = Task.objects.all()

        query = request.GET.get("q")
        if query:
            all_tasks = Task.objects.filter(
                Q(task_title__icontains=query) |
                Q(course__icontains=query)
            ).distinct()
            return render(request, 'assignments/index.html', {'all_tasks': all_tasks})

        return render(request, 'assignments/index.html', {'all_tasks': all_tasks})


def hw_index(request):
    if not request.user.is_authenticated():
        return render(request, 'assignments/login.html')
    else:
        hws = Hw.objects.all()
        return render(request, 'assignments/hw_index.html', {'hws': hws})


def hw_detail(request, hw_id):
    if not request.user.is_authenticated():
        return render(request, 'assignments/login.html')
    else:
        hw = get_object_or_404(Hw, pk=hw_id)
        task = get_object_or_404(Task, pk=hw.task.id)
        hws = task.hw.all()
        if hw.writer == request.user or request.user.username == 'admin':
            return render(request, 'assignments/hw_detail.html', {'hw': hw})
        else:
            return render(request, 'assignments/detail.html', {'task': task,
                                                               'hws': hws,
                                                               })


def detail(request, task_id):
    if not request.user.is_authenticated():
        return render(request, 'assignments/login.html')
    else:
        task = get_object_or_404(Task, pk=task_id)
        hws = task.hw.all()
        return render(request, 'assignments/detail.html', {'task': task,
                                                           'hws': hws,
                                                           })


def plagdetec(request, task_id):
    if not request.user.is_authenticated():
        return render(request, 'assignments/login.html')
    else:
        task = get_object_or_404(Task, pk=task_id)
        hws = task.hw.all()
        i_range = range(hws.count())
        j_range = range(hws.count())
        return render(request, 'assignments/plagdetec.html', {'task': task,
                                                               'hws': hws,
                                                               'i_range': i_range,
                                                               'j_range': j_range, })


def sim_detail(request, hw_id1, hw_id2):
    if not request.user.is_authenticated():
        return render(request, 'assignments/login.html')
    else:
        hw1 = get_object_or_404(Hw, pk=hw_id1)
        hw2 = get_object_or_404(Hw, pk=hw_id2)
        return render(request, 'assignments/sim_detail.html', {'hw1': hw1, 'hw2': hw2})


# 出现NoReverseMatch错误是因为url里匹配的变量名是task_id, 不是pk
# @permission_required('tasks.add_task')
class TaskCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('tasks.add_task',)
    model = Task
    fields = ['course', 'task_title', 'description']

    def handle_no_permission(self):
        messages.error(self.request, '你没有此行为的权限！')
        return redirect('/assignments/')


class TaskUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('tasks.change_task',)
    model = Task
    fields = ['course', 'task_title', 'description']

    def handle_no_permission(self):
        messages.error(self.request, '你没有此行为的权限！')
        return redirect('/assignments/')


class TaskDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('tasks.delete_task',)
    model = Task
    success_url = reverse_lazy('assignments:index')

    def handle_no_permission(self):
        messages.error(self.request, '你没有此行为的权限！')
        return redirect('/assignments/')


def create_hw(request, task_id):
    if not request.user.is_authenticated():
        return render(request, 'assignments/login.html')
    else:
        task = get_object_or_404(Task, pk=task_id)
        form = HwForm(None or request.POST, request.FILES)
        if form.is_valid():
            task_hws = task.hw.all()
            for h in task_hws:
                if h.hw_title == form.cleaned_data.get("hw_title"):
                    context = {
                        'task': task,
                        'form': form,
                        'error_message': '你已经提交了该作业',
                    }
                    return render(request, 'assignments/hw_form.html', context)
            hw = form.save(commit=False)
            hw.task = task
            hw.writer = request.user
            hw.save()
            return render(request, 'assignments/detail.html', {'task': task})
        context = {
            'task': task,
            'form': form,
        }
        return render(request, 'assignments/hw_form.html', context)


# def update_hw(request, task_id, hw_id):
#     task = get_object_or_404(Task, pk=task_id)
#     hwk = Hw.objects.get(pk=hw_id)
#
#     # form = HwForm(request.POST or None, initial={'task': task, 'hw_title': hwk.hw_title, 'hw_content': hwk.hw_content})
#     form = HwForm(request.POST or None, initial={'task': task})
#     if form.is_valid():
#         task_hws = task.hw.all()
#         for h in task_hws:
#             if h.hw_title == form.cleaned_data.get("hw_title"):
#                 context = {
#                     'task': task,
#                     'form': form,
#                     'error_message': 'You already added that song',
#                 }
#                 return render(request, 'assignments/hw_form.html', context)
#         hw = form.save(commit=False)
#         hw.task = task
#         hw.save()
#         return render(request, 'assignments/detail.html', {'task': task})
#     context = {
#         'task': task,
#         'form': form,
#     }
#     return render(request, 'assignments/hw_form.html', context)


def delete_hw(request, task_id, hw_id):
    if not request.user.is_authenticated():
        return render(request, 'assignments/login.html')
    else:
        task = get_object_or_404(Task, pk=task_id)
        hws = task.hw.all()
        hw = Hw.objects.get(pk=hw_id)
        if hw.writer == request.user or request.user.username == 'admin':
            hw.delete()
            return render(request, 'assignments/detail.html', {'task': task})
        else:
            return render(request, 'assignments/detail.html', {'task': task,
                                                               'hws': hws,
                                                               })


class UserFormView(View):
    form_class = UserForm
    template_name = 'assignments/registration_form.html'

    # display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # submit some user data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # return User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('assignments:index')

        return render(request, self.template_name, {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                all_tasks = Task.objects.all()
                return render(request, 'assignments/index.html', {'all_tasks': all_tasks})
                # return redirect('assignments:index', context={'all_tasks': all_tasks})
            else:
                return render(request, 'assignments/login.html', {'error_message': 'Your account has been disabled'})

        else:
            return render(request, 'assignments/login.html', {'error_message': 'Invalid login'})
    return render(request, 'assignments/login.html')


@login_required
def logout_user(request):
    logout(request)
    # form = UserForm(request.POST or None)
    # context = {
    #     "form": form,
    # }
    return render(request, 'assignments/login.html')





