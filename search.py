import os   
from parallelHC import PARALLEL_HILLCLIMBER
phc = PARALLEL_HILLCLIMBER()
phc.Evolve()
phc.Show_Best()
# for i in range(5):
#     os.system("py generatek.py")
#     os.system("py hwi.py")
    