"""
    DECANUM - Robot Inventor MicroPython Software -
    Project     : Guidage vehicule 2 pairMotor avec joystick ( motor)  
                : et mémorisation du circuit.  
    Application : carguidage.py
    Auth        : remybeaudenon@yahoo.com
    Date        : 06/2023
"""

version = "v1p1"

import gc, os, umachine, ubinascii
gc.collect()

from mindstorms import MSHub
hub = MSHub()
lm = hub.light_matrix
lm.set_orientation('right')
lm.show_image('SQUARE')
sp = hub.speaker
sp.beep(72)

# Remove any files from older versions
for fn in os.listdir("/"):
    if len(fn) > 10:
        ver = None
        if fn[-3:] == ".py" and (
            fn[:-7] == "mcricolors_" or
            fn[:-7] == "mcrimaps_" or
            fn[:-7] == "mcrisolver_" or
            fn[:-7] == "mindcuberri_"
            ):
            ver = fn[-7:-3]
        elif fn[-4:] == ".bin" and (
            fn[:-8] == "mcrimtab1_" or
            fn[:-8] == "mcrimtab4_"
            ):
            ver = fn[-8:-4]
        if ver != None and ver < version:
            print("DELETING: "+fn)
            os.unlink(fn)

def file_exists(fn):
    try:
        ok = os.stat(fn) != None
    except:
        ok = False
    return ok

found = 0

def open_bin(fn):
    global sp, ofn, of, on, found
    sp.beep(67)
    ofn = fn
    of= open(ofn, 'wb')
    on= 0
    found += 1

def wbin(data):
    global of, on
    of.write(data)
    on += 1
    if on % 50 == 0:
        lm.show_image('CLOCK'+str(1+(int(on/50)%12)))

def close_of():
    global of, ofn
    of.close()
    of = None
    print("SAVED: "+ofn+" "+str(os.stat(ofn)[6])+"B")
    gc.collect()

print("Installing...")
open_bin("mcrimtab1_"+version+".bin")
wbin(b"\x0c\x33\xf5\x0e\xff\xff\x03\x53\xff\x03\x55\xff\x09\xf9\xff\x03\x54\xff\x11\x35\xf3\x06\x88\xff\x0c\xff\xff\x0a\xf9\xff\x06\x86\xff\x00\xfa\xff\x0b\xf9\xff\x0d\xff\xff\x02\x98\xff\x02\xfa\xff\x03\x5b\xff\x05\x33\xff\x04\x4b\xff\x01\xfa\xff\x00\x98\xff\x08\x6e\xf5\x06\x96\xf3\x08\xee\xf5\x03\x6c\xff\x08\x5e\xff\x09\x96\xf3\x08\x8e\xf5\x08\x9e\x59\x0b\xe8\xf5\x06\x39\xff\x08\x7e\xf5\x09\xe8\xf5\x0a\xe8\xf5\x0b\x96\xf3\x0c\x96\xf3\x0e\xc3\xf6\x03\x3c\xf3\x06\x39\xfb\x05\xb4\xf8\x04\xb2\xf3\x02\xc0\x33\x03\x5c")
wbin(b"\xff\x0f\xc5\xe8\xe6\xf3\xff\xff\x08\xd1\xe1\xe1\xe1\xf6\xff\x03\x99\x80\x0b\xe2\xc2\xff\x05\xd4\xc6\xc8\xc6\x36\xff\x07\xbc\x0e\x2e\x9d\x7e\xff\x11\x81\xb9\xab\xc1\xff\xff\x02\xa2\xd9\x87\x3a\x2d\xff\x0f\x77\xb2\x70\xe7\x46\xf5\x0f\xe5\x02\x8b\x33\x09\xff\x09\x5d\x3e\x5d\x3e\xbc\xff\x05\x3c\x5e\x3c\x0d\x2c\xff\x05\x35\x5e\x8e\x6d\x35\xf4\x00\x2e\xfc\xff\xff\xff\xff\x11\xc0\xac\xbd\x9c\xac\x2b\x0f\xd1\x28\x08\x66\x2d\x2e\x08\x1d\x2c\x2e\x6d\x03\x22\x11\xbb\x25\x90\xc9\xf0\xff\x0f\x60\x36\x5e\x85\xf2\xff\x03")
wbin(b"\xab\xc4\xe6\x4a\x29\xf2\x05\x85\xe2\x60\x36\xfc\xff\x0f\x96\x00\xb2\xe8\xf5\xff\x03\x99\x0c\xbe\x5b\xf2\xff\x05\xb2\xe8\xc3\x96\xf0\xff\x03\xb0\x4a\x8c\xae\x94\xf5")
close_of()

# Install MindCuber-RI v1p1 files
prj = "/projects/"
with open(prj+".slots","r") as f:
    slots = eval(f.read())
for s in slots:
    base = prj+str(slots[s]['id'])
    # Filename used by latest hub OS
    fn = base+"/__init__.py"
    if not file_exists(fn):
        # Try filename used by older versions of hub OS
        fn = base+".py"
    if file_exists(fn):
        with open(fn) as f:
            for i in range(3):
                l = f.readline()
                if l == "#MINDCUBERRI_FILES_V1P1#\n":
                    print("SLOT: "+str(s)+" "+fn+" "+str(os.stat(fn)[6])+"B")
                    print("Installing...")
                    of = None
                    b64 = False
                    n = 0
                    for l in f:
                        if l[:5] == "#FILE":
                            lfn = l[5:-1]
                            b64 = lfn[-4:] == ".bin"
                            open_bin(lfn)
                        elif l[:8] == "#ENDFILE":
                            close_of()
                        elif of != None:
                            if b64:
                                if l[0:5] != "#====":
                                    of.write(ubinascii.a2b_base64(l[1:-1]))
                            else:
                                of.write(l)
                            n += 1
                            if n % 50 == 0:
                                lm.show_image('CLOCK'+str(1+(int(n/50)%12)))
                    if of != None:
                        # Missing end of file
                        of.close()
                        print("ERROR: end file marker expected")
                        print("DELETING: "+ofn)
                        ofn.unlink()
os.sync()
if found > 0:
    sp.beep(72)
    msg = "MindCuber-RI v1p1 "+str(found)+" files installed"
    print("FINISHED "+msg)
    lm.write(msg)
    lm.show_image('YES')
else:
    msg = "ERROR: no files found to install"
    print(msg)
    lm.write(msg)
    lm.show_image('NO')

# END
