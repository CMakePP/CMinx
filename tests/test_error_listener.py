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
        #This method will only be called if the grammar is bad, call manually to ensure that if it is ever called we get an error
        self.assertRaises(RuntimeError, self.listener.reportAmbiguity, None, None, None, None, None, None, None)

    def test_full_context(self):
        #No-op, we include it for documentation purposes
        #Will be called if an SLL conflict occurs but before a full-context LL resolution is made
        #Not an error, only a notification of a differing method than normal resolution
        self.assertEqual(None, self.listener.reportAttemptingFullContext(None, None, None, None, None, None))

    def test_context_sensitivity(self):
        #May be called in normal operating conditions and does not necessarily represent an error
        #Included for documentation purposes
        #No-op
        self.assertEqual(None, self.listener.reportContextSensitivity(None, None, None, None, None, None))
