import parser

parser = parser.Parser("./basicLoop/BasicLoop.vm")
code = parser.get_code()
print(code)