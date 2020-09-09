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

# jinjia2 environments
JINJA_ENV = Environment(loader=FileSystemLoader('templates'))


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


def _create_from_templates(tpl2meta):
    for tpl_path, meta in tpl2meta.items():
        abs_path = meta.get('dest')
        content = meta.get('content')
        filename = meta.get('filename')

        if not os.path.exists(abs_path):
            os.makedirs(abs_path)

        if not filename:
            filename = os.path.basename(tpl_path).split('-')[0]

        path = os.path.join(abs_path, filename)
        tpl = JINJA_ENV.get_template(tpl_path)
        file_content = tpl.render(content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(file_content)


def _create_modules(app_path, module_names):
    module_tpl_base_dir = 'project_tpl/src_tpl/project_name/app_tpl/app_name/'
    api_tpl_base_dir = 'project_tpl/src_tpl/project_name/app_tpl/api_tpl/'
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

        module2meta = {
            module_tpl_base_dir + '__init__.py-tpl': {
                'dest': module_dir,
                'content': {
                    'module_name': module_name
                }
            },
            module_tpl_base_dir + 'models.py-tpl': {
                'dest': module_dir,
                'content': {}
            },
            module_tpl_base_dir + 'routes.py-tpl': {
                'dest': module_dir,
                'content': {
                    'module_name': module_name
                }
            },

            api_tpl_base_dir + 'api.py-tpl': {
                'dest': api_path,
                'content': {},
                'filename': module_name + '.py'
            }
        }
        _create_from_templates(module2meta)

    with open(init_path, 'r', encoding='utf-8') as f:
        file = f.read()
        replaced = file.replace('blueprints = []',
                                f'blueprints = {str(module_names)}')
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(replaced)


@click.group()
def main():
    pass


@main.command('start', short_help='Create a Flask RESTful API project.')
@click.option('--name', '-n', prompt='What is your project\'s name?',
              default='myeasyflask', help='The project\'s name.')
@click.option('--directory', '-d',
              prompt='Where you want to create?(empty to current dir)',
              default=os.getcwd(),
              help='Optional destination directory')
@click.option('--modules',
              prompt='Your project\'s modules(use whitespace to split)',
              default='mymodule',
              help='Porject\'s module names')
@click.option('--swagger', prompt='Need swagger support?(y/n)', default='y',
              help='Swagger support')
def start(name, directory, modules, swagger):
    _check_project_name(name)
    module_names = modules.split(' ')
    swagger_needed = True if swagger == 'y' else False

    project_root = os.path.join(directory, name)
    src_project_root = os.path.join(project_root, f'src/{name}')

    app_root = os.path.join(src_project_root, 'app')
    api_root = os.path.join(app_root, 'api')
    extension_root = os.path.join(src_project_root, 'extension')
    # util_root = os.path.join(src_project_root, 'util')

    tpl2meta = {
        # files in project's base-diractory
        'project_tpl/README.rst-tpl': {
            'dest': project_root,
            'content': {
                'project_name': name
            }
        },
        'project_tpl/.gitignore-tpl': {
            'dest': project_root,
            'content': {}
        },
        'project_tpl/CHANGES.rst-tpl': {
            'dest': project_root,
            'content': {}
        },

        # files in src/<name>
        'project_tpl/src_tpl/project_name/__init__.py-tpl': {
            'dest': src_project_root,
            'content': {}
        },
        'project_tpl/src_tpl/project_name/config.py-tpl': {
            'dest': src_project_root,
            'content': {
                'project_name': name,
                'secret_key': base64.b64encode(os.urandom(24)).decode('utf-8'),
                'swagger_needed': swagger_needed
            }
        },
        'project_tpl/src_tpl/project_name/manage.py-tpl': {
            'dest': src_project_root,
            'content': {}
        },

        # files in src/<name>/app
        'project_tpl/src_tpl/project_name/app_tpl/__init__.py-tpl': {
            'dest': app_root,
            'content': {
                'swagger_needed': swagger_needed
            }
        },

        # files in src/<name>/app/api
        'project_tpl/src_tpl/project_name/app_tpl/api_tpl/__init__.py-tpl': {
            'dest': api_root,
            'content': {}
        },

        # files in src/<name>/extension
        'project_tpl/src_tpl/project_name/extension_tpl/__init__.py-tpl': {
            'dest': extension_root,
            'content': {}
        },
        'project_tpl/src_tpl/project_name/extension_tpl/mysql.py-tpl': {
            'dest': extension_root,
            'content': {}
        }
    }

    _create_from_templates(tpl2meta)

    _create_modules(app_root, module_names)


command = click.CommandCollection(sources=[main])

if __name__ == '__main__':
    command()
