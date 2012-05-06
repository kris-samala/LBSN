#!/bin/bash

count=1
for p in `seq 0.015 .001 .025`; do
    for t in `seq 1 1 10`; do
        ./runCmd -c "python faster_sim.py 10000000 $p out/contact_dist.out citydata/states.p citydata/census.p out/trans_prob.csv out/city_list.p results2/matrix$count-$t" -e err2/out$count-$t.err -o output2/out$count-$t --nowait
    done
    let count+=1
done
