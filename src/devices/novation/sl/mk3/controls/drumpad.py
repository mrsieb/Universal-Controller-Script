"""
devices > novation > sl > mk3 > controls > drumpad

Definition for the SL Mk3 Drumpads

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from controlsurfaces.eventpatterns import ForwardedPattern, NotePattern
from controlsurfaces.valuestrategies import NoteStrategy, ForwardedStrategy
from controlsurfaces import DrumPad
from . import SlColorSurface
from devices.matchers import (
    BasicControlMatcher,
)


DRUM_NOTES = [
    [i + 0x60 for i in range(8)],
    [i + 0x70 for i in range(8)]
]
DRUM_LIGHTS = [
    [i + 0x26 for i in range(8)],
    [i + 0x2E for i in range(8)]
]


class SlDrumPad(SlColorSurface, DrumPad):
    """
    Custom drum pad implementation used by SL Mk3 controllers
    to provide RGB functionality
    """
    def __init__(
        self,
        coordinate: tuple[int, int]
    ) -> None:
        r, c = coordinate
        SlColorSurface.__init__(
            self,
            DRUM_LIGHTS[r][c],
        )
        DrumPad.__init__(
            self,
            # TODO: Make sure it's actually channel F?
            ForwardedPattern(2, NotePattern(DRUM_NOTES[r][c], 0xF)),
            ForwardedStrategy(NoteStrategy()),
            coordinate
        )


class SlDrumPadMatcher(BasicControlMatcher):
    """Matcher for SL drum pads"""
    def __init__(self) -> None:
        super().__init__()
        for r in range(2):
            for c in range(8):
                self.addControl(SlDrumPad((r, c)), 10)
