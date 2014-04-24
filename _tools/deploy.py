import glob
from fabric.api import cd, local, run, put, sudo, prefix
from fabric.contrib.project import rsync_project

WEB_ROOT = '/var/www/img-resizer/'
UWSGI_CONFIG_DIR = '/etc/uwsgi/apps-available/'
NGINX_CONF_DIR = '/etc/nginx/sites-available/'

def deploy_api():
    rsync_project(
        remote_dir=WEB_ROOT,
        local_dir='*'
    )

def build_virtual_env():
    with cd(WEB_ROOT), prefix('. env/bin/activate'):
        run('pip install -q -r requirements.txt')

def deploy_nginx_config():
    put(local_path='_conf/img-resizer.nginx',
        remote_path=NGINX_CONF_DIR,
        use_sudo=True)

def update_nginx_symlink():
    with cd('/etc/nginx/sites-enabled'):
        sudo('ln -s --force ../sites-available/img-resizer.nginx img-resizer.nginx')

def reload_nginx_config():
    sudo('service nginx reload')

def deploy_uwsgi_config():
    put(local_path='_conf/img-resizer.ini',
        remote_path=UWSGI_CONFIG_DIR,
        use_sudo=True)

def update_uwsgi_symlink():
    with cd('/etc/uwsgi/apps-enabled'):
        sudo('ln -s --force ../apps-available/img-resizer.ini img-resizer.ini')

def restart_uwsgi():
    sudo('touch /etc/uwsgi/apps-enabled/img-resizer.ini')

def build_and_deploy():
    deploy_api()
    build_virtual_env()
    deploy_nginx_config()
    update_nginx_symlink()
    reload_nginx_config()
    deploy_uwsgi_config()
    update_uwsgi_symlink()
    restart_uwsgi()
