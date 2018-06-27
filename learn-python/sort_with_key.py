
        
ips = [
	'10.0.0.5',
	'10.5.3.1',
	'192.168.11.10',
	'2.2.2.2',
	'100.0.0.1',
	'20.3.2.4'
	]

def getKey(item):
	return tuple(int(part) for part in item.split('.'))

def sort_ips(iplist):
	return sorted(ips, key=getKey)

print(sort_ips(ips))


