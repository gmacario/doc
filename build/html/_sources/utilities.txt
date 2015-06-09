=========
Utilities
=========

Crash Logging
=============

Android
-------

Splunk MINT is used to log crash reports. To enable it, it's necessary to be registered on their service
(https://mint.splunk.com/) Next to the app creation on their portal initiate this code inside the Activity wich extends
AXMActivity with::

    this.startCrashReporter();


The next step is to add this config string inside strings.xml file inside res/values folder inside your Android
project. This String resource contains the api-key got by Splunk MINT Portal for your application.

    <string name='splunk_api_key'></string>

In the end you have to configure gradle to work with the new Mint dependency required.
Add this code to your build.gradle project file::

    repositories {
        maven {
            url "https://mint.splunk.com/gradle/"
        }
    }

    dependencies {
        compile 'com.splunk.mint:mint:4.2'
    }

Once these 3 steps are done you have a fully implemented crash reporter on your Axemas Application.
