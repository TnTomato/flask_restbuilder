# -*- coding: utf-8 -*-
"""
    flask_restbuilder.cli
    ~~~~~~~~~~~~~~~~~~~~~

    Command line application

    :copyright: 2020 TnTomato
    :license: BSD-3-Clause
"""
import base64
import os
from importlib import import_module

import click
from jinja2 import Environment, FileSystemLoader

# jinjia2 environments
PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(PATH, 'templates')
JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATE_PATH))


def _check_project_name(name):
    if not name.isidentifier():
        raise click.BadParameter(f'`{name}` is not a valid name.')

    try:
        import_module(name)
    except ImportError:
        pass
    else:
        raise click.BadParameter(f'`{name}` is conflict with the name of an '
                                 f'existing Python module.')


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


def _create_modules(app_path, module_names, db_support):
    module_tpl_base_dir = 'project_tpl/src_tpl/project_name/app_tpl/app_name/'
    api_tpl_base_dir = 'project_tpl/src_tpl/project_name/app_tpl/api_tpl/'
    api_path = os.path.join(app_path, 'api')
    init_path = os.path.join(app_path, '__init__.py')
    for module_name in module_names:
        module_dir = os.path.join(app_path, module_name)
        try:
            os.makedirs(module_dir)
        except FileExistsError:
            raise FileExistsError(f'module dir `{module_dir}` already exists')
        except Exception as e:
            raise click.ClickException(str(e))

        module2meta = {
            # files in src/<name>/app/<module_name>
            module_tpl_base_dir + '__init__.py-tpl': {
                'dest': module_dir,
                'content': {
                    'module_name': module_name
                }
            },
            module_tpl_base_dir + 'routes.py-tpl': {
                'dest': module_dir,
                'content': {
                    'module_name': module_name
                }
            },

            # files in src/<name>/app/api
            api_tpl_base_dir + 'api.py-tpl': {
                'dest': api_path,
                'content': {},
                'filename': module_name + '.py'
            }
        }

        if db_support:
            module2meta.update(
                {
                    module_tpl_base_dir + 'models.py-tpl': {
                        'dest': module_dir,
                        'content': {}
                    }
                }
            )

        _create_from_templates(module2meta)

    # update flask factory blueprints
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
              default='myproject', help='The project\'s name.')
@click.option('--directory', '-d',
              prompt='Where you want to create?(empty to current dir)',
              default=os.getcwd(),
              help='Optional destination directory')
@click.option('--modules',
              prompt='Your project\'s modules(use whitespace to split)',
              default='mymodule',
              help='Porject\'s module names')
@click.option('--db',
              prompt='''Need db support?
1. Flask-SQLAlchemy;
2. Flask-PyMongo;
Input numbers, use whitespace to split''',
              default='')
@click.option('--swagger', prompt='Need swagger support?(y/n)', default='y',
              help='Swagger support')
def start(name, directory, modules, db, swagger):
    try:
        _check_project_name(name)
    except click.BadParameter as e:
        click.echo(e)
        return

    module_names = modules.split(' ')

    swagger_support = True if swagger == 'y' else False

    dbs = db.split(' ')
    sa_support = True if '1' in dbs else False
    pymongo_support = True if '2' in dbs else False

    project_root = os.path.join(directory, name)
    src_project_root = os.path.join(project_root, f'src/{name}')

    app_root = os.path.join(src_project_root, 'app')
    api_root = os.path.join(app_root, 'api')
    extension_root = os.path.join(src_project_root, 'extension')

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
        'project_tpl/requirements.txt-tpl': {
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
                'sa_support': sa_support,
                'pymongo_support': pymongo_support,
                'swagger_support': swagger_support
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
                'sa_support': sa_support,
                'pymongo_support': pymongo_support,
                'swagger_support': swagger_support
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
        }
    }

    if sa_support:
        tpl2meta.update(
            {
                'project_tpl/src_tpl/project_name/extension_tpl/sa.py-tpl': {
                    'dest': extension_root,
                    'content': {}
                }
            }
        )

    if pymongo_support:
        tpl2meta.update(
            {
                'project_tpl/src_tpl/project_name/extension_tpl/mongo.py-tpl': {
                    'dest': extension_root,
                    'content': {}
                }
            }
        )

    _create_from_templates(tpl2meta)

    # decide whether models.py need to be added to each app package
    db_support = True if db else False

    try:
        _create_modules(app_root, module_names, db_support)
    except Exception as e:
        click.echo(e)
        return


@main.command('startapp', short_help='Create a module in the project.')
@click.option('--name', '-n', prompt='What is your module\'s name?',
              default='mymodule', help='The module\'s name.')
def startapp(name):
    this_path = os.getcwd()
    project_name = os.path.basename(this_path)
    src_dir = os.path.join(this_path, 'src')
    if not os.path.exists(src_dir):
        click.echo('wrong directory')
        return

    extension_dir = os.path.join(src_dir, f'{project_name}/extension')
    if os.path.exists(os.path.join(extension_dir, 'sa.py')) \
            or os.path.exists(os.path.join(extension_dir, 'mongo.py')):
        db_support = True
    else:
        db_support = False

    app_dir = os.path.join(src_dir, f'{project_name}/app')
    try:
        _create_modules(app_dir, [name], db_support)
    except Exception as e:
        click.echo(e)
        return


command = click.CommandCollection(sources=[main])

if __name__ == '__main__':
    command()
