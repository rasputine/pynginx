def cacti(blob, subcommand):
	if len(subcommand)<2: 
		subcommand=['cacti','index']
	if subcommand[1]=='index': 
		for line in cactiIndex(blob): print line
	elif subcommand[1]=='query': 
		for line in cactiQuery(blob, subcommand[2]): print line
	elif subcommand[1]=='get':
		print cactiGet(blob, subcommand[2], subcommand[3])
	else: print "Unrecognized command: {0}".format(subcommand[1])

def cactiIndex(blob):
	results=[]
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]:
			results.append(instance["server"])
	return results

def cactiQuery(blob, query):
	results=[]
	if query == 'upstream':
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]:
				results.append("!".join([instance["server"], upstream]))
	elif query == 'hostname':
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]:
				results.append("!".join([instance["server"], upstream]))
	else:
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]:
				results.append("!".join([instance["server"], str(instance[query])]))
	return results

def cactiGet(blob, query, index):
	index=str(index)
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]:
			if instance["server"]==index:
				return instance[query]
	return None
	