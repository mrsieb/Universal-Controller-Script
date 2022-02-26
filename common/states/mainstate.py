"""
common > mainstate

Represents the script in its main state, where the device is recognised and
behaving as expected.
"""

import time
import plugins
from typing import TYPE_CHECKING

import common
from common import log, verbosity
from common.types import EventData
from common.util.apifixes import getFocusedPluginIndex, WindowIndex, PluginIndex
from common.util.events import eventToString
from .scriptstate import IScriptState

if TYPE_CHECKING:
    from devices import Device

class MainState(IScriptState):
    """
    Represents the main state of the script, where the device is recognised and
    behaving as expected.
    """
    
    def __init__(self, device: 'Device') -> None:
        self._device = device
    
    def initialise(self) -> None:
        pass
    
    def tick(self) -> None:
        self._device.tick()

        # Tick special plugins
        for p in common.ExtensionManager.getSpecialPlugins(self._device):
            p.tick()
            p.apply()

        # Tick active standard plugin or window
        plug_idx = common.getContext().active.getActive()
        if plug_idx is not None:
            if isinstance(plug_idx, tuple):
                try:
                    plug_id = plugins.getPluginName(*plug_idx)
                except TypeError:
                    # Plugin not valid
                    plug_id = ""
                plug = common.ExtensionManager.getPluginById(plug_id, self._device)
                if plug is not None:
                    plug.tick(plug_idx)
                    plug.apply()
            else:
                window = common.ExtensionManager.getWindowById(plug_idx, self._device)
                if window is not None:
                    window.tick()
                    window.apply()

    def processEvent(self, event: EventData) -> None:
        t_start = time.time()
        mapping = self._device.matchEvent(event)
        match_time = time.time() - t_start
        if mapping is None:
            event.handled = True
            log(
                "device.event.in",
                f"Failed to recognise event: {eventToString(event)}",
                verbosity.CRITICAL,
                f"This usually means that the device hasn't been configured "
                f"correctly. Please contact the device's maintainer.\n"
                f"Search time: {match_time:.3} seconds"
            )
            # raise ValueError(f"Couldn't identify event: {eventToString(event)}")
            return
            
        else:
            log(
                "device.event.in",
                f"Recognised event in {match_time:.3} seconds: {mapping.getControl()}",
                verbosity.EVENT,
                detailed_msg=eventToString(event)
            )
        # Get active standard plugin
        plug_idx = common.getContext().active.getActive()
        if plug_idx is not None:
            if isinstance(plug_idx, tuple):
                try:
                    plug_id = plugins.getPluginName(*plug_idx)
                except TypeError:
                    # Plugin not valid
                    plug_id = ""
                plug = common.ExtensionManager.getPluginById(plug_id, self._device)
                if plug is not None:
                    if plug.processEvent(mapping, plug_idx):
                        event.handled = True
                        return
            else:
                window = common.ExtensionManager.getWindowById(plug_idx, self._device)
                if window is not None:
                    if window.processEvent(mapping, plug_idx):
                        event.handled = True
                        return

        # Get special plugins
        for p in common.ExtensionManager.getSpecialPlugins(self._device):
            if p.processEvent(mapping, plug_idx):
                event.handled = True
                return
