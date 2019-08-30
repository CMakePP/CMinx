import re


class CMakeRegexer:
    """Encapsulates the regexes associated with parsing a CMake source file.

    The CMakeRegexer class is used to determine what a line of CMake code does.
    We term this the line's "purpose". Currently the choices for the purpose
    are:

    - "function start" : e.g. ``function(name_of_function arg1...)``
    - "function end" : e.g. ``endfunction()``
    - "macro start" : e.g. ``macro(name_of_macro arg1...)``
    - "macro end" : e.g. ``endmacro()``
    - "single line comment" : e.g. ``# A single line comment``
    - "single line docstring" : e.g. ``## Documentation for the thing``
    - "block docstring" : e.g. ``#[[[ Beginning of block doc string``
    - "block comment start" : e.g. ``#[[``
    - "block comment end" : e.g. ``#]]``
    - ``blank`` : e.g. ``     ``
    - "other" : e.g. ``set(var value)``

    All regexes strive to embrace the full flexibility of the CMake language so
    as to not generate false positives or overlook a valid variant of the above.
    For example the regexes that look for ``function``, ``macro``, etc. are
    case-insensitive and we allow for whitespace around each parenthesis. That
    said, there are some known restrictions:

    - All regexes only look at the first non-whitespace characters on the line.

    :param regexes: Mapping from purposes to regexes
    :type regexes: dict[str, RegexObject]
    """

    def __init__(self):
        """Initialize ``regexes`` to the default set"""
        ic = re.IGNORECASE
        self.regexes = {
            "function start": re.compile(r'^\s*function\(', ic),
            "function end": re.compile(r'^\s*endfunction\(\s*\)', ic),
            "macro start": re.compile(r'^\s*macro\(', ic),
            "macro end": re.compile(r'^\s*endmacro\(\s*\)', ic),
            "single line comment": re.compile(r'^\s*#[^#\[\]]'),
            "single line docstring": re.compile(r'^\s*##'),
            "block docstring": re.compile(r'^\s*#\[\[\['),
            "block comment start": re.compile(r'^\s*#\[\[(?!\[)'),
            "block comment end": re.compile(r'^\s*#\]\]'),
            "blank": re.compile(r'^\s*\n?$')
        }

    def get_purpose(self, line):
        """Return the purpose of the line.

        This function is used to determine which of the recognized purposes the
        line maps to. See the class description for a list of possible purposes.

        :param line: The line of CMake code to analyze.
        :type line: str
        :return: The purpose of ``line``.
        :rtype: str
        """
        for type_i, regex_i in self.regexes.items():
            if regex_i.match(line):
                return type_i
        return "other"

    def has_purpose(self, line, purpose):
        """Determine if a line has a specific purpose.

        This function is basically ``purpose == get_purpose(line)`` except that
        it additionally ensures that ``purpose`` is a recognized purpose.

        :param line: The line of CMake code to analyze.
        :type line: str
        :param purpose: The purpose we are wondering if ``line`` serves.
        :type purpose: str
        :return: True if ``line`` serves purpose ``purpose`` otherwise False.
        :rtype: bool
        :raise ValueError: If ``purpose`` is not a recognized purpose.
        """

        if purpose not in self.regexes and purpose != 'other':
            raise ValueError(purpose + " is not a known purpose.")

        if purpose == 'other':
            for type_i, regex_i in self.regexes.items():
                if regex_i.match(line):
                    return False
            return True

        return bool(self.regexes[purpose].match(line))
