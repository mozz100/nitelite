#!/usr/bin/env python -u
import os, json, yaml, sys

import logging
logging.basicConfig()

from phue import Bridge

# Load some config.  The hue_config.json must contain a username that's whitelisted
# on the specified bridge.  See https://github.com/studioimaginaire/phue
this_dir             = os.path.dirname(os.path.realpath(__file__))
hue_config_file_path = os.path.join(this_dir, 'hue_config.json')
nitelite_config_path = os.path.join(this_dir, 'nitelite.yml')

with open(hue_config_file_path, 'r') as f:
    hue_config = json.loads(f.read())
with open(nitelite_config_path, 'r') as f:
    nitelite_config = yaml.safe_load(f.read())

light_ids  = nitelite_config['light_ids']
bridge     = Bridge(hue_config['hue']['address'], config_file_path=hue_config_file_path)

# Use the phue API to get a dictionary with the light id as the key
all_lights = bridge.get_light_objects('id')

# Now get just the lights specified by the nitelite.yml file
lights     = [all_lights[k] for k in all_lights.keys() if k in light_ids]

def set_state(state_name):
    """
    Apply each property found in the named state.
    States are defined in nitelite.yml.
    """
    desired_state = nitelite_config[state_name]

    for l in lights:
        for prop in desired_state.keys():
            print "%s: Setting %s to %s" % (l.name, prop, desired_state[prop])
            setattr(l, prop, desired_state[prop])

# Can call with a state name to use from the command line
if __name__ == "__main__":
    state_name = sys.argv[1]
    set_state(state_name)