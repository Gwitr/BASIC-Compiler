import lark
import basic_parser

TABSIZE = 16

class InterpreterError(Exception):
    pass

class Interpreter():
    
    def __init__(self, code):
        self.ast = basic_parser.parse(code)
        self.current_line = 0
        self.label_lines = {}
        for i, node in enumerate(self.ast.children):
            if node.data == "label":
                self.label_lines[str(node.children[0])] = i
        
        self.variables = {}
    
    def tick(self):
        if self.current_line >= len(self.ast.children):
            return False
        
        node = self.ast.children[self.current_line]
        if node.data == "label":
            self.current_line += 1
        
        elif node.data == "let":
            name = node.children[0].children[0]
            if name[-1] not in "%$!":
                # Variables are float by default
                name += "!"
            expr = self.eval_expr(node.children[1])
            sym = self.type_to_symbol(type(expr))
            if name[-1] == "!" and sym == "%":
                expr = float(expr)
            elif name[-1] == "%" and sym == "!":
                expr = int(expr)
            elif name[-1] != sym:
                raise InterpreterError("Tried assigning a %s value a variable of type %s" % (sym, name[-1]))
            # print(name, "=", expr)
            self.variables[name] = expr
            self.current_line += 1
        
        elif node.data == "goto":
            if str(node.children[0]) not in self.label_lines:
                raise InterpreterError("Unknown label %r" % str(node.children[0]))
            
            self.current_line = self.label_lines[str(node.children[0])]
        
        elif node.data == "print":
            s = ""
            i = 0
            while i < len(node.children):
                s += str(self.eval_expr(node.children[i]))
                
                i += 1
                if i < len(node.children) and str(node.children[i]) == ",":
                    s += " " * (TABSIZE - len(s) % TABSIZE)
                i += 1
            
            if i == len(node.children):
                print(s, end="")
            else:
                print(s)
            
            self.current_line += 1
        
        else:
            raise NotImplementedError("Node %s" % node.data)
        
        return True
    
    def eval_expr(self, node):
        def _binop_getargs(name, allowed_types, cast):
            L = self.eval_expr(node.children[0])
            R = self.eval_expr(node.children[1])
            
            if (type(L), type(R)) in cast:
                lt, rt = cast[type(L), type(R)]
                L = lt(L)
                R = rt(R)

            for combination in allowed_types:
                if {type(L), type(R)} == combination:
                    break
            else:
                raise InterpreterError("Cannot %s %s value and %s value" % (name, self.type_to_symbol(type(L)), self.type_to_symbol(type(R))))
            
            return L, R
        
        if type(node) is lark.Token:
            return self.eval_token(node)
        
        if node.data == "add":
            L, R = _binop_getargs("add", [{int, int}, {float, float}, {str, str}], {(float, int): (float, float), (int, float): (float, float)})
            return type(L)(L + R)
        
        elif node.data == "sub":
            L, R = _binop_getargs("subtract", [{int, int}, {float, float}, {str, str}], {(float, int): (float, float), (int, float): (float, float)})
            return type(L)(L + R)
        
        elif node.data == "mul":
            L, R = _binop_getargs("multiply", [{int, int}, {float, float}, {str, str}], {(float, int): (float, float), (int, float): (float, float)})
            return type(L)(L * R)
        
        elif node.data == "div":
            L, R = _binop_getargs("divide", [{int, int}, {float, float}, {str, str}], {(float, int): (float, float), (int, float): (float, float)})
            return type(L)(L / R)
        
        elif node.data in {"intvar", "floatvar", "strvar"}:
            name = str(node.children[0])
            if name[-1] not in "!%$":
                name += "!"
            if name not in self.variables:
                raise InterpreterError("Variable %s doesn't exist" % name)
            return self.variables[name]
        
        else:
            raise NotImplementedError("Node %s" % node.data)
    
    def eval_token(self, node):
        snode = str(node)
        if node.type == "QSTR":
            # Lark doesn't allow adding additional parsing code to tokens so it has to be done here
            s = ""
            i = 1
            while i < len(snode) - 1:
                if snode[i] == "\\":
                    i += 1
                s += snode[i]
                i += 1
            return s
        
        elif node.type == "NUMBER":
            return float(snode)

        else:
            raise NotImplementedError("Token %s" % node)
    
    def type_to_symbol(self, t):
        return {int: "%", float: "!", str: "$"}[t]

if __name__ == "__main__":
    it = Interpreter("""
let I = 0
loop:
    print "I = "; I
    let I = I + 1
    goto loop
""")
    print(it.ast.pretty())
    while it.tick():
        pass
