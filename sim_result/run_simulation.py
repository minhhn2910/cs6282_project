#!/usr/bin/python
#this file runs simulation on 1 core/ 1 thread to collect statistics data for modeling, will merge later
import sys
def main(argv):
	#argv[0] is log file name 
	f = open("trace_file_list", "w")
	f.write('1\n') #single kernel, we cant model multple kernels sharing 1 gpu now
	f.write(argv[0] + '\n')
	f.close()
if __name__ == '__main__':
	main(sys.argv[1:])
