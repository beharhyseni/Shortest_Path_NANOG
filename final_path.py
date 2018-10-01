import networkx as nx
from ncclient import manager
import json as json
from graphs import *
import sys

# Do not forget to change to your path 
FILE = 'topology.json'

# Open the JSON file that contains the router information:
with open(FILE) as topology:    data = json.load(topology)

# Constains the JSON list of "ted-database-information"
ted_database_info = data["ted-database-information"]

# Constains the JSON list of "ted-database"
ted_database = ted_database_info[0]['ted-database']

# Calculates and saves the number of nodes
dict_length = len(ted_database)

# Contains the names of the Node IDs
id_list = []
sid_indexes = []
ted_block_starts = []


for i in range(0, dict_length):
    id = ted_database[i]["ted-database-id"][0]["data"].encode("ascii")
    id_list.append(id)
    
for k in range(0, dict_length):
   block_start = ted_database[k]["ted-spring-capability"][0]["ted-spring-srgb-block"][0]["ted-spring-srgb-block-start"][0]["data"].encode("ascii")
   sid_index  = ted_database[k]["ted-prefixes"][0]["ted-prefix"][0]["ted-prefix-sid"][0]["ted-prefix-sid-index"][0]["data"].encode("ascii")
   ted_block_starts.append(block_start)
   sid_indexes.append(sid_index)
   

# Extracts the "ted-link" key from the given topology json
ted_link = ted_database[0]["ted-link"]

# Initializes the arrays to be used (they will be 2D arrays after inserting 1D arrays into them)
links = []
cost = []
capacity = []
local_addresses = []
next_hop_addresses = []


# Loop through every element of the json list with keyname: "ted-database" 
for n in range(0,len(ted_database)):
    
    # reset the lists to be used for next nodes' elements
    list = []
    cost_list = []
    capacity_list = []
    local_address = []
    next_hop_address = []
    
    # Loop through every links to other routers from the given router n
    for i in range(0,len(ted_database[n]["ted-link"])):
        
        # Insert the router links of the first router
        list.append(ted_database[n]["ted-link"][i]["ted-link-to"][0]["data"].encode("ascii"))
        
        # Insert the router links' costs of the first router
        cost_list.append(ted_database[n]["ted-link"][i]["ted-link-metric"][0]["data"].encode("ascii"))
        
        # Insert the router links' capacities of the first router
        capacity_list.append(ted_database[n]["ted-link"][i]["ted-link-static-bandwidth"][0]["data"].encode("ascii"))
   
        # Insert the router interfaces' local IP addresses
        local_address.append(ted_database[n]["ted-link"][i]["ted-link-local-address"][0]["data"].encode("ascii"))
         
        # Insert the router intefaces' remote/next hop IP addresses
        next_hop_address.append(ted_database[n]["ted-link"][i]["ted-link-remote-address"][0]["data"].encode("ascii"))
   
    # Insert the 1D lists of routers' links, costs, capacities, interfaces' local and remote IP addresses into the 2D arrays.
    links.append(list)
    cost.append(cost_list)
    capacity.append(capacity_list)
    local_addresses.append(local_address)
    next_hop_addresses.append(next_hop_address)
    
    
    
    
    
    
    
    

G = nx.Graph()
for i,j in enumerate(id_list):
    G.add_node(j)
    for k,l in enumerate(links[i]):
        the_cost = int(cost[i][k])
        the_capacity = int(capacity[i][k][:-4])
        G.add_edge(j, links[i][k], cost=the_cost, capacity=the_capacity)
    
    

# print " "  
# print "Nodes: "
print id_list
# print " "
# 
# print "links: "
# print links
# print " "
# 
# print "links costs: "
# print cost
# print " "
# 
# print "links capacities: "
# print capacity
# print " "
# 
# print "Block starts : "
# print ted_block_starts
# print " "
# 
# print "SID Indexes:  "
# print sid_indexes
# print " "
# 
# print "Local IP Addresses of the Interfaces: "
# print local_addresses
# print " "
# 
# print "Remote IP Addresses of the Interfaces:  "
# print next_hop_addresses
# print " "
# 
print "The edges with the right costs and capacities: "
for u,v,atr in G.edges(data=True):
    print u, v, atr
print " "
print sys.argv
#values =  shortestPath(G, sys.argv[1], sys.argv[2], sys.argv[3])
values =  shortestPath(G, "mx3.00(10.0.0.3)", "mx4.00(10.0.0.4)", 200)
#val = multiCommodity(G,"mx3.00(10.0.0.3)", "mx4.00(10.0.0.4)", "mx5.00(10.0.0.5)", "mx4.00(10.0.0.4)", 200, 60)
#values = val[0]
#values = val[1]
label = []                                                                                                
for sid in sid_indexes:                                                                                   
    label.append("800000"+sid)
        
id_list_short = []                                                                                        
#for id in id_list:
#    id_list_short.append(id[:4])                                                                          
dictionary = dict(zip(id_list, label))                                                             
odict = dict(zip(id_list, next_hop_addresses))                                                         
    
    
packet_labels = []
next_hop = []                                                                                             
for value in values:                                                                                      
    packet_labels.append(dictionary[value])                                                               
    next_hop.append(odict[value])                                                                         
string = ""                                                                                               
for x in range(2, len(packet_labels)):                                                                   
    string += packet_labels[x] + " "                                                                       
print next_hop                                                                                                         
line = "neighbor " + "100.96.0.8 " + " announce route " + values[-1][7:15] + " next-hop " + next_hop[0][1] + " label [ " + string + "]\n"
with open("routes.log","a") as myfile:                                                                    
    myfile.write(line)
