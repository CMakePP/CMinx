# Generated from CMake.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CMakeParser import CMakeParser
else:
    from CMakeParser import CMakeParser

# This class defines a complete listener for a parse tree produced by CMakeParser.
class CMakeListener(ParseTreeListener):

    # Enter a parse tree produced by CMakeParser#cmake_file.
    def enterCmake_file(self, ctx:CMakeParser.Cmake_fileContext):
        pass

    # Exit a parse tree produced by CMakeParser#cmake_file.
    def exitCmake_file(self, ctx:CMakeParser.Cmake_fileContext):
        pass


    # Enter a parse tree produced by CMakeParser#documented_command.
    def enterDocumented_command(self, ctx:CMakeParser.Documented_commandContext):
        pass

    # Exit a parse tree produced by CMakeParser#documented_command.
    def exitDocumented_command(self, ctx:CMakeParser.Documented_commandContext):
        pass


    # Enter a parse tree produced by CMakeParser#documented_module.
    def enterDocumented_module(self, ctx:CMakeParser.Documented_moduleContext):
        pass

    # Exit a parse tree produced by CMakeParser#documented_module.
    def exitDocumented_module(self, ctx:CMakeParser.Documented_moduleContext):
        pass


    # Enter a parse tree produced by CMakeParser#bracket_doccomment.
    def enterBracket_doccomment(self, ctx:CMakeParser.Bracket_doccommentContext):
        pass

    # Exit a parse tree produced by CMakeParser#bracket_doccomment.
    def exitBracket_doccomment(self, ctx:CMakeParser.Bracket_doccommentContext):
        pass


    # Enter a parse tree produced by CMakeParser#command_invocation.
    def enterCommand_invocation(self, ctx:CMakeParser.Command_invocationContext):
        pass

    # Exit a parse tree produced by CMakeParser#command_invocation.
    def exitCommand_invocation(self, ctx:CMakeParser.Command_invocationContext):
        pass


    # Enter a parse tree produced by CMakeParser#single_argument.
    def enterSingle_argument(self, ctx:CMakeParser.Single_argumentContext):
        pass

    # Exit a parse tree produced by CMakeParser#single_argument.
    def exitSingle_argument(self, ctx:CMakeParser.Single_argumentContext):
        pass


    # Enter a parse tree produced by CMakeParser#compound_argument.
    def enterCompound_argument(self, ctx:CMakeParser.Compound_argumentContext):
        pass

    # Exit a parse tree produced by CMakeParser#compound_argument.
    def exitCompound_argument(self, ctx:CMakeParser.Compound_argumentContext):
        pass


