import re
import urllib
import json
import whois
import tldextract
import pylev
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urlparse import urlparse
from dateutil import relativedelta

NEGATIVE_STR = "no"		# which means not phishing
POSITIVE_STR = "yes"	# which means phishing

K_CONFIDENCE = 2
DELIMITERS = ['.', '-', '_']
MIMIC_MAP = {
	'a': '@',
	'i': '!',
	'o': '0',
	'B': '3',
	'1': 'I'
}

def bs_kdistance(str1, str2, k):
	# Normalize mimics
	for key, val in MIMIC_MAP.iteritems():
		str1 = str1.replace(val, key)
		str2 = str2.replace(val, key)

	# Normalize delimiters
	for d in DELIMITERS:
		str1 = str1.replace(d, '')
		str2 = str2.replace(d, '')

	# similarity around k-neighborhood
	s = 0
	for i in range(len(str1)):
		for j in range(k):
			if i + j < len(str2):
				rindex = i + j
				if str1[i] == str2[rindex]:
					s += 1
					break

			if len(str2) > i - j > 0:
				lindex = i - j
				if str1[i] == str2[lindex]:
					s += 1
					break

	d = len(str1) - s

	return d

# Functions to prepare dataset

# Search for domain pattern in the path, the query or the host part
def embedded_domain(hostname, url_path, url_query):
	PATH_DOMAIN_REGEX = "[a-zA-Z0-9-]{1,64}(\.|-|_|,).{2,3}(?![a-zA-Z0-9])"
	HOST_DOMAIN_REGEX = "[a-zA-Z0-9]{1,64}(\.|-|_|,)[a-zA-Z]{2,3}((\.|-|_|,)[a-zA-Z0-9]{1,64})*[a-zA-Z]{2,3}"
	if re.search(HOST_DOMAIN_REGEX, hostname):
		return 1
	elif re.search(PATH_DOMAIN_REGEX, url_path) or re.search(PATH_DOMAIN_REGEX, url_query):
		return 0
	else:
		return -1

def url_contains_targeted_brand(tokenized_url):
	fd = open('brands.txt')

	for line in fd:
		for token in tokenized_url:
			line = line.lower().strip('\n').strip('\t')
			if len(line) > 3:
				d = bs_kdistance(token, line, 3)
			else:
				d = 1

			if line in token or d == 0:
				return 1

	return -1

# Check whether hostname is an ip address
def hostname_is_ip_address(url_hostname):
	if re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", url_hostname):
		return 1
	else:
		return -1

def number_of_dots_in_url(nod):
	if nod < 3:			# legitimate
		return -1
	elif nod == 3:		# neutral
		return 0
	else:
		return 1		# phishing

def hostname_has_dash(url_hostname):
	if url_hostname.count('-') > 1:
		return 1
	else:
		return -1

def url_has_dictionary_word(tokenized_url):
	fd = open('dictionary.txt')

	for line in fd:
		for token in tokenized_url:
			line = line.lower().strip('\n').strip('\t')
			if len(line) > 3:
				d = bs_kdistance(token, line, 3)
			else:
				d = 1

			if line in token or d == 0:
				return 1

	return -1

def url_has_at(url):
	if '?' in url:
		u = url.split('?')
		if '@' in u[0]:
			return 1
		else:
			return -1
	else:
		if '@' in url:
			return 1
		else:
			return -1 

def http_in_hostname(url_hostname):
	if "http" in url_hostname:
		return 1
	else:
		return -1

def age_of_domain_is_young(domain):
	whois_info = whois.query(str(domain))
	if whois_info.creation_date:
		current_date = datetime.now()
		created_on = whois_info.creation_date
		diff = relativedelta.relativedelta(current_date, created_on)
		age = 12*diff.years + diff.months

	if age < 5:
		return 1
	else:
		return -1

def redirecting_url(url):
	REGEX = "\/\/http\:\/\/"

	if re.search(REGEX, url):
		return 1
	else:
		return -1

def use_https(schema):
	if schema == 'https':
		return -1
	else:
		return 1

