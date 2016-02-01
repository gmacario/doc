.. _ios_api:

=======
iOS API
=======

Declaring Sections
==================

The main application controller (``window.rootViewController``) must be
created using ``[NavigationSectionsManager makeApplicationRootController]``.

``makeApplicationRootController`` accepts an array of section data, each data
will be used to create a tab with a section inside.

To create an application with a stack of sections (using a *Navigation Controller*),
and not tabs, just pass data for a single section data:

.. code-block:: objc

    [NavigationSectionsManager makeApplicationRootController:@[@{
            @"url":@"www/index.html",
            @"title":@"Home",
        }]
    ];

The created section will contain content of ``www/index.html`` and will be
titled ``Home``. Further sections can be pushed onto the navigation stack
using ``axemas.goto(dictionary)`` from Javascript. 

To create an application with a TabBar just pass data for multiple sections
into the ``makeApplicationRootController`` array, each section must have an
``url`` pointing to the section path and can have a ``title`` and ``icon`` which
will be used as title and icon for the TabBar tabs.

An application with sidebar can also be created by passing a section data as
sidebar to the ``makeApplicationRootController``:

.. code-block:: objc

    [NavigationSectionsManager 
        makeApplicationRootController:@[@{
            @"url":@"www/index.html",
            @"title":@"Home",
            @"toggleSidebarIcon":@"reveal-icon"}]
        withSidebar:@{@"url":@"www/sidebar.html"}
    ];

The sidebar will be created with content from the section data passed in
``withSidebar`` parameter, sections that have a ``toggleSidebarIcon``
value in section data will provide a button to open and close the sidebar
with the given icon. If the value is omitted, even when the sidebar is
enabled, there will be no button to show it.

.. _ios_section_controller:

Section Controllers
===================

Section controllers permit to attach native code to each section,
doing so is as simple as subclassing section controllers and
providing ``sectionWillLoad`` and ``sectionDidLoad`` methods.

Inside those methods it is possible to register additional native
functions on the javascript bridge.

Inside ``viewWillLoad`` method of ``SectionController`` subclass
it is possible to register handlers which will be available
in Javascript using ``axemas.call``:

.. code-block:: objc

    @implementation HomeSectionController

    - (void)sectionWillLoad {
        [self.section.bridge registerHandler:@"openMap" handler:^(id data, WVJBResponseCallback responseCallback) {
            UINavigationController *navController = [NavigationSectionsManager activeNavigationController];
            [navController pushViewController:[[MapViewController alloc] init] animated:YES];

            if (responseCallback) {
                responseCallback(nil);
            }
        }];
    }

    @end

Registering the ``SectionController`` for a section can be done
using the ``NavigationSectionsManager``:

.. code-block:: objc

    [NavigationSectionsManager registerController:[HomeSectionController class] forRoute:@"www/index.html"];

Calling JS from native code is also possible using the section bridge,
after you registered your handlers in JavaScript with ``axemas.register``:

.. code-block:: javascript

    axemas.register("handler_name", function(data, callback) {
        callback({data: data});
    });

Calling ``handler_name`` from native code from a ``SectionController``
is possibile using the javascript bridge ``callHandler``:

.. code-block:: objc

    [self.section.bridge callHandler:@"handler_name"
                                data:@{@"key": @"value"}
                    responseCallback:^(id responseData) {
            NSLog(@"Callback with responseData: %@", responseData);
    }];

``SectionController`` available callbacks:

- *sectionDidLoad* triggered when the webpage finished loading
- *sectionWillLoad* just before the webpage will start to load
- *sectionViewWillAppear* when the section is going to be displayed to the user.
- *sectionOnViewCreate:(UIView*)view* when the section view is first created.
- *(BOOL)isInsideWebView:(CGPoint)point withEvent:(UIEvent*)event* whenever a touch event for the webview happens, can be used to return block events to be trapped by webview.
- *navigationbarRightButtonAction* Triggered whenever the right button in the navigationBar is pressed.

