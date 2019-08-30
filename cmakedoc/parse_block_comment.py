from .cmake_regexer import CMakeRegexer


def _parse_comment_block(lines):
    """Code factorization for parse_block_comment/parse_block_docstring

    This function is responsible for extracting a CMake block comment regardless
    of whether it is a standard CMake block comment or a CMakeDoc documentation
    comment. This function iterates over the CMake code in ``lines`` until the
    end of the block comment is found. The block comment and ``lines`` are then
    returned with the block comment removed from ``lines``.

    :param lines: Lines of CMake code, the first of which should start with
                  either a non-documentation or documentation block comment.
    :type lines: list[str]
    :return: the block comment and ``lines`` with the block comment removed.
    :rtype: tuple(str, list[str])
    :raise ValueError: Raised if ``lines`` is empty.
    :raise SyntaxError: Raised if ``lines`` does not contain the end of the
                        block comment.
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
    """Extracts a normal block comment from CMake code.

    This function will extract a normal CMake block comment by calling
    ``_parse_comment_block``.

    :param lines: The CMake code, separated by lines, that this function should
                  extract the block comment from.
    :type lines: list[str]
    :return: The block comment and ``lines`` advanced to past the block comment.
    :rtype: tuple[str, list[str]]
    :raise ValueError: Raised if ``lines`` does not start with a normal block
                       comment.
    """

    regexer = CMakeRegexer()

    if not regexer.has_purpose(lines[0], 'block comment start'):
        msg = 'line: "{}" is not the start of a block comment'.format(lines[0])
        raise ValueError(msg)

    return _parse_comment_block(lines)


def parse_block_docstring(lines):
    """Extracts a docstring block comment from CMake code.

    This function will extract a docstring CMake block comment by calling
    ``_parse_comment_block``.

    :param lines: The CMake code, separated by lines, that this function should
                  extract the docstring block comment from.
    :type lines: list[str]
    :return: The docstring and ``lines`` advanced to past the docstring.
    :rtype: tuple[str, list[str]]
    :raise ValueError: Raised if ``lines`` does not start with a docstring block
                       comment.
    """

    regexer = CMakeRegexer()

    if not regexer.has_purpose(lines[0], 'block docstring'):
        msg = 'line: "{}" is not the start of a block docstring'.format(lines[0])
        raise ValueError(msg)

    return _parse_comment_block(lines)