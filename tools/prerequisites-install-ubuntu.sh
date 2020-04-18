# This script is used to get the stb prerequisites installed.
#   - Installs Gstreamer
#   - Installs LIRC
#   - Builds and installs OpenCV from source.
#
# Note: It may take somewhere between 10 minutes to 2 hours to get everything
# installed and built, depending on how powerful of a machine you're using. 
# 90% of that time comes from building and installing OpenCV.
# To speed things up, add a -j# argument to `make`, where the # is your number 
# of CPU cores.

# General Dependencies for opencv
sudo apt install -y build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev

# LIRC
sudo apt install -y lirc

# GStreamer
sudo apt install -y libgstreamer1.0-0 gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa \
    gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio

# Clone down repos. If you want a particular version of OpenCV
# rather than the latest, add `git checkout <opencv-version>` commands
# after the clones.
mkdir ~/opencv_build && cd ~/opencv_build
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git

# Temp build directories
cd ~/opencv_build/opencv
mkdir build && cd build

# Build Opencv
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON \
    -D WITH_LIBV4L=ON \    
    -D WITH_FFMPEG=ON \
    -D WITH_TBB=ON \   
    -D WITH_GTK=ON \
    -D WITH_V4L=ON \
    -D WITH_OPENGL=ON ..

make
sudo make install
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig

# Ensure install was successful
pkg-config --modversion opencv4

echo "You can delete ~/opencv_build now"
echo "Make sure to add 'export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig' to your shell startup file"

# Known Issues
# stb: error while loading shared libraries: libopencv_highgui.so.4.2: cannot open
# shared object file: No such file or directory.
# Solution: https://github.com/cggos/dip_cvqt/issues/1#issuecomment-284103343