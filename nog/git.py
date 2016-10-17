import subprocess

import sh
import click
from path import Path


def run(command):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr = stdout.decode('ascii'), stderr.decode('ascii')
    process.stdout = stdout
    process.stderr = stderr
    return process


def clone(source, destination):
    for line in sh.git.clone(source, destination):
        click.echo(line)


def get_remote(source):
    with Path(source):
        return sh.git.config('--get', 'remote.origin.url').strip()


def checkout(source, branch_name, base_branch, new=False):
    with Path(source):
        if new:
            click.echo(sh.git.checkout(base_branch))
            click.echo(sh.git.checkout('-b', branch_name))
        else:
            click.echo(sh.git.checkout(branch_name))


def status(source):
    return run('git --work-tree {0} status -s'.format(source)).stdout.strip()


def is_repo(source):
    with Path(source):
        try:
            sh.git('rev-parse')
            return True
        except:
            return False
