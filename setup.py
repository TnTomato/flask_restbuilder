import re

from setuptools import find_packages, setup

with open('README.rst', 'rt', encoding='utf-8') as f:
    readme = f.read()

with open('src/easyflask/__init__.py', 'rt', encoding="utf-8") as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)

setup(
    name='easyflask',
    version=version,
    url='https://github.com/TnTomato/easyflask',
    project_urls={
      'Code': 'https://github.com/TnTomato/easyflask'
    },
    license='BSD-3-Clause',
    author='TnTomato',
    author_email='474093103@qq.com',
    maintainer='TnTomato',
    description='A microframework makes building RESTful API projects easier.',
    long_description=readme,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    data_files=[
        (
            'Lib/site-packages/easyflask/tpls/project_template',
            ['src/easyflask/tpls/project_template/.gitignore-tpl',
             'src/easyflask/tpls/project_template/CHANGES.rst-tpl',
             'src/easyflask/tpls/project_template/README.rst-tpl']
        ),
        (
            'Lib/site-packages/easyflask/tpls/src_template',
            ['src/easyflask/tpls/src_template/config.py-tpl',
             'src/easyflask/tpls/src_template/manage.py-tpl']),
        (
            'Lib/site-packages/easyflask/tpls/src_template/app',
            ['src/easyflask/tpls/src_template/app/__init__.py-tpl']
        ),
        (
            'Lib/site-packages/easyflask/tpls/src_template/app/api_template',
            ['src/easyflask/tpls/src_template/app/api_template/__init__.py-tpl',
             'src/easyflask/tpls/src_template/app/api_template/app_api.py-tpl']
        ),
        (
            'Lib/site-packages/easyflask/tpls/src_template/app/app_template',
            ['src/easyflask/tpls/src_template/app/app_template/__init__.py-tpl',
             'src/easyflask/tpls/src_template/app/app_template/models.py-tpl',
             'src/easyflask/tpls/src_template/app/app_template/routes.py-tpl']
        )
    ],
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'aniso8601>=8.0.0',
        'attrs>=20.1.0',
        'click>=7.1.2',
        'flasgger>=0.9.5',
        'Flask>=1.1.2',
        'Flask-RESTful>=0.3.8',
        'Flask-Script>=2.0.6',
        'Flask-SQLAlchemy>=2.4.4',
        'itsdangerous>=1.1.0',
        'Jinja2>=2.11.2',
        'jsonschema>=3.2.0',
        'MarkupSafe>=1.1.1',
        'mistune>=0.8.4',
        'pyrsistent>=0.16.0',
        'pytz>=2020.1',
        'PyYAML>=5.3.1',
        'six>=1.15.0',
        'SQLAlchemy>=1.3.19',
        'Werkzeug>=1.0.1'
    ],
    entry_points={'console_scripts': ['easyflask = easyflask.cli:main']}
)
