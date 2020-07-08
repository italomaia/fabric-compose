from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import task
from fabric.context_managers import cd

import os

env.forward_agent = True
env.user = 'root'
env.hosts = ['your production host']

project_dst = 'project-name'

compose_cmd = [
    'docker-compose',
    '-f', 'docker-compose.yml',
    '-f',
]

# service to run commands against
SERVICE_NAME = None
ENV = 'dev'  # dev by default
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(CURRENT_DIR, 'app')


def create_compose_cmd() -> list:
    return compose_cmd + ['docker-compose-%s.yml' % ENV]


def call(arg, *args, **kwargs) -> str:
    """
    Returns the correct function call for the environment.
    """
    fn = run if ENV == 'prd' else local
    return fn(' '.join(arg) if type(arg) in (tuple, list) else arg)


def test_cmd_exists(cmd: str) -> bool:
    """
    Tests whether `cmd` executable is in the path.
    """
    msg = '"%s" not found in path. Please, install it to continue.'

    if 'not found' in local('which %s' % cmd, capture=True):
        raise Exception(msg % cmd)


def insert_line_after(lines: list, line: str, after: str) -> None:
    """
    Inserts `line` after the line in `lines` that has
    `after` as a substring.
    """
    for i in range(len(lines)):
        if after in lines[i]:
            lines.insert(i+1, line)
            break


def replace_line(lines: list, line: str, condition: str) -> None:
    """
    Replaces the line in `lines` that has `condition` as a substring
    with `line`.
    """
    for i in range(len(lines)):
        if condition in lines[i]:
            lines[i] = line
            break


@task(name='env')
def set_env(local_env):
    "Sets docker-compose environment"
    global ENV

    ENV = local_env


@task(name='up')
def compose_up(name: str = None) -> None:
    """
    Calls docker compose up using the correct environment.
    """
    opt = ['-d'] if ENV == 'prd' else []

    # note `cd` is ignored locally
    with cd(project_dst):
        local_cmd = create_compose_cmd() + ['up']
        local_cmd += opt
        local_cmd += [name] if name else []
        call(local_cmd)


@task(name='build')
def compose_build(name: str = None) -> None:
    """
    Calls docker compose build using the correct environment.
    """
    with cd(project_dst):
        local_cmd = create_compose_cmd() + ['build']
        local_cmd += [name] if name else []

        call(local_cmd)


@task(name='on')
def on_service(name: str) -> None:
    """
    Define service where command should run
    """
    global SERVICE_NAME

    SERVICE_NAME = name


@task(name='run')
def compose_run(cmd: str) -> None:
    """
    Calls docker compose run using the correct environment.

    :param cmd: run command, including container name.
    """
    opt = ['--rm']

    if SERVICE_NAME is None:
        print("please, provide service name")
        exit()

    with cd(project_dst):
        local_cmd = create_compose_cmd() + ['run']
        local_cmd += opt
        local_cmd += [SERVICE_NAME]
        local_cmd += cmd.split()
        call(local_cmd)


@task(name='logs')
def docker_logs(name: None) -> None:
    """
    Get docker container logs.
    """
    call('docker logs %s' % name)
