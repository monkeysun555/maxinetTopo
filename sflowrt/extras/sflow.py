from mininet.net import Mininet
from mininet.util import quietRun
from requests import put
from json import dumps
from os import listdir, environ
import re
import socket
import fcntl
import array
import struct
import sys

collector = environ.get('COLLECTOR','127.0.0.1')
sampling = environ.get('SAMPLING','10')
polling = environ.get('POLLING','10')

def getIfInfo(dst):
  is_64bits = sys.maxsize > 2**32
  struct_size = 40 if is_64bits else 32
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  max_possible = 8 # initial value
  while True:
    bytes = max_possible * struct_size
    names = array.array('B')
    for i in range(0, bytes):
      names.append(0)
    outbytes = struct.unpack('iL', fcntl.ioctl(
      s.fileno(),
      0x8912,  # SIOCGIFCONF
      struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    if outbytes == bytes:
      max_possible *= 2
    else:
      break
  namestr = names.tostring()
  s.connect((dst, 0))
  ip = s.getsockname()[0]
  for i in range(0, outbytes, struct_size):
    name = namestr[i:i+16].split('\0', 1)[0]
    addr = socket.inet_ntoa(namestr[i+20:i+24])
    if addr == ip:
      return (name,addr)

def configSFlow(net,collector,ifname):
  print "*** Enabling sFlow:"
  sflow = 'ovs-vsctl -- --id=@sflow create sflow agent=%s target=%s sampling=%s polling=%s --' % (ifname,collector,sampling,polling)
  for s in net.switches:
    sflow += ' -- set bridge %s sflow=@sflow' % s
  print ' '.join([s.name for s in net.switches])
  quietRun(sflow)

def sendTopology(net,agent,collector):
  print "*** Sending topology"
  topo = {'nodes':{}, 'links':{}}
  for s in net.switches:
    topo['nodes'][s.name] = {'agent':agent, 'ports':{}}
  path = '/sys/devices/virtual/net/'
  for child in listdir(path):
    parts = re.match('(^.+)-(.+)', child)
    if parts == None: continue
    if parts.group(1) in topo['nodes']:
      # print('path is :' + path+child+'/ifindex')
      ifindex = open(path+child+'/ifindex').read().split('\n',1)[0]
      # print('then path: %s' % open(path+child+'/ifindex').read())
      # print('then path: %s' % open(path+child+'/ifindex').read().split('\n',1))
      # print('index is %s' % ifindex)
      topo['nodes'][parts.group(1)]['ports'][child] = {'ifindex': ifindex}
  i = 0
  for s1 in net.switches:
    j = 0
    for s2 in net.switches:
      if j > i:
        intfs = s1.connectionsTo(s2)
        for intf in intfs:
          s1ifIdx = topo['nodes'][s1.name]['ports'][intf[0].name]['ifindex']
          s2ifIdx = topo['nodes'][s2.name]['ports'][intf[1].name]['ifindex']
          linkName = '%s-%s' % (s1.name, s2.name)
          topo['links'][linkName] = {'node1': s1.name, 'port1': intf[0].name, 'node2': s2.name, 'port2': intf[1].name}
      j += 1
    i += 1
  print(topo)
  put('http://'+collector+':8008/topology/json',data=dumps(topo))


def newSendTopology(net, agent, collector):
  topo = {'nodes':{}, 'links':{}}
  children = []
  for s in net.switches:
    ip = s.worker.ip()
    topo['nodes'][s.name] = {'agent':ip, 'ports':{}}
  path = '/sys/devices/virtual/net/'
  for worker_name in net.cluster.hostname_to_worker:
    if worker_name != 'worker1':
      worker = net.cluster.get_worker(worker_name)
      childIntf = worker.run_cmd('ls '+ path)
      # print('%s path is %s' % (worker_name, childIntf))
      # children.append(childIntf)
      for interface in childIntf.split('\n'):
        print('interface is %s on worker %s' % (interface,worker_name))
        parts = re.match('(^.+)-(.+)', interface)
        if parts == None: continue
        if parts.group(1) in topo['nodes']:
          ifindex = worker.run_cmd('more '+ path + interface + '/ifindex').split('\n',1)[0]
          # print('ifindex is %s' % ifindex)
          topo['nodes'][parts.group(1)]['ports'][interface] = {'ifindex': ifindex}
    else:
      for interface in listdir(path):
        print('interface is %s on worker %s' % (interface,worker_name))
        parts = re.match('(^.+)-(.+)', interface)
        if parts == None: continue
        if parts.group(1) in topo['nodes']:
          ifindex = open(path+interface+'/ifindex').read().split('\n',1)[0]
          topo['nodes'][parts.group(1)]['ports'][interface] = {'ifindex': ifindex}

  for link in net.origtopology.links():
    info = net.origtopology.linkInfo(link[0], link[1])
    # print(link[0], link[1])
    print('link info is %s' % info)
    s1name = info.get('node1')
    s2name = info.get('node2')
    if net.node_to_worker[s1name] == net.node_to_worker[s2name]:
      s1port = s1name + '-eth' + str(info.get('port1'))
      s2port = s2name + '-eth' + str(info.get('port2'))
      # s1ifIdx = topo['nodes'][s1name]['ports'][s1port]['ifindex']
      # s2ifIdx = topo['nodes'][s2name]['ports'][s2port]['ifindex']
      linkName = '%s-%s' % (s1name, s2name)
      topo['links'][linkName] = {'node1': s1name, 'port1': s1port, 'node2': s2name, 'port2':s2port}

  # handle with tunnel between different workers
  for tunnel in net.tunnellookup:
    if net.node_to_worker[(str(tunnel[0]))].hn() != 'worker1':
      worker = net.node_to_worker[(str(tunnel[0]))]
      ifindex = worker.run_cmd('more '+ path + net.tunnellookup[tunnel] + '/ifindex').split('\n',1)[0]
      topo['nodes'][str(tunnel[0])]['ports'][net.tunnellookup[tunnel]] = {'ifindex': ifindex}
    else:
      ifindex = open(path + net.tunnellookup[tunnel]+'/ifindex').read().split('\n',1)[0]
      topo['nodes'][str(tunnel[0])]['ports'][net.tunnellookup[tunnel]] = {'ifindex': ifindex}

  added_tunnel = []
  for tunnel in net.tunnellookup:
    if net.tunnellookup[tunnel] not in added_tunnel:
      added_tunnel.append(net.tunnellookup[tunnel])
      s1name = str(tunnel[0])
      s2name = str(tunnel[1])
      s1port = net.tunnellookup[tunnel]
      s2port = net.tunnellookup[tunnel]
      linkName = '%s-%s' % (s1name, s2name)
      topo['links'][linkName] = {'node1': s1name, 'port1': s1port, 'node2': s2name, 'port2':s2port}

  print(topo)
  put('http://'+collector+':8008/topology/json',data=dumps(topo))

# For test
def tunnel_func(net, agent, collector):
  print('%s is in exp tunnel lookup' % net.tunnellookup)
  for tunnel in net.tunnellookup:
    print(net.node_to_worker[(str(tunnel[0]))].hn())
    print(type(tunnel))
    print(net.tunnellookup[tunnel])
  # for x in net.node_to_worker:
  # print(net.node_to_worker)
  # Other tested functions might be helpful
  # for intf in s.intfNames():
  #   link = intf
  #   print('link of %s includes %s' % (s.name, link))

def wrapper(fn,collector):
  def result( *args, **kwargs):
    res = fn( *args, **kwargs)
    net = args[0]
    (ifname, agent) = getIfInfo(collector)
    configSFlow(net,collector,ifname)
    sendTopology(net,agent,collector) 
    return res
  return result

setattr(Mininet, 'start', wrapper(Mininet.__dict__['start'], collector))
  
