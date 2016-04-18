#!/usr/bin/python
import sys
def main(argv):
	if len(argv)!=2:
		print "./bernoulli_model.py IPC_single_warp No_warp_to_predict"
		exit(0)
	#input is IPC-single warp + number of warps to model
	new_IPC =  1-(1-float(argv[0]))**int(argv[1])
	print new_IPC
if __name__ == '__main__':
    main(sys.argv[1:])	
