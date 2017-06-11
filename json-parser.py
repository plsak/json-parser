#!/usr/bin/python
# By Martin Plsek, plsek.martin@gmail.com
# Utility to parse and print JSON data from FILE, URL or STDIN
# v0.13, 2017-06-11, Initial
#
my_ver = '0.13'

# Import modules
import sys, getopt, signal, re, json, urllib2

#------------------------------------------------------------------------------#
# Functions

# Main function, rest invoked from here
def main(argv):
	json_file = ''
	json_url = ''
	json_stdin = False
	verbose_run = False

	# Get options and catch getopt exceptions (invalid opt)
	try:
		opts, args = getopt.gnu_getopt(argv,"hvf:u:s")
	except getopt.GetoptError as ex:
		print >> sys.stderr, "[ERROR] %s: %s" % (ex.args, my_usage)
		sys.exit(2)

	# Parse options, have to process all to delete all 'opt' and 'arg' from argv - will use non-option params as well
	for opt, arg in opts:
		argv.remove(opt)
		if (arg != '') : argv.remove(arg)

		if opt == '-h':
			print "%s %s" % (my_nm, my_usage)
			sys.exit(0)
		elif opt == '-v':
			verbose_run = True
		elif opt == '-f':
			json_file = arg
		elif opt == '-u':
			json_url = arg
		elif opt == '-s':
			json_stdin = True

	# Get json_data - highest priority FILE, then URL, then STDIN, exit if nothing is set
	if json_file != '':
		json_data = json_from_file(json_file, verbose_run)
	elif json_url != '':
		json_data = json_from_url(json_url, url_timeout, verbose_run)
	elif json_stdin:
		json_data = json_from_stdin(verbose_run)
	else:
		print >> sys.stderr, "%s %s" % (my_nm, my_usage)
		sys.exit(2)

	# Process json_data
	process_json_data(json_data, argv)

# Function to read from FILE
def json_from_file(file, verbose):
	if (verbose): print >> sys.stderr, "%-19s: '%s'" % ('Will read from FILE', file)
	try:
		with open(file) as fh:
			data = fh.read()
	except Exception as ex:
		print >> sys.stderr, "[ERROR] Failed to read from '%s': `%s' -> %s" % (file, type(ex).__name__, ex.args)
		sys.exit(1)

	return data

# Function to read from URL
def json_from_url(url, url_timeout, verbose):
	if (verbose): print >> sys.stderr, "%-19s: '%s'" % ('Will read from URL', url)
	try:
		data = urllib2.urlopen(url, timeout = url_timeout)
	except Exception as ex:
		print >> sys.stderr, "[ERROR] Failed to read from '%s': `%s' -> %s" % (url, type(ex).__name__, ex.args)
		sys.exit(1)

	return data.read()

# Function to read from STDIN
def json_from_stdin(verbose):
	if (verbose): print >> sys.stderr, "Will read from STDIN"
	try:
		data = sys.stdin.read()
	except Exception as ex:
		print >> sys.stderr, "[ERROR] Failed to read from STDIN: `%s' -> %s" % (type(ex).__name__, ex.args)
		sys.exit(1)
	return data

# Function to parse and print json_data
def process_json_data(data, argv):
	json_parsed = ''
	try:
		json_parsed = json.loads(str(data))
	except Exception as ex:
		print >> sys.stderr, "[ERROR] Failed to parse data: `%s' -> %s" % (type(ex).__name__, ex.args)
		sys.exit(1)

	if len(argv) > 0:
		for key in argv:
			try:
				if re.search(r'list', str(type(json_parsed))):
					json_parsed = json_parsed[int(key)]
				else:
					json_parsed = json_parsed[str(key)]
			except Exception as ex:
				print >> sys.stderr, "[ERROR] Failed for KEY '%s' (confirm structure): `%s' -> %s" % (key, type(ex).__name__, ex.args)
				sys.exit(1)

	print json.dumps(json_parsed, indent=4, sort_keys=True)

# Handle selected signals
def sig_handler(signum, stack):
	print >> sys.stderr, "[ERROR] Signal '%s' detected, exiting!" % (str(signum))
	sys.exit(1)

#------------------------------------------------------------------------------#
# Code processing

# Set basic variables
my_nm = '[json-parser, v' + my_ver + ']' 
my_usage = sys.argv[0] + ' [-h|-v] <-f FILE|-u URL|-s (read STDIN)> [KEY1] [KEY2] ...'
url_timeout = 15

# Run code if executed as main program
if __name__ == "__main__":
	signal.signal(signal.SIGHUP, sig_handler)
	signal.signal(signal.SIGINT, sig_handler)
	signal.signal(signal.SIGTERM, sig_handler)
	main(sys.argv[1:])

