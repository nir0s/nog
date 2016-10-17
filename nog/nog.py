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

import os
import sys
import json
from functools import wraps
try:
    from urllib.parse import urlparse
except ImportError:
    # python 2
    from urlparse import urlparse


import click
from tinydb import Query

# import nog
from . import git
# from . import runner
from . import storage


def assert_initialized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_initialized():
            raise Exception('Please run `nog init` first')
        return func(*args, **kwargs)

    return wrapper


jsonify_option = click.option(
    '-j',
    '--jsonify',
    is_flag=True,
    default=False,
    help='Output in JSON instead')


@click.group(name='nog')
def main():
    """Nognog
    """


def is_initialized():
    return os.path.isfile(storage.NOG_FILE)


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
@click.option('-t',
              '--tag',
              multiple=True,
              help="A tag to assign to the repo")
@click.option('--method',
              type=click.Choice(['ssh', 'https']),
              default='ssh',
              help="Method to use when cloning repositories")
@assert_initialized
def add(source, tag, method):
    """Add a single or multiple repositories to manage

    \b
    SOURCE can be one of:
     * A path to a local repo
     * A repo URL in the form of git@github:org/repo.git
     * A repo URL in the form of https://github.com/org/repo
     * An org/repo string.
    \b
    if source is full url to repo, get its name, clone it* and add it
    if source is a cutout github path, check if it's local and a repo.
        if it's local and a repo, get its name and org and add it
        if it's local and not, clone it and add it
    """
    # TODO: Validate that the repo is accessible before adding it
    # TODO: Allow to clone to another destination
    db = storage.load('repos')

    click.echo('Analyzing source {0}'.format(source))
    source = os.path.expanduser(source)
    if ('://' or 'git@') in source:
        name = _get_name_from_git_url(source)
        repo_path = os.path.join(storage.NOG_HOME, name)
    elif os.path.isdir(source):
        if git.is_repo(source):
            url = git.get_remote(source)
            name = _get_name_from_git_url(url)
            repo_path = os.path.abspath(source)
        else:
            # TODO: Deal with an existing path which is not a repository
            # and thus should be cloned
            raise
    elif not os.path.isdir(source):
        if '/' in source:
            name = source
            repo_path = os.path.join(storage.NOG_HOME, name)
            # TODO: Fix if a repo was already cloned in, for example ssh,
            # and then removed, re-adding it with another method will not work
            # as the remote origin is still the same for the previously cloned
            # repo.
            if method == 'ssh':
                source = 'git@github.com:{0}.git'.format(source)
            else:
                source = 'https://github.com/{0}.git'.format(source)
        else:
            raise

    existing = db.search((Query().name == name) | (Query().source == source))
    if existing:
        raise Exception(
            'Repo with name {0} or source {1} already exists.'.format(
                name, source))

    if not os.path.isdir(repo_path):
        # TODO: clean if repo wasn't found as there will be org dir leftovers.
        git.clone(source, repo_path)
    url = git.get_remote(repo_path)

    repo = dict(name=name, path=repo_path, tags=list(tag), origin=url)
    db.insert(repo)
    click.echo('Added repository {0}'.format(source))


def _get_name_from_git_url(source):
    # TODO: try urlparse, then try regex on
    if '://' in source:
        return os.path.splitext(urlparse(source).path.lstrip('/'))[0]
    elif 'git@' in source:
        return os.path.splitext(source.split(':')[1])[0]
    else:
        raise Exception('{0} is not a valid url'.format(source))


@main.command()
@click.argument('REPO_NAME')
def remove(repo_name):
    """Start a workflow
    """
    db = storage.load('repos')
    query = Query().name == repo_name
    assert_repo_exists(repo_name)
    db.remove(query)


def assert_repo_exists(repo_name):
    repo = _get_repo(repo_name)
    if not repo:
        sys.exit('Repo {0} does not exist'.format(repo_name))


def assert_feature_exists(feature_name):
    feature = _get_feature(feature_name)
    if not feature:
        sys.exit('Feature {0} does not exist'.format(feature_name))


@main.command()
@click.argument('REPO_NAME')
@click.option('-t',
              '--tag',
              multiple=True,
              help="A tag to assign to the repo")
def tag(repo_name, tag):
    """Tag a single or multiple repositories managed by nog
    """
    click.echo('Appending tags {0}...'.format(tag))
    db = storage.load('repos')
    query = Query().name == repo_name
    assert_repo_exists(repo_name)
    db.update(dict(tags=list(tag)), query)


def _prettify_list(items, title='Repos:'):
    """Return a human readable format of a list.

    Example:

    Available Keys:
      - my_first_key
      - my_second_key
    """
    assert isinstance(items, list)

    keys_list = title
    for item in items:
        keys_list += '\n  - {0}'.format(item)
    return keys_list


