#!/usr/bin/env python
"""
Entities within this document is supporting the implementations of project assignment.
YOU MAY NOT CHANGE OR MODIFY ANYTHING IN THIS FILE!!
"""
import os
import sys

STATE_RIM, STATE_DEAD, STATE_ALIVE = '#', '-', 'X'  # base cell states
STATE_ELDER, STATE_PRIME_ELDER = 'E', 'P'           # cell states used for higher grade


def get_print_value(_val: str) -> str:
    """ Format output value for printing. """
    def get_state_color(state):
        """ Used to color console output. """
        switcher = {
            STATE_RIM: '\033[45m',          # Magenta background color
            STATE_DEAD: '\033[31m',         # Red foreground color
            STATE_ALIVE: '\033[36m',        # Cyan foreground color
            STATE_ELDER: '\033[32m',        # Green foreground color
            STATE_PRIME_ELDER: '\033[34m',  # Blue foreground color
            'ENDC': '\033[0m'               # Reset console color
        }
        return switcher.get(state, None)
    return "{}{}{}".format(get_state_color(_val), _val, get_state_color('ENDC'))
    #return get_state_color(val) + val + get_state_color('ENDC')


def progress(_status: str):
    """ Update progress information in console. """
    sys.stdout.write("{}".format(_status))


def clear_console():
    """ Clear the console. POSIX refers to OSX/Linux. """
    os.system('clear' if os.name == 'posix' else 'cls')


def get_pattern(_pattern: str, _world_size: tuple) -> list:
    """ Add predefined pattern to initial seed. """

    def create_gliders() -> list:
        """ Create gliders (simple spaceships) at each corner of the world which will eventually
        collide and spawn other patterns. """

        # world width and height, compensating for rim cells
        _w, _h = _world_size[0] - 1, _world_size[1] - 1

        return [  # creates a glider at each corner of world: NW, NE, SW, SE
            (1, 3), (2, 3), (3, 3), (2, 1), (3, 2),
            (1, _w - 3), (2, _w - 3), (3, _w - 3), (2, _w - 1), (3, _w - 2),
            (_h - 1, 3), (_h - 2, 3), (_h - 3, 3), (_h - 3, 2), (_h - 2, 1),
            (_h - 1, _w - 3), (_h - 2, _w - 3), (_h - 3, _w - 3), (_h - 3, _w - 2), (_h - 2, _w - 1)
        ]

    def create_pulsar() -> list:
        """ Create a pulsar, which is an period 3 oscillator pattern. """
        _vc = int(_world_size[1] * .5)  # vertical center
        _hc = int(_world_size[0] * .5)  # horizontal center

        mapped_vals = {  # map column values to row keys
            1: [2, 3, 4],
            2: [1, 6],
            3: [1, 6],
            4: [1, 6],
            6: [2, 3, 4]
        }

        pulsar = []
        for row, cols in mapped_vals.items():
            for col in cols:
                pulsar.append(tuple((_vc - row, _hc - col)))  # top-left
                pulsar.append(tuple((_vc - row, _hc + col)))  # top-right
                pulsar.append(tuple((_vc + row, _hc - col)))  # bottom-left
                pulsar.append(tuple((_vc + row, _hc + col)))  # bottom-right

        return pulsar

    def create_penta_decathlon() -> list:
        """ Create a Penta-decathlon, which is a 15 period oscillator. """
        _vc = int(_world_size[1] * .5 - 1)  # vertical center
        _hc = int(_world_size[0] * .5)  # horizontal center
        return [
            (_vc - 5, _hc - 1), (_vc - 5, _hc), (_vc - 5, _hc + 1),
            (_vc - 4, _hc), (_vc - 3, _hc),
            (_vc - 2, _hc - 1), (_vc - 2, _hc), (_vc - 2, _hc + 1),

            (_vc, _hc - 1), (_vc, _hc), (_vc, _hc + 1),
            (_vc + 1, _hc - 1), (_vc + 1, _hc), (_vc + 1, _hc + 1),

            (_vc + 3, _hc - 1), (_vc + 3, _hc), (_vc + 3, _hc + 1),
            (_vc + 4, _hc), (_vc + 5, _hc),
            (_vc + 6, _hc - 1), (_vc + 6, _hc), (_vc + 6, _hc + 1)
        ]

    switcher = {
        'gliders': create_gliders(),
        'pulsar': create_pulsar(),
        'penta': create_penta_decathlon()
    }
    return switcher.get(_pattern, None)
