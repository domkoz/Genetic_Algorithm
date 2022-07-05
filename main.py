from algorithm import geneticAlgorithm
from problem import NASA
from functools import partial


def save_high_score(score, value):
    with open("record.txt", mode="w") as record:
        record.write(f"{score} for {value}")


def read_high_score():
    with open("record.txt", mode="r") as record:
        return int(record.read().split()[0])


things = NASA.scientists
counter = read_high_score()

things.print_graph()

population, generations = geneticAlgorithm.run_evolution(
    populate_func=partial(geneticAlgorithm.generate_population, 10, things.count_vertices()),
    fitness_func=partial(NASA.fitness, things),
    fitness_limit=6000,
    generation_limit=10
)

result = 0
for z in population[0]:
    if z == 1:
        result += 1
    if result > counter:
        counter = result
        save_high_score(counter, population[0])

print(f" result {result}")

correction = NASA.bonus(things, population[0])
if NASA.fitness(things, correction) > result:
    save_high_score(NASA.fitness(things, correction), correction)
    print(read_high_score())
