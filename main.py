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

print(parser.parse("""
loop:
    print "Hello, world!"; CHR$(17 * 2); "abc"; CHR$(32 + 2)
    goto loop
""").pretty())
