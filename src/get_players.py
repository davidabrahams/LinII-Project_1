import csv

with open('../data/projections.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	if (row[0] == 'Player Name '):
    		pass
    	else:
        	print row