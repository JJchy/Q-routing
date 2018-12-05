import numpy as np
import simulator as sim
import q_agent as Q

def main ():
    result = np.zeros ((10, 1, 2))
    for i in range (1):
        for j in range (10):    
            env = sim.NetworkSimulatorEnv ((5) * 0.1)
            packet = env.reset ()
            agent = Q.Q_agent (env.nnode, env.link, env.packet_types, True)
            distance = shortest_length (env.link)
            real_time = 0

            num_packet = np.zeros ((env.nnode, env.nnode))
            total_time = np.zeros ((env.nnode, env.nnode))
            num_packet_p = np.zeros ((env.nnode, env.nnode))
            total_time_p = np.zeros ((env.nnode, env.nnode))
            num_packet_n = np.zeros ((env.nnode, env.nnode))
            total_time_n = np.zeros ((env.nnode, env.nnode))


            for t in xrange (500000):
                #print env.queue_state
                action = agent.act (packet, False)
                new_packet, reward, arrive, _ = env.step (action)
                agent.learn (packet, action, reward, arrive)

                if arrive == True:
                    #print packet.service_time - packet.made_time, packet.source, packet.dest
                    total_time[packet.source, packet.dest] += packet.service_time - packet.made_time
                    #print packet.service_time - packet.made_time, packet.service_time, packet.made_time, packet.source, packet.dest, env.queue_state
                    num_packet[packet.source, packet.dest] += 1
                    if packet.flow_type == 0:
                        total_time_p[packet.source, packet.dest] += packet.service_time - packet.made_time
                        num_packet_p[packet.source, packet.dest] += 1
                    elif packet.flow_type == 1:
                        total_time_n[packet.source, packet.dest] += packet.service_time - packet.made_time
                        num_packet_n[packet.source, packet.dest] += 1

                if real_time * 10000 < packet.service_time:
                    real_time += 1
                    average_time = total_time / (num_packet + 0.000000001)
                    average_time_p = total_time_p / (num_packet_p + 0.00000001)
                    average_time_n = total_time_n / (num_packet_n + 0.00000001)
                    print "{}: Average Packet Time = {}".format (t, np.sum (average_time) / np.count_nonzero (average_time))
                    print "{}: Average Packet Time = {}".format (t, np.sum (average_time_p) / np.count_nonzero (average_time_p))
                    print "{}: Average Packet Time = {}".format (t, np.sum (average_time_n) / np.count_nonzero (average_time_n))
                    print env.queue_state
                    print np.sum(num_packet), np.sum(num_packet_p)
                    #print agent.q[1, :, :], np.sum (num_packet), np.sum (total_time) 
                    num_packet = np.zeros ((env.nnode, env.nnode))
                    total_time = np.zeros ((env.nnode, env.nnode))
                    num_packet_p = np.zeros ((env.nnode, env.nnode))
                    total_time_p = np.zeros ((env.nnode, env.nnode))
                    num_packet_n = np.zeros ((env.nnode, env.nnode))
                    total_time_n = np.zeros ((env.nnode, env.nnode))

                packet = new_packet

            result[j, i, 0] = np.sum (average_time_p) / np.count_nonzero (average_time_p)
            result[j, i, 1] = np.sum (average_time) / np.count_nonzero (average_time)
            print (i, j)

    result_avg = np.average (result, axis = 0)
    result_std = np.std (result, axis = 0)

    print result_avg
    print result_std


    

def shortest_length (link):
    nnode = link.shape[0]
    result = np.ones ((nnode, nnode)) * (nnode + 1)

    for i in range(nnode):
        for j in range(nnode):
            if i == j:
                result[i, j] = 0
            elif link[i, j] == 1:
                result[i, j] = 1

    for k in range(nnode):
        for i in range(nnode):
            for j in range(nnode):
                if result[i, j] > result[i, k] + result[k, j]:
                    result[i, j] = result[i, k] + result[k, j]
    
    return result

if __name__ == '__main__':
    main ()

