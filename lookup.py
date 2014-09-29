import socket
import os
import json
import sys

class Lookup():
	"""DNS lookup and (slow) cache
	Reverse-lookup for for nginx/nagios cross talk.

	Args:
		file (str):
			Name of the file used for storing dns responses.

	"""
	def __init__(self, dnsfile):
		self.dnsfile = dnsfile
		self.names = self.readDNS(dnsfile)

	def readDNS(self, dnsfile):
		with open(dnsfile, 'r+') as file:
			try:
				return json.load(file)
			except ValueError as v:
				return dict()
				
	def writeDNS(self):
		with open(self.dnsfile, 'w') as file:
			file.write(str(self.names))
	
	def lookup(self, address, qm=None):
		"""Return hostname of host at address.
		Returns address if dns doesn't respond.
		"""
		ip=self.ip(address, qm)
		try:
			hostname=socket.gethostbyaddr(ip)[0].split('.')[0]
		except socket.herror:
			self.names[ip]="Unkown host"
			return ip
		else:
			print hostname
			self.names[ip]=hostname
			return hostname

	def ip(self, address, qm=None):
		ip = str(address.split(':')[0])
		if qm=='dev':
			#hackiness for environment specific silliness.
			#Changes ips, eg from x.x.x.x to x.x.2.x
			ip=ip.split('.')
			ip[2]=2
			ip=(str(ip[0])+'.'+str(ip[1])+'.'+str(ip[2])+'.'+str(ip[3]))
		elif qm=='prod':
			ip=ip.split('.')
			ip[2]=1
			ip=(str(ip[0])+'.'+str(ip[1])+'.'+str(ip[2])+'.'+str(ip[3]))
		return ip