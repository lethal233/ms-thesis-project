#!/bin/bash
if [ $# -lt 1 ]; then
    echo "Usage: $0 recording_db_file_path"
    exit 1
fi

source $HOME/Desktop/shilonl/autoware/install/setup.bash

ros2 bag play $1 -r 0.5 -s sqlite3