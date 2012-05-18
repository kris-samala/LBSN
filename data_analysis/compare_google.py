import sys
import fileinput
import csv
import operator
import numpy as np
import scipy.spatial.distance as sd

#python compare_google.py [google_all] [avg-$count-norm] scores$count

google = []
matrix = []

infile = sys.argv[2]

google_reader = csv.reader(open(sys.argv[1], 'rb'), delimiter=',')
matrix_reader = csv.reader(open(infile, 'rb'), delimiter=',')
results = open(sys.argv[3], 'wb')

weeks = 52

def compute_score(m, g):
    sum = 0
    for i in range(m.shape[1]):
        sum += sd.euclidean(m[:,i],g[:,i])

    score = sum/float(m.shape[1])

    return score

#store google data
for row in google_reader:
    row = [(int(x) if x else 0) for x in row]
    google.append(np.array(row))

google = np.array(google)

gnorm = []
for i in range(google.shape[0]):
    row = []
    for j in range(google.shape[1]):
        colsum = np.sum(google[:,j])
        if colsum > 0:
            normval = google[i,j] / float(colsum)
        else:
            normval = 0.0
        row.append(normval)
    gnorm.append(row)
gnorm = np.array(gnorm)

for row in matrix_reader:
    row = [(float(x) if x else 0) for x in row]
    matrix.append(np.array(row))

matrix = np.array(matrix)

scores = {}
for i in range(gnorm.shape[0]-weeks):
    scores[infile+'-'+str(i)] = compute_score(matrix, gnorm[i:i+weeks])

sorted_scores = sorted(scores.iteritems(), key=operator.itemgetter(1))

for name,score in sorted_scores:
    results.write(name+':'+str(score)+'\n')

results.close()