def _prettify_dict(key, key_space_prefix=0, key_space_suffix=0):
    """Return a human readable format of a key (dict).

    Example:

    Description:   My Wonderful Key
    Uid:           a54d6de1-922a-4998-ad34-cb838646daaa
    Created_At:    2016-09-15T12:42:32
    Metadata:      owner=me;
    Modified_At:   2016-09-15T12:42:32
    Value:         secret_key=my_secret_key;access_key=my_access_key
    Name:          aws
    """
    assert isinstance(key, dict)

    key_space_prefix = ' ' * key_space_prefix
    key_space_suffix = ' ' * key_space_suffix

    pretty_key = ''
    for key, value in key.items():
        if isinstance(value, dict):
            pretty_value = ''
            for k, v in value.items():
                pretty_value += '{0}={1};'.format(k, v)
            value = pretty_value
        elif isinstance(value, list):
            value = ', '.join(value) if value else 'null'
        pretty_key += '{0}{1:15}{2}\n{3}'.format(
            key_space_prefix,
            key.title() + ':',
            value,
            key_space_suffix)
    return pretty_key


@main.command(name='list')
def _list():
    """List all repositories/features
    """
    db = storage.load('repos')
    repos = db.search(Query().name.matches('.*'))
    if not repos:
        click.echo('You did not add any repositories')
        sys.exit(0)
    repos = [_prettify_dict(repo, 0, 4) for repo in repos]
    click.echo(_prettify_list(repos))


def _get_repo(repo_name):
    db = storage.load('repos')
    repo = db.get(Query().name == repo_name)
    return repo


def _get_feature(feature_name):
    db = storage.load('features')
    feature = db.get(Query().name == feature_name)
    return feature


@main.command(name='get-repo')
@click.argument('REPO_NAME')
@jsonify_option
def get_repo(repo_name, jsonify):
    """Retrieve a repository's info
    """
    assert_repo_exists(repo_name)
    repo = _get_repo(repo_name)
    if jsonify:
        click.echo(json.dumps(repo, indent=4, sort_keys=False))
    else:
        click.echo(_prettify_dict(repo))


@main.command(name='get-feature')
@click.argument('FEATURE_NAME')
@jsonify_option
def get_feature(feature_name, jsonify):
    """Retrieve a repository's info
    """
    assert_feature_exists(feature_name)
    feature = _get_feature(feature_name)
    if jsonify:
        click.echo(json.dumps(feature, indent=4, sort_keys=False))
    else:
        click.echo(_prettify_dict(feature))


@main.command()
def pull():
    """Pull all repositories or for specific tags/feature
    """


@main.command()
@click.argument('REPO_NAME', required=False)
def status(repo_name):
    """Print out the status of all repositories or for specific tags/feature
    """
    db = storage.load('repos')
    query = Query().name == repo_name
    assert_repo_exists(repo_name)
    path = db.get(query)['path']
    click.echo(git.status(path))


@main.command()
@click.argument('FEATURE_NAME')
@click.option('-r',
              '--repo',
              multiple=True,
              help="Repository to add to the feature")
@click.option('-b',
              '--base-branch',
              default='master',
              help="Branch to checkout from")
@click.option('--no-pull',
              is_flag=True,
              default=False,
              help="Pull base branch on all repos first")
def create(feature_name, repo, base_branch, no_pull):
    # TODO: add_missing should allow to add missing repos automatically
    db = storage.load('features')
    # TODO: Don't allow to create a feautre if it already exists
    repos = repo
    for repo in repos:
        # TODO: Summarize non-existing repos instead
        assert_repo_exists(repo)
    for repo in repos:
        repo_path = _get_repo(repo)['path']
        git.checkout(repo_path, base_branch, feature_name)
    db.insert(dict(
        name=feature_name,
        repos=list(repos),
        base_branch=base_branch))

    db = storage.load('active')
    if not db.get(eid=1):
        db.insert(dict(active=feature_name))
    else:
        db.update(dict(active=feature_name), eids=[1])


@main.command(name='add-repo')
@click.argument('REPO_NAME', nargs=-1, required=True)
@click.option('-f',
              '--feature-name',
              required=True,
              help='Feature to add repo to')
def add_repo(repo_name, feature_name):
    """Add a repository or multiple repositories to a feature
    """
    assert_feature_exists(feature_name)
    repos = list(repo_name)
    for repo in repos:
        assert_repo_exists(repo)
    db = storage.load('features')
    current_repos = _get_feature(feature_name)['repos']
    current_repos.extend(repos)
    current_repos = list(set(current_repos))
    db.update(dict(repos=current_repos), Query().name == feature_name)


@main.command(name='remove-repo')
@click.argument('REPO_NAME')
@click.option('-f',
              '--feature-name',
              required=True,
              help='Feature to remove repo from')
def remove_repo(repo_name, feature_name):
    db = storage.load('features')
    current_repos = _get_feature(feature_name)['repos']
    current_repos.remove(repo_name)
    db.update(dict(repos=current_repos), Query().name == feature_name)


@main.command()
@click.argument('FEATURE_NAME')
def work(feature_name):
    """Start a workflow
    """
    db = storage.load('active')
    if not db.get(eid=1):
        db.insert(dict(active=feature_name))
    else:
        db.update(dict(active=feature_name), eids=[1])


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


@main.command(name='next')
def _next():
    """Advance a single step in a workflow
    """
