#!/bin/bash

count=0
for i in `seq 0 .001 .010`;
do
  runCmd -c "python simulation.py 52 10 500000 $i 2 12 out/locations.p
  citydata/census.p out/gowalla_net results/sim$count results/map$count" -o
  results/out$count.txt -e results/out$count.err --nowait
done
