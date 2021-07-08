// ===== Parser arguments =====
// KWARG: parser=lalr
// KWARG: start=program
// ============================



program: _NEWLINE* statement (_NEWLINE+ statement)* _NEWLINE+

// Add new commands here
?statement: NAME ":"                       -> label
    | _GOTO NAME                           -> goto
    | _PRINT expr (psep expr)* [psep]      -> print
    | _LET variable "=" expr               -> let


?psep: COMMA | SEMICOLON


// ===== Operators and expressions =====
?expr: addsub

?addsub: muldiv
    | addsub "+" muldiv -> add
    | addsub "-" muldiv -> sub

?muldiv: atom
    | muldiv "*" atom -> mul
    | muldiv "/" atom -> div

?atom: "(" expr ")"
    | variable
    | NUMBER
    | QSTR 
    
    | fname "(" [expr ("," expr)*] ")"  -> call

?variable: NAME "%"  -> intvar
    | NAME "$"       -> strvar
    | NAME "!"       -> floatvar
    | NAME           -> floatvar

?fname: NAME "%"  -> intfunc
    | NAME "$"    -> strfunc
    | NAME "!"    -> floatfunc
    | NAME        -> floatfunc
// =====================================

// ===== Terminals =====
// Generic tokens
NAME.1: /[A-Za-z_][A-Za-z0-9_]*/
NUMBER: /[1-9][0-9]*|0/
QSTR: ESCAPED_STRING     // Lark doesn't remove any special characters :/

// Instruction tokens
// Note: The ".3" is required so that the parser doesn't parse them as NAME tokens
_PRINT.3: "print"i
_GOTO.3:  "goto"i
_LET.3:   "let"i

// Constant tokens
_NEWLINE: /\n/
COMMA: ","
SEMICOLON: ";"
// =====================

// ===== Parser directives =====
%ignore /[\t\r ]/
%import common.ESCAPED_STRING
// =============================