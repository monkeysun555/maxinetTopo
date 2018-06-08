
from mininet.topo import Topo
import random
import re

class DataCenter(Topo):
	def randByte(self, max=255):
		return hex(random.randint(0, max))[2:]

	def makeMAC(self, i):
		return "00:" + self.randByte() + ":" + \
			   self.randByte() + ":00:00:" + hex(i)[2:]

	def makeDPID(self, i):
		a = self.makeMAC(i)
		dp = "".join(re.findall(r'[a-f0-9]+', a))
		return "0" * (16 - len(dp)) + dp

	# Here in order to establish the Datercenter topo. User define the number of software router
	# and end nodes.
	def __init__(self, 	numbSr=3, srsartID = 1, nodesPerSR=1, nodeStartID=1, subnet='10.0.0.', topology='fullmesh', 
						bwlimit=10, lat=1, **opts):
		Topo.__init__(self, **opts)
		assert numbSr > 0
		assert srsartID > 0
		assert nodesPerSR > 0
		assert nodeStartID > 0
		nodes = []
		serRouter = []
		if topology == 'fullmesh':
			for i in range(numbSr): 

				# Create service router 
				sr = self.addSwitch('sr'+ str(srsartID), dpid=self.makeDPID(srsartID),
									**dict(listenPort=(13000+srsartID-1)))
				srsartID = srsartID + 1
				for tempSr in serRouter:
					self.addLink(sr, tempSr, bw=2.0*bwlimit, delay=str(lat)+'ms')
				serRouter.append(sr)

				# Create node for each service router
				# And connect to service router
				for j in range(nodesPerSR):
					h = self.addHost('h' + str(nodeStartID+j), mac=self.makeMAC(nodeStartID+j),
							ip=subnet+str(nodeStartID+j))
					self.addLink(h, sr, bw=bwlimit, delay=str(lat)+'ms')
					nodeStartID = nodeStartID + 1
					nodes.append(h)

		self.sg = serRouter[0];
