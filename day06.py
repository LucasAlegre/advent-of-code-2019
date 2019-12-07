def compute_orbits(node, graph, orbits):
    if node in orbits:
        return orbits[node]
    if len(graph[node]) == 0:
        orbits[node] = 0
        return 0

    orbits[node] = sum([1 + compute_orbits(n, graph, orbits) for n in graph[node]])
    return orbits[node]

def distance(origin, dest, graph):
    distances = {node: 999999999 for node in graph.keys()}
    visited = {node: False for node in graph.keys()}
    distances[origin] = 0
    queue = [origin]
    while len(queue) > 0:
        node = queue.pop(0)
        visited[node] = True
        for n in graph[node]:
            if not visited[n]:
                distances[n] = min(distances[n], distances[node] + 1)
                queue.insert(0, n)

    return distances[dest]
    

if __name__ == '__main__':

    with open('day06.txt') as f:
        inp = f.readlines()
    
    graph = dict()
    reachable = set()
    for line in inp:
        a, b = line.strip().split(')')
        if b in graph:
            graph[b].append(a)
        else:
            graph[b] = [a]
        if a not in graph:
            graph[a] = []
        reachable.add(a)
    
    orbits = dict()
    for node in graph.keys():
        if node not in reachable:
            compute_orbits(node, graph, orbits)
    
    # part 1
    print(sum(orbits.values()))

    # part 2 (it must be bidirected)
    for u in graph:
        for v in graph[u]:
            graph[v].append(u)

    print(distance(graph['YOU'][0], graph['SAN'][0], graph))

    