#!/bin/env python
import subprocess
import json
import re

models = subprocess.Popen(['xsetwacom', '--list'], stdout=subprocess.PIPE).communicate()[0].split(b'\n')
devices = {}
pr_re = re.compile("\\+([a-zA-Z]+) -\\1")
final_format = {}

def get_device_properties(device_name):
    buttons = {}
    try:
        max_but = int(subprocess.getoutput('xsetwacom -s --get "%s" all | grep -v "does not exist" | grep \'"Button"\''%device_name).split('\n')[-1].split('"Button" ')[1].split('"')[1])
    except IndexError: # no button
        return {}
    for n in range(1, max_but+1):
        o = subprocess.getoutput('xsetwacom --get "%s" Button %d'%(device_name, n))
        if len(o) > 4:
            buttons[n] = o.strip()
    return buttons

for model in models:
    if len(model) < 10:
        continue
    model = model.decode('utf-8').strip()
    model_info = model.split('\t')
    fullname = model_info[0]
    params = dict( p.split(': ') for p in model_info[1:] )
    for typename in 'Finger Pen Pad'.split():
        i = fullname.find(typename)
        if i != -1:
            shortname = fullname[:i-1]
            break
    else:
        print('Unable to find real device name')

    params['name'] = fullname.strip()

    if shortname not in devices:
        devices[shortname] = []

    devices[shortname].append(params)

for name, devices_info in devices.items():
    button_binding = {}
    for device in devices_info:
        buttons = get_device_properties(device['id'])
        if not buttons:
            continue
        dev = {"%s:%s"%(device['type'], but_name) : pr_re.sub("\\1", binding) for but_name, binding in buttons.items()}
        button_binding[device['name']] = dev
    final_format[name] = button_binding

try:
    SUBMODE
except:
    print('\n\nCopy the line below:\n====================\n')
    print(json.dumps(final_format) + '\n')
