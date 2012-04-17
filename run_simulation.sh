#!/bin/bash

count=1
for p in `seq 0.001 .001 .1`; do
    for g in `seq 1 1 5`; do
        for s in `seq .01 .01 1`; do
            ./runCmd -c "python simulation.py 52 1 100000 $p $g $s out/locations.p citydata/census.p out/gowalla_net results/sim$count results/map$count" -o results/out$count.txt -e results/out$count.err --nowait
            let count+=1
        done
    done
done
