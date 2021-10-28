# plant-manager
Plant manager using Grow Care VegTrug

The goal of this project is to receive an email when any of the plants connected to the manager need to be watered or reviewed.

## Usage
Running plantmgr.py file with default settings file (config.yaml) will iterarte within each device looking for their active parameters. You also can define a custom settings file by defining their name into config.yaml (eg. specific_config.yaml) where you would define your own values for any parameter. Program will look for the value in custom config file and if it can't find it, the default value will be used.

You can configure the project in demo mode by setting 'DEMO' in 'mode' param at settings file. Otherwise, application will run in real mode. In demo mode, no bluetooth connection is established and no email is sent.

If you want to schedule the program you can set a crontab that runs the program. With the example below, program will run at 18:00 every day. Notice that cd command before running python program helps to find settings file.

```sh
crontab -e
0 18 * * * cd [YOUR_PATH_TO_PLANTSMGR] && /usr/bin/python3 plantmgr.py
```

## Dependences (WIP)
:warning: this list is not completed.
```sh
pip3 install mailjet_rest
```