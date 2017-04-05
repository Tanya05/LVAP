import tokenize

file = open("sample.py")

def tokeneater(type, token, (srow, scol), (erow, ecol), line):
    print "%d,%d-%d,%d:\t%s\t%s\t\t\t\t%s" % \
        (srow, scol, erow, ecol, tokenize.tok_name[type], repr(token), line)

tokenize.tokenize(file.readline, tokeneater)	