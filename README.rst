Flask-RESTBuilder
=================

Flask-RESTBuilder is a mircroframework based on Flask and some Flask's
extensions. It's aimed to make it easier to build a RESTful API project in Flask.

Installing
==========

Install and update by pip:

.. code-block:: text

    pip install flask_restbuilder

Example
=======

About Project
-------------

Use command ``flask_restbuilder start`` to create a project:

.. code-block:: text

    path/to/project: flask_restbuilder start
    What is your project's name? [myproject]: myproject
    Where you want to create?(empty to current dir) [path/to/project]:
    Your project's modules(use whitespace to split) [mymodule]: app1 app2
    Need db support?
    1. Flask-SQLAlchemy;
    2. Flask-PyMongo;
    Input numbers, use whitespace to split []: 1 2
    Need swagger support?(y/n) [y]: y

Follow the guidance and finish the questions below, you will get a directory
(The project directory is based on **src mode**):

.. code-block:: text

    myproject
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
            └─ extension
                ├─ __init__.py
                ├─ mongo.py
                └─ sa.py

About API
---------

Create your API views like:

.. code-block:: python

    from flask_restbuilder import RESTful

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

There some basic errors in ``flask_restbuilder.exceptions``. Customize your
exceptions from ``flask_restbuilder.BaseError``:

.. code-block:: python

    from flask_restbuilder import BaseError

    class MyError(BaseError):
        code = 12345
        message = 'my error message'

Other built-in exceptions in ``flask_restbuilder.exceptions`` are waiting for
you to discover.

About Database
--------------

Flask-SQLAlchemy
^^^^^^^^^^^^^^^^

Flask-SQLAlchemy is equipped if you need. If you turn on the SQLAlchemy support,
you can see in ``extension/sa.py`` and can freely edit any basic options.

Create your model classes from ``:class:`~extension.sa.SABaseModel``` to equip
some basic attributes like: auto-increment string-type id(*id*), logically
deleting identifier(*is_enbale*), creating and updating time(*created_on* and
*updated_on*). Default SQLAlchemy Query is provided to do some automatic work
during data operations. Turn to ``sa.py`` in your project for more informations.

Flask-PyMongo
^^^^^^^^^^^^^

Flask-PyMongo is equipped if you need.If you turn on the PyMongo support,
you can see in ``extension/mongo.py`` and can freely edit any basic options.

There are also some auto added fields in MongoDB's data structure from this
project. They are the same as above: id, is_enable, created_on and updated_on.

Models should be created from ``:class:`~extension.mongo.MongoBaseModel```.
You need to specify a collection's name with attribute: __collectionname__.
For example:

.. code-block:: python

    from extension.mongo import MongoBaseModel

    class MyModel(MongoBaseModel):
        __collectionname__ = 'mycollection'

Then try some pymongo operations with ``MyModel`` such as:

.. code-block:: python

    MyModel().insert_one({'id': 1, 'name': 'test'})

Some of the navite PyMongo API are overrided, but some are not.You can also
access to the native PyMongo API using the ``coll`` attribute as a collection
instance in PyMongo:

.. code-block:: python

    MyModel().coll.find_one({'id': 1})

For more information, check ``mongo.py`` in your project.

Thanks to
=========

    - `Flask`_
    - `Jinja`_
    - `Click`_
    - `Flask-RESTful`_
    - `Flask-SQLAlchemy`_
    - `Flask-PyMongo`_
    - `Flask-Script`_
    - `Flasgger`_

.. _Flask: https://github.com/pallets/flask
.. _Jinja: https://github.com/pallets/jinja
.. _Click: https://github.com/pallets/click
.. _Flask-RESTful: https://github.com/flask-restful/flask-restful
.. _Flask-SQLAlchemy: https://github.com/pallets/flask-sqlalchemy
.. _Flask-PyMongo: https://github.com/dcrosta/flask-pymongo
.. _Flask-Script: https://github.com/smurfix/flask-script
.. _Flasgger: https://github.com/flasgger/flasgger

And other basic packages used in the frameworks above.
