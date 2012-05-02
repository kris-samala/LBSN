#!/bin/bash

count=1
for p in `seq 0.01 .01 .4`; do
    for t in `seq 1 1 10`; do
        ./runCmd -c "python sim.py 300000000 $p out/contact_dist.out citydata/states.p citydata/census.p out/trans_prob.csv out/city_list.p results/matrix$count-$t" -e err/out$count-$t.err --nowait
    done
    let count+=1
done
