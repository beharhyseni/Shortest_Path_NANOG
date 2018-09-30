import networkx as nx
from ncclient import manager
import json as json

# Do not forget to change to your path 
FILE = 'C:/Users/behar/Desktop/Shortest_Path_NANOG/topology.json'

with open(FILE) as topology:    data = json.load(topology)

# Constains the JSON list of "ted-database-information"
ted_database_info = data["ted-database-information"]

# Constains the JSON list of "ted-database"
ted_database = ted_database_info[0]['ted-database']

# Calculates and saves the number of nodes
dict_length = len(ted_database)

# Contains the names of the Node IDs
id_list = []


for i in range(0, dict_length-1):
    id = ted_database[i]["ted-database-id"][0]["data"]
    id_list.append(id)
    

print id_list