NavigationSectionsManager
=========================

The ``NavigationSectionsManager`` manages the whole AXEMAS navigation
system, creates the sections and keeps track of the current *Navigation Controller*,
*TabBar Controller* and *Sidebar Controller* which are exposed through
``NavigationSectionsManager``.

.. objc:method:: (void)registerDefaultController:(Class)controllerClass

    Registers a given :ref:`ios_section_controller` for the specified route (html file).

.. objc:method:: (void)registerController:(Class)controllerClass forRoute:(NSString*)path

    Registers a given :ref:`ios_section_controller` as the default controller which is used for all
    the sections that do not provide a specific section controller.

.. objc:method:: (UIViewController*)makeApplicationRootController:(NSArray*)tabs

    Creates one or more :ref:`ios_section_controller`. The first controller specified
    in the array is considered the root controller. If more than one controller is
    provided a ``TabBar`` is created with each controller being a Tab.

    The ``tabs`` list should contain dictionaries in the format:

    .. code-block:: objc

        @{
            @"url": @"www/index.html",
            @"title": @"Home",
            @"toggleSidebarIcon": @"reveal-icon"
        }

.. objc:method:: (UIViewController*)makeApplicationRootController:(NSArray*)tabs withSidebar:(NSDictionary*)sidebarData

    Creates one or more :ref:`ios_section_controller`. The first controller specified
    in the array is considered the root controller. If more than one controller is
    provided a ``TabBar`` is created with each controller being a Tab.

    This also creates a ``SideBar`` with the :ref:`ios_section_controller` described by ``sidebarData``
    as the sidebar content.

    The ``tabs`` list and ``sidebarData`` should contain dictionaries in the format:

    .. code-block:: objc

        @{
            @"url": @"www/index.html",
            @"title": @"Home",
            @"toggleSidebarIcon": @"reveal-icon"
        }

.. objc:method:: (UINavigationController*)activeNavigationController

    Returns the `UINavigationController <https://developer.apple.com/library/ios/documentation/UIKit/Reference/UINavigationController_Class/>`_
    of the application. This is the object that manages the navigation stack (pushing and popping section controllers).
    See reference for a list of provided methods.

.. objc:method:: (UIViewController*)activeController

    Returns the current :ref:`ios_section_controller` on top of the navigation stack.
    This is usually the view that the user is currently looking at.

.. objc:method:: (id)activeSidebarController

    Returns the :java:ref:`AXMSidebarController` of the application.
    This is the object that manages the sidebar of the application if available.
    It also provides the following methods to manage the sidebar:

        - ``(IBAction)revealToggle:(id)sender``
        - ``UIViewController *rearViewController``
        - ``FrontViewPosition frontViewPosition``
        - ``(void)setFrontViewPosition:(FrontViewPosition)frontViewPosition animated:(BOOL)animated``

.. objc:method:: (void) setSidebarButtonVisibility:(BOOL)visible

    Hides/Shows the sidebar button in the navigationbar

.. objc:method:: (void)goto:(NSDictionary*)data animated:(BOOL)animated

    Pushes on the view navigation stack the given  :ref:`ios_section_controller`. This works like
    :ref:`js_goto` and accepts ``data`` as ``NSDictionary`` with the same data as the related Javascript
    Object.

.. objc:method:: (void)showProgressDialog

    Displays a spinner on top of the application. This is automatically called
    whenever a new section is loaded.

.. objc:method:: (void)hideProgressDialog

    Hides the currently displayed spinner.

.. objc:method:: (void)store:(NSString*)value withKey:(NSString *)key

    Stores a new value in the application persistent storage.

.. objc:method:: (NSString *)getValueFrom:(NSString*)key

    Retrieves a previously stored value from the application persistent storage.

.. objc:method:: (void)removeValueFrom:(NSString*)key

    Deletes a value from the application persistent storage.
