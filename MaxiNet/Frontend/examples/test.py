import time
import sys
from MaxiNet.Frontend import maxinet
from MaxiNet.Frontend import cli
from MaxiNet.tools import FatTree
from mininet.node import OVSSwitch
import overlay 
sys.path.append('/home/maxinet/MaxiNet/sflowrt/extras/')
import sflow as sflow
import console
# Build up the topology and distribute to worders
topo = overlay.Overlay()


mapping = {"h1": 0, "h2": 0, "h5": 2, "h6": 2, \
			"sr1": 0, "sr2": 0, "sr3": 2, "sr4": 2, \
			 "intR1": 1, "intR2": 1}



cluster = maxinet.Cluster(minWorkers=3,maxWorkers=3)
exp = maxinet.Experiment(cluster, topo, switch=OVSSwitch, nodemapping=mapping)
exp.setup()


# Feed the topo data to sflow dashboard
(ifname, agent) = sflow.getIfInfo(sflow.collector)
print('ifname is %s and agent is %s' % (ifname, agent))
sflow.newconfigSFlow(exp, sflow.collector, ifname)
sflow.newSendTopology(exp, agent, sflow.collector)
# sflow.tunnel_func(exp, agent, sflow.collector)

# Test 
print "waiting 5 seconds for routing algorithms on the controller to converge"
time.sleep(5)
## enable initial routing
worker = exp.cluster.get_worker('worker1')
worker.run_cmd('~/routing.sh')
worker = exp.cluster.get_worker('worker2')
worker.run_cmd('~/routing.sh')
worker = exp.cluster.get_worker('worker3')
worker.run_cmd('~/routing.sh')
# print("Initialized with Static Routing")
# print exp.get_node("h2").cmd("ping -c 3 10.0.0.6")
# mode = 'static'

exp.CLI('./', './')
# console.console_platform(mode, n_path)

exp.stop()
