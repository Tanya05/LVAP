import ast 

num_lines = sum(1 for line in open('sample.py'))
#print num_lines

content = open("sample.py").read()
tree = ast.parse(content)

for node in ast.walk(tree):
    if isinstance(node, ast.Name):
        print str(node.id) + " " + str(node.ctx) + " at line " + str(node.lineno)

var_info = {}

for node in ast.walk(tree):
    if isinstance(node, ast.Name):
        if node.id not in var_info:
        	var_info[node.id] = [[],[],[]]
    	if isinstance (node.ctx, ast.Load):
    		var_info[node.id][0].append(node.lineno)
    	if isinstance (node.ctx, ast.Store):
    		var_info[node.id][1].append(node.lineno)
    	if isinstance (node.ctx, ast.Param):
    		var_info[node.id][2].append(node.lineno)

print var_info
print "\n\n"

for key in var_info:
	line_info = {}
	line_info[key] = []
	for i in range(1,num_lines+1):
		if i in var_info[key][0]:
			line_info[key].append("Load")
		elif i in var_info[key][1]:
			line_info[key].append("Store")
		elif i in var_info[key][2]:
			line_info[key].append("Param")
		else:	
			line_info[key].append("Not Present")
	print line_info	