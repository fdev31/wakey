#!/usr/bin/env python

SUBMODE = True

def dprint(*a, **k):
    return
    print(*a, **k)

import os
import itertools
BASEDIR = os.path.abspath(os.path.dirname(__file__)).rsplit('/', 1)[0]

span_template = '''
    <text
       xml:space="preserve"
       style="font-style:normal;font-weight:normal;font-size:21.37210274px;line-height:125%%;font-family:Lato;letter-spacing:0px;word-spacing:0px;fill:#0055d4;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
       x="%(x)s"
       y="%(y)s"
       id="atext_%(id)s"
       sodipodi:linespacing="125%%"
       wakey="%(wakey)s"><tspan
         sodipodi:role="line"
         id="atspan_%(id)s"
         x="%(x)s"
         y="%(y)s"
         style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:21.37210274px;font-family:Lato;-inkscape-font-specification:Lato">%(text)s</tspan></text>
'''

exec(open(BASEDIR + '/site/wakey_inspector.py').read(), globals())

def set_key(dev_id, but_id, value=None):
    dprint('xsetwacom', '--set', dev_id, 'Button', but_id, value or 'key +shift %s -shift'%but_id)
    subprocess.Popen(['xsetwacom', '--set', dev_id, 'Button', but_id, value or 'key +shift %s -shift'%but_id], stderr=subprocess.PIPE)

for tab_name, tab_devices in final_format.items():
    TEMPLATE = os.path.join(BASEDIR, 'models', tab_name, 'template.svg')
    try:
        os.mkdir(os.path.join(BASEDIR, 'models', tab_name))
    except:
        pass
    else: # gen svg
        svg_code = []
        for j, buttons in enumerate((tab_devices.values())):
            for n, i in enumerate(sorted(buttons.items())):
                d = dict(
                        wakey = i[0],
                        id = "%s_%s"%(j,n),
                        x = 50 + j*120,
                        y = 460 + n*30,
                        text = i[0],
                    )
                svg_code.append(span_template % d)

        open(TEMPLATE, 'w').write(
                open(os.path.join(BASEDIR, 'models', 'template.svg')).read().replace('{{{BUTTONS}}}', '\n'.join(svg_code))
                )

        subprocess.Popen(['inkscape', TEMPLATE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("SVG saved, now to help you know the button number of each device,\n pressing buttons will display the number, we will proceed device by device...")

    print('\nEdit template.svg to adapt text positions or drawings to match the tablet')
    print('For each device, press device buttons to know the mapping or ENTER to skip next (infinite loop, enter "q" to leave)\n')

    print('')
    for tab_name, tab_devices in final_format.items():
        # set straingforward values
        for device_name, buttons in itertools.cycle(reversed(sorted(tab_devices.items()))):
            device_name = "%s %s"%(tab_name, device_name)
            button_numbers = []
            for but_id in buttons.keys():
                but_nr = but_id.split(':')[1]
                button_numbers.append(but_nr)
                set_key(device_name, but_nr)
            if buttons:
                a = input(" - %s declares %d buttons: "%(device_name, len(button_numbers)))
                # revert values
                for but_id, binding in buttons.items():
                    but_nr = but_id.split(':')[1]
                    set_key(device_name, but_nr, binding)
                if a.strip().lower() == 'q':
                    break


