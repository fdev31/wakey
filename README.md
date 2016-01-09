Wakey
-----

Try the [demo](http://planetedessonges.org:8010/wakey/)

![screenshot](https://github.com/fdev31/wakey/raw/master/site/screenshot.jpg)

What is it ?
============

It's a simple GUI to help you configure wacom devices under Linux

Currently, only *Bamboo Fun small* is supported, but supporting new devices is very easy, contact me if you are interested.

Adding new tablets
==================

- Run `xsetwacom --list`

    Wacom Intuos PT S Pen stylus        id: 8   type: STYLUS    
    Wacom Intuos PT S Finger touch      id: 9   type: TOUCH     
    Wacom Intuos PT S Pad pad           id: 10  type: PAD       
    Wacom Intuos PT S Pen eraser        id: 13  type: ERASER    

- Now notice the device names, you can split it into two parts: one prefix and one specific.

- Take the **prefix** part of it (here *Wacom Intuos PT S*) and create a new subfolder using this prefix in `models`, then copy a tempate from another model.

    mkdir "models/Wacom Intuos PT M"
    cp  "models/Wacom Intuos PT S" "models/Wacom Intuos PT M"

- Edit the SVG template in inkscape
- Change drawing accordingly

- For each device returned by `xsetwacom --list`, note the **type** (ex: ERASER, STYLUS, ...)
    - run `xsetwacom -s --get 8 all 2>/dev/null |grep '"Button"'|cut -d ' ' -f 5` to get the buttons list for a given device id (here id: 8, for the STYLUS)
    - Add text where you want the user to be able to edit a button
        - edit XML (Ctrl + Shift + X)
        - add a `wykey` property, the value should be *DEVICE TYPE* : *BUTTON ID*, ex: `STYLUS:8`
    - In case you are not sure about the button to button id match, use something like:

        xsetwacom --set 8 Button 3 "key x"

      Then when you press the button "3" of the device "8" (STYLUS) it should be the same as pressing "x" on a keyboard

- Once it works, zip the folder and send it to me, or do a pull request with the additional content
