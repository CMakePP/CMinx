/*
Copyright (c) 2018  zbq.

License for use and distribution: Eclipse Public License

CMake language grammar reference:
https://cmake.org/cmake/help/v3.12/manual/cmake-language.7.html

Modified by Branden Butler on behalf of Ames Laboratory/Department of Energy
October 31st, 2019

*/

grammar CMake;

/*
Changes:
	Renamed from file to cmake_file to avoid conflict with Python
	Added documented_command to list of expected parser rules
	Added bracket_doccomment to parser rules
	Added Docstring to lexer rules
*/
cmake_file
	: documented_module? (documented_command | command_invocation)* EOF
	;

/*Begin CMinx*/

documented_command
	: bracket_doccomment command_invocation
	;

documented_module
    : Module_docstring
    ;

bracket_doccomment
    : Docstring
    ;

Module_docstring
    : Doccomment_start Space? '@module' (Space Unquoted_argument)? .*? '#]]'
    ;

Docstring
        : Doccomment_start .*? '#]]'
	;


Doccomment_start
    : '#[[['
    ;

Blockcomment_end
    : '#]]'
    ;



/*End Cminx*/

command_invocation
	: Identifier '(' (single_argument|compound_argument)* ')'
	;

single_argument
	: Identifier | Unquoted_argument | Bracket_argument | Quoted_argument
	;

compound_argument
	: '(' (single_argument|compound_argument)* ')'
	;

Identifier
	: [A-Za-z_][A-Za-z0-9_]*
	;

Unquoted_argument
	: (~[ \t\r\n()#"\\] | Escape_sequence)+
	;

Escape_sequence
	: Escape_identity | Escape_encoded | Escape_semicolon
	;

fragment
Escape_identity
	: '\\' ~[A-Za-z0-9;]
	;

fragment
Escape_encoded
	: '\\t' | '\\r' | '\\n'
	;

fragment
Escape_semicolon
	: '\\;'
	;

Quoted_argument
	: '"' (~[\\"] | Escape_sequence | Quoted_cont)* '"'
	;

fragment
Quoted_cont
	: '\\' ('\r' '\n'? | '\n')
	;

Bracket_argument
	: '[' Bracket_arg_nested ']'
	;

fragment
Bracket_arg_nested
	: '=' Bracket_arg_nested '='
	| '[' .*? ']'
	;




Bracket_comment
	: '#[' Bracket_arg_nested ']'
	-> skip
	;

Line_comment
	: '#' (  // #
	  	  | '[' '='*   // #[==
		  | '[' '='* ~('=' | '[' | '\r' | '\n') ~('\r' | '\n')*  // #[==xx
		  | ~('[' | '\r' | '\n') ~('\r' | '\n')*  // #xx
		  ) ('\r' '\n'? | '\n' | EOF)
    -> skip
	;

Newline
	: ('\r' '\n'? | '\n')+
	-> skip
	;

Space
	: [ \t]+
	-> skip
	;


