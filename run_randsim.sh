#!/bin/bash

count=0
for p in `seq 0.019 .001 .022`; do
    for t in `seq 1 1 50`; do
        ./runCmd -c "python random_sim.py 300000000 $p out/school_contacts.p citydata/states.p citydata/census.p out/trans_prob.csv out/city_list.p google_data/50states04-12.csv randresults/matrix$count-$t" -e randerr/out$count-$t.err -o randoutput/out$count-$t --nowait
    done
    let count+=1
done
