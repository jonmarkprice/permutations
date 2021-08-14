# from typing import
# type Permutation

from itertools import chain

class Permutation:


    def __init__(self, cardinality, mapping, name = None):
        self.cardinality = cardinality
        self.mapping = mapping
        self.name = name


    def __eq__(self, other):
        return self.mapping == other.mapping


    # TODO: test
    def __mul__(self, other):
        return compose(self, other)


    # TODO: replace 'index' with 'key'
    def __find_cycles(self):
        # print('finding cycles')
        cycles = []
        current_cycle = []
        indices = set(range(1, self.cardinality + 1))

        # prime loop
        # index = indices.pop()
        # current_cycle.append(index)

        # while indices:
        #     result = self.compute(result)
        #     # if result == index: # index was just added to current_cycle
        #     if result == current_cycle[0]:
        #         # found cycle
        #         cycles.append(current_cycle)
        #         current_cycle = []

        #         # start new cycle
        #         index = indices.pop()
        #     else:
        #         # keep going
        #         current_cycle.append(result)
        #         index = result

        # try without needing to prime
        while indices:
            # print("indices: ", indices)
            # print("current cycle ", current_cycle)
            if not current_cycle: # empty
                index = indices.pop()
                # print("index ", index)
                current_cycle.append(index)
            # print('index: ', index)
            result = self.mapping[index] # compute(index)
            # print('result ', result)

            if result == current_cycle[0]:
                # found cycle
                if len(current_cycle) > 1:
                    cycles.append(current_cycle)
                current_cycle = []
            else:
                # keep going
                indices.remove(result)
                current_cycle.append(result)
                index = result # in order for top of loop to compute new result
        
        if current_cycle:
            if len(current_cycle) > 1:
                cycles.append(current_cycle)
        # print(cycles)
        return cycles


    def __str__(self):
        cycles = self.__find_cycles()
        if cycles == []:
            return 'id'
        else:
            return ''.join(('(' + ' '.join(map(str, cycle)) + ')' for cycle in cycles))


    def pow(self, power):
        if power == 0:
            return identity(self.cardinality)
        elif power < 0:
            # TODO: should unit test
            # also unit test that -power = inv(power) = power(inv)
            return (self.inverse()).pow(-power)
        else:
            mapping = {}
            # steps = list(reversed(permutations))
            keys = set(range(1, self.cardinality + 1))
            # while keys:
            #     key = keys.pop()
            for key in keys:
                # print('key ', key)
                result = key
                for _ in range(power):
                    # print(step.name)
                    result = self.mapping[result]
                    # print('result ', result)
                mapping[key] = result
                # print(f'setting {key} to {result}')

            # mapping[]
            return Permutation(self.cardinality, mapping)


    def inverse(self):
        mapping = {}
        for key in self.mapping:
            mapping[self.mapping[key]] = key
        return Permutation(self.cardinality, mapping)


    def ext(self, n):
        if n < self.cardinality:
            raise ValueError(f'Cardinality {self.cardinality} is greater than extension: {n}')
        elif n == self.cardinality:
            return self

        mapping = self.mapping.copy()
        for key in range(self.cardinality + 1, n + 1):
            mapping[key] = key
        return Permutation(n, mapping)


def identity(cardinality):
    return Permutation(cardinality, {x: x for x in range(1, cardinality + 1)})


def successor(cardinality):
    mapping = {x: x + 1 for x in range(1, cardinality)}
    mapping[cardinality] = 1
    return Permutation(cardinality, mapping)


def predecessor(cardinality):
    mapping = {x: x - 1 for x in range(2, cardinality + 1)}
    mapping[1] = cardinality
    return Permutation(cardinality, mapping)


def tr(i, j, cardinality) -> Permutation:
    mapping = {x: x for x in range(1, cardinality + 1)}
    mapping[i] = j
    mapping[j] = i
    return Permutation(cardinality, mapping)


def compose(*permutations):
    # make sure we don't use permutations twice since
    # it's a generated
    steps = list(reversed(permutations))

    # print('steps: ', steps)

    n = max(p.cardinality for p in steps)
    mapping = {}

    # print(f'cardinality: {n}')
    # steps_extended = [p.ext(n) for p in steps]

    # TODO: check that ext(n) preserves permutations    

    # steps = list(reversed(permutations))
    keys = set(range(1, n + 1))
    for key in keys:
        # print('key ', key)
        result = key
        for step in steps:
            # print(step.name)
            # print(step.mapping)
            # result = step.ext(n).mapping[result]
            result = step.ext(n).mapping[result]
            # print('result ', result)
        mapping[key] = result
        # print(f'setting {key} to {result}')

    # mapping[]
    return Permutation(n, mapping)


# TODO: check that each 1...n appears exacty once
# TODO: add explicit (optional) cardinality
# List[List[int]] -> Permutation:
# Index is a bad name... 
def make_map(cycles, n = None):
    if not cycles:
        raise ValueError(f'Cycles is empty')

    maximum = 1
    specified = set()
    for element in chain(*cycles):
        if element in specified:
            raise ValueError(f'Duplicate element in cycle: {element}')
        else:
            if element > maximum:
                maximum = element
            specified.add(element)

    mapping = {}
    if n is None:
        n = maximum
    all_keys = set(range(1, n + 1))
    unspecified = all_keys - specified

    for cycle in cycles:
        for i, key in enumerate(cycle):
            if len(cycle) > i + 1:
                # case len = 3, i = 0,1
                mapping[key] = cycle[i + 1]
            else: # last index
                # case len = 1, i = 0
                # case len = 3, i = 2
                mapping[key] = cycle[0]
    for key in unspecified:
        mapping[key] = key

    return Permutation(len(mapping), mapping)

# TODO def make_map (from str)
# TODO def is_inverse
