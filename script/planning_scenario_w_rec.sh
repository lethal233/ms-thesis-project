#!/bin/bash
if [ $# -lt 2 ]; then
    echo "Usage: $0 scenario_name [true/false]"
    exit 1
fi

ros2 launch scenario_test_runner scenario_test_runner.launch.py \
    architecture_type:=awf/universe \
    record:=$2 \
    scenario:=$1 \
    sensor_model:=sample_sensor_kit \
    vehicle_model:=sample_vehicle