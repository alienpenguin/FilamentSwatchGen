#!/usr/bin/env python3

import subprocess
import csv
import os
import platform
import sys

if platform.system() == 'Windows':
    OPENSCAD = 'C:\Program Files\OpenSCAD\openscad.exe'
elif platform.system() == 'Linux':
    OPENSCAD = 'openscad'
else:
    OPENSCAD = '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'

MYDIR = os.path.dirname(os.path.realpath(__file__))


def gen_samples(file=f"{MYDIR}/samples.csv"):
    os.makedirs(f"{MYDIR}/stl", exist_ok=True)
    with open(file, '+r') as f:
        data = csv.reader(f)

        for l in data:
            if len(l) > 0:
                print("Processing:", l)
                filename = "stl/" + "_".join(l) + ".stl"
                args = [OPENSCAD]  # process name
                outfile = ['-o', filename]
                brand = ['-D', f'BRAND="{l[0]}"']
                type = ['-D', f'TYPE="{l[1]}"']
                color = ['-D', f'COLOR="{l[2]}"']
                noztemp = ['-D', f'TEMP_HOTEND="{l[3]}"']
                bedtemp = ['-D', f'TEMP_BED="{l[4]}"']
                # extra parameter
                font_size = None
                if len(l) > 5:
                    font_size = ['-D', f'TYPE_SIZE={l[5]}']
                infile = f'{MYDIR}/FilamentSamples.scad'
                args.extend(outfile)
                args.extend(brand)
                args.extend(type)
                args.extend(color)
                args.extend(noztemp)
                args.extend(bedtemp)
                if font_size:
                    print("adding optional parameter font_size: " + l[5])
                    args.extend(font_size)
                args.append(infile)  # this MUST be last param
                print("Calling OpenSCAD with params: ", args)
                subprocess.run(args, check=True)


def find_mac_openscad():
    global OPENSCAD
    # on mac verify we have openscad
    if platform.system() == 'Darwin':
        found = False
        if not os.path.exists(OPENSCAD):
            print("OpenSCAD is not in default /Applications")
            if not os.path.exists(os.path.expanduser('~') + OPENSCAD):
                print("OpenSCAD is not in user's ~/Applications")
                print("Trying to see if there is an openscad command in your path...")
                args = ['openscad', '-v']
                try:
                    proc = subprocess.run(args, capture_output=True, check=True)
                    if proc.returncode == 0:
                        found = True
                        print("openscad version found in path: ", proc.stderr.decode())
                        OPENSCAD='openscad'
                except Exception:
                    print("Could not find any openscad command in your path... aborting")
            else:
                print("OpenSCAD found in user's application folder")
                OPENSCAD = os.path.expanduser('~') + OPENSCAD
                found = True
        else:
            print("OpenSCAD found in system application folder")
            found = True
        if not found:
            print("Could not find OpenSCAD binary, please makesure that you have the OpenSCAD app in /applications or "
                  "~/Applications or an 'openscad' command in your path")
            sys.exit(1)


if __name__ == "__main__":
    find_mac_openscad()

    if len(sys.argv) < 2:
        print("You did not pass any .csv file, using samples.csv")
        gen_samples()
    else:
        swatch_file = sys.argv[1]
        print("Using swatch file: " + swatch_file)
        gen_samples(swatch_file)
