#!/bin/bash

count=1
for p in `seq 0.31 .01 .4`; do
    for t in `seq 1 1 10`; do
        python faster_sim.py 100000 $p out/contact_dist.out citydata/states.p citydata/census.p out/trans_prob.csv out/city_list.p results2/matrix$count-$t > output2/out$count-$t
    done
    let count+=1
done
