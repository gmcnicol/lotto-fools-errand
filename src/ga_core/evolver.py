"""Generic genetic algorithm utilities."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, Generic, List, Tuple, TypeVar

Chromosome = TypeVar("Chromosome")
Score = float

# Function type aliases
InitFunc = Callable[[int], List[Chromosome]]
FitnessFunc = Callable[[Chromosome], Score]
MutateFunc = Callable[[Chromosome], Chromosome]
CrossoverFunc = Callable[[Chromosome, Chromosome], Chromosome]

SelectFunc = Callable[[List[Chromosome], List[Score], int], List[Chromosome]]

# Convergence function: returns True when evolution should stop
ConvergenceFunc = Callable[[int, List[Score]], bool]


def never_stop(_: int, __: List[Score]) -> bool:
    """Default convergence function that never stops early."""
    return False


class NoImprovement:
    """Stop after no improvement is seen for a number of generations."""

    def __init__(self, window: int) -> None:
        self.window = window
        self.best = float("-inf")
        self.no_improve = 0

    def __call__(self, _: int, history: List[Score]) -> bool:
        current = history[-1]
        if current > self.best:
            self.best = current
            self.no_improve = 0
        else:
            self.no_improve += 1
        return self.no_improve >= self.window


def default_select(population: List[Chromosome],
                   scores: List[Score],
                   elite_size: int) -> List[Chromosome]:
    """Roulette-wheel selection with elitism."""
    paired = sorted(zip(scores, population), key=lambda x: x[0], reverse=True)
    elites = [p for _, p in paired[:elite_size]]
    rest_scores, rest_pop = zip(*paired[elite_size:]) if len(paired) > elite_size else ([], [])
    if rest_pop:
        # Normalize scores to positive values
        min_score = min(rest_scores)
        adj_scores = [s - min_score + 1e-9 for s in rest_scores]
        chosen = random.choices(list(rest_pop), weights=adj_scores, k=len(population) - elite_size)
    else:
        chosen = []
    return elites + chosen


@dataclass
class Evolver(Generic[Chromosome]):
    population_size: int
    init_func: InitFunc
    fitness_func: FitnessFunc
    mutate_func: MutateFunc
    crossover_func: CrossoverFunc
    select_func: SelectFunc = default_select
    elite_size: int = 1
    convergence_func: ConvergenceFunc = never_stop
    history: List[Tuple[Chromosome, Score]] = field(default_factory=list)

    def initialize(self) -> List[Chromosome]:
        return self.init_func(self.population_size)

    def score_population(self, population: List[Chromosome]) -> List[Score]:
        return [self.fitness_func(ch) for ch in population]

    def evolve_generation(self, population: List[Chromosome], scores: List[Score]) -> Tuple[List[Chromosome], List[Score]]:
        parents = self.select_func(population, scores, self.elite_size)
        next_pop = parents[:self.elite_size]
        while len(next_pop) < self.population_size:
            p1, p2 = random.sample(parents, 2)
            child = self.crossover_func(p1, p2)
            child = self.mutate_func(child)
            next_pop.append(child)
        next_scores = self.score_population(next_pop)
        return next_pop, next_scores

    def run(self, generations: int) -> Tuple[Chromosome, Score]:
        population = self.initialize()
        scores = self.score_population(population)
        best_idx = int(max(range(len(scores)), key=lambda i: scores[i]))
        best = population[best_idx]
        best_score = scores[best_idx]
        self.history.append((best, best_score))
        if self.convergence_func(0, [best_score]):
            return best, best_score

        for gen in range(1, generations + 1):
            population, scores = self.evolve_generation(population, scores)
            idx = int(max(range(len(scores)), key=lambda i: scores[i]))
            if scores[idx] > best_score:
                best_score = scores[idx]
                best = population[idx]
            self.history.append((best, best_score))
            if self.convergence_func(gen, [s for _, s in self.history]):
                break

        return best, best_score
