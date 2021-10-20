# plant-manager
Plant manager using Grow Care VegTrug

The goal of this project is to receive an email when any of the plants connected to the manager need to be watered.

## Usage
Running plantmgr.py file with default settings file (config.yaml) will iterarte within each device looking for their active parameters. You also can define a custom settings file by defining their name into config.yaml (eg. specific_config.yaml) where you would define your own values for any parameter. Program will look for the value in custom config file and if it can't find it, the default value will be used.

## Dependences (WIP)
pip install mailjet_rest