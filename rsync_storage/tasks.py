#-*- coding: utf8 -*-
import os
from celery.task import task
import subprocess
import pid

RSYNC_PID_PATH = '/tmp/rsync_task.pid'

def _copy_to_remote_host(dir_from, remote_dir_to):
    try:
        # sshpass для того, чтобы не пробрасывать ssh_key в docker контейнерах. Так проще.
        # res_code = subprocess.call(['sshpass', '-p', 'root', 'rsync', dir_from, remote_dir_to, '-avz'])
        # res_code = subprocess.call(['rsync', dir_from, remote_dir_to, '-avz'])
        if os.path.isfile(RSYNC_PID_PATH):
            lines = file(RSYNC_PID_PATH, 'r').readlines()
            if lines:
                exist_pid = lines[0]
                if pid.check_running(exist_pid):
                    pid.create_file(RSYNC_PID_PATH)
                    res_code = subprocess.call(["rsync", "-avz", "-e", "ssh -oNumberOfPasswordPrompts=0", dir_from, remote_dir_to])
                    if res_code != 0:
                        raise IOError(u'no ssh connection to %s' % remote_dir_to)
                    os.unlink(RSYNC_PID_PATH)
    except OSError as ex:
        return False
    if res_code != 0:
        return False
    return True

@task(ignore_result=False, time_limit=300)
def rsync_task(dir_from, dir_to):
    _copy_to_remote_host(dir_from, dir_to)



