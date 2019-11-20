from antlr4.error.ErrorListener import ErrorListener

class CMakeSyntaxError(SyntaxError):
    pass


class ParserErrorListener( ErrorListener ):
    """
    Listens for parser errors and raises exceptions when they occur.
    """
    def __init__(self):
        super(ParserErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """
        Called when the parser expects a particular token but encounters a different one.

        :raises CMakeSyntaxError:
        """

        s = CMakeSyntaxError()
        s.lineno = line
        s.msg = msg
        raise s

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        """
        Antlr4 Python documentation is pretty sparse, but it appears this is called when the
        parser encounters a section where multiple parse rules apply and it cannot resolve which to execute.

        :raises RuntimeError:
        """

        raise RuntimeError("Parse ambiguity")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        """
        Very little documentation for the Python Antlr4 API,
        but this appears to be triggered when the parser encounters an error
        in while processing a context-sensitive parser rule and tries
        to run a full-context (I think that means global or root context) parser rule

        :raises RuntimeError:
        """
        raise RuntimeError("Parser attempting full context")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        """
        Very little documentation for the Python Antlr4 API,
        but this appears to be triggered when a problem occurs during resolution
        of a context-sensitive parser rule

        :raises RuntimeError
        """
        raise RuntimeError("Parser context sensitivity")
