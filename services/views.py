import os
from django import forms
from django.shortcuts import render
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import UploadFileForm, FileTable, File
from cloud.settings import MEDIA_URL, MEDIA_ROOT

# from django.views.generic.edit import FormView
# class FileFieldView(FormView):
#     form_class = UploadFileForm
#     template_name = 'upload.html'  # Replace with your template.
#     success_url = 'index.html'  # Replace with your URL or reverse().
#
#     def post(self, request, *args, **kwargs):
#         print("HERE")
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             for f in files:
#                 request.user.profile.files.append(f)
#                 print(f)
#             request.user.save()
#
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

def index(request):
    if request.user.is_active:
        return welcome(request)
    else:
        return render(request, 'index.html')

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            for f in files:
                file = File(f)
                path = os.path.join(MEDIA_ROOT, request.user.username)

                if not os.path.exists(path):
                    os.mkdir(path)

                path = os.path.join(path, file.name)

                with open(path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                if not file in request.user.profile.files:
                    request.user.profile.files.append(file)

                request.user.save()
            return index(request)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', context={'user': request.user, 'form': UploadFileForm})

def welcome(request):
    data = []
    for file in request.user.profile.files:
        data.append({'name': file.name, 'date': file.date})
    table = FileTable(data)

    print(table)
    return render(request, 'welcome.html', context={'user': request.user, 'table': table})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not active")
        else:
            return HttpResponse("Invalid login details.")

    else:
        return render(request, 'index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def user_account(request):
    if request.method == 'POST':
        old = request.POST.get('password')
        password = request.POST.get('password_n')
        password_conf = request.POST.get('password_nconf')

        if password != password_conf:
            raise(forms.ValidationError("The two password fields must match."))
        if not authenticate(username = request.user.username, password = old):
            raise(forms.ValidationError("Old and new password do not match."))
        else:
            request.user.set_password(password)
            request.user.save()
            return index(request)

    username = request.user.username
    return render(request, 'account.html', context={'user': request.user})
