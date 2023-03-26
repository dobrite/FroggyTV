# FroggyTV

hehe froggy

# TODO:

- Rename bpm to clock, ticks, pulses or similar
- Bpm.RESOLUTION = 640 (32x10x2)
  - 32 MAX_MULT
  - 10 PERCENT_INCREMENTS
  - 2 pulses per bpm (one on one off)
  - FWIW Pams is 192 mult @ 320 BPM
- Implement PWM in terms of Sequence
  - Only one Delay gets ticked at a time, rather than all
- Flesh out Gate screens
- Implement Sync and Reset
  - Is stop/start a reset, or resume?
    - reset!
- Implement probability
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
- Dynamically adjust PWM percentage as mult increases?
- C/C++/Rust timing library?
- "pew" mode (10ms trigger)

### Viewing Logs with Mu

Assumes bash or bash-like shell (not Windows).
Assumes `screen` is installed and avaiable in `$PATH`.
Replace `usbmodem143401` with output of `ls`.

```bash
ls /dev/tty.*
screen /dev/tty.usbmodem14340 1115200
```

### Running Tests and Linting with Nox

First, ensure `nox` is installed and in your `$PATH`.

```
python3 -m pip install nox
```

Then it is easy as running:

```bash
nox
```

### Rerunning Nox on File Changes

```
rerun -c -p "**/*.py" nox
```

### Rerunning Tests (pytest) on File Changes

```
rerun -c -p '**/*.py' 'pytest -rx'
```

### Copy Files to Pi Pico on Save

Requires the `rerun` Ruby gem to be installed and avaiable in `$PATH`.
Assumes pi pico is mounted at the location specified.
Assumes bash or bash-like shell. i.e. probably needs adjusted on windows.

```bash
rerun -c -p "src/**/*.py" "cp -R src/froggytv/*.py /Volumes/CIRCUITPY/"
```

### Overclocking?

This may work, but it could be dumb to implement as below
https://github.com/adafruit/circuitpython/issues/4339#issuecomment-857351719
