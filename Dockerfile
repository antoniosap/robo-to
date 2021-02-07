#
#
#
FROM ros:foxy

RUN apt-get update && apt-get install -y \
    python3-tk qt5-qmake qtbase5-dev \
    ros-foxy-control-msgs \
    ros-foxy-example-interfaces
    ros-foxy-test-msgs && \
    rm -rf /var/lib/apt/lists/*
