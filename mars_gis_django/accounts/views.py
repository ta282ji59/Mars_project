import os
import errno
import requests
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from spectra.models import Spectrum
from . import forms
from .models import Project
from .forms import ProjectCreationForm, ProjectJoinForm
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

# TODO usui ユーザー情報をjupyterhubにも同時作成したい、今は使用していない
@login_required
def create_jupyterhub_user(request):
    # Djangoユーザー情報を取得
    django_user = request.user

    # JupyterHub APIトークン、本来は秘密にする。
    jupyterhub_api_token = '2073ade9d907484e959595a601d7fccc'

    # JupyterHubに新しいユーザーを作成
    # jupyterhub_api_url = 'http://0.0.0.0:8000/hub/api/users'
    jupyterhub_api_url = 'http://192.168.1.53:8000/hub/api/users'
    headers = {'Authorization': f'token {jupyterhub_api_token}'}
    
    response = requests.post(
        jupyterhub_api_url,
        json={'name': django_user.username, 'admin': False},
        headers=headers
    )

    if response.status_code == 201:
        print('success --> create_jupyterhub_user')
        # return render(request, 'success.html', {'message': 'User created successfully'})
    else:
        print('fail --> create_jupyterhub_user')
        # return render(request, 'error.html', {'message': 'Failed to create user'})
    
def create_jupyter_dir(parent_dir, dir_name):
    """ redace1_v5.0/workspace/mars-gis-django/mars-gis-django/jupyterhub/data/ 配下にディレクトリ作成。

    Args:
        parent_dir (_type_): groups or users.
        dir_name (_type_): group or user name.
    """
    # code_dir = os.getcwd()
    # data_dir = os.path.join(code_dir, 'data')
    # parent_dir = os.path.join('/data/', parent_dir)
    parent_dir = f"/data/{parent_dir}"

    try:
        os.makedirs(f"{parent_dir}/{dir_name}")
        # os.makedirs(os.path.join(parent_dir, dir_name))
    except OSError as e:
        if e.errno == errno.EEXIST:
            # フォルダがすでに存在する場合は何もしない
            pass
        else:
            # フォルダの作成に失敗した場合はエラーを表示
            raise

@login_required
def users_home(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = get_object_or_404(get_user_model(), pk=user_id)
        spectra = user.spectrum_set.all()
        qs = Spectrum.objects.all()
        # groups = request.user.groups.all()
        projects = Project.objects.filter(member__in=[user_id])
        project_ids = [project.id for project in projects]
        spectra_test = Spectrum.objects.filter(share_project__in=project_ids)
        # spectra_instrument = [spectrum.instrument for spectrum in spectra_test]

        create_jupyter_dir('users', user.username)
        # create_jupyterhub_user(request)

        settings = {
            'user': user,
            'spectra': spectra,
            'qs':qs,
            # 'groups': groups,
            'projects':projects,
            'spectra_test':spectra_test,
        }
        
        return render(request, "accounts/home.html", settings)
    else:
        return render(request, "accounts/login.html", settings)


@login_required
def create_project(request):
    """ グループディレクトリ作成（作成者）。
        グループだとDjangoのデフォルトのグループと混在したため、プロジェクトにしている。
    """
    if request.method == 'POST':
        print("POST request received")
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            password_hash = make_password(password)
            project = Project(name=name, password=password_hash)
            project.save()
            project.admin.add(request.user)
            project.member.add(request.user)

            # messages.success(request, 'プロジェクトが作成されました。')
            # user_dir = f"users/{name}"
            create_jupyter_dir('groups', name)
            # create_jupyter_dir(f"users/{request.user}", name)
            # code_dir = os.getcwd()
            os.symlink(f"/data/groups/{name}/", f"/data/users/{request.user}/{name}")

            return redirect('accounts:home')
    else:
        form = ProjectCreationForm()
        messages.error(request, '修正内容の保存に失敗しました。')

    return render(request, 'accounts/create_project.html', {'form': form})

@login_required
def join_project(request):
    """ グループディレクトリ作成（参加者）。
        グループだとDjangoのデフォルトのグループと混在したため、プロジェクトにしている。
    """
    if request.method == 'POST':
        form = ProjectJoinForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']

            try:
                project = Project.objects.get(name=name)

                if check_password(password, project.password):
                    project.member.add(request.user)
                    # messages.success(request, 'プロジェクトに参加しました。')
                    create_jupyter_dir(f"users/{request.user}", name)
                    os.symlink(f"groups/{name}", f"users/{request.user}/{name}")

                    return redirect('accounts:home')
                else:
                    messages.error(request, 'パスワードが正しくありません。')
            except Project.DoesNotExist:
                messages.error(request, '指定されたプロジェクトは存在しません。')
    else:
        form = ProjectJoinForm()
        # messages.error(request, '修正内容の保存に失敗しました。')

    return render(request, 'accounts/join_project.html', {'form': form})

