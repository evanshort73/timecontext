Temporarily change the meaning of Vocola commands. See `volume_and_selection_example.vcl` for ideas on how to use it.

To install, copy `vocola_ext_time_context.py` into `/NatLink/NatLink/Vocola/extensions`

`TimeContext.Start("some_name", 23)` sets the `"some_name"` context for 23 seconds. Floating point durations are also allowed.

`TimeContext.Start("some_name", 0)` unsets the `"some_name"` context immediately.

`TimeContext.Restart("some_name", 15)` extends the `"some_name"` context for 15 seconds and returns `True`, but only if the context is currently set. If the `"some_name"` context is not currently set, `TimeContext.Restart` does nothing and returns `False`.

`TimeContext.Restart("some_name")` extends the `"some_name"` context, keeping the original duration. Does nothing and returns `False` if the context is not set.

`TimeContext.Hold` is the same as `TimeContext.Restart` except that it never decreases the remaining time. Also, the second argument is not optional because `Hold` with the original duration would be the same as `Restart` with the original duration.

To see my current voice command setup using this extension, go to https://github.com/evanshort73/mypersonalvcl
