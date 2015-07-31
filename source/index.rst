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

To create a new AXEMAS project try :ref:`quickstart`

Example
-------

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
