#!/bin/bash

count=1
for p in `seq 0.01 .01 .01`; do
    for k in `seq 1 1 1`; do
        for s in `seq .5 .5 .5`; do
            for t in `seq 1 1 10`; do
                ./runCmd -c "python sim.py 100000000 $p $k $s citydata/states.p citydata/census.p out/gowalla_net out/trans_prob.csv out/city_list.p results/matrix$count-$t" -e err/out$count.err --nowait
            done
            let count+=1
        done
    done
done
