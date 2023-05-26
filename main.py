from collections import deque, defaultdict
def probabilistic_bisimulation(lts):
    bisim_graph = {}
    bisim_classes = defaultdict(set)
    queue = deque()

    # Initialize the bisimulation graph with nodes for each state
    for state in lts:
        bisim_graph[state] = set()
        queue.append(state)

    # Compute bisimulation classes using breadth-first search
    while queue:
        p = queue.popleft()
        if p not in bisim_classes:
            bisim_classes[p] = set([p])
            for q in bisim_graph:
                if q not in bisim_classes:
                    continue
                if lts[p]['label'] == lts[q]['label']:
                    bisim_check = True
                    for p_t in lts[p]:
                        if p_t == 'label':
                            continue
                        q_t = str(p_t) # convert to string
                        if q_t not in lts[q]:
                            bisim_check = False
                            break
                        if lts[p][p_t] != lts[q][q_t] or bisim_classes[str(lts[p][p_t])] != bisim_classes[str(lts[q][q_t])]:
                            bisim_check = False
                            break
                    if not bisim_check:
                        continue
                    for q_t in lts[q]:
                        if q_t == 'label':
                            continue
                        if str(q_t) not in lts[p]:
                            bisim_check = False
                            break
                        p_t = str(q_t) # convert to string
                        if lts[q][q_t] != lts[p][p_t] or bisim_classes[str(lts[q][q_t])] != bisim_classes[str(lts[p][p_t])]:
                            bisim_check = False
                            break
                    if bisim_check:
                        bisim_classes[p].add(q)
                        bisim_classes[q].add(p)
                        bisim_graph[p].add(q)
                        bisim_graph[q].add(p)
                        queue.append(q)

    return bisim_classes, bisim_graph


# Define the LTS
lts = {
    's1': {'label': 'a', 's2': '0.2', 's3': '0.8'},
    's2': {'label': 'b', 's1': '0.3', 's3': '0.7'},
    's3': {'label': 'a', 's2': '0.4', 's4': '0.6'},
    's4': {'label': 'b', 's3': '1.0'}
}

# Compute the bisimulation classes and graph
bisim_classes, bisim_graph = probabilistic_bisimulation(lts)

# Print the results
print("Bisimulation classes:", bisim_classes)
print("Bisimulation graph:", bisim_graph)
