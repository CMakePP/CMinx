# Generated from ./src/cminx/parser/CMake.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,15,58,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,1,0,3,0,16,8,0,1,0,1,0,1,0,5,0,21,8,0,10,0,12,0,24,9,0,1,0,1,0,
        1,1,1,1,1,1,1,2,1,2,1,3,1,3,1,4,1,4,1,4,1,4,5,4,39,8,4,10,4,12,4,
        42,9,4,1,4,1,4,1,5,1,5,1,6,1,6,1,6,5,6,51,8,6,10,6,12,6,54,9,6,1,
        6,1,6,1,6,0,0,7,0,2,4,6,8,10,12,0,1,2,0,7,8,10,11,58,0,15,1,0,0,
        0,2,27,1,0,0,0,4,30,1,0,0,0,6,32,1,0,0,0,8,34,1,0,0,0,10,45,1,0,
        0,0,12,47,1,0,0,0,14,16,3,4,2,0,15,14,1,0,0,0,15,16,1,0,0,0,16,22,
        1,0,0,0,17,21,3,2,1,0,18,21,3,8,4,0,19,21,3,6,3,0,20,17,1,0,0,0,
        20,18,1,0,0,0,20,19,1,0,0,0,21,24,1,0,0,0,22,20,1,0,0,0,22,23,1,
        0,0,0,23,25,1,0,0,0,24,22,1,0,0,0,25,26,5,0,0,1,26,1,1,0,0,0,27,
        28,3,6,3,0,28,29,3,8,4,0,29,3,1,0,0,0,30,31,5,3,0,0,31,5,1,0,0,0,
        32,33,5,4,0,0,33,7,1,0,0,0,34,35,5,7,0,0,35,40,5,1,0,0,36,39,3,10,
        5,0,37,39,3,12,6,0,38,36,1,0,0,0,38,37,1,0,0,0,39,42,1,0,0,0,40,
        38,1,0,0,0,40,41,1,0,0,0,41,43,1,0,0,0,42,40,1,0,0,0,43,44,5,2,0,
        0,44,9,1,0,0,0,45,46,7,0,0,0,46,11,1,0,0,0,47,52,5,1,0,0,48,51,3,
        10,5,0,49,51,3,12,6,0,50,48,1,0,0,0,50,49,1,0,0,0,51,54,1,0,0,0,
        52,50,1,0,0,0,52,53,1,0,0,0,53,55,1,0,0,0,54,52,1,0,0,0,55,56,5,
        2,0,0,56,13,1,0,0,0,7,15,20,22,38,40,50,52
    ]

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
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Cmake_fileContext(ParserRuleContext):
        __slots__ = 'parser'

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
            if _la==3:
                self.state = 14
                self.documented_module()


            self.state = 22
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==4 or _la==7:
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
        __slots__ = 'parser'

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
        __slots__ = 'parser'

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
        __slots__ = 'parser'

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
        __slots__ = 'parser'

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
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3458) != 0):
                self.state = 38
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [7, 8, 10, 11]:
                    self.state = 36
                    self.single_argument()
                    pass
                elif token in [1]:
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
        __slots__ = 'parser'

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
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3456) != 0)):
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
        __slots__ = 'parser'

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
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3458) != 0):
                self.state = 50
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [7, 8, 10, 11]:
                    self.state = 48
                    self.single_argument()
                    pass
                elif token in [1]:
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





