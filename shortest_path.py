import networkx as nx
from ncclient import manager
import json as json

# Do not forget to change to your path 
FILE = 'C:/Users/behar/Desktop/Shortest_Path_NANOG/topology.json'

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
    
    
    
    
    
    
print " "  
print "Nodes: "
print id_list
print " "

print "links: "
print links
print " "

print "links costs: "
print cost
print " "

print "links capacities: "
print capacity
print " "

print "Block starts : "
print ted_block_starts
print " "

print "SID Indexes:  "
print sid_indexes
print " "

print "Local IP Addresses of the Interfaces: "
print local_addresses
print " "

print "Remote IP Addresses of the Interfaces:  "
print next_hop_addresses
print " "

