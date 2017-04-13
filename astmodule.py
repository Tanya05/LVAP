import ast 

content = open("sample.py").read()
tree = ast.parse(content)
for node in ast.walk(tree):
    if isinstance(node, ast.Name):
        print str(node.id) + " " + str(node.ctx) + " at line " + str(node.lineno)
    	# if isinstance (node.ctx, ast.Store):
    	# 	print node.id 
    	# 	print node.lineno
    	# else:
    	# 	print "hi"