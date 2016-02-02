.. _js_api:

JavaScript API
==============

The JavaScript module ``axemas.js`` permits interaction with the native code of the application:

    - goto
    - gotoFromSidebar
    - call
    - alert
    - dialog
    - showProgressHUD
    - hideProgressHUD
    - getPlatform
    - storeData
    - fetchData
    - removeData
    - log

.. _js_goto:

goto
----

Pushes new ``section`` on the navigation stack. It is the equivalent of the iOS ``[NavigationSectionsManager goto]`` and Android's ``NavigationSectionsManager.goTo()``.
All three functions accept a dictionary as **payload** which defines the extra actions the ``goto`` call must execute::

    axemas.goto(
        {"url":"www/home.html",
        "title":"HOME",
        "toggleSidebarIcon":"slide_icon",
        "stackMaintainedElements": 0,
        "stackPopElements": 0}
    );

The **payload** structure is shared between JavaScript, Objective C and Java, and accepts the following parameters:

    - ``url`` contains the local or remote address from which the WebView must load the content
    - ``title`` (optional) is the tile show in the application's ViewController / Action Bar.
    - ``toggleSidebarIcon`` (optional) is the sidebar's icon to be displayed and if missing a button to open the sidebar will not be created
    - ``actionbarRightIcon`` (optional) icon to display as a button on the right of the actionbar inside the target section, pressing the button triggers the ``navigationbarRightButtonAction`` event on section controllers.
    - ``stackMaintainedElements`` (optional) instructs the navigation stack to pop all views and maintain the last X ``sections`` indicated on the bottom of the stack; it is ill advised to use in conjunction with ``stackPopElements``
    - ``stackPopElements`` (optional) instructs the navigation stack to pop the first X ``sections``; it is ill advised to use in conjunction with ``stackMaintainedElements``
    - ``animation`` (optional) only supported on iOS platform, can be used to change the default push/pop animation in one of ``"fade"`` or ``"slidein"`` values

gotoFromSidebar
---------------

Same as ``goto`` but closes the sidebar and must be used only inside the sidebar ``section``. Refer to ``goto``::

    axemas.gotoFromSidebar(
        {"url":"www/home.html",
        "title":"HOME",
        "toggleSidebarIcon":"slide_icon",
        "stackMaintainedElements": 0,
        "stackPopElements": 0}
    );

call
----

The ``call`` enables JavaScript to execute a native registered handler inside a ``SectionController``::

    axemas.call('openNativeController');

    axemas.call('execute-and-return', '{"payload": "something"}', function(result) {
        alert(JSON.strgify(result));
    });

alert
-----

Creates a native dismissible alert dialog with a title and a message::

    axemas.alert('Alert title', "Alert message");


dialog
------

Generates a native dialog with a title, a message and a maximum of three buttons. When pressing a button a callback returns the button's value as integer, range [0-3]::

    axemas.dialog('Dialog title', 'Dialog display message', ['Cancel', 'Ok'],function(data) {
        axemas.alert('Pressed button', data.button);
    });

showProgressHUD
---------------

Locks interface interaction by displaying a spinner on the screen. The same spinner is always displayed when lading the contents of a page inside a ``section``::

     axemas.showProgressHUD();


hideProgressHUD
---------------

Used to dismiss a previously displayed progressHUD::

     axemas.hideProgressHUD();


getPlatform
-----------

Uses the ``navigator.userAgent`` object to determine if the current platform. Returns ``Android``, ``iOS`` or ``unsupported``::

     if (axemas.getPlatform() == 'your_platform') {
         //do something
     }


storeData
---------

Uses the Native/WebView's ``localSotrage`` for key/value storing. Data stored will be available next time the application is launched::

    axemas.storeData("key","only_string_values");

fetchData
---------

Returns a previously stored ``value`` providing a ``key``::

    var value = axemas.fetchData("key");

removeData
----------

Permanently removes the previously saved data from the locationStorage::

    axemas.removeData("key")

log
----------

Utility for use native and javascript log system::

    axemas.log("Hello World");

or::
    
    axemas.log({'tag': 'CustomTAG', 'message': "Hello World"});

- ``tag`` is the tag for Android, default is AXEMAS_LOG
- ``message`` is the message of the log as String
