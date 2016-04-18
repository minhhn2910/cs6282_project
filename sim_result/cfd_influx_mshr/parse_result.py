#!/usr/bin/python
import sys

def main(argv):
	#directory path is in argv[0]
	cpi_file = argv[0] + "/general.stat.out"
	mem_file = argv[0] + "/memory.stat.out"
	insts_file = argv[0] + "/inst.stat.out"
	total_cycles = 0
	total_inst = 0
	mem_req = 0
	mem_inst = 0
	avg_mem_lat = 0.0
	#open general.stat.out
	f = open(cpi_file,"r")
	for line in f:
		if "CYC_COUNT_TOT" in line:
			array = line.split()
			total_cycles = int(array[1])
		elif "UOP_COUNT_TOT" in line:
			array = line.split()
			#print array
			total_inst = int(array[1])
	f1 = open(mem_file,"r")
	for line in f1:
		if "AVG_MEMORY_LATENCY" in line:
			array = line.split()
			avg_mem_lat = float(array[2])
		elif "TOTAL_MEMORY" in line and "_MERGE" not in line:
			#print line
			#print array
			array = line.split()
			mem_req = int(array[1])
	f2 = open(insts_file, "r")
	for line in f2:
		if "OP_CAT_GPU_MEM_LD_GM" in line:
			array = line.split()
			mem_inst = int(array[1])
	print "%d, %d, %d, %d, %f, %f\n" %(total_inst, total_cycles, mem_req, mem_inst, avg_mem_lat, float(total_inst)/float(total_cycles))

if __name__ == '__main__':
    main(sys.argv[1:])	
