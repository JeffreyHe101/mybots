from solution import SOLUTION
import constants as c
import copy
import os
import matplotlib.pyplot as plt
class PARALLEL_HILLCLIMBER:
    def __init__(self):
        self.parents = {}
        self.fitnesslist = []
        self.nextAvailableID = 0
        self.count = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID +=1
        #os.system(del )
#        self.parent = SOLUTION()
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
    #print("Files in %r: %s" % (cwd, files))
        for i in files:
            if i[:3] == "fit":
                print(i)
                os.remove(i)
            elif i[:3] == "bra":
                print(i)
                os.remove(i)


    def Evolve_For_One_Generation(self):
        self.count += 1
        print(self.count)
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Select()
       # print(self.parents.fitness, self.child.fitness)

    def Spawn(self):
        self.children = {}
        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].SetID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for key in self.children:
            self.children[key].Mutate()
        #print(self.parent.weights)
        #print(self.child.weights)

    def Select(self):
        fitness_5 = []
        for i in range(c.populationSize):
            if self.parents[i].fitness < self.children[i].fitness:
              #  print("CHANGE")
              #  print(self.parents[i].fitness)
               # #print(self.children[i].fitness)
                self.parents[i] = self.children[i]
            fitness_5.append(self.parents[i].fitness)
        self.fitnesslist.append(fitness_5)
    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Show_Best(self):
        best_fit = self.parents[0].fitness
        best_parent = self.parents[0]
        d = 0
        for i in self.parents:
            if self.parents[i].fitness > best_fit:
                best_fit = self.parents[i].fitness
                best_parent = self.parents[i]
                d = i
        #print("Best Fitness Score: " + str(best_parent.fitness))
        #print(self.fitnesslist,)

        self.parents[d].Start_Simulation("GUI")
        x_var = [i for i in range(0, c.numberOfGenerations)]
        for i in range(c.populationSize):
            plt.plot(x_var, [item[i] for item in self.fitnesslist], label = "num" + str(i+1))
        plt.show()
        #self.parent.Evaluate("GUI")
      #  print("ADSADSADS")

    def Evaluate(self, solutions):
        for i in range(c.populationSize):
            solutions[i].Start_Simulation("DIRECT")
       #     print("startid: " + str(solutions[i].myID))
            #self.parents[i].Start_Simulation("DIRECT", self.nextAvailableID)
        for j in range(c.populationSize):
        #    print("id: " + str(solutions[j].myID))
            solutions[j].Wait_For_Simulation_To_End()