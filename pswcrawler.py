'''
	PSWCrawler: Python Simple Web Crawler
	v1.0.0
	Made by Safflower (fuzzer@nate.com)
'''


import urllib.parse, urllib.request
import re
import argparse


target_url_list = []

def explore(target_url, depth, padding = ''):
	target_url_list.append(target_url)

	url_pattern = '^' \
		'(http|https)://' \
		'([^/]+)' \
		'(/?[^\?#]*)' \
		'(\?*[^#]*)' \
		'(#*.*)' \
		'$'

	target = re.findall(url_pattern, target_url, re.I + re.S);
	if len(target) == 1:
		target = target[0]
		target_count = len(target)
	else:
		print(padding + '[!] Skip: Not Supported URL Type')
		print(padding + ' (%s)' % target_url)
		return

	target_protocol = target[0]
	target_host = target[1]
	target_path = target[2]
	if not target_path:
		target_path = '/'
	target_query = target[3]
	target_hash = target[4]

	try:
		req = urllib.request.Request(target_url)
		res = urllib.request.urlopen(req)
		contents = str(res.read())

	except Exception as err_msg:
		print(padding + '[!] %s' % err_msg)
		print(padding + ' (%s)' % target_url)
		return

	href_list = re.findall('\shref\s*=\s*["|\'](.*?)["|\']', contents, re.I)
	href_list_count = len(href_list)

	print(padding + '[*] Find: Processing %s Links' % href_list_count)
	print(padding + ' (%s)' % target_url)

	temp_url_list = []
	for href in href_list:

		if href in temp_url_list:
			continue

		elif re.match('^(mailto|tel|data|ssh|ftp|sftp|file|javascript|urn):(.*)$', href, re.I + re.S):
			continue

		elif href.startswith('//'):
			href = 'http:' + href

		elif href.startswith('/'):
			href = target_protocol + '://' + target_host + href

		elif href.startswith('./'):
			if target_path.endswith('/'):
				href = target_protocol + '://' + target_host + target_path + href[2:]
			else:
				href = target_protocol + '://' + target_host + target_path + href[1:]

		elif not re.match(url_pattern, href):
			if target_path.endswith('/'):
				href = target_protocol + '://' + target_host + target_path + href
			else:
				href = target_protocol + '://' + target_host + target_path + '/' + href

		print(padding + '%s' % href)
		temp_url_list.append(href)

		if depth and not href in target_url_list:
			explore(href, depth - 1, padding + '\t')


def main():
	parser = argparse.ArgumentParser(description = 'Python Simple Web Crawler')
	parser.add_argument('url', type = str, help = 'URL of target website (e.g. http://example.com/)')
	parser.add_argument('depth', type = int, help = 'Explore depth (e.g. 0, 1, 2, ...)')
	args = parser.parse_args()

	explore(args.url, args.depth)


if __name__ == '__main__':
	main()	


# EOF