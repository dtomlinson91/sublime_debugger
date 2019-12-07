import click
import sys

import sublime_debugger.change_project as change_project
from sublime_debugger.__version__ import __version__
from sublime_debugger import CONFIG as config


@click.command()
@click.help_option()
@click.version_option(version=__version__)
@click.option(
    '-u',
    '--update',
    'update',
    is_flag=True,
    help='update the sublime project file with the active virtualenv',
)
def cli(update) -> None:
    """utility to change the sublime debugger virtualenv path for python to
    the current :envvar:`VIRTUAL_ENV` environment variable in the sublime
    project
    file"""
    if update:
        change_project.SetEnvironment().update_debugger_path()
        click.echo(
            f"""Successfully updated {config.sublime_project_file} with {config
            .sublime_virtualenv}"""
        )


if __name__ == '__main__':
    cli(sys.argv[1:])
