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


import click


@click.group(name='nog')
def main():
    """Nognog
    """


@main.command()
def init():
    """Initialize a nog working env
    """


@main.command()
def add():
    """Add a single or multiple repositories to manage
    """


@main.command()
def tag():
    """Tag a single or multiple repositories managed by nog
    """


@main.command(name='list')
def _list():
    """List all repositories/features
    """


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
