#!/usr/bin/python3

import context
import unittest
from cmakedoc.parser import ParserErrorListener, CMakeSyntaxError

class TestErrorListener(unittest.TestCase):
    def setUp(self):
        self.listener = ParserErrorListener()

    def test_syntax_error(self):
        self.assertRaises(CMakeSyntaxError, self.listener.syntaxError, None, None, 1, 1, "Test message", None)

    def test_ambiguity(self):
        #Unsure of how to trigger this failure type in Antlr, will look into it more later
        self.assertRaises(RuntimeError, self.listener.reportAmbiguity, None, None, None, None, None, None, None)

    def test_full_context(self):
        #Unsure of how to trigger this error
        self.assertRaises(RuntimeError, self.listener.reportAttemptingFullContext, None, None, None, None, None, None)

    def test_context_sensitivity(self):
        #Unsure of how to trigger this error
        self.assertRaises(RuntimeError, self.listener.reportContextSensitivity, None, None, None, None, None, None)
