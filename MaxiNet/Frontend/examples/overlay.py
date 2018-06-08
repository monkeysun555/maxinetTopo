
from mininet.topo import Topo
from MaxiNet.tools import Tools
from mininet.node import OVSSwitch
from MaxiNet.Frontend import maxinet

import random
import re
import time

class Overlay(Topo):

	# Here in order to establish the datacenter topo. User define the number of software router
	# and end nodes.
	def __init__(self, 	numDC=2, numSr=3, nodesPerSr=1,  \
				internetTopo = 'singleRouter', DCtopo='line', subnet='10.0.0.', \
				bwlimit=10, lat=1, **opts):

		Topo.__init__(self, **opts)
		assert numSr > 0
		assert nodesPerSr > 0
		assert numDC > 0
		
		numofDC = 0
		# self.datacenters = []
		# self.servicerouters = []
		# self.nodes = []

		internet = self.createInternet()

		for i in range(numDC):
			datacenter, srList, nodeList = self.createDC(numofDC, numSr, nodesPerSr, DCtopo, subnet, bwlimit, lat)
			self.connect(datacenter[1], internet[0], bwlimit, lat)
			numofDC += 1
			# self.datacenters.append(datacenter)
			# self.servicerouters.append(srList)
			# self.nodes.append(nodeList)


	def createInternet(self, internetTopo='singleRouter'):
		routerIndex = 1
		internetRouterList = []
		if internetTopo == 'singleRouter':
			internetRouter = self.addSwitch('intR'+ str(routerIndex), dpid=Tools.makeDPID(routerIndex),
										**dict(listenPort=(10000+routerIndex-1)))
			internetRouterList.append(internetRouter)
		return internetRouterList

	def createDC(self, numofDC, numSr, nodesPerSr, DCtopo, subnet, bwlimit, lat):

		srList = []
		nodeList = []
		DCIdx = numofDC + 1
		srIdx = numofDC * numSr + 1
		nodeIdx = numofDC * numSr * nodesPerSr + 1
		#create service router 

		for i in range(numSr):
			sr = self.addSwitch('sr'+ str(srIdx), dpid=Tools.makeDPID(srIdx),
										**dict(listenPort=(13000+srIdx-1)))
			print("create sr %s" % sr)
			# create nodes
			for j in range(nodesPerSr):
				h = self.addHost('h' + str(nodeIdx), mac=Tools.makeMAC(nodeIdx),
								ip=subnet+str(nodeIdx))
				print("create host %s" % h)
				nodeList.append(h)
				self.addLink(h, sr, bw=bwlimit, delay=str(lat)+'ms')
				print("add link between %s and %s" % (h, sr))
				nodeIdx += 1
			srIdx += 1
			
			# if fullmesh, ovs should be defined to break loop!!!
			if DCtopo == 'fullmesh':
			# connect sr to previous srs
				for tempSrIdx in range(len(srList)):
					self.addLink(sr, srList[tempSrIdx], bw=bwlimit, delay=str(lat)+'ms')
					print("add link between %s and %s" % (sr, srList[tempSrIdx]))
			elif DCtopo == 'line':
				if len(srList) > 0:
					self.addLink(sr, srList[-1], bw=bwlimit, delay=str(lat)+'ms')
			srList.append(sr)

		DC = [DCIdx, srList[0]]
		return DC, srList, nodeList

	def connect(self, component1, component2, bwlimit, lat):
		self.addLink(component1, component2, bw=bwlimit, delay=str(lat)+'ms')
		print("add link between %s and %s" % (component1, component2))

	# def listComponents(self):
	# 	print("DC lists: %s" % self.datacenters)
	# 	print("Service router list: %s" % self.servicerouters)
	# 	print("Node lists: %s" % self.nodes)
	# 	return





# class pair(Topo):
# 	def __init__(self, **opts):
# 		Topo.__init__(self, **opts)
# 		subnet='10.0.0.'
# 		bwlimit = 1
# 		lat = 1
# 		s = 1
# 		k = 1
# 		sr1 = self.addSwitch('sr'+ str(s), dpid=Tools.makeDPID(s), **dict(listenPort=(13000+s-1)))
# 		s += 1
# 		h1 = self.addHost('h' + str(k), mac=Tools.makeMAC(k), ip=subnet+str(k))
# 		k += 1
# 		self.addLink(h1, sr1, bw=bwlimit, delay=str(lat)+'ms')

# 		sr2 = self.addSwitch('sr'+ str(s), dpid=Tools.makeDPID(s), **dict(listenPort=(13000+s-1)))
# 		s += 1
# 		h2 = self.addHost('h' + str(k), mac=Tools.makeMAC(k), ip=subnet+str(k))
# 		k += 1
# 		self.addLink(h2, sr2, bw=bwlimit, delay=str(lat)+'ms')

# 		self.addLink(sr1, sr2, bw=bwlimit, delay=str(lat)+'ms')






