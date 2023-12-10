#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/hnam/kobuki_ws/src/kobuki_desktop/kobuki_dashboard"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/hnam/kobuki_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/hnam/kobuki_ws/install/lib/python3/dist-packages:/home/hnam/kobuki_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/hnam/kobuki_ws/build" \
    "/usr/bin/python3" \
    "/home/hnam/kobuki_ws/src/kobuki_desktop/kobuki_dashboard/setup.py" \
     \
    build --build-base "/home/hnam/kobuki_ws/build/kobuki_desktop/kobuki_dashboard" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/hnam/kobuki_ws/install" --install-scripts="/home/hnam/kobuki_ws/install/bin"
