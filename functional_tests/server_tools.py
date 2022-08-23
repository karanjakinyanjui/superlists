from fabric.api import run, env
from fabric.context_managers import settings


def _manage(host, command):
    site_folder = f"/home/user/sites/{host}"
    source_folder = site_folder + "/source"
    virtualenv_folder = f'{site_folder}/virtualenv'
    bin_folder = f"{virtualenv_folder}/bin"
    manage = f"cd {source_folder} && {bin_folder}/python manage.py"
    return run(f"{manage} {command}")


def create_session_on_server(host, email):
    print(env)
    with settings(host_string=f'user@{host}'):
        session_key = _manage(host, f'create_session {email}')
        return session_key.strip()


def reset_database(host):
    with settings(host_string=f'user@{host}'):
        _manage(host, f'flush --noinput')
