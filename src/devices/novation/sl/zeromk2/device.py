"""
devices > novation > sl > zeromk2 > device

Device definitions for ZeRO SL Mk2 controllers

Authors:
* mrsieb [me@mrsieb.net]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""


import device

from control_surfaces.event_patterns import BasicPattern
from common.extension_manager import ExtensionManager

from fl_classes import FlMidiMsg
from control_surfaces import (
    StandardModWheel,
    StandardPitchWheel,
    SustainPedal,
)
from devices import Device
from control_surfaces.matchers import BasicControlMatcher, NoteMatcher
from .controls.transport import (
    SlPlayButton,
    SlStopButton,
    SlLoopButton,
    SlRecordButton,
    SlDirectionNext,
    SlDirectionPrevious,
    SlRewindButton,
    SlFastForwardButton,
)
from .controls import (
    SlFaderSet,
    SlDrumPadMatcher,
    SlNotifMsg,
)

DEVICE_ID = "Novation.SL.ZeROMk2"

class Zeromk2(Device):
    """
    Novation ZeRO SL Mk2
    """

    def __init__(self, matcher: BasicControlMatcher) -> None:

        # Notes
        matcher.addControls(getNotesAllChannels())

        # Create knob controls, using a loop
        for i in range(8):
            matcher.addControl( # Register the control
                Knob(
                    BasicPattern(0xB0, i, ...), # Pattern for event
                    Data2Strategy(),  # Get the value from data 2
                    (0, i) # Coordinate should be the index in the loop
                )
            )

        # Add a stop button
        matcher.addControl(StopButton(
            BasicPattern(0xB0, 0x72, ...),
            ButtonData2Strategy()
        ))
        # Add a standard pitch wheel
        #matcher.addControl(StandardPitchWheel())

        # Finally finish the initialization
        super().__init__(matcher)

    @staticmethod
    def getDrumPadSize() -> tuple[int, int]:
        return 1, 8
    
    @classmethod
    def create(cls, event: FlMidiMsg = None, id: str = None) -> 'Device':
        return cls()

    @staticmethod
    def getId() -> str:
        return DEVICE_ID

    @staticmethod
    def getUniversalEnquiryResponsePattern():
        return BasicPattern(
            [
                0xF0, # Sysex start
                0x7E, # Device response
                ..., # OS Device ID
                0x06, # Separator
                0x02, # Separator
                0x00, # Manufacturer
                0x77, # Manufacturer
                0x77, # Manufacturer
                0x01, # Family code
                0x4D, # Family code
                # Add any other required details
            ]
        )

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        # Since we're providing a universal enquiry response pattern, we don't
        # need to bother implementing this as all devices should be matched
        # correctly from the pattern.
        # In non-standard devices, this function can be used as a backup
        # system, by using an expression such as the following:
        return name == "My Controller"

ExtensionManager.devices.register(Zeromk2)
