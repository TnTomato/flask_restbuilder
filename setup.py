import re

from setuptools import find_packages, setup

with open("src/easyflask/__init__.py", encoding="utf-8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='easyflask',
    version=version,
    project_urls={
      'Code': 'https://github.com/TnTomato/easyflask'
    },
    license='BSD-3-Clause',
    author='TnTomato',
    author_email='474093103@qq.com',
    maintainer='TnTomato',
    description='A microframework makes building RESTful API projects easier.',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'aniso8601>=8.0.0',
        'click>=7.1.2',
        'Flask>=1.1.2',
        'Flask-RESTful>=0.3.8',
        'itsdangerous>=1.1.0',
        'Jinja2>=2.11.2',
        'MarkupSafe>=1.1.1',
        'pytz>=2020.1',
        'six>=1.15.0',
        'Werkzeug>=1.0.1'
    ],
    entry_points={'console_scripts': ['easyflask = easyflask.cli:main']}
)
