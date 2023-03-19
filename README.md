# FroggyTV

hehe froggy

# TODO:

- Flesh out Gate screens
- Implement Sync and Reset
- Implement probability
- Re-Implement pulse width adjustment
- Stress test max 12 gate screens? - (Is an expander possible?)

# IDEAS:

- Metronome screen
- Loading/splash screen
- Phase/offset?
- Settings menu?
  - Swappable pointer sprite?
- Frames on menu UI?
- Alternate screen modes:
  - Type 1: Pulse width + Probability
  - Type 2: Simple Euclidean Sequencer (Length and Density)
  - Type 3: Binary Sequencer (A la Trigseq on O_C Hemispheres)

### Viewing Logs with Mu

Assumes bash or bash-like shell (not Windows).
Assumes `screen` is installed and avaiable in `$PATH`.
Replace `.usbmodem143401` with output of `ls`.

```bash
ls /dev/tty.*
screen /dev/tty.usbmodem14340 1115200
```

### Copy Files to Pi Pico on Save

Requires the `rerun` Ruby gem to be installed and avaiable in `$PATH`.
Assumes pi pico is mounted at the location specified.
Assumes bash or bash-like shell. i.e. probably needs adjusted on windows.

```bash
rerun -c -p "**/*.py" "cp -R *.py /Volumes/CIRCUITPY/"
```

### Overclocking?
This may work, but it could be dumb to implement as below
https://github.com/adafruit/circuitpython/issues/4339#issuecomment-857351719