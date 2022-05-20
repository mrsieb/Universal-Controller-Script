"""
common > eventpattern

Contains code for pattern matching with MIDI events, including IEventPattern,
a simple way to match events, and IEventPattern, and interface from which
custom pattern matchers can be derived.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'ByteMatch',
    'fromNibbles',
    'IEventPattern',
    'UnionPattern',
    'BasicPattern',
    'ForwardedPattern',
    'ForwardedUnionPattern',
    'NullPattern',
    'NotePattern',
    'fulfil',
]

from .byte_match import ByteMatch, fromNibbles
from .event_pattern import IEventPattern
from .union_pattern import UnionPattern
from .basic_pattern import BasicPattern
from .forwarded_pattern import ForwardedPattern, ForwardedUnionPattern
from .null_pattern import NullPattern
from .note_pattern import NotePattern
from .fulfil import fulfil
