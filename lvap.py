import ast 

num_lines = sum(1 for line in open('sample2.py'))
#print num_lines

content = open("sample2.py").read()
tree = ast.parse(content)

# for node in ast.walk(tree):
#     if isinstance(node, ast.Name):
#         print str(node.id) + " " + str(node.ctx) + " at line " + str(node.lineno)

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

# print var_info
# print "\n\n"

for key in var_info:
	line_info = []
	for i in range(1,num_lines+1):
		if i in var_info[key][0]:
			line_info.append("Load")
		elif i in var_info[key][1]:
			line_info.append("Store")
		elif i in var_info[key][2]:
			line_info.append("Param")
		else:	
			line_info.append("Not Present")
	#print "\n" + key + " " + str(line_info)
	analysis = {}	
	if "Param" not in line_info:
		i = 0
		while i < len(line_info):
			if i < len(line_info) and line_info[i] == "Store":
				analysis[str(i+1)] = "Live, written to"
				temp_load = 0
				i=i+1
				#print str(i) + "store"
				while i < len(line_info) and line_info[i] != "Store":
					if i < len(line_info) and line_info[i] == "Load":
						analysis[str(i+1)] = "Live, read"
						temp_load = i+1
						i=i+1
						#print str(i) + "load in store"
					if i < len(line_info) and line_info[i] == "Not Present":
						analysis[str(i+1)] = "Live"
						i=i+1
						#print str(i) + "nil in store"
				if temp_load < i:
					for index in range(temp_load, i):
						analysis[str(index+1)] = "Not Live"
			if i < len(line_info) and line_info[i] == "Not Present":
				analysis[str(i+1)] = "Not Live"
				i=i+1
				#print str(i) + "Nil"
			if i < len(line_info) and line_info[i] == "Load":
				analysis[str(i+1)] = "Live, read"
				temp_load = i+1
				i=i+1
				#print str(i) + "load"
				while i < len(line_info) and line_info[i] != "Store":
					if i < len(line_info) and line_info[i] == "Load":
						analysis[str(i+1)] = "Live, read"
						temp_load = i+1
						i=i+1
						#print str(i) + "load in load"
					if i < len(line_info) and line_info[i] == "Not Present":
						analysis[str(i+1)] = "Live"
						i=i+1
						#print str(i) + "nil in load"
				if temp_load < i:
					for index in range(temp_load, i):
						analysis[str(index+1)] = "Not Live"
	print "\nAnalysis For " + key #+ " " + str(analysis) + "\n\n"
	for x in range(1, num_lines+1):
		print "At Line: " + str(x) + " - " + str(analysis[str(x)])