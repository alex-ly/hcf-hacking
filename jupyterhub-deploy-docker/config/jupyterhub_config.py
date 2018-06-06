# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

from dockerspawner import DockerSpawner

c = get_config()

class DemoFormSpawner(DockerSpawner):
    def _options_form_default(self):
        default_stack = "jupyter/minimal-notebook"
        return """
        <label for="stack">Select your desired stack</label>
        <select name="stack" size="1">
        <option value="jupyter/r-notebook">R: </option>
        <option value="jupyter/tensorflow-notebook">Tensorflow: </option>
        <option value="jupyter/datascience-notebook">Datascience: </option>
        <option value="jupyter/all-spark-notebook">Spark: </option>
        </select>
        """.format(stack=default_stack)

    def options_from_form(self, formdata):
        options = {}
        options['stack'] = formdata['stack']
        container_image = ''.join(formdata['stack'])
        print("SPAWN: " + container_image + " IMAGE" )
        self.container_image = container_image
        return options

c.JupyterHub.spawner_class = DemoFormSpawner

#c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_NOTEBOOK_IMAGE']
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })

# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }

#notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
#c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.notebook_dir = "/home/jovyan"

prefix = os.environ.get('USER_PROBLEMSETS_PREFIX', '')
c.DockerSpawner.volumes = { 
        ('%s-{username}' % prefix) : "/home/jovyan/problemsets" 
        }

c.DockerSpawner.remove_containers = True
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# TLS config
c.JupyterHub.port = 8000

#
# Authenticate users with Google
#
### c.GoogleOAuthenticator.oauth_callback_url = "http://db.science.uoit.ca:8000/hub/oauth_callback"
### c.GoogleOAuthenticator.client_id = os.environ['GOOGLE_CLIENT_ID']
### c.GoogleOAuthenticator.client_secret = os.environ['GOOGLE_CLIENT_SECRET']
### from oauthenticator import GoogleOAuthenticator
### class MyGoogleOAuthenticator(GoogleOAuthenticator):
###     async def authenticate(self, handler, data=None):
###         user = await super().authenticate(handler, data)
###         if '@' in user['name']:
###             user['name'] = user['name'].replace('@', '-at-')
###         return user
### 
### c.JupyterHub.authenticator_class = MyGoogleOAuthenticator

#
# Authenticate users with my own
#
from jupyterhub.auth import Authenticator
import re

class DebugAuthenticator(Authenticator):
    async def authenticate(self, handler, data):
        name = data["username"]
        password = data["password"]

        if password == "jjj" and re.match(r'^[\w-]+$', name):
            return dict(name=name)
        else:
            return None

c.JupyterHub.authenticator_class = DebugAuthenticator

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir, 'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
)

# Whitlelist users and admins
#c.Authenticator.whitelist = whitelist = set()
#c.Authenticator.admin_users = admin = set()
#c.JupyterHub.admin_access = True
#pwd = os.path.dirname(__file__)
#with open(os.path.join(pwd, 'userlist')) as f:
#    for line in f:
#        if not line:
#            continue
#        parts = line.split()
#        name = parts[0]
#        whitelist.add(name)
#        if len(parts) > 1 and parts[1] == 'admin':
#            admin.add(name)

c.JupyterHub.base_url = "/course/"
