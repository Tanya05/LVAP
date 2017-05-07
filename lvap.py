import ast 

# Change sample.py to filename in next 2 lines to run LVAP on you code.
#find number of lines and read code from given source.
num_lines = sum(1 for line in open('sample.py'))
content = open("sample.py").read()
tree = ast.parse(content)
var_info = {}

#Create priliminary datastructure.
#Datastructure used: Dictionary of lists: {'variable' : [][]][]}
#List 1: Variables being loaded on the lines.
#List 2: Variables being stored on the lines
#List 3: Variables used as params
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



#implementing the algorithm for Live Variable Analysis
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
	analysis = {}
	if "Param" not in line_info:
		i = 0
	else:
		i = line_info.index("Param")
		for x in range(1,i+1):
			analysis[str(x)] = "Not Live"
		analysis[str(i+1)] = "Parameter variable, function definiton"
		i = i+1
	while i < len(line_info):
		if i < len(line_info) and line_info[i] == "Store":
			analysis[str(i+1)] = "Live, written to"
			temp_load = -1
			temp_store = i+1
			i=i+1
			while i < len(line_info) and line_info[i] != "Store":
				if i < len(line_info) and line_info[i] == "Load":
					analysis[str(i+1)] = "Live, read"
					temp_load = i+1
					i=i+1
				if i < len(line_info) and line_info[i] == "Not Present":
					analysis[str(i+1)] = "Live"
					i=i+1
			if temp_load != -1 and temp_load > temp_store:
				for index in range(temp_load, i):
					analysis[str(index+1)] = "Not Live"
			if temp_load < temp_store:
				for index in range(temp_store, i):
					analysis[str(index+1)] = "Not Live"
		if i < len(line_info) and line_info[i] == "Not Present":
			analysis[str(i+1)] = "Not Live"
			i=i+1
		if i < len(line_info) and line_info[i] == "Load":
			analysis[str(i+1)] = "Live, read"
			temp_load = i+1
			i=i+1
			while i < len(line_info) and line_info[i] != "Store":
				if i < len(line_info) and line_info[i] == "Load":
					analysis[str(i+1)] = "Live, read"
					temp_load = i+1
					i=i+1
				if i < len(line_info) and line_info[i] == "Not Present":
					analysis[str(i+1)] = "Live"
					i=i+1
			if temp_load != -1 and temp_load < i:
				for index in range(temp_load, i):
					analysis[str(index+1)] = "Not Live"
	print "\nAnalysis For " + key #+ " " + str(analysis) + "\n\n"
	for x in range(1, num_lines+1):
		print "At Line: " + str(x) + " - " + str(analysis[str(x)])