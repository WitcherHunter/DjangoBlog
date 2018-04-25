from fabric.api import env,run
from fabric.operations import sudo

GIT_REPO = 'https://github.com/WitcherHunter/DjangoBlog.git'

env.user = 'maodou'
env.password = 'beibeilove'

env.hosts = 'www.yinzimiao.club'

env.port = '22'

def deploy():
	source_folder = '/home/maodou/sites/www.yinzimiao.club/DjangoBlog'

	run('cd %s && git pull' % source_folder)
	run("""
		cd {} &&
		../Python3/bin/pip install -r requirements.txt &&
		../Python3/bin/python3 manage.py collectstatic --noinput &&
		../Python3/bin/python3 manage.py makemigrations --merge &&
		../Python3/bin/python3 manage.py migrate
		""".format(source_folder))
	sudo('restart www.yinzimiao.club')
	sudo('service nginx reload')