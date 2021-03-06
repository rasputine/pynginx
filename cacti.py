from sys import stdout
from lookup import lookup
from re import match
def cacti(blob, subcommand, regex, env):
	"""Processes commands to return data in cacti's format.
	"""
	if len(subcommand)<2: #Default to providing an index if too few inputs are provided.
		subcommand=['cacti','index']
	if subcommand[1]=='index': 
		for line in cactiIndex(blob, regex): 
			print line
	elif subcommand[1]=='count':
		print len(cactiIndex(blob, regex))
	elif subcommand[1]=='query': 
		for line in cactiQuery(blob, subcommand[2], regex, env): 
			print line
	elif subcommand[1]=='get':
		stdout.write( str(cactiGet(blob, subcommand[2], subcommand[3], regex, env)) )
	elif subcommand[1]=='connections':
		for L in blob['connections']: stdout.write( ":".join( [str(L), str(blob['connections'][L])]) + " " )
		for L in blob['requests']: stdout.write( ":".join( [str(L), str(blob['requests'][L])]) + " ")
	else: 
		print "Unrecognized command: {0}".format(subcommand[1])

def cactiIndex(blob, regex):
	"""Returns a list of backends for cacti.
	These will be ip:port, one per line.
	These must be unique for cacti"""
	results=[]
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]["peers"]:
			if match(regex,upstream): results.append(instance["server"])
	return results

def cactiQuery(blob, query, regex, env):

	results=[]
	if query == 'upstream':
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]["peers"]:
				if match(regex,upstream): results.append("!".join([instance["server"], upstream]))
	elif query == 'hostname':
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]["peers"]:
				if match(regex,upstream): results.append("!".join([instance["server"], lookup(instance["server"], env)]))
	else:
		for upstream in blob["upstreams"]:
			for instance in blob["upstreams"][upstream]["peers"]:
				if match(regex,upstream): results.append("!".join([instance["server"], str(instance[query])]))
	return results

def cactiGet(blob, query, index, regex, env):
	index=str(index)
	for upstream in blob["upstreams"]:
		for instance in blob["upstreams"][upstream]["peers"]:
			if instance["server"]==index and match(regex,upstream):
				if query == "hostname":
					return lookup(instance["server"], env)
				return instance[query]
	return None
