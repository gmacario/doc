.. AXEMAS documentation master file, created by
   sphinx-quickstart on Fri Jan  2 14:50:37 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   
================================
Welcome to AXEMAS documentation!
================================

Development Framework for MultiPlatform hybrid mobile applications.

AXEMAS handles the whole navigation of the application and transition between views, 
while it permits to implement the views content in HTML itself.

AXEMAS works using ``sections``, each ``Section`` represents the content of the view
and is loaded from an HTML file or from an external URL.

Whenever native code requires to be attached to a section, it is possible to attach
a ``SectionController`` to a ``Section`` itself.

Getting Started
---------------

To Install AXEMAS you need ``Python 2.7`` with the ``pip`` package manager installed
as AXEMAS uses Python to generate project skeletons. To install ``pip`` follow the
`Pip Install Guidelines <https://pip.pypa.io/en/latest/installing.html>`_.
Then you can install AXEMAS toolkit using::

    $ pip install axemas

To create a new AXEMAS project you can then use the ``axemas-quickstart`` command,
it will automatically create a new AXEMAS project::

    $ gearbox axemas-quickstart -n ProjectName -p com.company.example

See :ref:`quickstart` for additional details on the ``gearbox`` command.

Basic Project Introduction
~~~~~~~~~~~~~~~~~~~~~~~~~~

The most simple AXEMAS application will start by creating a root ``Section``.
The following is as much as you need to load a section from the ``www/home.html`` file.

Inside your ``AppDelegate`` for **iOS**:

.. code-block:: objc

    @implementation AppDelegate

    - (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
        self.window.rootViewController = [NavigationSectionsManager makeApplicationRootController:@[@{
            @"title": @"Home",
            @"url": @"www/home.html",
        }]];

        [self.window makeKeyAndVisible];
        return YES;
    }

    @end

Or in your ``AXMActivity`` subclass ``onCreate()`` method for **Android**:

.. code-block:: java

    public class MainActivity extends AXMActivity {
        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);

            if (savedInstanceState == null) {
                JSONObject data = new JSONObject();
                try {
                    data.put("url", "www/home.html");
                    data.put("title", "Home");
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                NavigationSectionsManager.makeApplicationRootController(this, data);
            }
        }
    }

From the loaded web page, you can then use the :ref:`js_api` to push and pop additional
sections and implement your whole Application.

Binding to Native Code
~~~~~~~~~~~~~~~~~~~~~~

The previous code shows how to load ``HTML`` based sections and rely on the :ref:`js_api`
to implement your web application. When more advanced features or interaction with the
hardware is needed you might need to get to native code level. AXEMAS has been designed
specifically to make it as easy as possible to work with native code, the main difference
with frameworks like Cordova is explicitly that AXEMAS makes native a first citizen of
your application.

The binding between the ``HTML Sections`` and native code is performed using
``SectionControllers``, to link a section to a section controller is as easy as
registering the controller class for the specified route:

.. code-block:: objc

    [NavigationSectionsManager registerController:[MySecionController class] forRoute:@"www/mysection.html"];

.. code-block:: java

    NavigationSectionsManager.registerController(this, MySecionController.class, "www/mysection.html");

To get started using ``SectionControllers`` read the :ref:`ios_api` and :ref:`android_api`.


Contents:

.. toctree::
    :maxdepth: 2

    ios_api
    android_api
    js_api
    utilities
    cookbook
    gearbox_extension
    maintain_axemas
    

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
