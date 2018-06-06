import os
import sys
import subprocess
import time

OUTBOUND = os.path.join(os.environ.get('HOME'), "exchange/problemsets/outbound")
USERS_ROOT = "/user-problemsets"

def slashed(x):
    if x.endswith("/"):
        return x
    else:
        return x + "/"

def list_users():
    for x in os.listdir(USERS_ROOT):
        if os.path.isdir(os.path.join(USERS_ROOT, x)):
            yield dict(name=x, path=os.path.join(USERS_ROOT, x))

def copy_problemsets(u, force=False, debug=False):
    src = OUTBOUND
    tgt = u['path']
    if not os.path.exists(src):
        print("src %s not found" % src)
        return
    if not os.path.exists(tgt):
        print("tgt %s not found" % tgt)
        return

    cmd = ['rsync',
            '-a',
            '--delete',
            '--ignore-existing',
            slashed(src),
            slashed(tgt)]
    result = subprocess.run(cmd, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    if debug or result.returncode != 0:
        message = ""
        if result.stdout:
            message = message + result.stdout.decode('utf8') + "\n"
        if result.stderr:
            message = message + result.stderr.decode('utf8') + "\n"
        print("=================")
        print(message)
        print("=================")


def test():
    import pprint
    users = list(list_users())
    pprint.pprint(users)
    cmd = ["rsync", "--version"]
    x = subprocess.run(cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    print("RET:", x.returncode)
    if x.stdout:
        print("=========== STDOUT ==========")
        print(x.stdout.decode('utf8'))
    if x.stderr:
        print("=========== STDERR ==========")
        print(x.stderr.decode('utf8'))

if __name__ == '__main__':
    delay = 3
    while True:
        start = time.time()
        count = 0
        print(">>>")
        for u in list_users():
            print("user: %s" % u['name'])
            copy_problemsets(u, force=False)
            count += 1
        duration = time.time() - start
        print("[%s users in %.2f seconds], sleeping for %d seconds" % (
            count, duration, delay))
        time.sleep(delay)

