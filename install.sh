#!/bin/bash

AUTOLAUNCH_DIR=~/Library/ApplicationSupport/iTerm2/Scripts/Autolaunch
ITERM_WEATHER_AUTOLAUNCH_DIR="$AUTOLAUNCH_DIR/iterm-weather-component"
VIRTUAL_ENV_DIR="$ITERM_WEATHER_AUTOLAUNCH_DIR/iterm2env/versions/3.7.2"

if [ ! -d "$AUTOLAUNCH_DIR" ]; then
    mkdir -p $AUTOLAUNCH_DIR
fi

# Copy repo.
cp -r ../iterm-weather-component $ITERM_WEATHER_AUTOLAUNCH_DIR

# Start your python env.
if [ ! -d "$VIRTUAL_ENV_DIR" ]
then
    python3 -m venv $VIRTUAL_ENV_DIR 
fi

# Activate env.
source $VIRTUAL_ENV_DIR/bin/activate

# Install dependencies
pip install -r $ITERM_WEATHER_AUTOLAUNCH_DIR/requirements.txt

# Deactivate env.
source deactivate 
