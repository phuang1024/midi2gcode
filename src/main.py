#
#  MIDI2GCODE
#  Play a song with a 3D printer.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import argparse
import mido

HALF_STEP = 2 ** (1/12)


def parse_midi(midi):
    """
    Returns list of tuples of (note, duration).
    if note is None, rest.
    """
    msgs = []

    t = 0
    n = None
    for msg in midi:
        t += msg.time
        if msg.type in ("note_on", "note_off"):
            if t != 0:
                msgs.append((n, t))
            n = msg.note if msg.type == "note_on" and msg.velocity > 0 else None
            t = 0

    return msgs


def main():
    parser = argparse.ArgumentParser(description="Play a song with a 3D printer.")
    parser.add_argument("-i", "--input", help="Input MIDI file", required=True)
    parser.add_argument("-o", "--output", help="Output GCODE file", required=True)
    parser.add_argument("-p", "--pitch", help="Pitch of playback", type=float, default=1.0)
    parser.add_argument("-l", "--length", help="Length of axis", required=True)
    parser.add_argument("-a", "--axis", help="Axis e.g. \"Y\"", required=True, default="Y")
    args = parser.parse_args()

    midi = mido.MidiFile(args.input)
    notes = parse_midi(midi)

    with open(args.output, "w") as fp:
        fp.write("; Generated by MIDI2GCODE\n")
        fp.write("G28 ; Home\n")
        fp.write("G91 ; Relative\n")

        i = 0
        for n, t in notes:
            if n is None:
                # Drive extruder for rest
                rate = int(600 / t)
                fp.write(f"G1 F{rate} E-10\n")

            else:
                rate = int(HALF_STEP ** (n-60) * args.pitch * 100)
                dist = (rate/60) * t * (1 if i == 0 else -1)
                fp.write(f"G0 F{rate} {args.axis}{dist}\n")

                i = 1 if i == 0 else 0


main()
