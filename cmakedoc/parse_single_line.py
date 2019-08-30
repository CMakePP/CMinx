from .cmake_regexer import CMakeRegexer


def _parse_single_line(purpose, lines):
    """Extract (possibly) a block of single line comments

    This function is primarily meant as code factorization for
    ``parse_single_line_comment`` and ``parse_single_line_docstring``. Given a
    list of un-parsed CMake code, the first line of which is a single line
    comment/docstring, this function will extract that comment/docstring and all
    subsequent lines of CMake code that are also single line comments/docstrings
    until a non-single-line comment/docstring is encountered.

    :param purpose: Expected to be either "single line comment" or
                    "single line docstring" depending on whether we are
                    respectively parsing a comment or a docstring.
    :type purpose: str
    :param lines: The CMake code to be parsed by this function.
    :type lines: list[str]
    :return: The block of consecutive line comments and ``lines`` advanced to
             past the block.
    :rtype: tuple[str, list[str]]
    """
    regexer = CMakeRegexer()

    if len(lines) == 0 or not regexer.has_purpose(lines[0], purpose):
        raise ValueError("Input does not start with a " + purpose)

    data = lines[0]

    for new_next_line in range(1, len(lines)):
        if not regexer.has_purpose(lines[new_next_line], purpose):
            return data, lines[new_next_line:]

        data += '\n' + lines[new_next_line]

    # If we got here then we added all the lines to the comment
    return data, []


def parse_single_line_comment(lines):
    """Extract a block of consecutive single-line comments.

    This function calls ``_parse_single_line`` in order to extract a single
    line comment. It is assumed that consecutive single-line comments are
    actually intended as a block comment and the extracted comment is actually
    the block of single-line comments.

    :param lines: The list of lines of CMake code from which to extract the
                  comments. It is assumed that the first line in ``lines`` is
                  a single-line comment.
    :type lines: list[str]
    :return: The block of consecutive single-line comments and ``lines``. Upon
             return ``lines`` will be advanced to the line following the
             comments.
    :rtype: tuple[str, list[str]]
    """
    return _parse_single_line('single line comment', lines)


def parse_single_line_docstring(lines):
    """Extract a block of consecutive single-line docstrings.

    This function calls ``_parse_line_comment`` in order to extract a single
    line docstring. It is assumed that consecutive single-line docstrings are
    actually intended as a block docstring and the extracted docstring is
    actually the block of single-line docstrings.

    :param lines: The list of lines of CMake code from which to extract the
                  docstring. It is assumed that the first line in ``lines`` is
                  a single-line docstring.
    :type lines: list[str]
    :return: The block of consecutive single-line docstrings and ``lines``. Upon
             return ``lines`` will be advanced to the line following the
             docstrings.
    :rtype: tuple[str, list[str]]
    """
    return _parse_single_line('single line docstring', lines)


def parse_other_line(lines):
    """Extract a block of CMake code with unknown purpose.

    This function calls ``_parse_single_line`` in order to extract CMake code
    that serves a purpose other than the ones we dispatch on. Consecutive lines
    of unknown purpose CMake code are extracted together as a single entity.

    :param lines: The list of lines of CMake code from which to extract the
                  docstring. It is assumed that the first line in ``lines`` is
                  a line of CMake code of unknown origin.
    :type lines: list[str]
    :return: The block of consecutive unknown CMake code and ``lines``. Upon
             return ``lines`` will be advanced to the line following the
             extracted code.
    :rtype: tuple[str, list[str]]
    """

    return _parse_single_line('other', lines)


def parse_blank_line(lines):
    """Extract a block of blank lines from a CMake source file.

    This function calls ``_parse_single_line`` in order to extract blank lines
    from the source file. Consecutive blank lines are extracted together and
    returned as a single entity.

    :param lines: The list of lines of CMake code from which to extract the
                  blank lines. It is assumed that the first line in ``lines`` is
                  a blank line.
    :type lines: list[str]
    :return: The block of consecutive blank lines and ``lines``. Upon return
             ``lines`` will be advanced to the line following the blank lines.
    :rtype: tuple[str, list[str]]
    """

    return _parse_single_line('blank', lines)
