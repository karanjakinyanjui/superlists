import secrets

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = "https://github.com/karanjakinyanjui/superlists.git"

site_folder = f"/home/{env.user}/sites/{env.host}"
source_folder = site_folder + "/source"
virtualenv_folder = f'{source_folder}/../virtualenv'
bin_folder = f"{virtualenv_folder}/bin"
manage = f"cd {source_folder} && {bin_folder}/python manage.py"


def _create_directory_structure():
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
    settings_path = f"{source_folder}/superlists/settings/py"
    sed(settings_path, "DEBUG = True", "Debug = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        f'ALLOWED HOSTS = ["{site_name}"]'
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


def deploy():
    _create_directory_structure()
    _get_latest_source()
    _update_settings(env.host)
    _update_virtualenv()
    _update_static_files()
    _update_database()
