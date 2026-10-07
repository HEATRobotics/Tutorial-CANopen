FROM ros:humble-ros-base-jammy
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive ROS_HOME=/tmp/ros
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions python3-pip python3-pytest \
    ros-humble-rosidl-default-generators ros-humble-rosidl-default-runtime \
    ros-humble-std-msgs ros-humble-std-srvs can-utils iproute2 git \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt
COPY ros2_ws/src/ /opt/tutorial_ws/src/
RUN source /opt/ros/humble/setup.bash && cd /opt/tutorial_ws \
    && colcon build --symlink-install --base-paths src
COPY docker/entrypoint.sh /usr/local/bin/rosenv
RUN chmod +x /usr/local/bin/rosenv \
    && printf '\nsource /opt/ros/humble/setup.bash\nsource /opt/tutorial_ws/install/setup.bash\nif [ -f /work/tutorial/ros2_ws/install/setup.bash ]; then source /work/tutorial/ros2_ws/install/setup.bash; fi\n' >> /etc/bash.bashrc
WORKDIR /work/tutorial
ENTRYPOINT ["/usr/local/bin/rosenv"]
# Packages are installed; node exercises intentionally remain incomplete.
CMD ["sleep", "infinity"]
