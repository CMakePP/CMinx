from .cmake_regexer import CMakeRegexer


def _parse_signature(fxn_type, lines):
    """Code factorization for parse_function_start/parse_macro_start.

    This function actually implements ``parse_function_start`` and
    ``parse_macro_start``. It starts by looping over lines until the end of the
    signature is found (*i.e.*, the closing ``)``). The function then removes
    CMake code from ``lines`` until ``lines`` is set to the line after the
    function/macro definition.

    :param fxn_type: Either "function" or "macro" depending on whether we are
                     parsing a function or a macro.
    :type fxn_type: str
    :param lines: The CMake code we are extracting the signature from.
    :type lines: list[str]
    :return: The signature of the function/macro that is being defined and
             ``lines`` advanced to the CMake code line following the function or
             macro definition.
    :rtype: tuple[str, list[str]]
    :raise SyntaxError: If the closing ``)`` can not be found or if the
                        corresponding ``endfunction()``/``endmacro()`` can not
                        be found.
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
    if not CMakeRegexer().has_purpose(lines[0], "function start"):
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
    if not CMakeRegexer().has_purpose(lines[0], "macro start"):
        raise ValueError(lines[0] + " is not the start of a CMake macro")

    return _parse_signature("macro", lines)
