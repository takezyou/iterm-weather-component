#!/bin/bash

AUTOLAUNCH_DIR=~/Library/ApplicationSupport/iTerm2/Scripts/Autolaunch

if [ -d "$AUTOLAUNCH_DIR" ]; then
    cp -r ../iterm-weather-component $AUTOLAUNCH_DIR/iterm-weather-component
else
    mkdir -p $AUTOLAUNCH_DIR
    cp -r ../iterm-weather-component $AUTOLAUNCH_DIR/iterm-weather-component
fi
