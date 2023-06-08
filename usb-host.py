import hub
import time

# Connect to virtual com port over bluetooth
vcp = hub.BT_VCP(0)
# Show hint on the hub, console and host
hub.display.show( hub.Image("90090:90090:99099:99090:99099") )
print("Welcome to host-hub (BT)")  # Host needs string
vcp.write( b"Send a char\r\n" ) # Host needs bytes
# Last time the wait-for-key hint was shown
prev = time.time()
while True:
    # Listen to port
    now = time.time()
    raw = vcp.readline()
    if raw == None : # There is no message from host
        if now-prev >= 10 : # hint every 10 sec
            # Show hint on the hub, console and host
            hub.display.show("?")
            print("nothing ...")
            vcp.write(b"waiting ...\r\n")
            # Clear hub
            time.sleep(0.2)
            hub.display.show(" ")
            prev = now
    else : # There is a message from the host
        msg= raw.decode("UTF-8") # decode bytes to string
        hub.display.show(msg)
        print("received '"+msg+"'")
        vcp.write( b"ack '"+raw+"'\r\n" )
        prev = now
