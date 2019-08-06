from constant import*
import random
from Player import Player

#Initialise the nodes
def init_all_nodes(G):
    for i in range(number_of_nodes):
        #Each node have a dict memory for neighbours' behaviours
        G.node[i]['history'] = {}
        G.node[i]['history_t1'] = {}
        #Check if played already
        G.node[i]['play_record'] = []
        #For calculating the proportion of cooperation
        G.node[i]['cooperation'] = 0
        #Record of own payoff after interacting with all neighbours
        G.node[i]['payoff'] = 0
        #Record of own strategy
        G.node[i]['behavior'] = None
        G.node[i]['strategy'] = random.choice([1,3,4])
        G.node[i]['agent'] = Player(i, G)
    
    #Task: different ratio of strategies

def check_ratio(G):
    #Set up counters
    uc = 0
    ud = 0
    tft = 0
    cr = 0
    ur = 0
    sj = 0
    
    for i in G.nodes:
        if G.node[i]['strategy'] == 0:
            uc += 1
        elif G.node[i]['strategy'] == 1:
            ud += 1
        elif G.node[i]['strategy'] == 2:
            tft += 1
        elif G.node[i]['strategy'] == 3:
            cr += 1
        elif G.node[i]['strategy'] == 4:
            ur += 1
        else:
            sj += 1
            
    rate_uc = uc/number_of_nodes
    rate_ud = ud/number_of_nodes
    rate_tft = tft/number_of_nodes
    rate_cr = cr/number_of_nodes
    rate_ur = ur/number_of_nodes
    rate_sj = sj/number_of_nodes
    
    result = [rate_uc, rate_ud, rate_tft, rate_cr, rate_ur, rate_sj]
    
    return result

        

    