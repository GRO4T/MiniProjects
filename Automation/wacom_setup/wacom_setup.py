#!/usr/bin

import sys
import subprocess

class Display:
    def __init__(self, resolution, output):
        self.resolution = resolution
        self.output = output

def run_bash_command(command):
    returned_value = subprocess.check_output(command, shell=True)
    #print('Running: ',command)
    return returned_value

def detect_displays():
    # we want to fill this list with instances of Display class
    display_list = []

    res_bytes = run_bash_command("xrandr | grep \* | cut -d' ' -f4") # detect connected resolutions
    # by now we have something like this b'1280x1024\n1440x900\n'
    # but we want to make a list from it
    res_bytes_list = res_bytes.split(b'\n')
    res_bytes_list.remove(b'') # remove last empty byte
    # now we want to search for video outputs that correspond to that resolutions
    for resolution in res_bytes_list:
        get_output =  b"".join([b"xrandr | grep ", resolution, b"+ | cut -d' ' -f1"])
        video_output = run_bash_command(get_output).strip() # get video output and strip it of trailing newline character
        display_list.append(Display(resolution.decode("utf-8"), video_output.decode("utf-8")))

    """
    #print display list
    for display in display_list:
        print(display.resolution)
        print(display.output)
    """

    return display_list

# gets index of the display user wants the tablet be mapped to
def get_display_id(displays):
    print(len(displays), "displays detected")
    i = 0
    for display in displays:
        i += 1
        print("".join([str(i), "."]), display.resolution, "on", display.output)
    try:
        display_id = int(input("Give number of the display you want tablet be mapped to: "))
        if (display_id < 0 or display_id > len(displays)):
            raise ValueError
    except ValueError:
        while(True):
            try:
                display_id = int(input("Invalid index! Try again!: "))
                if (display_id < 0 or display_id > len(displays)):
                    raise ValueError
            except ValueError:
                continue
            break
    return display_id - 1

def set_tablet_area(wacom_stylus, screen_width, screen_height):
    get_area = ''.join(['xsetwacom --get ', '"', wacom_stylus, '"', ' area'])
    current_area = run_bash_command(get_area).strip().decode("utf-8").split()

    #calculate new width
    current_area[2] = screen_width * int(current_area[3]) // screen_height

    set_area = ''.join(['xsetwacom --set ', '"', wacom_stylus, '"', ' area '])
    for parameter in current_area:
        set_area = ''.join([set_area, str(parameter), ' '])
    run_bash_command(set_area)

def main():
    #print help info
    if (len(sys.argv) > 1 and str(sys.argv[1]) == "--help"):
        print("syntax")
        return

    # 'man xsetwacom' to get info about command
    run_bash_command('xsetwacom --set "Wacom One by Wacom S Pen stylus" Mode Absolute')

    displays = detect_displays()
    display_id = get_display_id(displays)

    wacom_stylus = run_bash_command("xsetwacom list devices | grep stylus | cut -d':' -f 1 | cut -d'i' -f 1").strip().decode("utf-8")

    # map tablet to display
    map_to_output = ''.join(['xsetwacom set ', '"', wacom_stylus, '"', ' MapToOutput '])
    map_to_display = ''.join([map_to_output, displays[display_id].output])
    run_bash_command(map_to_display)

    #set tablet's area that it fits display's aspect ratio (keep the same height change only width
    res_split = displays[display_id].resolution.split('x')
    set_tablet_area(wacom_stylus, int(res_split[0]), int(res_split[1]))

if __name__ == "__main__":
    main()


