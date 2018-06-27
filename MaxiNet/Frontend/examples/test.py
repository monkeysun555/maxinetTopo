import time
import sys
from MaxiNet.Frontend import maxinet
from MaxiNet.Frontend import cli
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
sflow.newconfigSFlow(exp, sflow.collector, ifname)
sflow.newSendTopology(exp, agent, sflow.collector)
# sflow.tunnel_func(exp, agent, sflow.collector)

# Test 
print "waiting 10 seconds for routing algorithms on the controller to converge"
time.sleep(5)
print exp.get_node("h2").cmd("ping -c 3 10.0.0.6")
time.sleep(1)
print exp.get_node("h5").cmd("ping -c 3 10.0.0.1")

# exp.CLI('./', './')
# print(exp.get_node("h6").cmd("iperf -s"))
# print(exp.get_node("h2").cmd("iperf -c 10.0.0.6 -t 10"))

exp.stop()


