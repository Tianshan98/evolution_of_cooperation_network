import networkx as nx
import random
import copy
from network_helper import*
from constant import*

#small world network
f = open('sw_test_result.txt', 'w+')
f.write('probability of rewiring an edge:')
f.write('{}'.format(P))
f.write('\n')

#omega = nx.omega(G)
#f.write('omega:')
#f.write('{}'.formate(omega))
#f.write('\n')
#print(omega)

for experiment in range(20):
    #small world network
    #n: the number of nodes
    #k: each node is connected to k nearest neighbours
    #p: probability of rewiring in each edge
    G = nx.watts_strogatz_graph(n = number_of_nodes, k = K, p = P)
    
    print(experiment)
    f.write('experiment number:')
    f.write('{}'.format(experiment))
    f.write('\n')
    
    init_all_nodes(G)
    counter = 0
    
    while True:
        counter += 1
        for i in range(number_of_nodes):
            G.node[i]['agent'].game()
               
        for i in range(number_of_nodes):
            G.node[i]['agent'].update_strategy()
    
        #Proportion of cooperation
        #Sigma C (only the last evolution) over Sigam d(degree of nodes)
        no_cooperation = 0
        for i in range(number_of_nodes):
            no_cooperation += G.node[i]['cooperation']
        
        cooperation_ratio = (no_cooperation/2)/G.number_of_edges()
        f.write("cooperation ratio:")
        f.write('{}'.format(cooperation_ratio))
        f.write('\n')
    
        for i in range(number_of_nodes):
            G.node[i]['payoff'] = 0
            G.node[i]['pay_record'] = []
            G.node[i]['history'] = copy.deepcopy(G.node[i]['history_t1'])
            G.node[i]['history_t1'].clear()
            G.node[i]['cooperation'] = 0
    
        f.write("rate_uc, rate_ud, rate_tft, rate_cr, rate_ur, rate_sj:")
        B = check_ratio(G)
    
        for ratio in B:
            f.write('{}'.format(ratio))
            f.write(',')
            #print(ratio)
        
        f.write('\n')
    
    
        #Stopping condition
        if 1 in B:
            f.write('{}'.format(counter))
            f.write('\n')
            break
    
        if counter == TMAX:
            f.write("Reaches 100000 rounds.")
            f.write('\n')
            break

f.close()
            
                