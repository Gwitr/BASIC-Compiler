import sys
import lark

with open("grammar.yy", encoding="utf8") as f:
    # Pre-process grammar file
    data = f.read()
    kwargs = {}
    for line in data.split("\n"):
        d = line.split("// KWARG: ")
        if len(d) > 1:
            d = "// KWARG: ".join(d[1:])
            key, *value = d.split("=")
            value = "=".join(value)
            kwargs[key] = value
    
    # Construct the parser
    parser = lark.Lark(data, **kwargs)

sys.modules[__name__] = parser

if __name__ == "__main__":
    print(parser.parse("""
    let I% = 0
    loop:
        print "I =", I%
        let I% = I% + 1
        goto loop
    """).pretty())
