#!/bin/bash

count=1
for p in `seq 0.01 .01 .5`; do
    for g in `seq .5 .5 3`; do
        for s in `seq .1 .1 1`; do
            ./runCmd -c "python simulation.py 52 1 500000 $p $g $s out/locations.p citydata/census.p out/gowalla_net results/sim$count results/map$count" -o results/out$count.txt -e results/out$count.err --nowait
            let count+=1
        done
    done
done
