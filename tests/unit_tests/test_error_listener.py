#!/usr/bin/python3
# Copyright 2021 CMakePP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest

from cminx.parser import ParserErrorListener, CMakeSyntaxError


class TestErrorListener(unittest.TestCase):
    def setUp(self):
        self.listener = ParserErrorListener()

    def test_syntax_error(self):
        self.assertRaises(CMakeSyntaxError, self.listener.syntaxError, None, None, 1, 1, "Test message", None)

    def test_ambiguity(self):
        # This method will only be called if the grammar is bad, call manually to ensure that if it is ever called we get an error
        self.assertRaises(RuntimeError, self.listener.reportAmbiguity, None, None, None, None, None, None, None)

    def test_full_context(self):
        # No-op, we include it for documentation purposes
        # Will be called if an SLL conflict occurs but before a full-context LL resolution is made
        # Not an error, only a notification of a differing method than normal resolution
        self.assertEqual(None, self.listener.reportAttemptingFullContext(None, None, None, None, None, None))

    def test_context_sensitivity(self):
        # May be called in normal operating conditions and does not necessarily represent an error
        # Included for documentation purposes
        # No-op
        self.assertEqual(None, self.listener.reportContextSensitivity(None, None, None, None, None, None))
