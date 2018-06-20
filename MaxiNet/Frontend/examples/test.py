import time
import sys
from MaxiNet.Frontend import maxinet
from MaxiNet.tools import FatTree
from mininet.node import OVSSwitch
import overlay 
sys.path.append('/home/maxinet/MaxiNet/sflowrt/extras/')
import sflow as sflow


# Build up the topology and distribute to worders
topo = overlay.Overlay()
cluster = maxinet.Cluster()
exp = maxinet.Experiment(cluster, topo, switch=OVSSwitch)
exp.setup()

# Feed the topo data to sflow dashboard
(ifname, agent) = sflow.getIfInfo(sflow.collector)
print('ifname is %s and agent is %s' % (ifname, agent))
sflow.configSFlow(exp, sflow.collector, ifname)
sflow.newSendTopology(exp, agent, sflow.collector)

# Test 
print "waiting 10 seconds for routing algorithms on the controller to converge"
time.sleep(50)
print exp.get_node("h1").cmd("ping -c 1 10.0.0.5")
print exp.get_node("h2").cmd("iperf -c 10.0.0.6 -t 10")

exp.stop()


