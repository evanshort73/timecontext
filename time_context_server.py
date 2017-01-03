import time
import threading
from vocola_ext_keys import send_input
import sys
import json

def noop():
    pass

class RestartableTimer(threading.Thread):
    def __init__(self, interval=0, function=noop, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.interval = interval
        self.release = function, args, kwargs

        self.smack_cam = threading.Condition()
        self.smack = threading.Event()
        self.exited = False
    
    def start(self):
        self.expiration = time.clock() + self.interval
        threading.Thread.start(self)

    def restart(self, interval=None, function=None, args=[], kwargs={}):
        # if restart returns False, the thread has already run the old release
        #     funciton and exited
        # if interval is zero and restart returns True, the thread has already
        #     run the new release function and exited
        # if interval is positive and restart returns True, the thread is
        #     waiting to run the new release function
        
        # implementation idea:
        # let current time be called A
        # send interrupt
        # wait until thread is waiting for interrupt or thread has exited
        # if thread started waiting for interrupt after time A, return true,
        #     otherwise false
        
        with self.smack_cam:
            # invariant: if we're holding self.smack_cam and self.exited is False
            #     then self.smack_cam.notify will eventually be called
            # note: self.exited can't change until we call
            #     self.smack_cam.wait
            # note: self.smack_cam.notify can't be called until we call
            #     self.smack_cam.wait
            if not self.exited:
                if interval is not None:
                    self.interval = interval
                    self.expiration = time.clock() + interval

                if function is not None:
                    self.release = function, args, kwargs

                self.smack.set()
                self.smack_cam.wait()
                # invariant: if self.exited is false when we re-acquire
                #     self.smack_cam, the new interval and release function
                #     must have taken effect
            
            if not self.interval and not self.exited:
                self.smack_cam.wait()
                assert self.exited
                return True

            return not self.exited

            
    def cancel(self):
        # returns true if the old release function was prevented from running
        return self.restart(0, noop)

    def run(self):
        release = self.release
        interval = self.interval
        while self.smack.wait(interval): # zzz
            self.smack.clear()
            with self.smack_cam:
                release = self.release
                interval = self.interval
                self.smack_cam.notify_all()

        function, args, kwargs = release
        function(*args, **kwargs)
                
        with self.smack_cam:
            self.exited = True
            self.smack_cam.notify_all()

class ExpiredTimer:
    def __init__(self):
        self.expiration = float("-inf")
    def restart(self, interval=None, function=None, args=[], kwargs={}):
        return False
    def cancel(self):
        return False

EXPIRED_TIMER = ExpiredTimer()

context_timers = {}

def time_context_start(name, duration, release):
    timer = RestartableTimer(float(duration), *parse_invocation(release))
    timer.daemon = True
    
    old_timer = context_timers.get(name, EXPIRED_TIMER)
    old_timer.restart(0) # call its release function
    
    timer.start()
    context_timers[name] = timer

def time_context_restart(name, grace_period=None, release=None):
    timer = context_timers.get(name, EXPIRED_TIMER)
    if grace_period is not None:
        grace_period = float(grace_period)
    return timer.restart(grace_period, *parse_invocation(release))

def time_context_hold(name, duration, release=None):
    timer = context_timers.get(name, EXPIRED_TIMER)
    new_duration = max(float(duration), timer.expiration - time.clock())
    return timer.restart(new_duration, *parse_invocation(release))

def parse_invocation(invocation):
    if invocation is None:
        return ()
    elif type(invocation) is tuple: # for debugging
        return invocation

    function, _, args = invocation.rpartition(")")[0].partition("(")
    if function == "Keys.SendInput":
        return send_input, [args]
    elif function == "noop":
        return noop,

    raise ValueError(invocation)
    
def parse_command_function(function):
    if function == "TimeContext.Start":
        return time_context_start
    elif function == "TimeContext.Restart":
        return time_context_restart
    elif function == "TimeContext.Hold":
        return time_context_hold
        
    raise ValueError(function)

def main_loop():
    global main_loop_expiration
    while True:
        command = raw_input()
        main_loop_expiration = time.clock() + MAIN_LOOP_TIMEOUT
        if command == "ping":
            print "pong"
            sys.stdout.flush()
        else:
            try:
                function, args = json.loads(command)
                function = parse_command_function(function)
                result = function(*args)
            except ValueError as error:
                result = {"__error__": True, "message": str(error)}

            print json.dumps(result)
            sys.stdout.flush()

# exit the server if no commands are recieved for 70 seconds.
# this is useful during debugging so that old iterations of the server program
# aren't orphaned. if you want a context to be held for more than a minute,
# you should increase this number
MAIN_LOOP_TIMEOUT = 70

main_loop_expiration = time.clock() + MAIN_LOOP_TIMEOUT
main_loop_thread = threading.Thread(target=main_loop)
main_loop_thread.daemon = True
main_loop_thread.start()

while time.clock() < main_loop_expiration:
    time.sleep(10)

# Example input for manual testing:
# ["TimeContext.Set", ["volume", "1", "Keys.SendInput({VolumeUp})"]]
