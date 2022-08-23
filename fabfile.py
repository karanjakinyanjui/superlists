import secrets

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random

REPO_URL = "https://github.com/karanjakinyanjui/superlists.git"


def init(username='user'):
    sudo(f'useradd -m {username}')
    sudo(f'passwd {username}')
    sudo(f'adduser {username} sudo')
    sudo(f'cp -r .ssh /home/{username}/.ssh')
    sudo(f'chown -R {username} /home/{username}')
    sudo('apt update')
    sudo(f'apt install -y nginx python3 python3-pip python3-venv')


def deploy(email_password):
    site_folder = f"/home/{env.user}/sites/{env.host}"
    source_folder = site_folder + "/source"
    virtualenv_folder = f'{source_folder}/../virtualenv'
    bin_folder = f"{virtualenv_folder}/bin"
    manage = f"cd {source_folder} && {bin_folder}/python manage.py"

    service_template = f"{source_folder}/deploy_config/gunicorn-systemd.template.service"
    nginx_template = f"{source_folder}/deploy_config/nginx.template.conf"

    def _create_directory_structure():
        if not exists(source_folder):
            for sub_folder in ("database", "static", "virtualenv", "source"):
                run(f"mkdir -p {site_folder}/{sub_folder}")

    def _get_latest_source():
        if exists(f"{source_folder}/.git"):
            run(f"cd {source_folder} && git fetch")
        else:
            run(f"git clone {REPO_URL} {source_folder}")
        current_commit = local("git log -n 1 --format=%H", capture=True)
        run(f"cd {source_folder} && git reset --hard {current_commit}")

    def _update_settings(site_name):
        settings_path = f"{source_folder}/superlists/settings.py"
        sed(settings_path, "DEBUG = True", "Debug = False")
        sed(settings_path,
            'ALLOWED_HOSTS = .+$',
            f'ALLOWED_HOSTS = ["{site_name}"]'
            )
        secret_key_file = f'{source_folder}/superlists/secret_key.py'
        if not exists(secret_key_file):
            chars = secrets.token_urlsafe(32)
            key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
            append(secret_key_file, f'SECRET_KEY = "{key}"')
        append(settings_path, '\nfrom .secret_key import SECRET_KEY')

    def _update_virtualenv():
        if not exists(bin_folder):
            run(f'python3 -m venv {virtualenv_folder}')
        run(f'{bin_folder}/pip install -r {source_folder}/requirements.txt')

    def _update_static_files():
        run(f"{manage} collectstatic --noinput")

    def _update_database():
        run(f"{manage} migrate --noinput")

    def _systemctl(action, service):
        sudo(f"systemctl {action} {service}")

    def _start_server():
        sed(nginx_template, "SITENAME", env.host)
        sed(service_template, "SITENAME", env.host)
        sed(service_template, "username", env.user)
        sed(service_template, "EMAIL_PASSWORD", email_password)
        sudo(f'cp {service_template} /etc/systemd/system/gunicorn.service')
        sudo(f'cp {nginx_template} /etc/nginx/sites-available/superlists')
        sudo(f'ln -fs /etc/nginx/sites-available/superlists /etc/nginx/sites-enabled/superlists')
        _systemctl("reload", "nginx")
        _systemctl("daemon-reload", '')
        _systemctl("enable", "gunicorn")
        _systemctl("restart", "gunicorn")

    _create_directory_structure()
    _get_latest_source()
    _update_settings(env.host)
    _update_virtualenv()
    _update_static_files()
    _update_database()
    _start_server()
