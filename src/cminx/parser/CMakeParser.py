# Generated from CMake.g4 by ANTLR 4.7.2
# encoding: utf-8
import sys
from io import StringIO

from antlr4 import *
from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\16")
        buf.write("\60\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\7")
        buf.write("\2\17\n\2\f\2\16\2\22\13\2\3\2\3\2\3\3\3\3\3\3\3\3\7\3")
        buf.write("\32\n\3\f\3\16\3\35\13\3\3\3\3\3\3\4\3\4\3\4\3\5\3\5\3")
        buf.write("\6\3\6\3\6\7\6)\n\6\f\6\16\6,\13\6\3\6\3\6\3\6\2\2\7\2")
        buf.write("\4\6\b\n\2\3\4\2\5\6\b\t\2\60\2\20\3\2\2\2\4\25\3\2\2")
        buf.write("\2\6 \3\2\2\2\b#\3\2\2\2\n%\3\2\2\2\f\17\5\6\4\2\r\17")
        buf.write("\5\4\3\2\16\f\3\2\2\2\16\r\3\2\2\2\17\22\3\2\2\2\20\16")
        buf.write("\3\2\2\2\20\21\3\2\2\2\21\23\3\2\2\2\22\20\3\2\2\2\23")
        buf.write("\24\7\2\2\3\24\3\3\2\2\2\25\26\7\5\2\2\26\33\7\3\2\2\27")
        buf.write("\32\5\b\5\2\30\32\5\n\6\2\31\27\3\2\2\2\31\30\3\2\2\2")
        buf.write("\32\35\3\2\2\2\33\31\3\2\2\2\33\34\3\2\2\2\34\36\3\2\2")
        buf.write("\2\35\33\3\2\2\2\36\37\7\4\2\2\37\5\3\2\2\2 !\7\n\2\2")
        buf.write("!\"\5\4\3\2\"\7\3\2\2\2#$\t\2\2\2$\t\3\2\2\2%*\7\3\2\2")
        buf.write("&)\5\b\5\2\')\5\n\6\2(&\3\2\2\2(\'\3\2\2\2),\3\2\2\2*")
        buf.write("(\3\2\2\2*+\3\2\2\2+-\3\2\2\2,*\3\2\2\2-.\7\4\2\2.\13")
        buf.write("\3\2\2\2\b\16\20\31\33(*")
        return buf.getvalue()


