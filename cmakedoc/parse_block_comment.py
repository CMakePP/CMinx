from .cmake_regexer import CMakeRegexer


def _parse_comment_block(lines):
    """Code factorization for parse_block_comment/parse_block_docstring

    This function is responsible for extracting a CMake block comment regardless of called when a non-documentation CMake block comment is
    found. This function iterates over the CMake code in ``lines`` until the end
    of the block comment is found. ``lines`` is then returned with the block
    comment removed.

    :param lines: Lines of CMake code, the first of which should start with a
                  non-documentation block comment.
    :type lines: list[str]
    :return: the block comment and ``lines`` with the block comment removed.
    :rtype: tuple(str, list[str])
    """

    regexer = CMakeRegexer()
    nlines = len(lines)

    # -- Basic input error checking --------------------------------------------
    if nlines == 0:
        raise ValueError('strings to parse are empty')

    # -- Extract the block comment ---------------------------------------------
    block_comment = lines[0]

    # Use a for-loop to enforce a termination condition
    for i in range(1, nlines):
        block_comment += '\n' + lines[i]
        if regexer.has_purpose(lines[i], 'block comment end'):
            return block_comment, lines[i + 1:]

    raise SyntaxError('End of block comment not found')


def parse_block_comment(lines):
    regexer = CMakeRegexer()

    if not regexer.has_purpose(lines[0], 'block comment start'):
        msg = 'line: "{}" is not the start of a block comment'.format(lines[0])
        raise ValueError(msg)

    return _parse_comment_block(lines)


def parse_block_docstring(lines):
    regexer = CMakeRegexer()

    if not regexer.has_purpose(lines[0], 'block docstring'):
        msg = 'line: "{}" is not the start of a block docstring'.format(lines[0])
        raise ValueError(msg)

    return _parse_comment_block(lines)