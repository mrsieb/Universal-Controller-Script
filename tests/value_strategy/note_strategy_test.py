"""
tests > value_strategy > note_strategy_test

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.types import EventData
from control_surfaces.value_strategies import NoteStrategy


def test_value_note_on():
    s = NoteStrategy()
    assert s.getValueFromEvent(EventData(0x9F, 0, 0x7F), 0.5) == 1.0
    assert s.getValueFromEvent(EventData(0x9F, 0, 64), 0.5) == 64/127


def test_value_note_off():
    s = NoteStrategy()
    assert s.getValueFromEvent(EventData(0x9F, 0, 0), 0.5) == 0.0
    assert s.getValueFromEvent(EventData(0x8F, 0, 0x7F), 0.5) == 0.0


def test_channel():
    s = NoteStrategy()
    assert s.getChannelFromEvent(EventData(0x9F, 0, 0)) == 0xF
    assert s.getChannelFromEvent(EventData(0x95, 0, 0)) == 0x5
