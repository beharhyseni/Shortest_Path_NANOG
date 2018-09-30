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
prefix_algs = []
ted_block_starts = []


for i in range(0, dict_length):
    id = ted_database[i]["ted-database-id"][0]["data"].encode("ascii")
    id_list.append(id)
    
for k in range(0, dict_length):
   block_start = ted_database[k]["ted-spring-capability"][0]["ted-spring-srgb-block"][0]["ted-spring-srgb-block-start"][0]["data"].encode("ascii")
   prefix_alg  = ted_database[k]["ted-prefixes"][0]["ted-prefix"][0]["ted-prefix-sid"][0]["ted-prefix-sid-algo"][0]["data"].encode("ascii")
   ted_block_starts.append(block_start)
   prefix_algs.append(prefix_alg)
   

#print ted_database[0]["ted-spring-capability"][0]["ted-spring-srgb-block"][0]["ted-spring-srgb-block-start"][0]["data"].encode("ascii")

ted_link = ted_database[0]["ted-link"]
links = []
cost = []
capacity = []


for n in range(0,len(ted_database)):
   
    list = []
    cost_list = []
    capacity_list = []
    for i in range(0,len(ted_database[n]["ted-link"])):
        list.append(ted_database[n]["ted-link"][i]["ted-link-to"][0]["data"].encode("ascii"))
        cost_list.append(ted_database[n]["ted-link"][i]["ted-link-metric"][0]["data"].encode("ascii"))
        capacity_list.append(ted_database[n]["ted-link"][i]["ted-link-static-bandwidth"][0]["data"].encode("ascii"))
   
    links.append(list)
    cost.append(cost_list)
    capacity.append(capacity_list)
    
    
    
    
    
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

print "prefix algorithms:  "
print prefix_algs
print " "

