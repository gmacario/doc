.. _android_api:

===========
Android API
===========

Declaring Sections
==================

The application MainActivity must extend ``AXMActivity`` which creates the application main structure.
In the ``onCreate`` of your MainActivity initialize the root section by
calling  ``NavigationSectionsManager.makeApplicationRootController()``
The ``makeApplicationRootController()`` accepts a JSONObject containing the section data:

.. code-block:: java

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
sidebar to the ``makeApplicationRootController``:

.. code-block:: java

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

.. _android_section_controller:

Section Controllers
===================

Section controllers permit to attach native code to each section,
doing so is as simple as subclassing section controllers and
providing ``sectionWillLoad`` and ``sectionDidLoad`` methods.

Inside those methods it is possible to register additional native
functions on the javascript bridge.

Inside ``sectionWillLoad`` method of ``SectionController`` subclass
it is possible to register handlers which will be available
in Javascript using ``axemas.call``:

.. code-block:: java

    this.section.getJSBridge().registerHandler("openMap", new JavascriptBridge.Handler() {
        @Override
        public void call(Object data, JavascriptBridge.Callback callback) {

            String uri = "https://maps.google.com/maps";
            Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse(uri));
            section.startActivity(i);

        }
    });

Registering the ``SectionController`` for a section can be done
using the ``NavigationSectionsManager``:

.. code-block:: java

    NavigationSectionsManager
                .registerController(this,HomeSectionController.class, "www/index.html");

Calling JS from native code is also possible using the section bridge,
after you registered your handlers in JavaScript with ``axemas.register``:

.. code-block:: javascript

    axemas.register("handler_name", function(data, callback) {
        callback({data: data});
    });

Calling ``handler_name`` from native code from a ``SectionController``
is possibile using the javascript bridge ``callHandler``:

.. code-block:: java

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
- *actionbarRightButtonAction* triggered whenever the right button is pressed in the actionbar

NavigationSectionsManager
=========================

The ``NavigationSectionsManager`` manages the whole AXEMAS navigation
system, creates the sections and keeps track of the current *Fragment Stack*,
*Action Bar* and *Sidebar* which are exposed through
``NavigationSectionsManager`` methods.

.. java:import:: android.content Context
.. java:import:: android.app Fragment
.. java:import:: android.app AlertDialog

.. java:method:: public static void registerController(Context context, Class controllerClass, String route)

    Registers a given :ref:`android_section_controller` for the specified route (html file).

.. java:method:: public static void registerDefaultController(Context context, Class controllerClass)

    Registers a given :ref:`android_section_controller` as the default controller which is used for all
    the setions that do not provide a specific section controller.

.. java:method:: public static void makeApplicationRootController(Context context, JSONObject data)

    Creates a new application root :ref:`android_section_controller` (must be called from ``MainActivity.onCreate``).
    ``data`` is the details of the section controller as you would pass them to :java:ref:`goTo`.

.. java:method:: public static void makeApplicationRootController(Context context, JSONObject data, String sidebarUrl)

    Creates a new application root :ref:`android_section_controller` (must be called from ``MainActivity.onCreate``).
    ``data`` is the details of the section controller as you would pass them to :java:ref:`goTo`.
    This method also adds a sidebar, ``sidebarUrl`` is the path of the section html file that should
    be loaded inside the sidebar.

.. java:method:: public static void makeApplicationRootController(Context context, JSONObject data, JSONObject... tabs)

    Creates a new application root :ref:`android_section_controller` (must be called from ``MainActivity.onCreate``).
    ``data`` is the details of the section controller as you would pass them to :java:ref:`goTo`.
    This method also provides additional **tabs** to the application, the root section controller is placed in
    the first tab, while the other ``tabs`` are also additional section controllers data used to fill
    additional tabs in the tabbar.

.. java:method:: public static void makeApplicationRootController(Context context, JSONObject data, String sidebarUrl, JSONObject... tabs)

    Creates a new application root :ref:`android_section_controller` (must be called from ``MainActivity.onCreate``).
    ``data`` is the details of the section controller as you would pass them to :java:ref:`goTo`.
    This method also adds a sidebar, ``sidebarUrl`` is the path of the section html file that should
    be loaded inside the sidebar.
    This method also provides additional **tabs** to the application, the root section controller is placed in
    the first tab, while the other ``tabs`` are also additional section controllers data used to fill
    additional tabs in the tabbar.

