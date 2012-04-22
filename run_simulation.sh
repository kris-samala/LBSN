#!/bin/bash

count=1
for p in `seq 0.001 .001 .001`; do
    for k in `seq 1 1 1`; do
        for s in `seq .1 .1 .1`; do
            ./runCmd -c "python simulation.py 100000000 $p $k $s citydata/states.p citydata/census.p out/gowalla_net results/matrix$count" -e err/out$count.err --nowait
            let count+=1
        done
    done
done
