# Configuration file for jupyterhub.

import subprocess
import pwd
from jupyterhub.auth import PAMAuthenticator
c = get_config()  # noqa

c.Application.log_datefmt = '%Y%m%d %H:%M:%S'


# c.JupyterHub.bind_url = 'http://192.168.1.53:8000'

# from jupyterhub.auth.generic import LocalAuthenticator


# class CustomLocalAuthenticator(LocalAuthenticator):
#     """
#     カスタムユーザーモデルをサポートする `LocalAuthenticator` クラスです。
#     """

#     custom_user_class = None

#     def get_user(self, username, password):
#         """
#         ユーザー情報を取得します。

#         Args:
#             username: ユーザー名
#             password: パスワード

#         Returns:
#             ユーザー情報
#         """
#         if self.custom_user_class is None:
#             raise ValueError("カスタムユーザーモデルが設定されていません。")

#         user = self.custom_user_class.objects.filter(username=username).first()
#         if user is None or not user.check_password(password):
#             return None

#         return user

c.JupyterHub.db_url = 'postgresql://m5211164:anpanman@postgis:5432/mars'

c.JupyterHub.log_level = 'WARN'

# import sys
# sys.path.insert(0, '/code')
# from accounts.auth_backends import DjangoBackend
# c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.JupyterHub.authenticator_class = 'native'
# c.JupyterHub.authenticator_class = 'jupyterhub.auth.LocalAuthenticator'
# c.JupyterHub.authenticator_class = 'DjangoBackend'
# c.JupyterHub.authenticator_class = 'accounts.auth_backends.DjangoBackend'
c.NativeAuthenticator.open_signup = True
# c.Authenticator = CustomLocalAuthenticator()
# c.Authenticator = LocalAuthenticator()
# c.Authenticator.auth_backend = "django"
# c.Authenticator.custom_user_class = "accounts.models.CustomUser"

c.Spawner.args = ['--log-level=WARN']
c.Spawner.default_url = '/lab'
# Jupyterlabで作成されたノートブックファイルなどが格納されるディレクトリ
c.Spawner.notebook_dir = "/data/users/{username}"

# ユーザーごとのディレクトリの基本パス
base_user_directory = '/data/groups'


def pre_spawn_hook(spawner):
    username = spawner.user.name
    try:
        pwd.getpwnam(username)
    except KeyError:
        subprocess.check_call(
            ['sh', '/srv/jupyterhub/hook-script/make-user-directory.sh', username]
        )

    # # ユーザーが所属する全てのグループを取得
    # user_groups = spawner.user.groups

    # # ユーザーが所属する全てのグループディレクトリへのパスを作成
    # group_directories = [f"/data/groups/{str(group).split()[1]}" for group in user_groups]

    # # ユーザーに複数のディレクトリを表示
    # spawner.notebook_dir += ','.join(group_directories)


c.Spawner.pre_spawn_hook = pre_spawn_hook

c.Authenticator.admin_users = {'testadmin'}
# c.Authenticator.allowed_users = {'testuser01'}

c.Authenticator.users = [
    {
        'username': 'testuser01',
        'groups': ['group1', 'group2'],
    },
    {
        'username': 'testuser02',
        'groups': ['group2'],
    },
]
c.Authenticator.auto_group_users = True
