===============
AXEMAS CookBook
===============

Updating Sidebar Whenever it appears
====================================

By default content of a section is only loaded once, the first time the section itself appears.
The Sidebar specifically is only loaded when the application starts, and is never reloaded again.

In case you need to display content that might change during the application lifetime, you will need
to somehow receive a notification each time the sidebar appears so that you can actually force its update.

IOS
---

On **iOS** you can easily achieve this, by calling a custom *handler* from your sidebar ``AXMSectionController``
each time the ``sectionViewWillAppear`` is performed::

    [NavigationSectionsManager registerController:[SidebarSectionController class] forRoute:@"www/sidebar.html"];

    @implementation SidebarSectionController
        - (void)sectionViewWillAppear {
            [self.section.bridge callHandler:@"on-sidebar-appears"];
        }
    @end


This will correctly call the ``on-sidebar-appears`` handler on Javascript both when the sidebar is
displayed the first time and each time its opened/closed by the user.

Android
-------

On **Android** you can achieve a similar result by relying on the ``sectionFragmentWillResume`` method::

    NavigationSectionsManager.registerController(this, SidebarSectionController.class, "www/sidebar.html");
    
    public class SidebarSectionController extends AXMSectionController  {
        @Override
        public void sectionFragmentWillResume() {
            super.sectionFragmentWillResume();
            section.getJSBridge().callJS("on-sidebar-appears", new JSONObject(), null);
        }
    }

While this is enough to update the sidebar each time the user switched the application in/out of background,
it won't update it when the sidebar is opened/closed through the sidebar button. So to achieve the same
behaviour we had on iOS it is required to also ``@Override`` the ``onSidebarOpened`` method inside the ``MainActivity``
and forcefully trigger a ``sectionFragmentWillResume`` each time the sidebar is opened/closed::

    public class MainActivity extends AXMActivity {
        @Override
        public void onSidebarOpened() {
            SectionFragment sidebarFragment = (SectionFragment)getFragmentManager().findFragmentByTag("sidebar_fragment");
            ((SidebarSectionController)sidebarFragment.getRegisteredSectionController()).sectionFragmentWillResume();
        }
    }
    
