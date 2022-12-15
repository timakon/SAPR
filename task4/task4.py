import csv
import math
from io import StringIO

def readString(string_data):
    result = []
    string_stream = StringIO(string_data)
    reader = csv.reader(string_stream, delimiter=",")
    for row in reader:
        result.append(row)
    return result


def getNodeList(graph):
    node_map = {}
    for [parent, child] in graph:
        node_map[parent] = True
        node_map[child] = True
    return list(node_map.keys())


def findChild(node, graph):
    found = []
    for [parent, child] in graph:
        if parent == node:
            found.append(child)
    return found


def findParent(node, graph):
    found = []
    for [parent, child] in graph:
        if child == node:
            found.append(parent)
    return found

def findAncestor(node, graph):
    found = []
    parents = findParent(node, graph)
    for parent in parents:
        grand_parents = findParent(parent, graph)
        if (len(grand_parents) > 0):
            found.extend(grand_parents)
            found.extend(findAncestor(parent, graph))
    return found

def findDescendant(node, graph):
    found = []
    children = findChild(node, graph)
    for child in children:
        grand_children = findChild(child, graph)
        if (len(grand_children) > 0):
            found.extend(grand_children)
            found.extend(findAncestor(child, graph))
    return found

def findNeighbours(node, graph):
    parents = findParent(node, graph)
    neighbours = []
    for parent in parents:
        children = findChild(parent, graph)
        children.remove(node)
        neighbours.extend(children)
    return neighbours

def findEntropy(graph_stats):
    total_sum = 0
    n = len(graph_stats)
    for [node, stats] in graph_stats:
        in_sum = 0
        for j in stats:
            p = j / (n - 1)
            if p > 0:
                b = math.log(p, 2)
                in_sum += p * b
        total_sum += in_sum
    return -total_sum

def task(str_graph):
    graph = readString(str_graph)
    node_list = getNodeList(graph)
    rez = []
    for node in node_list:
        r1 = findChild(node, graph)
        r2 = findParent(node, graph)
        r3 = findDescendant(node, graph)
        r4 = findAncestor(node, graph)
        r5 = findNeighbours(node, graph)
        rez.append(["n" + node, [len(r1), len(r2), len(r3), len(r4), len(r5)]])
    entropy = findEntropy(rez)
    return entropy