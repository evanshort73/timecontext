# Global voice commands

# start selection context
sky = TimeContext.Start("select", 40, "noop()");

# exit selection context (wrapped in If to avoid typing True or False)
ground = If(TimeContext.Restart("select", 0), "", "");

# show volume control and start volume context
volume =
  Keys.SendInput({VolumeUp}{VolumeDown})
  TimeContext.Start("volume", 3, "noop()");

lap = # left
  If(TimeContext.Restart("select"), {shift+left}, {left});
tar = # right
  If(TimeContext.Restart("select"), {shift+right}, {right});
chip = # up
  If(TimeContext.Restart("volume"),
     Keys.SendInput({VolumeUp_5}),
     If(TimeContext.Restart("select"),
        {shift+up},
        {up}));
bear = # down
  If(TimeContext.Restart("volume"),
     Keys.SendInput({VolumeDown_5}),
     If(TimeContext.Restart("select"),
        {shift+down},
        {down}));

# copying exits selection context
stoosh = {ctrl+c} If(TimeContext.Restart("select", 0), "", "");

# make sure time context is working
time context ping = TimeContext.Ping();
