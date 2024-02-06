#!/bin/bash
# this script is to kill the idle autoware process
ps aux | grep ros | head -n -1 | awk '{ print  }' | xargs kill -9