# Generated from CMake.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\21")
        buf.write("<\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\3\2\5\2\22\n\2\3\2\3\2\3\2\7\2\27\n\2\f\2\16\2\32")
        buf.write("\13\2\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\6")
        buf.write("\3\6\7\6)\n\6\f\6\16\6,\13\6\3\6\3\6\3\7\3\7\3\b\3\b\3")
        buf.write("\b\7\b\65\n\b\f\b\16\b8\13\b\3\b\3\b\3\b\2\2\t\2\4\6\b")
        buf.write("\n\f\16\2\3\4\2\t\n\f\r\2<\2\21\3\2\2\2\4\35\3\2\2\2\6")
        buf.write(" \3\2\2\2\b\"\3\2\2\2\n$\3\2\2\2\f/\3\2\2\2\16\61\3\2")
        buf.write("\2\2\20\22\5\6\4\2\21\20\3\2\2\2\21\22\3\2\2\2\22\30\3")
        buf.write("\2\2\2\23\27\5\4\3\2\24\27\5\n\6\2\25\27\5\b\5\2\26\23")
        buf.write("\3\2\2\2\26\24\3\2\2\2\26\25\3\2\2\2\27\32\3\2\2\2\30")
        buf.write("\26\3\2\2\2\30\31\3\2\2\2\31\33\3\2\2\2\32\30\3\2\2\2")
        buf.write("\33\34\7\2\2\3\34\3\3\2\2\2\35\36\5\b\5\2\36\37\5\n\6")
        buf.write("\2\37\5\3\2\2\2 !\7\5\2\2!\7\3\2\2\2\"#\7\6\2\2#\t\3\2")
        buf.write("\2\2$%\7\t\2\2%*\7\3\2\2&)\5\f\7\2\')\5\16\b\2(&\3\2\2")
        buf.write("\2(\'\3\2\2\2),\3\2\2\2*(\3\2\2\2*+\3\2\2\2+-\3\2\2\2")
        buf.write(",*\3\2\2\2-.\7\4\2\2.\13\3\2\2\2/\60\t\2\2\2\60\r\3\2")
        buf.write("\2\2\61\66\7\3\2\2\62\65\5\f\7\2\63\65\5\16\b\2\64\62")
        buf.write("\3\2\2\2\64\63\3\2\2\2\658\3\2\2\2\66\64\3\2\2\2\66\67")
        buf.write("\3\2\2\2\679\3\2\2\28\66\3\2\2\29:\7\4\2\2:\17\3\2\2\2")
        buf.write("\t\21\26\30(*\64\66")
        return buf.getvalue()


