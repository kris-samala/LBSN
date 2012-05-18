#!/bin/bash

count=0
for p in `seq 0.019 .001 .025`; do
    for t in `seq 1 1 10`; do
        ./runCmd -c "python faster_sim3.py 300000000 $p out/contact_dist.out citydata/states.p citydata/census.p out/trans_prob.csv out/city_list.p google_data/50states04-12.csv results5/matrix$count-$t" -e err5/out$count-$t.err -o output5/out$count-$t --nowait
    done
    let count+=1
done
