===============
Maintain AXEMAS
===============

AXEMAS framework
================

Repositories Structure
----------------------

The project is divided into 5 repositories::

    website
    examples
    framework
    releases
    doc

Inside framework repo (https://github.com/AXEMAS/framework) you will find the ``AXEMAS`` base library, composed by:

- Android library project
- iOS library project
- HTML library project

When you are done modifing the library please remember to update the debug projects and the release repository
with the following commands.


Debug Projects Update
---------------------

To update the ``Android`` and the ``iOS`` demo projects use the following command 
(examples folder must be in the same parent folder or will be cloned inside ../examples)::

    ./update_debug

Il will delete all the old files in the iOS and Android projects and copy the new library files;
native binaries and HTML.
If you want to release demo apps remember to make necessary fixes, tag version and push everything.


Release Repository Update
-------------------------

Same as for the Debug Project Update, this will update the repository that the 
``gearbox axemas-quickstart`` command needs to clone in order to quickstart a new project
(releases folder must be in the same parent folder or will be cloned inside ../releases, 
be careful if you have pending changes)::

    ./update_release

If you want to release new version remember to commit, tag version and push everything.

    
Android AXEMAS library
======================

This library project is used to build the axemas.aar used inside the Android application.


How to use
----------

After modifiying the library please inside this project's root folder::

./gradlew clean assemble

You will find the ``app-release.aar`` inside the ``app/build/outputs/aar/`` folder. Copy this file
inside the ``axemas-android`` project in the ``libs`` folder.


iOS AXEMAS library
==================

This project is used to build the axemas iOS library. Please use the following instructions to make
a new release.


Setup
-----


Install the command line tools, following the instructions at this link::

    https://developer.apple.com/library/ios/technotes/tn2339/_index.html



New Release
-----------

Use the following command in the ::
    cp ios
    ./build_libaxemas

In the release directory you will find all the neccessary files to import the project in Xcode.
