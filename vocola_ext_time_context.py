import time

contexts = {}

def get_expiration(duration):
  if duration > 0:
    return time.clock() + duration
  return float("-inf")

def append_expiration(duration):
  return duration, get_expiration(duration)

# Vocola procedure: TimeContext.Start
def time_context_start(name, duration):
    contexts[name] = append_expiration(float(duration))

# Vocola function: TimeContext.Restart,1-2
def time_context_restart(name, duration=None):
  old_duration, old_expiration = contexts.get(name, append_expiration(0))
  if time.clock() < old_expiration:
    contexts[name] = append_expiration(
      old_duration if duration is None else float(duration))
    return True
  return False

# Vocola function: TimeContext.Hold
def time_context_hold(name, duration):
  old_duration, old_expiration = contexts.get(name, append_expiration(0))
  if time.clock() < old_expiration:
    duration = float(duration)
    contexts[name] = (duration, max(old_expiration, get_expiration(duration)))
    return True
  return False
