from utils import graph
from algorithm.geneticAlgorithm import Genome

scientists = graph.Graph()
scientists.graph_from_edges("utils/data.txt", 0)


def fitness(graf: graph.Graph, genome: Genome) -> int:
    value = 0

    temporary = dict(zip(graf.vertices_list(), genome))
    for i, vertex in enumerate(graf.vertices_list()):
        is_it = True
        if genome[i] == 1:
            for g in graf.team_mate(vertex):
                if g == vertex:
                    pass
                elif temporary[g] == 1:
                    genome[i] = 0
                    is_it = False
                    break
            if (is_it):
                value += 1
    return value


def bonus(graf: graph.Graph, genome: Genome) -> Genome:
    copy = genome
    temporary = dict(zip(graf.vertices_list(), copy))
    for i, vertex in enumerate(graf.vertices_list()):
        if copy[i] == 0:
            can_he = 0
            for g in graf.team_mate(vertex):
                if g == vertex:
                    pass
                elif temporary[g] == 1:
                    can_he += 1
            if can_he == 0:
                copy[i] = 1
    return copy


# def from_genome(genome: Genome, things: graph.Graph) -> graph.Graph:
#     result = []
#     for i, thing in enumerate(things):
#         if genome[i] == 1:
#             result += [thing]
#
#     return result
