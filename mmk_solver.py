#!/usr/bin/python
import sys
import math

def mmk_solver(num_servers, arrival_rate, service_rate):
    #compute P0 (prob 0 job at the queue)
    sum_temp = 0.0
    p_temp = arrival_rate / service_rate
    p = arrival_rate/(service_rate*num_servers)
#    if p >= 1 :
#        print "wrong p"
#        return
    for i in range(num_servers):
        sum_temp += (p_temp**i)/math.factorial(i)
    sum_temp += ((p_temp)**num_servers/math.factorial(num_servers))/(1-p)
    P_0 = sum_temp**(-1)
    #P_queueing = P(k>num_servers)
    P_queueing = (((p_temp**num_servers)/math.factorial(num_servers))/(1-p))*P_0
    #compute only the waiting time in queue, the service_time is included in IPC model with mem_latency already
    W_time = (P_queueing*p)/(arrival_rate*(1-p))
    return W_time

def main(argv):
    if len(argv)!=3:
        print "./MMk_solver.py k_servers arrival_rate service_rate"
        exit()
    W_time = mmk_solver(int(argv[0]), float(argv[1]),float(argv[2]))
    print "waiting time on the MSHR queue %f"%(W_time)
if __name__ == '__main__':
    main(sys.argv[1:])
