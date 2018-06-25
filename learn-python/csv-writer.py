import csv

cols = ['No', 'Name', 'State', 'Score']

rows = [ ['13', 'Joe', 'CA', '5'],
         ['20', 'Sue', 'CA', '1'],
         ['34', 'Barbara', 'TX', '3'],
         ['32', 'Bob', 'WA', '1' ],
         ['41', 'Alice', 'NY', '8'],
         ['30', 'John', 'NV', '9']]

with open('out.csv', 'w') as csvfile:
	csvwriter = csv.writer(csvfile)

	csvwriter.writerow(cols)
	csvwriter.writerows(rows)
