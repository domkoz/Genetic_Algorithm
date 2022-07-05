from random import choices, randint, randrange, random
from typing import List, Callable, Tuple

from utils import graph

Genome = List[int]
Population = List[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], int]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]




# generujemy liste 0 i 1 o dlugosci listy z ktorej wybieramy.
def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


# tworzymy populacje, wzywa funkcje generujemy genom tyle razy, jak duza chcemy miec populacje
def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


# funkcja ta przyjmuje dwa genomy, ucina je w losowym miejscu, a nastepnie zwraca dwa nowe genomy.
def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")

    length = len(a)
    if length < 2:
        return a, b

    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


# funkcja ta bierze genom, z pewnym prawdopodbienstwem zamienia 0 na 1 / 1 na 0 i zwraca nam genom
# w tym celu wybieramy losowy index, jesli random zwroci nam liczbe wieksza niz prawdopodbienstwo, nic nie robi, jesli
# nie robi zamiane.
def mutation(genome: Genome, num: int = 1, probability: float = 0.02) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome


def population_fitness(population: Population, fitness_func: FitnessFunc) -> int:
    return sum([fitness_func(genome) for genome in population])


# wybiera sposrod rozwiazan te, ktore zostana uzyte do nastepnej generacji. Dokladnie wybiera 2 rodzicow. Rodzice z
# wiekszym fitnesem powinni byc bardziej prawdopodobnie wybrani. funkcja fitness ktora wybralismy, przybiera jak
# parametry liste elementow oraz limit wagowy, ktore sa potrzebne w tym dokladnym przypadku. To rozwiazanie pozwala
# nam zaimpelemntowac ten kod do innych problemow.
def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(gene) for gene in population],
        # jako wage wybieramy wartosc fittnes, czym wieksza tym lepiej
        k=2  # dwa razy wbieramy takie elementy z naszej populacji, poniewaz chcemy otrzymac pare
    )


def sort_population(population: Population, fitness_func: FitnessFunc) -> Population:
    return sorted(population, key=fitness_func, reverse=True)


def bonus(graf: graph.Graph, genome: Genome) -> Genome:
    kopia = genome
    temporary = dict(zip(graf.vertices_list(), kopia))
    for i, vertex in enumerate(graf.vertices_list()):
        if kopia[i] == 0:
            can_he = 0
            for g in graf.team_mate(vertex):
                if g == vertex:
                    pass
                elif temporary[g] == 1:
                    can_he += 1
            if can_he == 0:
                kopia[i] = 1
    return kopia


def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        # kiedy funkcja przekroczy ponizszy limit skonczylismy.
        fitness_limit: int,
        # gdyby nasza funkcja nie osiagnela fitness limit, skonczy sie po generation_ limit
        generation_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,

        ) \
        -> Tuple[Population, int]:
    # tworzymy nasza pierwsza populacje
    population = populate_func()

    for i in range(generation_limit):  # tyle petli ile generacji
        # sortujemy nasza populacje od tych z najwieksza wartoscia fitness
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        # jesli nasza populacja spelnia nasz limit, konczymy
        if fitness_func(population[0]) >= fitness_limit:
            break
        # wybieramy dwa najbardziej obiecujace rozwiazania
        next_generation = population[0:2]

        # generuejmy pozostale rozwiazania dla nastepnej  populacji przechodzimy po polowie dlugosci naszej populacji
        # ? Dlaczego ? -1 poniewaz wybralismy juz 2 najlepsze rozwiazania z obecnej. Za kazdym razem wybieramy
        # rodzicow nastepnie wybieramy dwojke dzieci do naszej nastepnej generacji, potem je mutujemy.
        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    return population, i