class CMakeParser ( Parser ):

    grammarFileName = "CMake.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "<INVALID>", "<INVALID>", 
                     "'#[[['", "'#]]'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "Module_docstring", 
                      "Docstring", "Doccomment_start", "Blockcomment_end", 
                      "Identifier", "Unquoted_argument", "Escape_sequence", 
                      "Quoted_argument", "Bracket_argument", "Bracket_comment", 
                      "Line_comment", "Newline", "Space" ]

    RULE_cmake_file = 0
    RULE_documented_command = 1
    RULE_documented_module = 2
    RULE_bracket_doccomment = 3
    RULE_command_invocation = 4
    RULE_single_argument = 5
    RULE_compound_argument = 6

    ruleNames =  [ "cmake_file", "documented_command", "documented_module", 
                   "bracket_doccomment", "command_invocation", "single_argument", 
                   "compound_argument" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    Module_docstring=3
    Docstring=4
    Doccomment_start=5
    Blockcomment_end=6
    Identifier=7
    Unquoted_argument=8
    Escape_sequence=9
    Quoted_argument=10
    Bracket_argument=11
    Bracket_comment=12
    Line_comment=13
    Newline=14
    Space=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class Cmake_fileContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(CMakeParser.EOF, 0)

        def documented_module(self):
            return self.getTypedRuleContext(CMakeParser.Documented_moduleContext,0)


        def documented_command(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Documented_commandContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Documented_commandContext,i)


        def command_invocation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Command_invocationContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Command_invocationContext,i)


        def bracket_doccomment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Bracket_doccommentContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Bracket_doccommentContext,i)


        def getRuleIndex(self):
            return CMakeParser.RULE_cmake_file

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCmake_file" ):
                listener.enterCmake_file(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCmake_file" ):
                listener.exitCmake_file(self)




    def cmake_file(self):

        localctx = CMakeParser.Cmake_fileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_cmake_file)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==CMakeParser.Module_docstring:
                self.state = 14
                self.documented_module()


            self.state = 22
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CMakeParser.Docstring or _la==CMakeParser.Identifier:
                self.state = 20
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                if la_ == 1:
                    self.state = 17
                    self.documented_command()
                    pass

                elif la_ == 2:
                    self.state = 18
                    self.command_invocation()
                    pass

                elif la_ == 3:
                    self.state = 19
                    self.bracket_doccomment()
                    pass


                self.state = 24
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 25
            self.match(CMakeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Documented_commandContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def bracket_doccomment(self):
            return self.getTypedRuleContext(CMakeParser.Bracket_doccommentContext,0)


        def command_invocation(self):
            return self.getTypedRuleContext(CMakeParser.Command_invocationContext,0)


        def getRuleIndex(self):
            return CMakeParser.RULE_documented_command

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDocumented_command" ):
                listener.enterDocumented_command(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDocumented_command" ):
                listener.exitDocumented_command(self)




    def documented_command(self):

        localctx = CMakeParser.Documented_commandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_documented_command)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.bracket_doccomment()
            self.state = 28
            self.command_invocation()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Documented_moduleContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Module_docstring(self):
            return self.getToken(CMakeParser.Module_docstring, 0)

        def getRuleIndex(self):
            return CMakeParser.RULE_documented_module

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDocumented_module" ):
                listener.enterDocumented_module(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDocumented_module" ):
                listener.exitDocumented_module(self)




    def documented_module(self):

        localctx = CMakeParser.Documented_moduleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_documented_module)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(CMakeParser.Module_docstring)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Bracket_doccommentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Docstring(self):
            return self.getToken(CMakeParser.Docstring, 0)

        def getRuleIndex(self):
            return CMakeParser.RULE_bracket_doccomment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBracket_doccomment" ):
                listener.enterBracket_doccomment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBracket_doccomment" ):
                listener.exitBracket_doccomment(self)




    def bracket_doccomment(self):

        localctx = CMakeParser.Bracket_doccommentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_bracket_doccomment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.match(CMakeParser.Docstring)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Command_invocationContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Identifier(self):
            return self.getToken(CMakeParser.Identifier, 0)

        def single_argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Single_argumentContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Single_argumentContext,i)


        def compound_argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Compound_argumentContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Compound_argumentContext,i)


        def getRuleIndex(self):
            return CMakeParser.RULE_command_invocation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommand_invocation" ):
                listener.enterCommand_invocation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommand_invocation" ):
                listener.exitCommand_invocation(self)




    def command_invocation(self):

        localctx = CMakeParser.Command_invocationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_command_invocation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self.match(CMakeParser.Identifier)
            self.state = 35
            self.match(CMakeParser.T__0)
            self.state = 40
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CMakeParser.T__0) | (1 << CMakeParser.Identifier) | (1 << CMakeParser.Unquoted_argument) | (1 << CMakeParser.Quoted_argument) | (1 << CMakeParser.Bracket_argument))) != 0):
                self.state = 38
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [CMakeParser.Identifier, CMakeParser.Unquoted_argument, CMakeParser.Quoted_argument, CMakeParser.Bracket_argument]:
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

    class Single_argumentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingle_argument" ):
                listener.enterSingle_argument(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingle_argument" ):
                listener.exitSingle_argument(self)




    def single_argument(self):

        localctx = CMakeParser.Single_argumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_single_argument)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CMakeParser.Identifier) | (1 << CMakeParser.Unquoted_argument) | (1 << CMakeParser.Quoted_argument) | (1 << CMakeParser.Bracket_argument))) != 0)):
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

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def single_argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Single_argumentContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Single_argumentContext,i)


        def compound_argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CMakeParser.Compound_argumentContext)
            else:
                return self.getTypedRuleContext(CMakeParser.Compound_argumentContext,i)


        def getRuleIndex(self):
            return CMakeParser.RULE_compound_argument

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompound_argument" ):
                listener.enterCompound_argument(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompound_argument" ):
                listener.exitCompound_argument(self)




    def compound_argument(self):

        localctx = CMakeParser.Compound_argumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_compound_argument)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self.match(CMakeParser.T__0)
            self.state = 52
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CMakeParser.T__0) | (1 << CMakeParser.Identifier) | (1 << CMakeParser.Unquoted_argument) | (1 << CMakeParser.Quoted_argument) | (1 << CMakeParser.Bracket_argument))) != 0):
                self.state = 50
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [CMakeParser.Identifier, CMakeParser.Unquoted_argument, CMakeParser.Quoted_argument, CMakeParser.Bracket_argument]:
                    self.state = 48
                    self.single_argument()
                    pass
                elif token in [CMakeParser.T__0]:
                    self.state = 49
                    self.compound_argument()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 54
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 55
            self.match(CMakeParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





