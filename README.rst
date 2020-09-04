EasyFlask
=========

EasyFlask is a mircroframework based on Flask and some Flask's extensions.
It's aimed to make it easier to build a RESTful API project in Flask.

Installing
==========

Install and update by pip:

.. code-block:: text

    pip install easyflask

Example
=======

About Project
-------------

Use command ``easyflask start`` to create a project:

.. code-block:: text

    path/to/project: easyflask start
    What is your project's name? [myeasyflask]: myproject
    Where you want to create?(empty to current dir) [path/to/project]:
    Your project's modules(use whitespace to split) [mymodule]: app1 app2
    Need swagger support?(y/n) [y]:

Follow the guidance and finish the questions below, you will get a directory
(The project directory is based on **src mode**):

.. code-block:: text

    ├─ .gitignore
    ├─ CHANGES.rst
    ├─ README.rst
    └─ src
        └─ myproject
            ├─ config.py
            ├─ manage.py
            ├─ app
            │   ├─ __init__.py
            │   ├─ api
            │   │   ├─ app1.py
            │   │   ├─ app2.py
            │   │   └─ __init__.py
            │   ├─ app1
            │   │   ├─ models.py
            │   │   ├─ routes.py
            │   │   └─ __init__.py
            │   └─ app2
            │       ├─ models.py
            │       ├─ routes.py
            │       └─ __init__.py
            ├─ extension
            │   └─ mysql.py
            │
            └─ util

About API
---------

Create your API views like:

.. code-block:: python

    from easyflask import RESTful

    class MyAPI(RESTful):

        def __init__(self):
            self.parser.add_argument('arg')
            self.parse_arguments()

        def get(self):
            result = self.init_response(data=self.args)
            return result

``self.parser`` is an instance of ``flask_restful.reqparse.RequestParser``,
use ``add_argument`` the same way. Use ``self.parse_arguments`` to make
``self.args = self.parser.parse_args()``

About Error
-----------

There some basic errors in ``easyflask.exceptions``. Customize your exceptions
from ``easyflask.BaseError``:

.. code-block:: python

    from easyflask import BaseError

    class MyError(BaseError):
        code = 12345
        message = 'my error message'

About Database
--------------

Flask_SQLAlchemy is equipped. You can see in ``extension/mysql.py`` and freely
edit any basic options.


Thanks to
=========

    - `Flask`_
    - `Jinja`_
    - `Click`_
    - `Flask-RESTful`_
    - `Flask-SQLAlchemy`_
    - `Flask-Script`_
    - `Flasgger`_

.. _Flask: https://github.com/pallets/flask
.. _Jinja: https://github.com/pallets/jinja
.. _Click: https://github.com/pallets/click
.. _Flask-RESTful: https://github.com/flask-restful/flask-restful
.. _Flask-SQLAlchemy: https://github.com/pallets/flask-sqlalchemy
.. _Flask-Script: https://github.com/smurfix/flask-script
.. _Flasgger: https://github.com/flasgger/flasgger