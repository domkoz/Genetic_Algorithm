from random import random


class Graph:
    def __init__(self):
        super(dict)
        self.graph = {}

    def add_vertex(self, vertex):
        """Nowy wierzchołek do istniejącego grafu"""
        if vertex not in self.graph:
            self.graph[vertex] = []

    def team_mate(self, vertex):
        return self.graph[vertex]
    def count_vertices(self):
        return len(self.graph.keys())
    def vertices_list(self):
        return self.graph.keys()

    def add_edge(self, edge):
        """Dodaje nową krawędź (parę wierzchołków) do istniejącego grafu
           traktując graf nieskierowany prosty jako prosty graf skierowany, ale symetryczny i bez pętli
        """
        u, v = edge
        self.add_vertex(u)
        self.add_vertex(v)
        if u == v:
            # print(f"pętla dla naukowca {u}")
            # raise ValueError("pętla!")
            pass
        if v not in self.graph[u]:
            self.graph[u].append(v)
        if u not in self.graph[v]:
            self.graph[v].append(u)

    def print_graph(self):
        """
        Wypisuje graf zadany jako słownik pythona
        """
        for v in self.graph:
            print(v, ":", end="")
            for u in self.graph[v]:
                print(" ", u, end="")
            print("")

    def random_graph(self, nb_vertices: int, propability: float):
        n = nb_vertices
        p = propability
        for i in range(1, n + 1):
            self.add_vertex(i)
            for j in range(1, i):
                if random() < p:
                    self.add_edge([i, j])

    def graph_from_edges(self, filename, directed=0):
        """
        Wczytuje graf z pliku tekstowego, który w każdej linii zawiera opis jednej krawędzi (pary słów),
        ewentualnie jednego wierzchołka (pojedyncze słowo). Jako wynik zwraca graf w formie listy sąsiedztwa
        Plik musi być w bierzącym katalogu lub filename zawierać całą ścieżkę do pliku.
        Funkcja zmodyfikowana - wczytuje także grafy z etykietowanymi krawędziami (np. ważone)
        """
        file = open(filename, "r")  # otwarcie pliku do odczytu
        for line in file:  # dla każdej linii w pliku
            words = line.split()  # rozbijam linię na słowa
            if len(words) == 1:  # jedno słowo - wierzchołek
                self.add_vertex(words[0])
            elif len(words) == 2:  # dwa słowa - opis krawędzi
                if directed:
                    self.add_arc((words[0], words[1]))
                else:
                    self.add_edge((words[0], words[1]))
            elif len(words) >= 3:  # więcej słów - używam trzech pierwszych - etykietowane krawędzie
                if directed:
                    self.add_arc((words[0], words[1]))
                    self.graph[words[0]][-1] = (words[1], words[2])
                else:
                    self.add_edge((words[0], words[1]))
                    self.graph[words[0]][-1] = (words[1], words[2])
                    self.graph[words[1]][-1] = (words[0], words[2])
        file.close()
