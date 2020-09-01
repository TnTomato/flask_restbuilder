import base64
import os

import click
from jinja2 import Environment, FileSystemLoader

# some directories of the project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'src/easyflask/conf/project_template')


@click.command('startproject', short_help='Create a Flask RESTful API project.')
@click.option('--name', '-n', default='myeasyflask', help='The project\'s name.')
@click.option('--directory',
              '-d',
              default=os.getcwd(),
              help='Optional destination directory')
def start_project(name, directory):
    project_root = os.path.join(directory, name)
    src_project_root = os.path.join(project_root, f'src/{name}')

    app_root = os.path.join(src_project_root, 'app')
    extension_root = os.path.join(src_project_root, 'extension')
    util_root = os.path.join(src_project_root, 'util')

    try:
        os.makedirs(app_root)
        os.makedirs(extension_root)
        os.makedirs(util_root)
    except FileExistsError:
        click.echo(f'`{project_root}` already exists')
    except OSError as e:
        click.echo(e)

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=['.html']
    )

    manage_tpl = env.get_template('manage.py-tpl')
    manage_file = manage_tpl.render()
    with open(os.path.join(src_project_root, 'manage.py'), 'w', encoding='utf-8') as f:
        f.write(manage_file)

    config_tpl = env.get_template('config.py-tpl')
    config_file = config_tpl.render(
        {
            'secret_key': base64.b64encode(os.urandom(24)).decode('utf-8'),
            'swagger_needed': True
        }
    )
    with open(os.path.join(src_project_root, 'config.py'), 'w', encoding='utf-8') as f:
        f.write(config_file)

    app_init_tpl = env.get_template('app/__init__.py-tpl')
    app_init_file = app_init_tpl.render(swagger_needed=True)
    with open(os.path.join(src_project_root, 'app/__init__.py'), 'w', encoding='utf-8') as f:
        f.write(app_init_file)

    # TODO: try jinja2


if __name__ == '__main__':
    start_project()
