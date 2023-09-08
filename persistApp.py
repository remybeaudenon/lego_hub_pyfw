# ----Main Program----
TRACE = True # Enable or desable flag
Log.trace('Main:Thread() Welcome to Discovery Hub os:{}version:{} fw:{}'. \
            format(sys.platform ,sys.version,LegoFw.__VERSION__))




# -- Sensors port---

# -- global instance ---
gc.collect()
hub    = MSHub()
Speaker.beep3()
try:
    tab_fname = "/data/test.dat"
    print("len: {}".format(os.stat(tab_fname)[6]))
except:
    None

try :
    persist = Persit()

    Persit.listdir(Persit.cwd() )

    prj = "/projects/"
    with open(prj+".slots","r") as f:
        slots = eval(f.read())
        for s in slots:
            base = prj+str(slots[s]['id'])
            print("--[{}]".format(base))


    #if Persit.chdir('/data') == None :
    #    Persit.mkdir('/data')
except Exception as e :
    print("Exception ==> {}".format(e))
finally :
    os.sync()
    gc.collect()
