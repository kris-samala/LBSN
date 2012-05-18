import sys
import fileinput
import glob
import numpy as np
import csv

#python compute_avg.py matrix$count n avg_matrix-$count

matrices = []
basename = sys.argv[1]
n = int(sys.argv[2])
avgwriter = csv.writer(open(sys.argv[3]+'.csv', 'wb'), delimiter=',')
normwriter = csv.writer(open(sys.argv[3]+'-norm.csv', 'wb'), delimiter=',')
max_col = 50
max_row = 52
days = 7

for i in range(1,n):
    filenames = glob.glob(basename+'-'+str(i)+'_'+'*')
    matrix = []
    for line in fileinput.input(filenames[0]):
        line = line.replace('[','').replace(']','').replace(' ','').strip()
        vals = np.array([float(x) for x in line.split(',')])
        matrix.append(vals)
    matrix = np.array(matrix)
    weekly_matrix = []
    week = np.array([0]*max_col)
    for row in range(matrix.shape[0]):
        week = week + matrix[row]
        if row % days == 0:
            weekly_matrix.append(week)
            week = np.array([0]*max_col)
    matrices.append(np.array(weekly_matrix[:max_row]))
matrices = np.array(matrices)

sum = np.array([[0]*max_col]*max_row)

for m in matrices:
    sum += m

avg = sum/matrices.shape[0]

for a in avg:
    avgwriter.writerow(a)

norm = []
for i in range(avg.shape[0]):
    row = []
    for j in range(avg.shape[1]):
        colsum = np.sum(avg[:,j])
        if colsum > 0:
            normval = avg[i,j] / float(colsum)
        else:
            normval = 0.0
        row.append(normval)
    norm.append(row)
norm = np.array(norm)
for a in norm:
    normwriter.writerow(a)


