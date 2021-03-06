#!/bin/bash

count=0
for p in `seq 0.019 .001 .025`; do
    for t in `seq 1 1 10`; do
        ./runCmd -c "python faster_sim.py 300000000 $p out/school_contacts.p citydata/states.p citydata/census.p out/trans_prob.csv out/city_list.p google_data/50states04-12.csv results/matrix$count-$t" -e err/out$count-$t.err -o output/out$count-$t --nowait
    done
    let count+=1
done
