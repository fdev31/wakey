import subprocess
import json
import re

models = subprocess.Popen(['xsetwacom', '--list'], stdout=subprocess.PIPE).communicate()[0].split(b'\n')
devices = {}
pr_re = re.compile("\\+([a-zA-Z]+) -\\1")
final_format = {}

def get_device_properties(device_name):
    raw = subprocess.Popen(['xsetwacom', '-s', '--get', device_name,  'all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    buttons = {}
    for line in raw[0].split(b'\n'):
        if b'"Button"' in line:
            line = line[line.index(b"Butt")+8:].decode('utf-8')
            but = line.split('"')[1::2]
            buttons[but[0]] = but[1].strip()
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
        dev = {"%s:%s"%(device['type'], but_name) : pr_re.sub("\\1", binding) for but_name, binding in buttons.items()}
        button_binding[device['name']] = dev
    final_format[name] = button_binding

print('\n\nCopy the line below:\n====================\n')
print(json.dumps(final_format) + '\n')