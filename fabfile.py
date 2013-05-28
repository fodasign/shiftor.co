import pip, os
from fabric.api import local

def less ():
    local("lessc -x static/bootstrap/less/bootstrap.less > static/css/style.css")

def freeze ():
    local("pip freeze > requirements.txt")
    local("git add requirements.txt")
    local("git commit -v")

def upgrade ():
    for dist in pip.get_installed_distributions():
        local("pip install --upgrade {0}".format(dist.project_name))

def load_env ():
    try:
        with open(".env") as f:
            content = f.readlines()
        for var in content:
            k, v = var.strip().split("=")
            os.environ[k] = v
    except IOError:
        # Guess this is being run on Heroku
        pass

def manage (cmd, prefix="python"):
    load_env()
    local("{0} jakt/manage.py {1}".format(prefix, cmd))

def migrate (app=None, flags=None):
    cmd = "migrate"
    if app:
        cmd += " {0}".format(app)
    if flags:
        cmd += " {0}".format(flags)
    manage(cmd)

def schemamigrate (app, flags="--auto"):
    manage("schemamigration {0} {1}".format(app, flags))

def syncdb ():
    manage("syncdb")

def shell ():
    manage("shell", prefix="ipython")

def backup (app="silk-prod"):
    local("heroku pgbackups:capture --app {app} --expire".format(app=app))

def transfer (from_app="silk-prod", to_app="silk-dev"):
    backup(app=from_app)
    backup(app=to_app)

    local("heroku pgbackups:restore DATABASE `heroku pgbackups:url --app {from_app}` --app {to_app}".format(from_app=from_app, to_app=to_app))
