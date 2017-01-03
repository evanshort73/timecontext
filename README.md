Temporarily change the meaning of Vocola commands. See `volume_and_selection_example.vcl` for ideas on how to use it.

To install, copy `vocola_ext_time_context.py` and `time_context_server.py` into `/NatLink/NatLink/Vocola/extensions`

Note: If your `pythonw.exe` is not in `/Python27` or your Vocola extensions are not in `/NatLink/NatLink/Vocola/extensions`,
you will have to edit the source code of `vocola_ext_time_context.py` to reflect that.

`TimeContext.Start("some_name", 23, "noop()")` sets the `"some_name"` context for 23 seconds. Floating point durations are also allowed.

`TimeContext.Start("some_name", 23, "Keys.SendInput({enter})")` sets the `"some_name"` context for 23 seconds and presses enter when it times out.

`Keys.SendInput` and `noop` are currently the only supported timeout hooks.

`TimeContext.Restart("some_name", 15, "Keys.SendInput({esc})")` extends the `"some_name"` context for 15 seconds and returns `True`, but only if the context is currently set. Any existing timeout hook will no longer run and escape will be pressed instead after 15 seconds. If the `"some_name"` context is not currently set, `TimeContext.Restart` does nothing and returns False.

`TimeContext.Restart("some_name")` extends the `"some_name"` context, keeping the original duration and timeout hook. Does nothing and returns `False` if the context is not set.

`TimeContext.Restart("some_name", 0, "noop()")` unsets the `"some_name"` context immediately and prevents any existing timeout hook from running. If it returns `True`, you can be sure that the existing timeout hook did not run.

`TimeContext.Hold` is the same as `TimeContext.Restart` except that it never decreases the remaining time. Also, the second argument is not optional because `Hold` with the original duration would be the same as `Restart` with the original duration.

Due to unfortunate circumstances, time context commands are run on a "server", which is actually a Python subprocess listening for commands on stdin. `TimeContext.Ping()` prints `"time context server running"` in the NatLink window if it could successfully communicate with the server.
