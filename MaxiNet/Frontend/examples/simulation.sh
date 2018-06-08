# pkill screen
# cd ~/pox
# screen -d -m -S PoxScr ./pox.py forwarding.l2_learning
# screen -d -m -S MaxiNetFrontend MaxiNetFrontendServer
# screen -d -m -S MaxiNetWorker sudo MaxiNetWorker

# sleep 1
# ssh maxinet@192.168.123.2 'screen -d -m -S MaxiNetWorker sudo MaxiNetWorker && exit'
# sleep 1
# ssh maxinet@192.168.123.3 'screen -d -m -S MaxiNetWorker sudo MaxiNetWorker && exit'

cd ~/MaxiNet/MaxiNet/Frontend/examples/
sudo mn -c
python ./test.py
