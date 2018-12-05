import gym
from gym.utils import seeding
import heapq
import numpy as np
import random
import time as t #debug

MAKING_PACKET = -1
UNKNOWN = -2

class event:
    def __init__ (self, time, curr, source, dest, flow_type):
        self.source = source
        self.dest = dest
        self.curr = curr
        self.arrival_time = time
        self.made_time = time
        self.service_time = UNKNOWN
        self.flow_type = flow_type    #0, 1

class SpecialQueue:
    def __init__(self, n_type=2):
        self.n_type = n_type
        self.s_queue = [[] for _ in range(self.n_type)]
        self.queue_state = np.zeros (self.n_type)

    def insert(self, packet):
        heapq.heappush (self.s_queue[packet.flow_type], (packet.arrival_time, packet))
        #heapq.heappush (self.s_queue[0], (packet.arrival_time, packet))
        self.queue_state[packet.flow_type] += 1
        #self.queue_state[0] += 1

    def pop(self, alpha):
        if np.random.rand() < alpha and self.queue_state[0] != 0: # C1(0): high priority
            self.queue_state[0] -= 1
            return heapq.heappop (self.s_queue[0])

        elif self.queue_state[1] != 0:
            self.queue_state[1] -= 1
            return heapq.heappop (self.s_queue[1])

        else:
            self.queue_state[0] -= 1
            return heapq.heappop (self.s_queue[0])

        
class NetworkSimulatorEnv (gym.Env):
    metadata = {
        'graph_name': 'lata_.net',
        'packet_time': 1
    }
    
    def __init__ (self, perc):
        self.turn_queue = []
        self.queue_state = []
        self.node_time = []
        self.internode_time = 1 #ms
        self.packet_types = 2
        self.perc = perc

        self.read_graph ()
        self.seed ()
    
    def step (self, action):
        current_packet = self.current_packet
        #print "packet", current_packet.made_time, current_packet.arrival_time, self.node_time[current_packet.curr], current_packet.curr, current_packet.dest, action
        reward = self.node_time[current_packet.curr] - self.current_packet.arrival_time
        #print "reward", reward

        if current_packet.dest != action:
            arrive = False

            new_packet = event (self.node_time[current_packet.curr], action, current_packet.source, current_packet.dest, current_packet.flow_type)
            new_packet.made_time = current_packet.made_time

            if self.queue_state[action] == 0:
                if self.node_time[action] < self.node_time[current_packet.curr]:
                    self.node_time[action] = self.node_time[current_packet.curr]
                heapq.heappush (self.turn_queue, (self.node_time[action], action))           

            self.node_queue[action].insert(new_packet)
            self.queue_state[action] += 1

        else:
            arrive = True
            #print current_packet.curr, self.node_time
            current_packet.service_time = self.node_time[current_packet.curr]
            #print "PACKET_DIE!"

        return self.get_new_packet (), reward, arrive, {}

    def reset (self):
        self.queue_state = np.zeros (self.nnode)
        self.node_time = np.zeros (self.nnode)
        self.node_queue = [SpecialQueue(self.packet_types) for _ in range (self.nnode)]

        heapq.heappush (self.turn_queue, (0.0, MAKING_PACKET))

        return self.get_new_packet ()

    def render (self, mode="visual"):
        return

    def seed (self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def close (self):
        return

    def read_graph (self):
        with open (self.metadata['graph_name']) as f:
            for i, line in enumerate(f):
                if i == 0:
                    self.nnode = int (line.split()[0])
                    self.link = np.zeros ((self.nnode, self.nnode))
                    continue
            
                node1, node2 = line.split()
                node1 = int (node1)
                node2 = int (node2)
                self.link[node1, node2] = 1
                self.link[node2, node1] = 1

    def get_new_packet (self):
        current_turn = heapq.heappop (self.turn_queue)

        while current_turn[1] == MAKING_PACKET:
            time = current_turn[0]
            new_time = time + np.random.exponential (self.metadata["packet_time"])
            heapq.heappush (self.turn_queue, (new_time, MAKING_PACKET))
            
            self.make_packet (time)

            current_turn = heapq.heappop (self.turn_queue)

        current_node = current_turn[1]
        current_event = self.node_queue[current_node].pop(1)[1]

        assert current_event.curr == current_node #debug
        
        self.queue_state[current_node] -= 1
        self.node_time[current_node] = max (self.node_time[current_node], current_event.arrival_time) + self.internode_time

        if self.queue_state[current_node] != 0:
            heapq.heappush (self.turn_queue, (self.node_time[current_node], current_node))

        self.current_packet = current_event
        #print current_event.dest, self.turn_queue, self.queue_state
        #t.sleep (0.001)
        return current_event

    def make_packet (self, time):
        source = np.random.randint(3)
        dest = np.random.randint(3) + 5
        while source == dest:
            dest = np.random.randint(self.nnode)
            
        flow_type = np.random.binomial(1, self.perc)
        new_packet = event (time, source, source, dest, flow_type)
        new_packet.curr = source

        if self.queue_state[source] == 0:
            if self.node_time[source] < time:
                self.node_time[source] = time
            heapq.heappush (self.turn_queue, (self.node_time[source], source))

        self.node_queue[source].insert(new_packet)
        self.queue_state[source] += 1 
        #print "MAKE PACKET"

