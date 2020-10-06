coordmanager
============

exercise for geosolution


Basic Commands
--------------

Import data from CSV file
^^^^^^^^^^^^^^^^^^^^^

* To load data from CSV file, use this command::

    $ python manage.py import_coordinates <file_name>


Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy coordmanager

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest


Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd coordmanager
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.
