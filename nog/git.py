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
        is_repo = sh.git.rev_parse()
        raise Exception(is_repo)
