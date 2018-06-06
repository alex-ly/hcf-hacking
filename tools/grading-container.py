import docker
import sys
import os

def get_running_instance(client):
    try:
        container = client.containers.get('grading')
        return container
    except:
        return None

def get_mount(client):
    vols = client.volumes.list()
    users = []
    prefix = os.environ.get('USER_PROBLEMSETS_PREFIX')
    if not prefix:
        raise Exception("USER_PROBLEMSETS_PREFIX is not set")
    prefix = prefix + "-"

    problemsets_volume = os.environ.get('PROBLEMSETS')
    if not problemsets_volume:
        raise Exception("PROBLEMSETS is not set")

    exchange_volume = os.environ.get('EXCHANGE')
    if not exchange_volume:
        raise Exception("EXCHANGE is not set")

    for v in vols:
        if v.name.startswith(prefix):
            users.append(v.name[len(prefix):])

    mount = dict((
        prefix + x, 
        dict(bind="/user-problemsets/%s" % x, mode='rw')) for x in users)

    mount[problemsets_volume] = dict(
            bind="/home/jovyan/problemsets",
            mode="rw")

    mount[exchange_volume] = dict(
            bind="/home/jovyan/exchange",
            mode="rw")

    mount[os.path.join(os.getcwd(), "grading-tools")] = dict(
            bind="/tools",
            mode="ro")

    return mount

def start(client):
    running = get_running_instance(client)
    if running:
        print("docker kill %s" % running.id, file=sys.stderr)
        sys.exit()
        try:
            running.kill()
            running.remove()
        except:
            pass

    mount = get_mount(client)

    client.containers.run("hcf/designer-notebook",
            command="python /tools/push-problemsets.py",
            name="grading",
            volumes=mount,
            remove=True,
            detach=True)


    print("""
    docker exec -it grading /bin/bash -c "export COLUMNS=`tput cols`; export LINES=`tput lines`; exec bash"
    """)

def kill(client):
    running = get_running_instance(client)
    if running:
        running.kill()
    else:
        print("Not running")

def test():
    import pprint
    client = docker.from_env()
    running = get_running_instance(client)
    if running:
        print("docker kill %s" % running.id, file=sys.stderr)
        sys.exit()

    mount = get_mount(client)
    pprint.pprint(mount)

if __name__ == '__main__':
    import sys
    op = "start"
    if sys.argv[1:]:
        op = sys.argv[1]

    client = docker.from_env()

    if op == 'start':
        start(client)
    elif op == 'stop':
        kill(client)
