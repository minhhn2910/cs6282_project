#!/usr/bin/python
import sys
import math
#use to build the transition matrix
num_requests = 0
def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)
#matrix multiplication
def matrixmult (A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    if cols_A != rows_B:
            print "Cannot multiply the two matrices. Incorrect dimensions."
            return
    C = [[0 for row in range(cols_B)] for col in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

def get_P_and_M(stat_file,N):
    global num_requests
    #p is the prob that a thread becomes stall
    #M is the length of the stall event in cycles
    f = open(stat_file,"r")
    array = f.read().replace("\n","").replace(" ","").split(",")
    #print array
    total_cycles = int(array[1])
    total_insts = int(array[0])
    average_mem_delay = float(array[4])
    num_requests = int(array[2])
    total_stall_events = int(array[3])
    #total_stall_events = (total_cycles - total_insts)/average_mem_delay
    P = float(total_stall_events)/total_insts
    # each instruction need 1 cycle to execute, to simplify the input gathering task
    M = average_mem_delay
    #M = float(total_cycles - total_insts)/total_stall_events
    return P,M

def build_transition_matrix(input_file, N):
    #N is the number of warps we want to predict the performance
    P,M = get_P_and_M(input_file,N)
    print "got P=%f and N=%f"%(P,M)
    trans_matrix = []
    for i in range(N+1):
        row = [0]*(N+1)
        for j in range(N+1):
            if (j>i): # 1 more thread becomes stall
                if (j == i+1):
                    row[j] = P*((1-1/M)**i)
            elif (j == i): #remains in the current state
                if(i == 0):
                    row[j] = 1-P
                elif (i == N):
                    row[j] = (1-1/M)**i
                else:
                    row[j] = (1-P)*((1-1/M)**i) + P*i*(1/M)*((1-1/M)**(i-1))
            else: # 1 or more threads exit the stall event
                if (i == N):
                    row[j] = nCr(i,i-j)*((1/M)**(i-j))*(1-1/M)**j
                elif (j == 0):
                    row[j] = (1-P)*(1/M)**i
                else:
                    row[j] = (1-P)*nCr(i,i-j)*((1/M)**(i-j))*((1-1/M)**j) + P*nCr(i,i-j+1)*((1/M)**(i-j+1))*((1-1/M)**(j-1))
        trans_matrix.append(row)
    #print trans_matrix
    return trans_matrix

def markov_solver(trans_matrix):
    N = len(trans_matrix[0]) #no of states
    for i in range(N): #sanity check, sum of each row = 1
        if abs(sum(trans_matrix[i])-1)> 1e-5:
            print "row %d not equal 1"%(i)
            print trans_matrix[i]
    array = [[0.0]*N]
    array[0][0] = 1.0
    err = 1.0
    #loop = 0
    while(err > 1e-4):
        #loop +=1
        array_temp = matrixmult(array, trans_matrix)
        err = 0.0
        for i in range(N):
            if abs(array_temp[0][i] - array[0][i]) > err:
                err = abs(array_temp[0][i] - array[0][i])
        array = array_temp
    #print loop
    #print array
    return array
def main(argv):
    if len(argv)!=2:
        print "./markov_model.py input_file_1_warp #No_warp_to_predict"
        exit()
    trans_matrix = build_transition_matrix(argv[0], int(argv[1]))
    state_prob = markov_solver(trans_matrix)
    arrivals = 0.0
    for i in range(len(state_prob[0])):
        arrivals += (len(state_prob[0])-1 - i)*state_prob[0][i]*num_requests
        #state i, i threads are stalling => N-i threads are issuing MSHR requests
    print "State probabilities"
    print state_prob
    print "predicted IPC %f"%(1.0-state_prob[0][len(state_prob[0])-1])

    print "predicted arrivals of mshr request %f"%(arrivals)

if __name__ == '__main__':
    main(sys.argv[1:])
