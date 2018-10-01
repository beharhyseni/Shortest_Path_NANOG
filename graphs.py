import networkx as nx

def shortPath(): 

    G = nx.Graph()
    for i in range(1,6):
        G.add_node("vmx{}".format(i))

    G.add_edge("vmx1","vmx3", cost=10, capacity=100)
    G.add_edge("vmx1","vmx2", cost=10, capacity=200)
    G.add_edge("vmx1","vmx4", cost=10, capacity=300)
    G.add_edge("vmx2","vmx3", cost=10, capacity=200)
    G.add_edge("vmx2","vmx5", cost=10, capacity=100)
    G.add_edge("vmx4","vmx5", cost=20, capacity=50)
    return shortestPath(G,"vmx3","vmx4",200)
def main():
    G = nx.Graph()
    for i in range(1,6):
        G.add_node("vmx{}".format(i))

    G.add_edge("vmx1","vmx3", cost=10, capacity=100)
    G.add_edge("vmx1","vmx2", cost=10, capacity=200)
    G.add_edge("vmx1","vmx4", cost=10, capacity=300)
    G.add_edge("vmx2","vmx3", cost=10, capacity=200)
    G.add_edge("vmx2","vmx5", cost=10, capacity=100)
    G.add_edge("vmx4","vmx5", cost=20, capacity=50)
    
    print
    print "Shortest path from vmx3 to vmx4:"
    print shortestPath(G,"vmx3","vmx4")
    
    print
    print "Shortest path from vmx3 to vmx4 with 200 payload:"
    print shortestPath(G,"vmx3","vmx4",200)
    
    print
    print "Shortest path from vmx3 to vmx4 with 200 payload and \
            \nshortest path from vmx5 to vmx4 with 60 payload."
    s1 = "vmx3"
    t1 = "vmx4"
    s2 = "vmx5"
    t2 = "vmx4"
    #multiCommodity(G,s1,t1,s2,t2,200,60)

def shortestPath(G, source=None, target=None, payload=0, cost="cost"):
    if payload == 0:
        return nx.shortest_path(G, source, target, cost)

    H = G.copy()
    for u,v,atr in H.edges(data=True):
        if atr['capacity'] < payload:
            H.remove_edge(u,v)
    return nx.shortest_path(H, source, target, cost)

def multiCommodity(G, s1, t1, s2, t2, p1=0, p2=0, cost="cost"):
    H1 = G.copy()
    for u,v,atr in H1.edges(data=True):
        if atr['capacity'] < p1:
            H1.remove_edge(u,v)

    H2 = G.copy()
    for u,v,atr in H2.edges(data=True):
        if atr['capacity'] < p2:
                H2.remove_edge(u,v)
   
    print H2.edges()

    P1 = nx.all_simple_paths(H1,s1,t1)
    P1_costs = {}
    P2 = nx.all_simple_paths(H2,s2,t2)
    P2_costs = {}

    for p in P1:
        P1_costs[p] = getPathCost(H1,p)
    for p in P2:
        P2_costs[p] = getPathCost(H2,p)

    min_P1 = min(P1)
    min_P2 = min(P2)

    while True:
        if compatable(min_P1, min_P2):
            return min_P1, min_P2
        else:
            P1.remove(min_P1)
            P2.remove(min_P2)

    return 

def getPathCost(G,p):
    total_cost = 0
    edge_costs = nx.get_edge_attributes(G,"cost")

    for i in range(len(p)-1):
        try:
            total_cost += edge_costs[(p[i],p[i+1])]
        except KeyError:
            try:
                total_cost += edge_costs[(p[i+1],p[i])]
            except KeyError:
                return "no edge","(",p[i],",",p[i+1],")"

    return total_cost

def compatable(p1, p2):
    l1 = len(p1)
    l2 = len(p2)
    
    if l1 < l2:
        for i in range(l1-1):
            if p1[i] == p2[i] and p1[i+1] == p2[i+1]: return False
        return True
    else:
        for i in range(l2-1):
            if p1[i] == p2[i] and p1[i+1] == p2[i+1]: return False
        return True



def iterativeDijsktra(G, source, target, payload=0, cost="cost"):
    H = G.copy()
    for u,v,atr in H.edges(data=True):
        if atr['capacity'] < payload:
            H.remove_edge(u,v)
    return

def getNextShortestPath(G, source, target, payload=0, cost="cost"):
    H = G.copy()
    for u,v,atr in H.edges(data=True):
        if atr['capacity'] < payload:
            H.remove_edge(u,v)
    yield nx.shortest_path(H, source, target, cost)

#main()
