import random
from constant import*

def initial_stra_ratio(p0, p1, p2, p3, p4, p5):
    return random.random(population = range(6), weights = [p0, p1, p2, p3, p4, p5])
    
def play_random():
    if random.random() > 0.5:
        return 1
    else:
        return 0

def play_pd(player, opponent):     
    if (player == 0) and (opponent == 0):
        return 1, 1
    
    elif (player == 0) and (opponent == 1):
        return 5, 0
    
    elif (player == 1) and (opponent == 1):
        return 3, 3
    
    elif (player == 1) and (opponent == 0):
        return 0, 5
        
        
def decide(player, opponent, G):
    #UC
    if G.node[player.agent_id]['strategy'] == 0:
        return 1
    #UD
    elif G.node[player.agent_id]['strategy'] == 1:
        return 0
    #TFT
    elif G.node[player.agent_id]['strategy'] == 2:
        # React to the opponent's last move
        if player.agent_id in G.node[opponent.agent_id]['history']:
            if G.node[opponent.agent_id]['history'][player.agent_id] == 1:
                return 1
            else:
                return 0
        #####Code check: if player has history with other opponents but not this opponent, return 1
        else:
            return 1
    #CR
    elif G.node[player.agent_id]['strategy'] == 3:
        return decide_cr(player, opponent, G)
    
    #UR
    elif G.node[player.agent_id]['strategy'] == 4:
        return decide_ur(player, opponent, G)
    
    #SJ
    elif G.node[player.agent_id]['strategy'] == 5:
        return decide_sj(player, opponent, G)
    
    #Print error if not found
    else:
        print('error: undefined strategy type')


#A function for CR
def decide_cr(player, opponent, G):
    #Find common neighbors(agent)
    
    A = player.get_neighboring_agents()
    B = opponent.get_neighboring_agents()
    #A list of common friends
    common_neighbors = [element for element in A if element in B]
    #Element type: Player
    
    #If there is no common friends, play randomly
    if len(common_neighbors) == 0:
        return play_random()
    else:
        #randomly select a common friend
        select_rand_friend = random.choice(common_neighbors)
        #Recall last behaviour to thie neighbor
        #If the Other played C against select_rand_friend in the previous step --> cooperate
        if select_rand_friend in G.node[opponent.agent_id]['history']:
            last_move = G.node[opponent.agent_id]['history'][select_rand_friend]
            if last_move == 1:
                return 1
            #If the Other played D against select_rand_friend in the previous step --> defect
            elif last_move == 0:
                #Forgiveness
                #If there is another common friend
                #Find his opinions
                common_neighbors.remove(select_rand_friend)
                if random.random() < PFOR:
                    if len(common_neighbors) > 0 :
                        #Eliminate the guy already choosen from the list of friends
                        #Randomly select anthter friend
                        select_rand_friend_2 = random.choice(common_neighbors)
                        if select_rand_friend_2 in G.node[opponent.agent_id]['history']:
                            last_move_2 = G.node[opponent.agent_id]['history'][select_rand_friend_2]
                            if last_move_2 == 1:
                                return 1
                            elif last_move_2 == 0:
                                return 0
                        else:
                            return play_random()
                else:
                    return 0     
        #If the Other player did not play against select_rand_friend in the previous step --> play randomly
        else:
            return play_random()
        
def decide_ur(player, opponent, G):
    #Find a list of neighbors of the opponent
    B = opponent.get_neighboring_agents()
    #Eliminate oneself from it
    B.remove(player.agent_id)
    #If the Other player did not play against select_rand_friend in the previous step --> play randomly
    if len(B) == 0:
        return play_random()
    else:
        #Select a random friend
        select_rand_friend = random.choice(B)
        if select_rand_friend in G.node[opponent.agent_id]['history']:
            last_move =  G.node[opponent.agent_id]['history'][select_rand_friend]
            if last_move == 1:
                return 1
            else:
                if random.random() < PFOR:
                    #Give opponent another chance based on another friend
                    B.remove(select_rand_friend)
                    if len(B) == 0:
                        return play_random()
                    else:
                        select_rand_friend_2 = random.choice(B)
                        if select_rand_friend_2 in G.node[opponent.agent_id]['history']:
                            last_move_2 = G.node[opponent.agent_id]['history'][select_rand_friend_2]
                            if last_move_2 == 1:
                                return 1
                            elif last_move_2 == 0:
                                return 0
                        else:
                            #If the Other player did not play against select_rand_friend in the previous step --> play randomly
                            return play_random()
                else:
                    return 0
    
        else:
            return play_random()

