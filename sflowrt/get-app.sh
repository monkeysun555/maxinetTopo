#!/bin/sh

usage ()
{
  echo "Usage   : $0 <github-user> <github-project>"
  echo "Example : $0 sflow-rt dashboard-example"
  echo "Catalog : http://sflow-rt.com/download.php#applications"
  exit
}

if [ "$#" -ne 2 ]; then
  usage
fi
cd `dirname $0`
java -jar lib/sflowrt.jar get-app github $1 $2
cd -
echo ""
echo "==================================="
echo "Restart sflow-rt to run application"
echo "==================================="
