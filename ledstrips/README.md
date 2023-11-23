# Ledstips

## Create the app outlines:
```
/> flet create ledstrips

    Copying from template version 0.0.0.post9.dev0+cdc6738
    create  .
    create  main.py
    create  assets
    create  assets/manifest.json
    create  assets/icon.png
    create  assets/favicon.png
    create  README.md
    create  .gitignore
    create  .gitattributes


    Done. Now run:

    cd ledstrips
    flet run
```

## Run the app on your Android device:
```
/> cd ledstrips
/> flet run --android
```
The app will be run in a web server in the background and a QR code will appear.  
Scan the QR code on your device and navigate to the app's web page.  

Note that code changes will get deployed while this is running, so you can "hot"
see and test your code changes!  

see: https://flet.dev/docs/guides/python/testing-on-android/  

---

## Build APK:
And here's where things get VERY complicated and I didn't get it to work.  
I spent several days trying all kinds of things.  
I've basically found 2 paths in generating a deployable Android APK:  
1. using the `Cordova` framework to basically run the app as a web app in its own container;  
2. using the `serious-python` framework to basically run the app through a light weight Flutter/Dart project that then loads your Python app and hands it over to the embedded Python executor;
https://github.com/flet-dev/serious-python/blob/main/README.md  

The app runs fine as a desktop app but I can't get it to load fully on either an Android VM or on a real physical device.  
I am able to build an APK without too much struggle and deploying it on an Android device will show the Flutter splashscreen, followed by an hourglass and never get any further.  It always shows this error:  
```
I/flutter ( 6972): Connecting to Flet server flet.sock...
I/flutter ( 6972): Connecting to Socket server flet.sock...
I/flutter ( 6972): Error connecting to Flet server: SocketException: Connection failed (OS Error: No such file or directory, errno = 2), address = flet.sock, port = 0
I/flutter ( 6972): Reconnect in 200 milliseconds
```

#### Going the `serious-python` route:
1. code ... (I'm using VSCode for the coding and Anaconda for Python environment management)

2. generate the app zip-file that `serious_python` will run on your device:
```
/> dart run serious_python:main package app/src

/> mv app/app.zip app/ledstrips.zip
/> ls -la app/
-rw-r--r--.  1 jcreyf 1615585 Nov 22 20:05 ledstrips.zip
```

3. build the APK:  
(get NDK from: https://developer.android.com/ndk/downloads)  
```
/> export ANDROID_SDK_ROOT="/tools/Android/Sdk"
/> export NDK_VERSION=26.1.10909125
/> export SDK_VERSION=android-33
/> export PATH=/tools/Android/Sdk/tools/bin:$PATH

/> pip install python-for-android
/> pip install --upgrade cython

/> p4a create --requirements flet,pyyaml --arch arm64-v8a --arch armeabi-v7a --arch x86_64 --sdk-dir $ANDROID_SDK_ROOT --ndk-dir $ANDROID_SDK_ROOT/ndk/$NDK_VERSION --dist-name serious_python
```
I got:  
```
lots and lots and lots of output...
...
[INFO]:    # Your distribution was created successfully, exiting.
[INFO]:    Dist can be found at (for now) /home/jcreyf/.local/share/python-for-android/dists/serious_python
```
no APK yet though!  
now actually generate the APK:  
https://github.com/flet-dev/serious-python/blob/main/README.md  
https://github.com/kivy/python-for-android  
https://docs.flutter.dev/deployment/android  
```
/> export SERIOUS_PYTHON_P4A_DIST=/home/jcreyf/.local/share/python-for-android/dists/serious_python
/> flutter clean
/> flutter build apk
...
Running Gradle task 'assembleRelease'...                           47.7s
✓  Built build/app/outputs/flutter-apk/app-release.apk (111.8MB).

/> ls -la build/app/outputs/flutter-apk/
-rw-r--r--. 1 jcreyf 117199261 Nov 22 20:11 app-release.apk
-rw-r--r--. 1 jcreyf        40 Nov 22 20:12 app-release.apk.sha1
```

4. copy the APK to your mobile device and install
(it installs fine but all I see when I start it, is the FLutter splash screen and then followed by waiting spinner for ever)
The above error shows when running in the Android Studio emulator.  
