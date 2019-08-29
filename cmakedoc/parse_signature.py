from .cmake_regexer import CMakeRegexer


def _parse_signature(fxn_type, lines):
    """Code factorization for parse_function_start/parse_macro_start.

    This function actually implements
    """
    data = lines[0]
    new_first_line = 1
    nlines = len(lines)

    while ')' not in data and new_first_line < nlines:
        temp_line = lines[new_first_line]

        # If we find a '(' the user must have forgotten ')' so abort looking
        if '(' in temp_line:
            new_first_line = nlines
            break

        data += '\n' + temp_line
        new_first_line += 1

    if new_first_line == nlines and ')' not in data:
        raise SyntaxError(fxn_type + '(...) is missing ")"')

    regexer = CMakeRegexer()
    end_found = False
    while new_first_line < nlines:
        new_first_line += 1
        if regexer.has_purpose(lines[new_first_line - 1], fxn_type + " end"):
            end_found = True
            break

    if not end_found:
        raise SyntaxError("end" + fxn_type + "() was not found")

    return data, lines[new_first_line:]


def parse_function_start(lines):
    """Extract a function's signature from CMake code

    This function will loop over the list of CMake code in ``lines`` and extract
    the signature of the function it finds. The returned signature will be
    something like ``function(my_function arg1 arg2)`` preserving spacing and
    newlines.

    :param lines: Lines of CMake code that have not been parsed yet. The first
                  line is assumed to declare a function.
    :type lines: list[str]
    :return: The function's signature and ``lines`` advanced past the function's
             definition.
    :rtype: tuple[str, list[str]]
    """
    if not CMakeRegexer().has_purpose("function start", lines[0]):
        raise ValueError(lines[0] + " is not the start of a CMake function")

    return _parse_signature("function", lines)


def parse_macro_start(lines):
    """Extract a macro's signature from CMake code

    This function will loop over the list of CMake code in ``lines`` and extract
    the signature of the macro it finds. The returned signature will be
    something like ``macro(my_macro arg1 arg2)`` preserving spacing and
    newlines.

    :param lines: Lines of CMake code that have not been parsed yet. The first
                  line is assumed to declare a macro.
    :type lines: list[str]
    :return: The macro's signature and ``lines`` advanced past the macro's
             definition.
    :rtype: tuple[str, list[str]]
    """
    if not CMakeRegexer().has_purpose("macro start", lines[0]):
        raise ValueError(lines[0] + " is not the start of a CMake macro")

    return _parse_signature("macro", lines)
