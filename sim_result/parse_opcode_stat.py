#!/usr/bin/python
#this file calculate the total number of instruction per warp
import sys
def main(argv):
	#argv[0] is log file name 
	f = open(argv[0], "r")
	sum = 0
	for line in f:
		args = line.split()
		sum  += int(args[1])
	print "from log " + str(sum)
	#argv[1] is debug file 
	f1 = open (argv[1], "r")
	sum_debug = 0
	for line in f1:
		if "is_fp" in line:
			sum_debug += 1
	print "from debug " + str(sum_debug)
if __name__ == '__main__':
	main(sys.argv[1:])
