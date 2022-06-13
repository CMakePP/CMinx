from antlr4.error.ErrorListener import ErrorListener


class CMakeSyntaxError(SyntaxError):
    pass


class ParserErrorListener(ErrorListener):
    """
    Listens for parser errors and raises exceptions when they occur.
    """

    def __init__(self):
        super(ParserErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """
        As per the Antlr4 Javadoc:
            Upon syntax error, notify any interested parties. This is not how to recover from errors or compute error messages.
            ErrorStrategy specifies how to recover from syntax errors and how to compute error messages.
            This listener's job is simply to emit a computed message, though it has enough information to create its own message in many cases.
            The RecognitionException (e) is non-null for all syntax errors except when we discover mismatched token errors that we can recover from in-line,
            without returning from the surrounding rule (via the single token insertion and deletion mechanism).
        :raises RecognitionException: When the mismatched token cannot be recovered from
        :raises CMakeSyntaxError: When it is possible to recover from this error via single token insertion/deletion.
        """
        if e is not None:
            raise e
        else:
            s = CMakeSyntaxError()
            s.lineno = f"{line}:{column}"
            s.msg = msg
            raise s

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        """
        As per the Antlr4 Javadoc:
            This method is called by the parser when a full-context prediction results in an ambiguity.
            Each full-context prediction which does not result in a syntax error will call either ErrorListener.reportContextSensitivity() or ErrorListener.reportAmbiguity().

            When ambigAlts is not None, it contains the set of potentially viable alternatives identified by the prediction algorithm. When ambigAlts is None, use ATNConfigSet.getAlts() to obtain the represented alternatives from the configs argument.

            When exact is True, all of the potentially viable alternatives are truly viable, i.e. this is reporting an exact ambiguity. When exact is False, at least two of the potentially viable alternatives are viable for the current input, but the prediction algorithm terminated as soon as it determined that at least the minimum potentially viable alternative is truly viable.

            When the PredictionMode.LL_EXACT_AMBIG_DETECTION prediction mode is used, the parser is required to identify exact ambiguities so exact will always be true.

            This method is not used by lexers.

        :raises RuntimeError: Unconditionally, we should not encounter ambiguities
        """

        raise RuntimeError("Parse ambiguity")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        """
        As per the Antlr4 Javadoc:
            This method is called when an SLL conflict occurs and the parser is about to use the full context information to make an LL decision.
            If one or more configurations in configs contains a semantic predicate, the predicates are evaluated before this method is called. The subset of alternatives which are still viable after predicates are evaluated is reported in conflictingAlts.

            This method is not used by lexers.

        Currently this is a no-op, it is unknown whether we should allow or disallow full context LL decisions.
        """
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        """
        As per the Antlr4 Javadoc:
            This method is called by the parser when a full-context prediction has a unique result.
            Each full-context prediction which does not result in a syntax error will call either ErrorListener.reportContextSensitivity() or ErrorListener.reportAmbiguity().

            For prediction implementations that only evaluate full-context predictions when an SLL conflict is found (including the default ParserATNSimulator implementation), this method reports cases where SLL conflicts were resolved to unique full-context predictions, i.e. the decision was context-sensitive.
            This report does not necessarily indicate a problem, and it may appear even in completely unambiguous grammars.
            configs may have more than one represented alternative if the full-context prediction algorithm does not evaluate predicates before beginning the full-context prediction. In all cases, the final prediction is passed as the prediction argument.

            Note that the definition of "context sensitivity" in this method differs from the concept in DecisionInfo.contextSensitivities. This method reports all instances where an SLL conflict occurred but LL parsing produced a unique result, whether or not that unique result matches the minimum alternative in the SLL conflicting set.

            This method is not used by lexers.

        This method is currently a no-op, as it being called does not indicate an error necessarily.
        """
        pass
