import re

'''
HTTP URL validator

You can add other protocols by modifiying schema.
HTTP paths may include almost anything. So I used (.) as the regular expression.
You can imit it by enabling the previous commented line.
You can see some new weird TLDs. Add them to the oTLDs.

Just copy the validateURL function and feed it with your urls.
The main is to give you an example.

-simsek

'''

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

if __name__ == "__main__":

	urls = ["http://en.wikipedia.org/wiki/Levenshtein_distance", "http://www.google.comtr"]

	for url in urls:
		if validateUrl(url):
			print url + " is valid"
		else:
			print url + " is not valid"