class CMakeParser(Parser):
    grammarFileName = "CMake.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'('", "')'"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "Identifier",
                     "Unquoted_argument", "Escape_sequence", "Quoted_argument",
                     "Bracket_argument", "Bracket_doccomment", "Bracket_comment",
                     "Line_comment", "Newline", "Space"]

    RULE_cmake_file = 0
    RULE_command_invocation = 1
    RULE_documented_command = 2
    RULE_single_argument = 3
    RULE_compound_argument = 4

    ruleNames = ["cmake_file", "command_invocation", "documented_command",
                 "single_argument", "compound_argument"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    Identifier = 3
    Unquoted_argument = 4
    Escape_sequence = 5
    Quoted_argument = 6
    Bracket_argument = 7
    Bracket_doccomment = 8
    Bracket_comment = 9
    Line_comment = 10
    Newline = 11
    Space = 12

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class Cmake_fileContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(CMakeParser.EOF, 0)

        def documented_command(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Documented_commandContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Documented_commandContext, i)

        def command_invocation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Command_invocationContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Command_invocationContext, i)

        def getRuleIndex(self):
            return CMakeParser.RULE_cmake_file

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCmake_file"):
                listener.enterCmake_file(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCmake_file"):
                listener.exitCmake_file(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCmake_file"):
                return visitor.visitCmake_file(self)
            else:
                return visitor.visitChildren(self)

    def cmake_file(self):

        localctx = CMakeParser.Cmake_fileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_cmake_file)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == CMakeParser.Identifier or _la == CMakeParser.Bracket_doccomment:
                self.state = 12
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [CMakeParser.Bracket_doccomment]:
                    self.state = 10
                    self.documented_command()
                    pass
                elif token in [CMakeParser.Identifier]:
                    self.state = 11
                    self.command_invocation()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 16
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 17
            self.match(CMakeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Command_invocationContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(CMakeParser.Identifier, 0)

        def single_argument(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Single_argumentContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Single_argumentContext, i)

        def compound_argument(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Compound_argumentContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Compound_argumentContext, i)

        def getRuleIndex(self):
            return CMakeParser.RULE_command_invocation

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCommand_invocation"):
                listener.enterCommand_invocation(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCommand_invocation"):
                listener.exitCommand_invocation(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCommand_invocation"):
                return visitor.visitCommand_invocation(self)
            else:
                return visitor.visitChildren(self)

    def command_invocation(self):

        localctx = CMakeParser.Command_invocationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_command_invocation)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self.match(CMakeParser.Identifier)
            self.state = 20
            self.match(CMakeParser.T__0)
            self.state = 25
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & (
                    (1 << CMakeParser.T__0) | (1 << CMakeParser.Identifier) | (1 << CMakeParser.Unquoted_argument) | (
                    1 << CMakeParser.Quoted_argument) | (1 << CMakeParser.Bracket_argument))) != 0):
                self.state = 23
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [CMakeParser.Identifier, CMakeParser.Unquoted_argument, CMakeParser.Quoted_argument,
                             CMakeParser.Bracket_argument]:
                    self.state = 21
                    self.single_argument()
                    pass
                elif token in [CMakeParser.T__0]:
                    self.state = 22
                    self.compound_argument()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 28
            self.match(CMakeParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Documented_commandContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Bracket_doccomment(self):
            return self.getToken(CMakeParser.Bracket_doccomment, 0)

        def command_invocation(self):
            return self.getTypedRuleContext(CMakeParser.Command_invocationContext, 0)

        def getRuleIndex(self):
            return CMakeParser.RULE_documented_command

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterDocumented_command"):
                listener.enterDocumented_command(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitDocumented_command"):
                listener.exitDocumented_command(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitDocumented_command"):
                return visitor.visitDocumented_command(self)
            else:
                return visitor.visitChildren(self)

    def documented_command(self):

        localctx = CMakeParser.Documented_commandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_documented_command)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(CMakeParser.Bracket_doccomment)
            self.state = 31
            self.command_invocation()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Single_argumentContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(CMakeParser.Identifier, 0)

        def Unquoted_argument(self):
            return self.getToken(CMakeParser.Unquoted_argument, 0)

        def Bracket_argument(self):
            return self.getToken(CMakeParser.Bracket_argument, 0)

        def Quoted_argument(self):
            return self.getToken(CMakeParser.Quoted_argument, 0)

        def getRuleIndex(self):
            return CMakeParser.RULE_single_argument

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterSingle_argument"):
                listener.enterSingle_argument(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitSingle_argument"):
                listener.exitSingle_argument(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitSingle_argument"):
                return visitor.visitSingle_argument(self)
            else:
                return visitor.visitChildren(self)

    def single_argument(self):

        localctx = CMakeParser.Single_argumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_single_argument)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & (
                    (1 << CMakeParser.Identifier) | (1 << CMakeParser.Unquoted_argument) | (
                    1 << CMakeParser.Quoted_argument) | (1 << CMakeParser.Bracket_argument))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Compound_argumentContext(ParserRuleContext):

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def single_argument(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Single_argumentContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Single_argumentContext, i)

        def compound_argument(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Compound_argumentContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Compound_argumentContext, i)

        def getRuleIndex(self):
            return CMakeParser.RULE_compound_argument

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCompound_argument"):
                listener.enterCompound_argument(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCompound_argument"):
                listener.exitCompound_argument(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCompound_argument"):
                return visitor.visitCompound_argument(self)
            else:
                return visitor.visitChildren(self)

    def compound_argument(self):

        localctx = CMakeParser.Compound_argumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_compound_argument)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(CMakeParser.T__0)
            self.state = 40
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & (
                    (1 << CMakeParser.T__0) | (1 << CMakeParser.Identifier) | (1 << CMakeParser.Unquoted_argument) | (
                    1 << CMakeParser.Quoted_argument) | (1 << CMakeParser.Bracket_argument))) != 0):
                self.state = 38
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [CMakeParser.Identifier, CMakeParser.Unquoted_argument, CMakeParser.Quoted_argument,
                             CMakeParser.Bracket_argument]:
                    self.state = 36
                    self.single_argument()
                    pass
                elif token in [CMakeParser.T__0]:
                    self.state = 37
                    self.compound_argument()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 42
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 43
            self.match(CMakeParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