def req_ext_url(url, domain):
	try:
		html_doc = requests.get(url, timeout=(5, 50))
	except:
		return 99   # Eliminate those lines

	soup = BeautifulSoup(html_doc.content, 'html.parser')

	refs1 = soup.find_all('a')

	ext = 0
	inter = 0
	
	for link in refs1:
		href = repr(link.get('href'))
		if 'http://' in href or 'https://' in href:
			if isValidUrl(href):
				parsed_url = parseUrl(href)
				parsed_domain = parsed_url['tld'] + '.' + parsed_url['suffix']
				if domain != parsed_domain:
					ext += 1
				else:
					inter += 1
			else:
				ext += 1
		else:
			inter += 1

	imgs = soup.find_all('img')
	scrs = soup.find_all('script')
	refs2 = imgs + scrs

	for link in refs2:
		href = repr(link.get('src'))
		if 'http://' in href or 'https://' in href:
			if isValidUrl(href):
				parsed_url = parseUrl(href)
				parsed_domain = parsed_url['tld'] + '.' + parsed_url['suffix']
				if domain != parsed_domain:
					ext += 1
				else:
					inter += 1
			else:
				ext += 1
		else:
			inter += 1

	ref_count = len(refs1) + len(refs2)

	if ref_count > 0:
		if (ext/ref_count)*100 > 20:
			return 1
		else:
			return -1
	else:
		return -1

def isValidUrl(url):
	schema = "(http(s)?:\/\/)?"
	subdomain = "([a-zA-Z0-9_-]+\.)+"
	tTLDs = "(com|net|org|edu|int|gov|mil)"
	cTLDs = "ac|ad|ae|af|ag|ai|al|am|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cw|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|za|zm|zw"
	oTLDs = "info|news"
	TLDs = tTLDs + "|" + cTLDs + "|" + oTLDs
	IP_addr = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
	localhost = "(localhost)"
	port = "(:[1-9][0-9]*)?"
	#SPECIAL_URL_CHARS = "\?=_\-\.%&#\:;,\/\+@\~\(\)!\$ "
	#path = "/([a-zA-Z0-9" + SPECIAL_URL_CHARS + "])*"
	path = "(/(.)*)*"
	URL_REGEX = "^" + schema + "(" + subdomain + TLDs + "|" + IP_addr + "|" + localhost + ")" + port + path + "$"

	if re.search(URL_REGEX, url):
		return 1
	else:
		return 0

def parseUrl(url):
	o = urlparse(url)

	try:
		tld = tldextract.extract(o.netloc)
	except:
		return {}

	try:
		nod = o.hostname.count('.')
	except:
		nod = 0

	parsed_url = {
		'schema': o.scheme,
		'subdomain': tld.subdomain,
		'tld': tld.domain,
		'suffix': tld.suffix,
		'hostname': o.hostname,
		'nod': nod,
		'port': o.port, 
		'path': o.path,
		'query': o.query
	}

	return parsed_url

def genFeatureMatrix(url, response):
	parsed_url = parseUrl(url)
	tokenized_url = url.replace('.', '/').replace('?', '/').replace('&', '/').replace('-', '/').replace('_', '/').split('/')

	domain = parsed_url['tld'] + '.' + parsed_url['suffix']
	url_hostname = parsed_url['hostname']
	url_path = parsed_url['path']

	x1 = embedded_domain(url_hostname, url_path, parsed_url['query'])
	x2 = hostname_is_ip_address(url_hostname)
	x3 = number_of_dots_in_url(parsed_url['nod'])
	x4 = hostname_has_dash(url_hostname)
	x5 = url_has_dictionary_word(tokenized_url)
	x6 = http_in_hostname(url_hostname)
	x8 = url_contains_targeted_brand(tokenized_url)
	x9 = redirecting_url(url)
	#x10 = use_https(parsed_url['schema'])
	x11 = req_ext_url(url, domain)

	print '"' + url + '",' + str(x1) + ',' + str(x2) + ',' + str(x3) + ',' + str(x4) + ',' + str(x5) + ',' + str(x6) + ',' + str(x8) + ',' + str(x9) + ',' + str(x11) + ',' + response

	return 0

def phishtank():

	PHISHTANK_API = 'http://data.phishtank.com/data/online-valid.json'

	response = urllib.urlopen(PHISHTANK_API)

	data = json.load(response)   

	for item in data:
		if "2017-10" in item['submission_time']:
			url = item['url'].strip().lower()
			if isValidUrl(url):
				genFeatureMatrix(url, POSITIVE_STR)


def openphish():

	#OPEN_API = 'https://openphish.com/feed.txt'
	#response = urllib.urlopen(OPEN_API)

	SAFE_FILE = 'openphish.txt'
	fd = open(SAFE_FILE)

	for line in fd:
		url = line.strip().lower()
		if isValidUrl(url):
			genFeatureMatrix(url, POSITIVE_STR)


def safeurls():

	SAFE_FILE = 'lurl.txt'

	fd = open(SAFE_FILE)

	for line in fd:
		url = line.strip().lower()
		if isValidUrl(url):
			genFeatureMatrix(url, NEGATIVE_STR)


if __name__ == "__main__":
	print "url,embedded_domain_in_path,ip_address,number_of_dots,host_has_dash,dictionary_word,http_in_hostname,targeted_brand,redirecting url,ext url,result"

	#phishtank()
	openphish()
	safeurls()







