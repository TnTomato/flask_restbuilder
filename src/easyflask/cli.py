# -*- coding: utf-8 -*-
"""
    easyflask.cli
    ~~~~~~~~~~~~~

    Command line application

    :copyright: 2020 TnTomato
    :license: BSD-3-Clause
"""
import base64
import os
import sys
from importlib import import_module

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


def _check_project_name(name):
    if not name.isidentifier():
        click.echo(f'{name} is not a valid name.')
        sys.exit(0)

    try:
        import_module(name)
    except ImportError:
        pass
    else:
        click.echo(f'{name} is conflict with the name of an existing Python '
                   f'module.')
        sys.exit(0)


def _create_folders(*folders):
    for folder in folders:
        try:
            os.makedirs(folder)
        except FileExistsError:
            click.echo(f'`{folder}` already exists')
        except OSError as e:
            click.echo(e)


def _create_from_template(path, tplenv, tplname, filename=None, **kwargs):
    tpl = tplenv.get_template(tplname)
    file = tpl.render(kwargs)
    if not filename:
        filename = tplname.split('-')[0]
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as f:
        f.write(file)


def _create_modules(app_path, module_names, *tplnames):
    api_path = os.path.join(app_path, 'api')
    init_path = os.path.join(app_path, '__init__.py')
    for module_name in module_names:
        module_dir = os.path.join(app_path, module_name)
        try:
            os.makedirs(module_dir)
        except FileExistsError:
            click.echo(f'`{module_dir}` already exists')
        except OSError as e:
            click.echo(e)

        _create_from_template(api_path, API_ENV, '__init__.py-tpl')
        _create_from_template(
            api_path, API_ENV, 'app_api.py-tpl', f'{module_name}.py')

        for tplname in tplnames:
            content = dict(module_name=module_name)
            _create_from_template(module_dir, APP_ENV, tplname, **content)

    with open(init_path, 'r', encoding='utf-8') as f:
        file = f.read()
        replaced = file.replace('blueprints = []',
                                f'blueprints = {str(module_names)}')
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(replaced)


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
def main(name, directory, modules, swagger):
    _check_project_name(name)
    module_names = modules.split(' ')
    swagger_needed = True if swagger == 'y' else False

    project_root = os.path.join(directory, name)
    src_project_root = os.path.join(project_root, f'src/{name}')

    app_root = os.path.join(src_project_root, 'app')
    api_root = os.path.join(app_root, 'api')
    extension_root = os.path.join(src_project_root, 'extension')
    util_root = os.path.join(src_project_root, 'util')

    _create_folders(app_root,
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
        _create_from_template(src_project_root, SRC_ENV, tpl_name, **content)

    project_tpl2content = {
        '.gitignore-tpl': {},
        'README.rst-tpl': {'project_name': name},
        'CHANGES.rst-tpl': {}
    }

    for tpl_name, content in project_tpl2content.items():
        _create_from_template(project_root, PROJECT_ENV, tpl_name, **content)

    _create_modules(app_root, module_names,
                    '__init__.py-tpl', 'routes.py-tpl', 'models.py-tpl')


if __name__ == '__main__':
    main()
