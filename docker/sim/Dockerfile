FROM ros:humble-ros-base

ARG USERNAME=rosdev
ARG UID=1000
ARG GID=1000

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        dbus-x11 \
        liburdfdom-tools \
        mesa-utils \
        python3-colcon-common-extensions \
        ros-humble-desktop \
        ros-humble-joint-state-publisher-gui \
        ros-humble-navigation2 \
        ros-humble-nav2-bringup \
        ros-humble-ros-gz \
        ros-humble-slam-toolbox \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid "${GID}" "${USERNAME}" \
    && useradd --uid "${UID}" --gid "${GID}" --create-home --shell /bin/bash "${USERNAME}"

COPY docker/sim/entrypoint.sh /entrypoint.sh
RUN chmod 0755 /entrypoint.sh

USER ${USERNAME}
WORKDIR /workspace

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
