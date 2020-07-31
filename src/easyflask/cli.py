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
    try:
        os.mkdir(project_root)
    except FileExistsError:
        click.echo(f'`{project_root}` allready exists')




if __name__ == '__main__':
    start_project()