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
        run('pip install -r requirements.txt')

def re_link_nginx_config():
    with cd(NGINX_CONF_DIR):
        sudo('ln -s --force {}_conf/img-resizer.nginx'.format(WEB_ROOT))

def _reload_nginx_config():
    sudo('service nginx reload')

def _update_server_status_in_nginx(i, down=True):
    if down:
        sudo('sed --follow-symlinks --in-place "s/$1:800{0};/$1:800{0} down;/" {1}*'.format(i, NGINX_CONF_DIR))
    else:
        sudo('sed --follow-symlinks --in-place "s/$1:800{0} down;/$1:800{0};/" {1}*'.format(i, NGINX_CONF_DIR))
    _reload_nginx_config()

def restart_supervisor_processes():
    for i in xrange(4):
        _update_server_status_in_nginx(i)
        sudo('supervisorctl restart img-resizer:{}'.format(i))
        _update_server_status_in_nginx(i, down=False)

def build_and_deploy():
    deploy_api()
    build_virtual_env()
    re_link_nginx_config()
    restart_supervisor_processes()
