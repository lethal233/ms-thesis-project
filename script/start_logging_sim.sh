#!/bin/bash
if [ $# -lt 1 ]; then
    echo "Usage: $0 map_folder"
    exit 1
fi
source $HOME/Desktop/shilonl/autoware/install/setup.bash

ros2 launch autoware_launch logging_simulator.launch.xml map_path:=$HOME/Desktop/shilonl/autoware/autoware_map/$1 \
    vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit