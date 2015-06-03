.. AXEMAS documentation master file, created by
   sphinx-quickstart on Fri Jan  2 14:50:37 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   
================================
Welcome to AXEMAS documentation!
================================

Development Framework for MultiPlatform hybrid mobile applications.

Core Concepts
=============

AXEMAS handles the whole navigation of the application and transition between views, 
while it permits to implement the views content in HTML itself.

AXEMAS works using ``sections``, each ``Section`` represents the content of the view
and is loaded from an HTML file or from an external URL.

Whenever native code requires to be attached to a section, it is possible to attach
a ``SectionController`` to a ``Section`` itself.

Contents:

.. toctree::
    :maxdepth: 2

    ios_api
    android_api
    js_api
    gearbox_extension
    maintain_axemas
    utilities

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
