#!/bin/bash

count=10
for p in `seq 0.019 .001 .022`; do
    for t in `seq 1 1 10`; do
        ./runCmd -c "python faster_sim4.py 300000000 $p out/school_contacts.p citydata/states.p citydata/census.p out/trans_prob.csv out/city_list.p google_data/50states04-12.csv results4/matrix$count-$t" -e err4/out$count-$t.err -o output4/out$count-$t --nowait
    done
    let count+=1
done
