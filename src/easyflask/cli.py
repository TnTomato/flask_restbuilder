import base64
import os

import click
from jinja2 import Environment, FileSystemLoader

# some directories and paths of the project
FILE_PATH = os.path.abspath(__file__)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(FILE_PATH)))
PROJECT_TPL_DIR = os.path.join(ROOT_DIR, 'src/easyflask/conf/project_template')
SRC_TPL_DIR = os.path.join(ROOT_DIR, 'src/easyflask/conf/src_template')
APP_TPL_DIR = os.path.join(SRC_TPL_DIR, 'app/app_template')
API_TPL_DIR = os.path.join(SRC_TPL_DIR, 'app/api_template')

# jinjia2 environments
SRC_ENV = Environment(loader=FileSystemLoader(SRC_TPL_DIR))
PROJECT_ENV = Environment(loader=FileSystemLoader(PROJECT_TPL_DIR))
APP_ENV = Environment(loader=FileSystemLoader(APP_TPL_DIR))
API_ENV = Environment(loader=FileSystemLoader(API_TPL_DIR))


def create_folders(*folders):
    for folder in folders:
        try:
            os.makedirs(folder)
        except FileExistsError:
            click.echo(f'`{folder}` already exists')
        except OSError as e:
            click.echo(e)


def create_from_template(path, tplenv, tplname, filename=None, **kwargs):
    tpl = tplenv.get_template(tplname)
    file = tpl.render(kwargs)
    if not filename:
        filename = tplname.split('-')[0]
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as f:
        f.write(file)


def create_modules(app_path, module_names, *tplnames):
    api_path = os.path.join(app_path, 'api')
    for module_name in module_names:
        module_dir = os.path.join(app_path, module_name)
        try:
            os.makedirs(module_dir)
        except FileExistsError:
            click.echo(f'`{module_dir}` already exists')
        except OSError as e:
            click.echo(e)

        create_from_template(api_path, API_ENV, '__init__.py-tpl')
        create_from_template(
            api_path, API_ENV, 'app_api.py-tpl', f'{module_name}.py')

        for tplname in tplnames:
            content = dict(module_name=module_name)
            create_from_template(module_dir, APP_ENV, tplname, **content)


@click.command('startproject', short_help='Create a Flask RESTful API project.')
@click.option('--name', '-n',  prompt='What is your project\'s name?',
              default='myeasyflask', help='The project\'s name.')
@click.option('--directory',
              '-d',
              prompt='Where you want to create?(empty to current dir)',
              default=os.getcwd(),
              help='Optional destination directory')
@click.option('--modules',
              prompt='Your project\'s modules(use whitespace to split)',
              default='mymodule',
              help='Porject\'s module names')
@click.option('--swagger', prompt='Need swagger support?(y/n)', default='y',
              help='Swagger support')
def start_project(name, directory, modules, swagger):
    module_names = modules.split(' ')
    swagger_needed = True if swagger == 'y' else False

    project_root = os.path.join(directory, name)
    src_project_root = os.path.join(project_root, f'src/{name}')

    app_root = os.path.join(src_project_root, 'app')
    api_root = os.path.join(app_root, 'api')
    extension_root = os.path.join(src_project_root, 'extension')
    util_root = os.path.join(src_project_root, 'util')

    create_folders(app_root,
                   api_root,
                   extension_root,
                   util_root)

    src_tpl2content = {
        'manage.py-tpl': {},
        'config.py-tpl': {
            'project_name': name,
            'secret_key': base64.b64encode(os.urandom(24)).decode('utf-8'),
            'swagger_needed': swagger_needed
        },
        'app/__init__.py-tpl': {
            'swagger_needed': swagger_needed
        },
        'extension/mysql.py-tpl': {},
    }

    for tpl_name, content in src_tpl2content.items():
        create_from_template(src_project_root, SRC_ENV, tpl_name, **content)

    project_tpl2content = {
        '.gitignore-tpl': {},
        'README.rst-tpl': {'project_name': name},
        'CHANGES.rst-tpl': {}
    }

    for tpl_name, content in project_tpl2content.items():
        create_from_template(project_root, PROJECT_ENV, tpl_name, **content)

    create_modules(app_root, module_names,
                   '__init__.py-tpl', 'routes.py-tpl', 'models.py-tpl')


if __name__ == '__main__':
    start_project()
