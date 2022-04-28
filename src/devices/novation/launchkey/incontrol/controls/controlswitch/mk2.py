
from .controlswitch import LkControlSwitchButton
from ...colors.standard import COLORS


class LkMk2ControlSwitchButton(LkControlSwitchButton):

    def __init__(
        self,
    ) -> None:
        super().__init__(
            0x9F,
            0xF,
            0x68,
            COLORS,
        )
