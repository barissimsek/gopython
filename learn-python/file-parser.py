import re

with open('/etc/passwd', 'r') as fd:
	for line in fd:
		if re.search('^.*:.*:.*:.*:.*:.*:.*$', line):
			parsed_line = line.split(':')
			#print(parsed_line[0] + ' ' + parsed_line[5])
			print ', '.join(parsed_line)


