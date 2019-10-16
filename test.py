"""

Implement a function, that will receive array of strings as an input.
All strings have same size and can contain only two characters - 'X' or ' ' (space character).
function should determine number of dots available in this array.
Function should return integer number of dots found and ignore other figures.
Figures are considered connected if the touch each other on the full side (diagonal connection doesn't count).

"""
import re
import pytest

VALIDATE_RX = re.compile(r'^[\s*X*]+$')


class EmptyLines(BaseException):
    pass


def validate_lengths(lines):
    if len(lines) == 0:
        raise EmptyLines
    length = len(lines[0])
    for line in lines[1:]:
        if len(line) != length:
            error_msg = f"Lines in {lines} array have different lengths."
            raise ValueError(error_msg)


def validate_symbols(line):
    if line and not VALIDATE_RX.match(line):
        raise ValueError(f'Invalid line "{line}"')


def validate_lines(lines):
    validate_lengths(lines)
    for line in lines:
        validate_symbols(line)


def line_to_bool(line):
    return list(map(lambda x: True if x == 'X' else False, line))


def figures(lines):
    dots_counter = 0
    try:
        validate_lines(lines)
    except EmptyLines:
        return dots_counter
    except Exception as e:
        raise e
    line_length = len(lines[0])
    bool_lines = list()
    for line in lines:
        bool_lines.append(line_to_bool(line))
    for line_number in range(0, len(bool_lines)):
        for index in range(0, line_length):
            current = bool_lines[line_number][index]
            if current:
                left = False if index == 0 else bool_lines[line_number][index - 1]
                right = False if index == line_length - 1 else bool_lines[line_number][index + 1]
                upper = False if line_number == 0 else bool_lines[line_number - 1][index]
                down = False if line_number == len(bool_lines) - 1 else bool_lines[line_number + 1][index]
                if current ^ left and current ^ right and current ^ upper and current ^ down:
                    dots_counter += 1
    return dots_counter


if __name__ == '__main__':
    assert figures([
        ' X '
    ]) == 1
    assert figures([' X  ',
                    '  X ']) == 2
    assert figures([
        ' XX '
    ]) == 0
    assert figures([' XX ',
                    ' XX ']) == 0
    assert figures([' X ',
                    ' X ']) == 0
    assert figures(['', '']) == 0
    assert figures(['']) == 0
    with pytest.raises(ValueError):
        assert figures(['a'])
    assert figures([]) == 0
    # predefined cases:
    assert figures([
        '          ',
        '          '
    ]) == 0
    assert figures([
        '  X        ',
        '           '
    ]) == 1
    assert figures([
        '                 X  ',
        '   X     XXX      X ',
        '     X   XXX        ',
        '    XX   XXX  XXX   '
    ]) == 3