.. java:method:: public static void goTo(Context context, JSONObject data)

    Pushes on the view navigation stack the given  :ref:`android_section_controller`. This works like
    :ref:`js_goto` and accepts ``data`` as ``JSONObject`` with the same data as the related Javascript
    Object.

.. java:method:: public static AXMNavigationController getActiveNavigationController(AXMActivity activity)

    Returns the :java:ref:`AXMNavigationController` of the application. This is the object that
    manages the navigation stack (pushing and popping section controllers) and provides the following
    methods to manage the navigation stack:

        - ``void popFragments(final int fragmentsToPop)`` -> Pops up to ``fragmentsToPop`` fragments (sections)
          from the navigation stack.
        - ``void popFragmentsAndMaintain(final int maintainedFragmentsArg)`` -> Pops until only
          ``maintainedFragmentsArg`` fragments (sections) are left on the stack.
        - ``void pushFragment(final Fragment fragment, final String tag)`` -> Pushes a new :java:ref:`Fragment`
          on the navigation stack.

.. java:method:: public static SectionFragment getActiveFragment(Context context)

    Returns the current :ref:`android_section_controller` on top of the navigation stack.
    This is usually the view that the user is currently looking at.

.. java:method:: public static AXMTabBarController getTabBarController(AXMActivity activity)

    Returns the :java:ref:`AXMTabBarController` of the application.
    This is the object that manages the application tabs if available.
    It also provides the following methods to manage the tabs:

        - ``int getSelectedTab()`` -> gets the index of the currently selected tab.
        - ``void setSelectedTab(int idx)`` -> sets the currently selected tab.

.. java:method:: public static AXMSidebarController getSidebarController(AXMActivity activity)

    Returns the :java:ref:`AXMSidebarController` of the application.
    This is the object that manages the sidebar of the application if available.
    It also provides the following methods to manage the sidebar:

        - ``AXMSectionController getSidebarSectionController()`` -> Retrieves the :ref:`android_section_controller`
          bound to the section loaded into the sidebar.
        - ``void setSidebarButtonVisibility(boolean visible)`` -> Hides/Shows the sidebar button in the actionbar
        - ``void setSideBarButtonIcon(String resourceName)`` -> Sets the sidebar button icon from a project resource
        - ``void setSidebarAnimationConfiguration(float alpha, int duration, String hexColor)`` -> change the
          sidebar animation configuration.
        - ``View enableFullSizeSidebar()`` -> Switches to full size sidebar mode. This moves the
          actionbar inside the sidebar instead of being on top of both the sidebar and the content.
          It returns the actionbar View.
        - ``boolean isOpening()`` -> Whenever the sidebar is open or not.
        - ``void toggleSidebar(boolean visible)`` -> Sets sidebar visibility.
        - ``void toggleSidebar()`` -> Toggles sidebar visibility.

.. java:method:: public static void showProgressDialog(Context context)

    Displays a spinner on top of the application. This is automatically called
    whenever a new section is loaded.

.. java:method:: public static void hideProgressDialog(Context context)

    Hides the currently displayed spinner.

.. java:method:: public static void showDismissibleAlertDialog(Context context, String title, String message)

    Displays an alert message with the specified ``title`` and ``message``.
    By default only a dismiss button is provided.

.. java:method:: public static void showDismissibleAlertDialog(Context context, AlertDialog.Builder builder)

    New alert message built with the user provided :java:ref:`AlertDialog.Builder` dialog builder.

.. java:method:: public static void enableBackButton(Context context, boolean toggle)

    Enables/disables the back button in the application.

.. java:method:: public static void store(Context context, String key, String value)

    Stores a new value in the application persistent storage.

.. java:method:: public static String getValueForKey(Context context, String key)

    Retrieves a previously stored value from the application persistent storage.

.. java:method:: public static void removeValue(Context context, String key)

    Deletes a value from the application persistent storage.
