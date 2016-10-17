import sh
import click
from path import Path


def clone(source, destination):
    for line in sh.git.clone(source, destination):
        click.echo(line)


def get_remote(source):
    with Path(source):
        return sh.git.config('--get', 'remote.origin.url').strip()


def status(source):
    with Path(source):
        return sh.git.status('-s')


def is_repo(source):
    with Path(source):
        try:
            sh.git('rev-parse')
            return True
        except:
            return False
