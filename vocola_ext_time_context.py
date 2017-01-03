import subprocess
import json
import time

class RemoteException(Exception):
    pass

def object_hook(d):
    if "__error__" in d:
        return RemoteException(d["message"])
    return d

# Vocola procedure: TimeContext.Start,3
def time_context_start(*args):
    write_to_server(json.dumps(["TimeContext.Start", args]))

    response = read_from_server()
    try:
        result = json.loads(response, object_hook=object_hook)
    except ValueError:
        raise ValueError("bad response: " + json.dumps(response))
    if type(result) is RemoteException:
        raise result

    return result

# Vocola function: TimeContext.Restart,1-3
def time_context_restart(*args):
    write_to_server(json.dumps(["TimeContext.Restart", args]))

    response = read_from_server()
    try:
        result = json.loads(response, object_hook=object_hook)
    except ValueError:
        raise ValueError("bad response: " + json.dumps(response))
    if type(result) is RemoteException:
        raise result

    return result

# Vocola function: TimeContext.Hold,2-3
def time_context_hold(*args):
    write_to_server(json.dumps(["TimeContext.Hold", args]))

    response = read_from_server()
    try:
        result = json.loads(response, object_hook=object_hook)
    except ValueError:
        raise ValueError("bad response: " + json.dumps(response))
    if type(result) is RemoteException:
        raise result

    return result

# Vocola procedure: TimeContext.Ping
def time_context_ping():
    write_to_server("ping")
    ping_response = read_from_server()
    if ping_response == "pong":
        print "time context server running"
    else:
        raise ValueError("bad response: " + json.dumps(ping_response))

# I would have liked to spawn the timer threads directly from this program but
# Python's global interpreter lock prevents them from running unless Vocola is
# actively processing a command. The next best thing would have been to start
# another Python process for the timers using the multiprocessing module, but
# on Windows it gets confused trying to find the python executable that's
# being used and ends up starting another instance of Dragon instead. That's
# why I ended up using the subprocess module and sending json commands over
# stdin.
server = None
def write_to_server(message):
    global server
    if server is None or server.poll() is not None:
        server = subprocess.Popen(
            ["/Python27/pythonw.exe",
             "/NatLink/NatLink/Vocola/extensions/time_context_server.py"],
            bufsize=-1, # system's default buffer size
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True) # replace \r\n with \n
    server.stdin.write(message + "\n")
    server.stdin.flush()

def read_from_server():
    return server.stdout.readline().rstrip("\n")

# note: NatLink doesn't print the output of this initial ping until you flush
# its buffer by running another command
time_context_ping() 

# Example command for manual testing:
# time_context_start("volume", "1", "Keys.SendInput({VolumeUp})")
