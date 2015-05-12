=================
Gearbox Extension
=================

This is a ``gearbox`` extension that will generate a new ``Axemas`` project. ``Axemas`` is a development Framework
for MultiPlatform hybrid mobile applications.

Installaton
-----------

Create a new virtual environment and install ``axemas`` with ``pip``. This will include all needed dependencies like
``gearbox``::

    $ virtualenv --no-site-packages axemas_builder
    $ . axemas_builder/bin/activate
    (axemas_builder)$ pip install axemas

Usage
-----

Run the following command to generate a project called ``new_project`` inside the directory where you want to
create the new project::

     (axemas_builder)$ gearbox axemas-setup -n ProjectName -p com.company.example



Project structure
-----------------

The resulting project structure will be as follows::

    /                   root of the project
    ----/android        Axemas Android native Java code
    ----/axemas-js      Axemas library JavaScript code imported by www
    ----/ios            Axemas iOS native Objective-C code
    ----/www            common share html/css/js/resource files