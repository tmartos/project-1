[app]

# (str) Title of your application
title = CuestionarioApp

# (str) Package name
package.name = cuestionarioapp

# (str) Package domain (needed for android/ios packaging)
package.domain = com.miempresa

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,json
android.presplash_color = #ffffff

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,temario/*

# (list) Source files to exclude using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,kivymd,cryptography,plyer

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,KIVY,ON_START

#
# OSX Specific identifiers
#

# (str) Name, formal name and short name of application
app.name = CuestionarioApp
app.formal_name = CuestionarioApp
app.short_name = CuestionarioApp


# (Versión mínima de Android)
android.minapi = 21

#
# author
#

# (str) Author of the application (used for labeling and packaging)
author = TuNombre

# (str) Author email
author.email = tuemail@example.com

# (str) Author url
author.url = http://www.example.com

# (str) Author username on PyPI
#author.username = TuNombre

# (str) Author's homepage (URL)
#author.homepage = http://www.example.com

# (str) Author's commercial homepage (URL)
#author.commercial = http://www.example.com

#
# Localizations
#

# (list) List of supported localizations
#localizations = en,it,fr

# (list) List of allowed localizations
#allowed_localizations = en,it,fr

# (str) Application license
#license = Apache-2.0

# (str) Application license file
#license.file = LICENSE

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (used if no presplash is set)
#android.presplash_background = #FFFFFF

# (string) Presplash animation using Lottie file (see http://airbnb.io/lottie)
#android.presplash_lottie = %(source.dir)s/data/splash.json

# (str) Path to a custom kivy project template (used to extend kivy default project)
#android.add_template = %(source.dir)s/android-template/

# (str) Android NDK version to use
android.ndk = 25b
android.sdk = 31
# (str) Android NDK API to use
android.ndk_api = 21

# (str) Android NDK language to use, options are x86, armeabi-v7a and arm64-v8a
#android.ndk_language = armeabi-v7a

# (str) Override the architecture used for NDK compilation. This is a list
# of the architectures you would like to use. Valid options are
# any combination of the following: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (str) ANT directory (needed for android support)
#android.ant_dir = /home/kivy/work/ant

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# during builds
#android.skip_update = False

# (bool) If True, then upload the source to p4a before building or deploying
#android.use_p4a = True

# (str) The path to the p4a build directory, if you want to override the default one
#android.p4a_dir = /some/custom/path

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the package
#android.whitelist =

# (str) Path to a custom Python library directory
#android.library_dir =

# (str) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android additional libraries to copy into libs/armeabi-v7a
#android.add_libs_armeabi-v7a = libs/android/*.so
#android.add_libs_armeabi-v7a = libs/android/*.jar

# (list) Android additional libraries to copy into libs/arm64-v8a
#android.add_libs_arm64-v8a = libs/android/*.so
#android.add_libs_arm64-v8a = libs/android/*.jar

# (list) Android additional libraries to copy into libs/x86
#android.add_libs_x86 = libs/android/*.so
#android.add_libs_x86 = libs/android/*.jar

# (list) Android additional libraries to copy into libs/x86_64
#android.add_libs_x86_64 = libs/android/*.so
#android.add_libs_x86_64 = libs/android/*.jar

# (bool) Indicate whether the app should be built as a universal binary
#android.universal_apk = True

# (str) Presplash background color (used if no presplash is set)
#android.presplash_background = #FFFFFF

# (str) Presplash animation using Lottie file (see http://airbnb.io/lottie)
#android.presplash_lottie = %(source.dir)s/data/splash.json

# (str) URL to the Git repository containing the source, will be added to the manifest.
#android.source_url =

# (list) List of Java .jar files to add to the libs/armeabi-v7a
#android.add_jars = libs/android/*.jar

# (list) List of Java files to add to the android project (can be java or a directory containing the files)
#android.add_src =

# (list) List of additional gradle dependencies
#android.gradle_dependencies = org.ini4j:ini4j:0.5.4

# (list) List of python packages to add to the build
#android.pip_packages = requests

# (str) Custom build tasks (i.e. prebuild, etc)
#android.add_tasks = prebuild,debug

# (str) Set the ANNDTOOL environment variable for android
#android.ann_dtool = "/path/to/your/android-ndk-rXX"

# (str) Google Play Store account credentials path .json file
#android.google_play_account_json = %(source.dir)s/android/credentials.json

# (str) Google Play Store packagename
#android.google_play_packagename = org.kivy.android.myapp

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (list) Features to add to your app's manifest
#android.features = FEATURE_CAMERA, HARDWARE_ACCELERATED

# (buildozer) The value of $(PACKAGE) as defined in buildozer.spec
#android.manifest_package = org.kivy.android.myapp

# (buildozer) The name of the python interpreter to use
#android.python_recipe = kivy_python

# (str) Android Gradle plugin version
#android.gradle_plugin_version = 3.0.1

# (str) Android Gradle plugin version
#android.gradle_plugin_version = 3.0.1

# (str) Python version to use
#android.python_version = 3.8

# (list) List of java .jar files to add to the project
#android.add_jars =

# (list) List of Java files to add to the project
#android.add_src =

# (list) List of Gradle dependencies to add
#android.gradle_dependencies =

# (list) List of pip packages to install
#android.pip_packages =

# (str) Path to a custom Gradle file
#android.gradle_file =

# (str) Additional arguments to pass to the Gradle build
#android.gradle_args =

# (list) List of Java .jar files to add to the project
#android.add_jars =

# (list) List of Java files to add to the project
#android.add_src =

# (list) List of Gradle dependencies to add
#android.gradle_dependencies =

# (list) List of pip packages to install
#android.pip_packages =

# (str) Path to a custom Gradle file
#android.gradle_file =

# (str) Additional arguments to pass to the Gradle build
#android.gradle_args =

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be cloned in the current directory)
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Bootstrap to use for android builds
#p4a.bootstrap = sdl2

# (str) Custom bootstrap
#p4a.custom_bootstrap =

# (str) Requirements to add if not already in the "requirements" section
#p4a.requirements =

# (str) Custom source dirs
#p4a.source_dirs =

# (list) Extra aapt flags
#p4a.aapt_flags = --extra-packages=org.kivy.android:org.kivy.android

# (bool) Add "armeabi-v7a" to list of supported architectures for android
#p4a.arch_armeabi = False

# (bool) Add "arm64-v8a" to list of supported architectures for android
#p4a.arch_arm64 = False

# (bool) Add "x86" to list of supported architectures for android
#p4a.arch_x86 = False

# (bool) Add "x86_64" to list of supported architectures for android
#p4a.arch_x86_64 = False

# (str) Custom command to build the APK.
#p4a.command =

# (str) Custom command to build the APK.
#p4a.command =

#
# iOS specific
#

# (str) Path to a custom kivy-ios build directory
#ios.kivy_ios_dir = ../kivy-ios

# (str) Name of the certificate to use for signing the app
#ios.codesign.debug = "iPhone Developer"

# (str) Name of the certificate to use for signing the app
#ios.codesign.release = "iPhone Distribution"

# (str) Path to the provisioning profile (if any)
#ios.provisioning_profile = %(source.dir)s/deploy/provision.plist

# (str) Path to the certificate file
#ios.certificate = %(source.dir)s/deploy/cert.p12

# (str) Password to the certificate file
#ios.password = XXXXXXXX

# (str) The architecture to target (armv7, arm64, x86_64)
#ios.arch = arm64

# (str) The build directory
#ios.build_dir = %(source.dir)s/build

# (str) The min iOS target version
#ios.min_version = 8.0

# (list) List of additional xcode build settings
#ios.codesign_flags = ["-F", "/Users/foo/provisioning_profiles"]

# (str) Pre-signed ipa path
#ios.ipa = %(source.dir)s/dist/myapp.ipa

# (str) Path to buildlib
#ios.buildlib = %(source.dir)s/libs

# (str) iOS framework to link against
#ios.frameworks = kivy

# (str) Specify a git checkout URL for the Kivy-iOS repo
#ios.kivy_ios_url = https://github.com/kivy/kivy-ios

# (str) Specify a git branch or tag for the Kivy-iOS repo
#ios.kivy_ios_branch = master

# (str) Additional xcode arguments
#ios.extra_xcode_args = ["-p", "123"]

# (str) Override for xcode configuration
#ios.xcode_configuration = Debug

# (str) Override for xcode action
#ios.xcode_action = build

# (str) Override for xcode sdk
#ios.xcode_sdk = iphoneos

# (str) Override for xcode target
#ios.xcode_target = %(app.name)s

# (str) Override for xcode workspace
#ios.xcode_workspace = %(app.name)s.xcworkspace

# (str) Override for xcode scheme
#ios.xcode_scheme = %(app.name)s

# (str) Override for xcode destination
#ios.xcode_destination = generic/platform=iOS

# (str) Override for xcode simulator
#ios.xcode_simulator = iPhone 11

# (str) Override for xcode device
#ios.xcode_device = auto

# (str) Override for xcode configuration
#ios.xcode_configuration = Debug

# (str) Override for xcode action
#ios.xcode_action = build

# (str) Override for xcode sdk
#ios.xcode_sdk = iphoneos

# (str) Override for xcode target
#ios.xcode_target = %(app.name)s

# (str) Override for xcode workspace
#ios.xcode_workspace = %(app.name)s.xcworkspace

# (str) Override for xcode scheme
#ios.xcode_scheme = %(app.name)s

# (str) Override for xcode destination
#ios.xcode_destination = generic/platform=iOS

# (str) Override for xcode simulator
#ios.xcode_simulator = iPhone 11

# (str) Override for xcode device
#ios.xcode_device = auto

# (str) Override for xcode configuration
#ios.xcode_configuration = Debug

# (str) Override for xcode action