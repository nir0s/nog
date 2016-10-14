# Copyright 2015,2016 Nir Cohen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# TODO: nog init ~/.nog --repos-path ~/repos/
# TODO: nog add [GITHUB_REPO_URL|REPOS_DIR|REPO_DIR]
# TODO: nog tag REPO_NAME
# TODO: nog clone - clone all added repos
# TODO: nog clone work - only clone added repos with the work tag
# TODO: nog pull [TAG_NAME/FEATURE_NAME]
# TODO: nog status [TAG_NAME/FEATURE_NAME] - display single line status
# TODO: nog work FEATURE_NAME
# TODO: nog commit [-m MESSAGE]
# TODO: nog push
# TODO: nog rebase [BRANCH_NAME]
# TODO: nog squash [COMMIT_SHA/HEAD_COUNT]
# TODO: nog stop FEATURE_NAME -f
# TODO: nog list [--features-only|--repos-only]
# TODO: nog workflows ...
# TODO: nog advance - advance to the next step

# nog init
# nog add nir0s/nog --tag private
# nog clone private
# nog status
# ... changes
# nog pull
# nog work new_feature
# nog commit
# nog push [-f]
# nog stop

# import os
# import pkg_resources

import click
from tinydb import Query

# import nog
from . import storage


@click.group(name='nog')
def main():
    """Nognog
    """


@main.command()
def init():
    """Initialize a nog working env
    """
    # nog_home = os.path.expanduser(os.path.join('~', '.nog'))
    # nog_init_file_path = os.path.join(nog_home, 'nog.yaml')
    # nog_init_file = pkg_resources.resource_string(
    #     nog.__name__, 'resources/nog.yaml')
    # with open(nog_init_file_path, 'w') as f:
    #     f.write(nog_init_file)
    #     f.write(os.linesep)

    click.echo('Initializing work env...')
    path = storage.init()
    click.echo('Initialized {0}'.format(path))


@main.command()
@click.argument('SOURCE')
@click.option('-n',
              '--name',
              help="The repository's name")
@click.option('-t',
              '--tag',
              multiple=True,
              help="A tag to assign to the repo")
def add(source, name, tag):
    """Add a single or multiple repositories to manage
    """
    name = name or _get_repo_name(source)
    db = storage.load()
    repos = db.table('repos')
    repos.insert({'name': name, 'source': source, 'tags': list(tag)})
    click.echo('Added repository {0}'.format(source))


def _get_repo_name(source):
    return


@main.command()
@click.argument('REPO_NAME')
@click.option('-t',
              '--tag',
              multiple=True,
              help="A tag to assign to the repo")
def tag(repo_name, tag):
    """Tag a single or multiple repositories managed by nog
    """
    db = storage.load('repos')
    repo = Query()
    db.update({'tags': list(tag)}, repo.name == repo_name)


def _prettify_list(items):
    """Return a human readable format of a list.

    Example:

    Available Keys:
      - my_first_key
      - my_second_key
    """
    assert isinstance(items, list)

    keys_list = 'Available Keys:'
    for item in items:
        keys_list += '\n  - {0}'.format(item)
    return keys_list


@main.command(name='list')
def _list():
    """List all repositories/features
    """
    db = storage.load('repos')
    repos = db.search(Query().name.matches('.*'))
    click.echo(_prettify_list(repos))


@main.command()
def clone():
    """Clone all repositories or for specific tags
    """


@main.command()
def pull():
    """Pull all repositories or for specific tags/feature
    """


@main.command()
def status():
    """Print out the status of all repositories or for specific tags/feature
    """


@main.command()
def work():
    """Start a workflow
    """


@main.command()
def commit():
    """Create a commit for a feature
    """


@main.command()
def push():
    """Push all repos belonging to a feature
    """


@main.command()
def rebase():
    """Rebase all repos belonging to a feature
    """


@main.command()
def squash():
    """Squash all repos belonging to a feature
    """


@main.command()
def stop():
    """Stop a workflow
    """


@main.command()
def advance():
    """Advance a single step in a workflow
    """
