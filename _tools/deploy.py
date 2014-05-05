import glob
from fabric.api import cd, local, run, put, sudo, prefix
from fabric.contrib.project import rsync_project

WEB_ROOT = '/home/ubuntu/img-resizer/'
NGINX_CONF_DIR = '/etc/nginx/sites-enabled/'

def deploy_api():
    rsync_project(
        remote_dir=WEB_ROOT,
        local_dir='*'
    )

def build_virtual_env():
    with cd(WEB_ROOT), prefix('. /home/ubuntu/.virtualenvs/img-resizer/bin/activate'):
        run('pip install -I -r requirements.txt')

def re_link_nginx_config():
    with cd(NGINX_CONF_DIR):
        sudo('ln -s --force {}_conf/img-resizer.nginx'.format(WEB_ROOT))

def reload_nginx_config():
    sudo('service nginx reload')

def restart_supervisor_processes():
    for i in xrange(4):
        sudo('supervisorctl restart img-resizer:img-resizer-{}'.format(i))

def restart_uwsgi():
    sudo('touch /etc/uwsgi/apps-enabled/img-resizer.uwsgi.ini')

def build_and_deploy():
    deploy_api()
    build_virtual_env()
    re_link_nginx_config()
    reload_nginx_config()
    restart_supervisor_processes()
