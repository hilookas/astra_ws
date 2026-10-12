#!/usr/bin/env bash
set -e

source /opt/ros/humble/setup.bash

if [[ -f /workspace/install/setup.bash ]]; then
  source /workspace/install/setup.bash
fi

exec "$@"
