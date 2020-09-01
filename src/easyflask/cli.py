import os

import click


@click.command('startproject', short_help='Create a Flask RESTful API project.')
@click.option('--name', '-n', default='myeasyflask', help='The project\'s name.')
@click.option('--directory',
              '-d',
              default=os.getcwd(),
              help='Optional destination directory')
def start_project(name, directory):
    project_root = os.path.join(directory, name)
    src_project_root = os.path.join(directory, f'src/{name}')

    app_root = os.path.join(src_project_root, 'app')
    extension_root = os.path.join(src_project_root, f'extension')

    try:
        os.makedirs(app_root)
        os.makedirs(extension_root)
    except FileExistsError:
        click.echo(f'`{project_root}` already exists')
    except OSError as e:
        click.echo(e)

    # TODO: try jinja2


if __name__ == '__main__':
    start_project()
