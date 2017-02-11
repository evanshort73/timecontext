# Global voice commands

# start selection context
grab = TimeContext.Start("select", 40);

# exit selection context
jetsam = TimeContext.Start("select", 0);

# show volume control and start volume context
volley =
  Keys.SendInput({VolumeUp}{VolumeDown})
  TimeContext.Start("volume", 3);

lap = # left
  If(TimeContext.Restart("select"), {shift+left}, {left});
tar = # right
  If(TimeContext.Restart("select"), {shift+right}, {right});
wick = # up
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
bottle = {ctrl+c} TimeContext.Start("select", 0);
