===========
Android API
===========

Declaring Sections
==================

The application's MainActivity must extend ``AXMActivity`` which creates the application main structure. Unlike iOS there is no support for tabs yet.
In the ``onCreate`` of your MainActivity initialize the root section by calling ``NavigationSectionsManager.makeApplicationRootController()``.
``makeApplicationRootController()`` accepts a JSONObject containing the section's data::

    JSONObject data = new JSONObject();
    try {
        data.put("url", "www/index.html");
        data.put("title", "Home");
    } catch (JSONException e) {
        e.printStackTrace();
    }
    NavigationSectionsManager
            .makeApplicationRootController(this, data);

The created section will contain content of ``www/index.html`` and will be
titled ``Home``. Further sections can be pushed onto the navigation stack
using ``axemas.goto(dictionary)`` from Javascript.

An application with sidebar can also be created by passing a section data as
sidebar to the ``makeApplicationRootController``::

    JSONObject data = new JSONObject();
    try {
        data.put("url", "www/index.html");
        data.put("toggleSidebarIcon", "reveal-icon");
        data.put("title", "Home");
    } catch (JSONException e) {
        e.printStackTrace();
    }
    NavigationSectionsManager
            .makeApplicationRootController(this, data, "www/sidebar.html");

The sidebar will be created with content from the section data passed as
``sidebarURL`` parameter, sections that have a ``toggleSidebarIcon`` 
value in section data will provide a button to open and close the sidebar
with the given icon. If the value is omitted, even when the sidebar is
enabled, there will be no button to show it.

The ``NavigationSectionsManager`` manages the whole AXEMAS navigation
system, creates the sections and keeps track of the current *Fragment Stack*,
*Action Bar* and *Sidebar* which are exposed through
``NavigationSectionsManager`` methods:

    - goTo
    - pushFragment
    - sidebarButtonVisibility
    - toggleSidebar
    - showProgressDialog
    - hideProgressDialog
    - showDismissibleAlertDialog
    - enableBackButton

Section Controllers
===================

Section controllers permit to attach native code to each section,
doing so is as simple as subclassing section controllers and
providing ``sectionWillLoad`` and ``sectionDidLoad`` methods.

Inside those methods it is possible to register additional native
functions on the javascript bridge.

Inside ``sectionWillLoad`` method of ``SectionController`` subclass
it is possible to register handlers which will be available
in Javascript using ``axemas.call``::

    this.section.getJSBridge().registerHandler("openMap", new JavascriptBridge.Handler() {
        @Override
        public void call(Object data, JavascriptBridge.Callback callback) {

            String uri = "https://maps.google.com/maps";
            Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse(uri));
            section.startActivity(i);

        }
    });

Registering the ``SectionController`` for a section can be done
using the ``NavigationSectionsManager``::

    NavigationSectionsManager
                .registerController(this,HomeSectionController.class, "www/index.html");

Calling JS from native code is also possible using the section bridge,
after you registered your handlers in JavaScript with ``axemas.register``::

    axemas.register("handler_name", function(data, callback) {
        callback({data: data});
    });

Calling ``handler_name`` from native code from a ``SectionController``
is possibile using the javascript bridge ``callHandler``::

    this.section.getJSBridge().callJS("send-passenger-count", data, new JavascriptBridge.AndroidCallback() {
        @Override
        public void call(JSONObject data) {
            Log.d("axemas", "Callback with responseData: "+ data.toString());
        }
    });

``SectionController`` available callbacks:

- *sectionDidLoad* triggered when the webpage finished loading
- *sectionWillLoad* just before the webpage will start to load
- *sectionOnViewCreate(ViewGroup view)* when the fragment is first created
- *boolean isInsideWebView(MotionEvent ev)* whenever a touch event for the webview happens, can be used to return block events to be trapped by webview.

- *sectionFragmentWillPause* triggered by fragment's onPause
- *sectionFragmentWillResume* triggered by fragment's onResume
- *sectionFragmentOnActivityResult* triggered by fragment's onActivityResult
- *sectionFragmentOnSaveInstanceState* triggered by fragment onSaveInstanceState
- *sectionFragmentOnCreateView* triggered by fragment View Creation during inflation


