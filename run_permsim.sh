#!/bin/bash

count=0
for p in `seq 0.019 .001 .022`; do
    for t in `seq 1 1 50`; do
        ./runCmd -c "python permute_sim.py 300000000 $p out/contact_dist.out citydata/states.p citydata/census.p out/trans_prob.csv out/city_list.p google_data/50states04-12.csv permresults/matrix$count-$t" -e permerr/out$count-$t.err -o permoutput/out$count-$t --nowait
    done
    let count+=1
done
