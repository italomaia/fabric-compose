# Fabric-Compose

Much like boilerplates that make it easy to work with web frameworks, this is a minimal boilerplate on a tool that makes it easy to control `docker-compose` with **python-fabric** during development time. It makes it easier to **build images**, **start containers** and leverage less than straightforward commands. 

# Requirements

* docker
* docker-compose 3.8+
* python3
* python virtualenvironment

# Getting Started

Copy all files to the root of your project (or just clone the damn repo), **configure your services in the docker-compose*.yml** files and you follow the steps below:

```bash
###  creates fabric virtualenv
python3 -m venv venv
# loads virtualenv
. /venv/bin/activate
# install only dependency; do not use plain fabric
pip install fabric3
# initiates all containers in dev environment
fab env:dev up
# run command in a particular image
fab env:dev on:myservice run:"echo 'hello world'"
# list all available commands
fab
```

# Files Explained

**docker-compose.yml**
: define all common rules/configuration here; you **should** modify this file

**docker-compose-dev.yml**
: define all development only rules/configuration here; you **should** modify this file

**docker-compose-prd.yml**
: define all production only rules/configuration here; you **should** modify this file

**env_dev.ini**
: define all non-sensitive development configuration here; you **should** modify this file

**env_prd.ini**
: define all non-sensitive production configuration here; you **should** modify this file

**fabfile.py**
: all fabric tasks are defined inside this file; check this file; add your own tasks too!