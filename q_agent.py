import numpy as np

inf = 10000000

class Q_agent:
    def __init__ (self, num_nodes, connection, packet_types, delay):
        self.setting = {
            "learning_rate" : 0.2,
            "discount" : 1,
            "delay" : delay                 #T/F
        }

        # connection belief (It can be changed.)
        # bidirectional
        self.connection = connection

        # (current, dest, action)
        self.q = np.repeat (np.expand_dims (connection, axis = 1), num_nodes, axis = 1)
        self.q = np.repeat (np.expand_dims (self.q, axis = 0), packet_types, axis = 0)
        self.q = inf * (1 - self.q)

    def act (self, packet, best = False):
        current = packet.curr
        dest = packet.dest
        ptype = 0 #packet.flow_type

        if best is True:
            if self.setting["delay"] is True:
                true_q = self.q[ptype, current, dest, :] * self.connection[current, :] + inf * (1 - self.connection[current, :])
                #true_q = self.q[current, dest, :] * self.connection[current, :] + inf * (1 - self.connection[current, :])
                action = np.where ((true_q == np.min(true_q)))[0][0]
            else:
                true_q = self.q[ptype, current, dest, :] * self.connection[current, :]
                #true_q = self.q[current, dest, :] * self.connection[current, :]
                action = np.where ((true_q == np.max(true_q)))[0][0]

        else:
            index = np.array (np.where (self.connection[current, :] == 1)[0])
            Q_value = self.q[ptype, current, dest, index]
            #Q_value = self.q[current, dest, index]
            if self.setting["delay"] is True:
                Q_value *= -1
            Q_value -= np.max (Q_value)
            Q_value /= (10 / (4 * np.sin (packet.made_time + 1) + 5)) 
            prob = np.exp (Q_value) / np.sum (np.exp (Q_value))
            action = index[np.where (np.random.multinomial (1, prob) == 1)[0][0]]
  
        return action

    def learn (self, packet, action, reward, arrive):
        current = packet.curr
        dest = packet.dest
        ptype = 0 #packet.flow_type

        if arrive is False:
            if self.setting["delay"] is True:
                next_true_q = self.q[ptype, action, dest, :] * self.connection[action, :] + inf * (1 - self.connection[action, :])
                #next_true_q = self.q[action, dest, :] * self.connection[action, :] + inf * (1 - self.connection[action, :])
                next_Q_value = np.min (next_true_q)
            else:
                next_true_q = self.q[ptype, action, dest, :] * self.connection[action, :]
                #next_true_q = self.q[action, dest, :] * self.connection[action, :]
                next_Q_value = np.max (next_true_q)

        assert (action != current)
        
        if arrive is False:
            #TD_error = reward + (self.setting["discount"] * next_Q_value) - self.q[current, dest, action]
            TD_error = reward + (self.setting["discount"] * next_Q_value) - self.q[ptype, current, dest, action]
        
        if arrive is True:
            #TD_error = reward - self.q[current, dest, action]
            TD_error = reward - self.q[ptype, current, dest, action]
        #print TD_error, reward, next_Q_value, self.q[current][dest][action]
        self.q[ptype, current, dest, action] += self.setting["learning_rate"] * TD_error 
        #self.q[current, dest, action] += self.setting["learning_rate"] * TD_error 

        # the connection change method?
        
