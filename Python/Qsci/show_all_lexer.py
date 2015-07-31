import PyQt4.Qsci

for sym in dir(PyQt4.Qsci):
    if sym.startswith('QsciLexer'):
        print(sym)

# check more at
# http://www.scintilla.org/ScintillaDoc.html
from PyQt4.Qsci import *

filetype_list = [
    ['QsciLexerBash', ['sh', 'bash']],
    ['QsciLexerCPP', ['c', 'cpp']],
    ['QsciLexerCSS', ['css']],
    ['QsciLexerCSharp', ['cs']],
    ['QsciLexerHTML', ['htm', 'html']],
    ['QsciLexerJava', ['java']],
    ['QsciLexerJavaScript', ['js']],
    ['QsciLexerLua', ['lua']],
    ['QsciLexerPerl', ['pl']],
    ['QsciLexerPostScript', ['ps']],
    ['QsciLexerTCL', ['tcl']],
    ['QsciLexerTeX', ['tex']],
    ['QsciLexerVHDL', ['vhd']],
    ['QsciLexerVerilog', ['v', 'sv']],
    ['QsciLexerXML', ['xml']],
    ['QsciLexerYAML', ['yaml']],
    ['QsciLexerPython', ['py']],
    ['QsciLexerRuby', ['rb']],
    ['QsciLexerSQL', ['sql']]
]

other_file_type = [
    [QsciLexerBatch],
    [QsciLexerCMake],
    [QsciLexerCustom],
    [QsciLexerD],
    [QsciLexerDiff],
    [QsciLexerFortran],
    [QsciLexerFortran77],
    [QsciLexerIDL],
    [QsciLexerMakefile],
    [QsciLexerMatlab],
    [QsciLexerOctave],
    [QsciLexerPOV],
    [QsciLexerPascal],
    [QsciLexerProperties],
    [QsciLexerSpice],
]

type_mapping = {}
for item in filetype_list:
    parser = item[0]
    exts = item[1]
    for ext in exts:
        type_mapping[ext] = parser

print("file_type_mapping = {")
for ext, parser in type_mapping.items():
    print("    \'%s\': %s," % (ext, parser))
print("}")