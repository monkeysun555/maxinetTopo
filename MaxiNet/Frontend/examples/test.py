import time
import sys
from MaxiNet.Frontend import maxinet
from MaxiNet.tools import FatTree
from mininet.node import OVSSwitch
import overlay 


sys.path.append('/home/maxinet/MaxiNet/sflowrt/extras/')

import sflow as sflow

topo = overlay.Overlay()
for s in topo.switches:
    print('111')
print ("Type of topo is %s" % type(topo))

# topo.listComponents()

# topo = overlay.pair()	

cluster = maxinet.Cluster()

exp = maxinet.Experiment(cluster, topo, switch=OVSSwitch)
exp.setup()

print ("Type of exp is %s" % type(exp))
print ("Type of exp.topo is %s" % type(exp.topology))
# print ("Type of exp is %s" % type(exp))


print exp.get_node("h1").cmd("ifconfig")  # call mininet cmd function of h1
print exp.get_node("h2").cmd("ifconfig")  # call mininet cmd function of h2
# print exp.get_node("h3").cmd("ifconfig")  # call mininet cmd function of h3

# print exp.get_node("h4").cmd("ifconfig")  # call mininet cmd function of h4
# print exp.get_node("h5").cmd("ifconfig")  # call mininet cmd function of h5
# print exp.get_node("h6").cmd("ifconfig")  # call mininet cmd function of h6

print "waiting 10 seconds for routing algorithms on the controller to converge"
time.sleep(5)

print exp.get_node("h1").cmd("ping -c 1 10.0.0.5")

# time.sleep(1)

# print exp.get_node("h1").cmd("ping -c 5 10.0.0.4")

# time.sleep(1)

# print exp.get_node("h5").cmd("ping -c 5 10.0.0.4")

# time.sleep(1)

# print exp.get_node("h5").cmd("ping -c 5 10.0.0.3")

exp.stop()
