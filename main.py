#
# Instituto Federal de Educação, Ciência e Tecnologia - IFPE
# Campus: Igarassu
# Course: Internet Systems
# Subject: Scientific Methodology
# Professor: Allan Lima - allan.lima@igarassu.ifpe.edu.br
#
# Public Domain Code: Feel free to use, modify, and redistribute it.
#

# Instructions for running the code:
# 1) If the interpreter does not recognize the enum class, install it using:
#    sudo pip install enum34
# 2) Ensure the code runs on Python 3:
#    python3 randomWalkModel.py

import enum
import random
from PIL import Image

# for image generation:
# pip install Pillow

# Enum class to represent the possible states of an individual in the simulation.
class State(enum.Enum):
    healthy = 0  # Healthy state
    exposed = 1 # Exposed state
    infected = 2 # Infected state
    incubation = 3 # Incubation state
    sick = 4  # Sick state
    recovered = 5  # recovered state
    dead = 6  # Dead state


# Class representing each individual in the population.
class Individual:
    def __init__(self, state):
        self.state = state  # Current state of the individual


# Main class implementing the Random Walk Model simulation.
class RandomWalkModel:
    """
    Initializes the simulation's population grid and parameters.

    Args:
        populationMatrixSize (int): The size of the square population matrix.
    """

    def __init__(self, populationMatrixSize, scenario):
        self.scenario = scenario
        self.population = []  # Current state of the population grid
        self.nextPopulation = []  # Next state of the population grid after interactions
        self.currentGeneration = 0  # Current generation count

        # Defines transition probabilities for state changes.
        if(scenario == 1):
            self.transitionProbabilities = [
                [0.70, 0.30, 0.00, 0.00, 0.00, 0.00, 0.00],  # Healthy transitions
                [0.00, 0.40, 0.60, 0.00, 0.00, 0.00, 0.00],  # Exposed transitions
                [0.00, 0.00, 0.40, 0.60, 0.00, 0.00, 0.00],  # Infected transitions
                [0.00, 0.00, 0.00, 0.02, 0.98, 0.00, 0.00],  # Incubation transitions
                [0.00, 0.00, 0.00, 0.00, 0.08, 0.02, 0.90],  # Sick transitions
                [0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00],  # recovered transitions
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00],  # Dead transitions
            ]
            self.contagionFactor = 0.5
        elif(scenario == 2):
            self.transitionProbabilities = [
                [0.95, 0.10, 0.00, 0.00, 0.00, 0.00, 0.00],  # Healthy transitions
                [0.00, 0.80, 0.20, 0.00, 0.00, 0.00, 0.00],  # Exposed transitions
                [0.00, 0.00, 0.40, 0.60, 0.00, 0.00, 0.00],  # Infected transitions
                [0.00, 0.00, 0.00, 0.02, 0.98, 0.00, 0.00],  # Incubation transitions
                [0.00, 0.00, 0.00, 0.00, 0.08, 0.02, 0.90],  # Sick transitions
                [0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00],  # recovered transitions
                [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00],  # Dead transitions
            ]
            self.contagionFactor = 0.3

        # self.contagionFactor = 0.5  # Probability of getting sick after interaction with a sick individual
        self.socialDistanceEffect = 0.0  # Probability of avoiding contact because of social distancing

        # Initializes the population matrix with healthy individuals.
        for i in range(populationMatrixSize):
            self.population.append([])
            self.nextPopulation.append([])
            for j in range(populationMatrixSize):
                self.population[i].append(Individual(State.healthy))
                self.nextPopulation[i].append(Individual(State.healthy))

        # Sets the initial sick individual at the center of the matrix.
        startIndex = int(populationMatrixSize / 2)
        self.population[startIndex][startIndex].state = State.sick
        self.nextPopulation[startIndex][startIndex].state = State.sick
        # print("first case", startIndex, startIndex)

    """
    Determines the next state of an individual based on transition probabilities 
    and processes interactions if the individual is sick.

    Args:
        line (int): The row index of the individual.
        column (int): The column index of the individual.
    """

    def individualTransition(self, line, column):
        individual = self.population[line][column]

        if (individual.state == State.sick or individual.state == State.dead):  # Only sick individuals with spread the virus
            self.computeSocialInteractions(line, column)
        else:
            return

        # TODO: Determines the next state using probabilities for the current state
        probabilities = self.transitionProbabilities[individual.state.value]
        number = random.random()
        cumulativeProbability = 0

        for index in range(len(probabilities)):
            cumulativeProbability += probabilities[index]
            if number <= cumulativeProbability:
                self.nextPopulation[line][column].state = State(index)
                break

    """
    Simulates the possibility of a healthy individual becoming sick 
    after interacting with a sick individual.

    Args:
        individual (Individual): The healthy individual being evaluated.
        neighbour (Individual): The sick neighbor.
    """

    def computeSickContact(self, neighbour):
        number = random.random()
        if (number <= self.contagionFactor):
            neighbour.state = State.sick  # an individual becomes sick

    """
    Evaluates interactions between a sick individual and its neighbors, 
    considering the possibility of contagion.

    Args:
        line (int): The row index of the sick individual.
        column (int): The column index of the sick individual.
    """

    def computeSocialInteractions(self, line, column):
        individual = self.population[line][column]
        initialLine = max(0, line - 1)
        finalLine = min(line + 2, len(self.population))

        # print(line, column)

        for i in range(initialLine, finalLine):
            initialColumn = max(0, column - 1)
            finalColumn = min(column + 2, len(self.population[i]))

            for j in range(initialColumn, finalColumn):
                if (i == line and j == column):  # Skips the individual itself
                    continue

                avoidContact = self.socialDistanceEffect >= random.random()

                if (not avoidContact):
                    neighbour = self.nextPopulation[i][j]
                    if (neighbour.state == State.healthy):
                        # print("->", i, j)
                        self.computeSickContact(neighbour)
                        # print("->", i, j, neighbour.state)

    """
    Advances the simulation by transitioning all individuals 
    to their next state based on current conditions.
    """

    def nextGeneration(self):
        for i in range(len(self.population)):
            for j in range(len(self.population[i])):
                self.individualTransition(i, j)

        # The next population becomes the current one
        for i in range(len(self.population)):
            for j in range(len(self.population[i])):
                self.population[i][j].state = self.nextPopulation[i][j].state

    """Generates a report of the current state counts in the population."""

    def report(self):
        states = list(State)
        cases = [0] * len(states)

        for row in self.population:
            for individual in row:
                cases[individual.state.value] += 1

        return cases

    """Prints the simulation report to the console."""

    def printReport(self, report):
        for cases in report:
            print(cases, '\t', end=' ')
        print()

    """
    Logs column headers representing states if verbose mode is enabled.

    Args:
        verbose (bool): Whether to print the headers.
    """

    def logHeaders(self, verbose):
        if (verbose):
            states = list(State)

            for state in states:
                print(state, '\t', end=' ')

            print()

    """
    Logs the simulation's current state counts if verbose mode is enabled.

    Args:
        verbose (bool): Whether to print the report.
    """

    def logReport(self, verbose):
        if (verbose):
            report = self.report()
            self.printReport(report)

    """
        Runs the simulation for the specified number of generations, 
        logging results if verbose mode is enabled.

        Args:
            generations (int): The number of generations to simulate.
            verbose (bool): Whether to print detailed simulation logs.
        """

    def simulation(self, generations, verbose):
        self.logHeaders(verbose)

        self.logReport(verbose)

        # self.logPopulation(self.population)

        for i in range(generations):
            self.nextGeneration()
            # self.logPopulation(self.population)
            self.logReport(verbose)
            if (i < 5):
                name = 'semana: ' + str(i + 1) + ' mortos: ' + str(self.numberOfDeaths()) + ' cenario:' + str(self.scenario)
                print(name)
                self.printImage(name)
            if (i == 23):
                name = 'semana: ' + str(i + 1) + ' mortos: ' + str(self.numberOfDeaths()) + ' cenario:' + str(self.scenario)
                print(name)
                self.printImage(name)
            # if(i < 5):
            #     model.printImage(str(i) + "generations-" + str(self.scenario))
        # if (i == generations):
        # model.printImage(i)

    """Counts the number of dead individuals in the population."""

    def numberOfDeaths(self):
        deaths = 0

        for row in self.population:
            for individual in row:
                if individual.state == State.dead:
                    deaths += 1
        return deaths

    """Prints the status of each individual in the population on the console, formatted in table form."""

    def logPopulation(self, population):
        for i in range(len(population)):
            for j in range(len(population)):
                print(population[i][j].state.value, '\t', end=' ')
            print()
        print()

    """
        Creates and displays an image of the population after the end of the simulation.
    """

    def printImage(self, name):

        lines = len(self.population)
        columns = len(self.population[0])
        img = Image.new(mode="RGB", size=(columns, lines))

        for i in range(lines):
            for j in range(columns):
                if (self.population[i][j].state == State.healthy):
                    img.putpixel((i, j), (187, 255, 0)) # green
                elif (self.population[i][j].state == State.exposed):
                    img.putpixel((i, j), (255, 227, 0)) # yellow
                elif (self.population[i][j].state == State.infected):
                    img.putpixel((i, j), (166, 0, 255)) # purple
                elif (self.population[i][j].state == State.incubation):
                    img.putpixel((i, j), (255, 153, 0)) # orange
                elif (self.population[i][j].state == State.sick):
                    img.putpixel((i, j), (255, 17, 0)) # red
                elif (self.population[i][j].state == State.recovered):
                    img.putpixel((i, j), (56, 182, 255)) # blue
                elif (self.population[i][j].state == State.dead):
                    img.putpixel((i, j), (0, 0, 0)) # black

        img.save("gen" + str(name) + ".png")
        # img.show()


# MAIN PROGRAM

numberOfRuns = 1 # Number of simulation runs
gridSize = 255  # Size of the population grid
numberOfGenerations = 52  # Number of generations (iterations) per simulation run
scenario = 2

sum = 0
numberOfDeaths = 0

# Run the simulation multiple times and print the number of deaths after each run
for i in range(numberOfRuns):
    model = RandomWalkModel(gridSize, scenario)
    model.simulation(numberOfGenerations, False)
    numberOfDeaths = model.numberOfDeaths()
    sum += numberOfDeaths


    # if(i == 0):
    #     model.printImage("finalresult-" + str(scenario))
print('ultima semana mortos: ' + str(numberOfDeaths))
print('cenario:' + str(scenario) + ' Media de mortos: ' + str(sum / numberOfRuns))
