# https://lego.github.io/MINDSTORMS-Robot-Inventor-hub-API/index.html

import gc, os, time, hub

hub.display.show(hub.Image.DIAMOND)

def Show(img):
    hub.display.show(img)

def Show3x3(s):
    Show(
        hub.Image('00000:0'+s[0:3]+'0:0'+s[3:6]+'0:0'+s[6:9]+'0:00000')
    )

def ScanDisp(p):
    Show3x3(('900000000', '009000000', '000000009', '000000900',
             '090000000', '000009000', '000000090', '000900000',
             '000090000')[p])

Show3x3('968776897')
time.sleep_ms(1000)
Show3x3('968576895')
time.sleep_ms(1000)
Show3x3('999999999')

print("hub.port.A {}".format(hub.port.A.info()))

raise SystemExit





