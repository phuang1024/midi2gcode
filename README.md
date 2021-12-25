# MIDI2GCODE

Play a song with a FDM 3D printer. SLA printers don't have motors, so they cannot play music.

**Warning**: Be ready to turn off the 3D printer in case the motor reaches
the axis limit.

## Usage:

`python main.py ...`

Args:

* `-i`: Input MIDI file.
* `-o`: Output G-code file.
* `-p`: Pitch multiplier.
* `-l`: Length of axis (currently ignored).
* `-a`: Axis to use e.g. `"Y"`. Normally, the Y axis is loudest.
* `-r`: Axis to use for rests. The `"X"` and `"E"`xtruder axes are quietest, but some printers
    don't move the extruder unless it is heated.
* `--home`: Move to home position before playing.

Copy the gcode to the printer and print it.
The gcode flavor is Marlin.

Example command:

`python main.py -i a.mid -o a.gcode -a Y -r X --home`

## How it works:

The 3D printer moves motors, and usually makes noises. These noises are arbitrary in most prints,
but if you move them at certain speeds, they may form a song.

The script computes the speeds based on a MIDI file (the song).

## Future features

* Multiple simultaneous voices and timbres using all axes.
* Compute direction of move to stay roughly in the middle.