def decide_sj(player, opponent, G):
    #Find a list of common friends
    A = player.get_neighboring_agents()
    B = opponent.get_neighboring_agents()
    common_neighbors = [element for element in A if element in B]
    #Play randomly if there is no common friends
    if len(common_neighbors) == 0:
        if random.random() > 0.5:
            return 1
        else:
            return 0
    else:
        #Randomly select a common friend
        select_rand_friend = random.choice(common_neighbors)
        if select_rand_friend in G.node[opponent.agent_id]['history']:
            #Action of Other with common friend
            last_move = G.node[opponent.agent_id]['history'][select_rand_friend]
            #Action of common friend with me
            if player.agent_id in G.node[select_rand_friend]['history']:
                last_move_2 = G.node[select_rand_friend]['history'][player.agent_id]
                #If the opponent cooperate with the common friend
                if last_move == 1: 
                    #If the common friend cooperates with the palyer
                    if last_move_2 == 1:
                        return 1
                    elif last_move_2 == 0:
                        return 0     
                elif last_move == 0:
                    if last_move_2 == 1:
                        return 0
                    elif last_move_2 == 0:
                        return 1
            #####Code change: if there is no interaction between common friend and me
            else:
                return play_random()
        else:
            return play_random()

#the strategy is randomly selected
#agent: same as 'process' in SimPy but behaviours are limited
#by its network
class Player:
    
    def __init__(self, agent_id, G):
        #Using agent_id to present strategy
        #0: UC
        #1: UD
        #2: TFT
        #3: CR
        #4: UR
        #5: SJ
        self.agent_id = agent_id
        self.G = G
    
    def update_payoff(self, payoff):
        self.G.node[self.agent_id]['payoff'] += payoff
    
    #decide to cooperate or defect by its strategy
    def update_behavior(self, neighbor):
        self.G.node[self.agent_id]['behavior'] = decide(self, neighbor, self.G)
        
    def update_cooperation(self):
        self.G.node[self.agent_id]['cooperation'] += 1
    
    #A dictionary recording last behaviour to a certain neifhbor
    def update_history(self, neighbor):
        #pass
        self.G.node[self.agent_id]['history_t1'][neighbor] = self.G.node[self.agent_id]['behavior']
        
    def get_neighboring_agents(self):
        return list(self.G.neighbors(self.agent_id))
        
    def update_strategy(self):
        #Copy the best
        if UPDATETYPE == 'st':
            if random.random() < PEVO:
                #All connections
                neighbors = self.get_neighboring_agents()
                #Also take in consideration itself
                neighbors.append(self.agent_id)
                #Find the maximum payoff in i neighbourhood
                max_payoff = max([self.G.node[neighbor]['payoff']/len(list(self.G.neighbors(neighbor))) for neighbor in neighbors])
                #Find who are the agents carrying that payoff
                max_payoffs = [neighbor for neighbor in neighbors if self.G.node[neighbor]['payoff']/len(list(self.G.neighbors(neighbor))) == max_payoff]
                #Randomly choose one of them
                neighbor = random.choice(max_payoffs)
                #Transform itself in that agent
                self.G.node[self.agent_id]['strategy'] = self.G.node[neighbor]['strategy']
            else:
                pass
        #Copy the (strictly) better
        else:
            if random.random() < PEVO:
                #All connections
                neighbors = self.get_neighboring_agents()
                #Also take in consideration itself
                neighbors.append(self.agent_id)
                #Select those who have larger payoffs than myself
                larger_payoffs = [neighbor for neighbor in neighbors if self.G.node[neighbor]['payoff']/len(list(self.G.neighbors(neighbor))) > self.G.node[self.agent_id]['payoff']/len(list(self.G.neighbors(self.agent_id)))]
                if len(larger_payoffs) > 0:
                    #Randomly choose one of them
                    neighbor = random.choice(larger_payoffs)
                    self.G.node[self.agent_id]['strategy'] = self.G.node[neighbor]['strategy']  
                else:
                    pass
    
    def game(self):
        my_neighbors = self.get_neighboring_agents()
        if not my_neighbors:
            print('error: isolate node - neighbor is None')
        else:
            for neighbor in my_neighbors:
                #If they have played before, do not replay the game
                if self.agent_id in self.G.node[neighbor]['play_record']:
                    pass
                else:
                    
                    self.G.node[self.agent_id]['play_record'].append(neighbor)
                    
                    neighbor_agent = self.G.node[neighbor]['agent']
                    #now .behavior is behaviour at t-1
                    #new_behavior is behaviour at t
                    self.update_behavior(neighbor_agent)
                    neighbor_agent.update_behavior(self)
                    
                    #Record if cooperates or not
                    if self.G.node[self.agent_id]['behavior'] == 1:
                        self.update_cooperation()
                    
                    if self.G.node[neighbor]['behavior'] == 1:
                        neighbor_agent.update_cooperation()
                        
                    #payoff at time t
                    my_payoff, neighbor_payoff = play_pd(self.G.node[self.agent_id]['behavior'], self.G.node[neighbor]['behavior'])
                    
                    #update total payoff
                    self.update_payoff(my_payoff)
                    neighbor_agent.update_payoff(neighbor_payoff)
                    
                    #update history in ordert to make decision fo t+1
                    self.update_history(neighbor)
                    neighbor_agent.update_history(self.agent_id)

    