#!/bin/bash

count=50
for p in `seq 0.019 .001 .22`; do
    for t in `seq 1 1 20`; do
        ./runCmd -c "python sim.py 10000000 $p out/contact_dist.out citydata/states.p citydata/census.p out/trans_prob.csv out/city_list.p results/matrix$count-$t" -e err/out$count-$t.err -o output/out$count-$t --nowait
    done
    let count+=1
done
