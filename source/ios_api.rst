=======
iOS API
=======

Declaring Sections
==================

The main application controller (``window.rootViewController``) must be
created using ``[NavigationSectionsManager makeApplicationRootController]``.

``makeApplicationRootController`` accepts an array of section data, each data
will be used to create a tab with a section inside.

To create an application with a stack of sections (using a *Navigation Controller*),
and not tabs, just pass data for a single section data::

    [NavigationSectionsManager makeApplicationRootController:@[@{
            @"url":@"www/index.html",
            @"title":@"Home",
        }]
    ];

The created section will contain content of ``www/index.html`` and will be
titled ``Home``. Further sections can be pushed onto the navigation stack
using ``axemas.goto(dictionary)`` from Javascript. 

To create an application with a TabBar just pass data for multiple sections
into the ``makeApplicationRootController`` array, each section must have an 
``url`` pointing to the section path and can have a ``title`` and ``icon`` which
will be used as title and icon for the TabBar tabs.

An application with sidebar can also be created by passing a section data as
sidebar to the ``makeApplicationRootController``::

    [NavigationSectionsManager 
        makeApplicationRootController:@[@{
            @"url":@"www/index.html",
            @"title":@"Home",
            @"toggleSidebarIcon":@"reveal-icon"}]
        withSidebar:@{@"url":@"www/sidebar.html"}
    ];

The sidebar will be created with content from the section data passed in
``withSidebar`` parameter, sections that have a ``toggleSidebarIcon`` 
value in section data will provide a button to open and close the sidebar
with the given icon. If the value is omitted, even when the sidebar is
enabled, there will be no button to show it.

The ``NavigationSectionsManager`` manages the whole AXEMAS navigation
system, creates the sections and keeps track of the current *Navigation Controller*,
*TabBar Controller* and *Sidebar Controller* which are exposed through
``NavigationSectionsManager`` methods:

    - activeNavigationController
    - activeController
    - activeSidebarController
    - goto
    - pushController
    

Section Controllers
===================

Section controllers permit to attach native code to each section,
doing so is as simple as subclassing section controllers and
providing ``sectionWillLoad`` and ``sectionDidLoad`` methods.

Inside those methods it is possible to register additional native
functions on the javascript bridge.

Inside ``viewWillLoad`` method of ``SectionController`` subclass
it is possible to register handlers which will be available
in Javascript using ``axemas.call``::

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

Registering the ``SectionController`` for a section can be done
using the ``NavigationSectionsManager``::

    [NavigationSectionsManager registerController:[HomeSectionController class] forRoute:@"www/index.html"];

Calling JS from native code is also possible using the section bridge,
after you registered your handlers in JavaScript with ``axemas.register``::

    axemas.register("handler_name", function(data, callback) {
        callback({data: data});
    });

Calling ``handler_name`` from native code from a ``SectionController``
is possibile using the javascript bridge ``callHandler``::

    [self.section.bridge callHandler:@"handler_name" 
                                data:@{@"key": @"value"} 
                    responseCallback:^(id responseData) {
            NSLog(@"Callback with responseData: %@", responseData);
        }];

``SectionController`` available callbacks:

- *sectionDidLoad* triggered when the webpage finished loading
- *sectionWillLoad* just before the webpage will start to load
