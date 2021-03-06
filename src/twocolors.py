# RHC should solve instantly. even for large number of queen
import sys
import os
import time

sys.path.append("/Users/alexisdurocher/Docs/YouTheaSea/P18/cours/MachineLearning/AS2/adurocher3/ABAGAIL/ABAGAIL.jar")
import java.io.FileReader as FileReader
import java.io.File as File
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscretePermutationDistribution as DiscretePermutationDistribution
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution

import opt.SwapNeighbor as SwapNeighbor
import opt.ga.SwapMutation as SwapMutation
import dist.Distribution as Distribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.EvaluationFunction as EvaluationFunction
import opt.example.TwoColorsEvaluationFunction as TwoColorsEvaluationFunction
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.HillClimbingProblem as HillClimbingProblem
import opt.NeighborFunction as NeighborFunction
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.example.FourPeaksEvaluationFunction as FourPeaksEvaluationFunction
import opt.ga.CrossoverFunction as CrossoverFunction
import opt.ga.SingleCrossOver as SingleCrossOver
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.GeneticAlgorithmProblem as GeneticAlgorithmProblem
import opt.ga.MutationFunction as MutationFunction
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.ga.UniformCrossOver as UniformCrossOver
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import opt.prob.ProbabilisticOptimizationProblem as ProbabilisticOptimizationProblem
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.ga.NQueensFitnessFunction as NQueensFitnessFunction
import opt.example.CountOnesEvaluationFunction as CountOnesEvaluationFunction
from array import array
from time import clock
from itertools import product

"""
Commandline parameter(s):
   none
"""

	
maxIters = 5001
numTrials=1
k = 2 # number of colors
N = 50 * k # number of value 
fill = [2] * N
ranges = array('i', fill)
outfile = './output/100_WOCOL_@ALG@_@N@_LOG.csv'


ef = TwoColorsEvaluationFunction();
cf = UniformCrossOver();
odd = DiscreteUniformDistribution(ranges)
nf = DiscreteChangeOneNeighbor(ranges)
mf = DiscreteChangeOneMutation(ranges)
df = DiscreteDependencyTree(.1, ranges)
hcp = GenericHillClimbingProblem(ef, odd, nf)
gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
pop = GenericProbabilisticOptimizationProblem(ef, odd, df)



#MIMIC
for t in range(numTrials):
	for samples, keep, m in product([200],[60,100],[0.9]):
		fname = outfile.replace('@ALG@', 'MIMIC{}_{}_{}'.format(samples, keep, m)).replace('@N@',str(t+1))
		with open(fname,'w') as f:
			f.write('iterations, fitness, time, fevals\n')
		gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
		df = DiscreteDependencyTree(m)
		pop = GenericProbabilisticOptimizationProblem(ef, odd, df)
        
		mimic = MIMIC(samples, keep, pop)
		fit = FixedIterationTrainer(mimic, 100)
		times =[0]
		for i in range(0,maxIters,100):
			start = clock()
			fit.train()
			elapsed = time.clock()-start
			times.append(times[-1]+elapsed)
			fevals = ef.fevals
			score = ef.value(mimic.getOptimal())
			ef.fevals -= 1
			st = '{},{},{},{}\n'.format(i, score, times[-1], fevals)
			print st
			with open(fname,'a+') as f:
				f.write(st)

quit()

#GA
for t in range(numTrials):
	for pop, mate, mutate in product([100],[30],[30]):
		fname = outfile.replace('@ALG@','GA{}_{}_{}'.format(pop, mate, mutate)).replace('@N@',str(t+1))
		with open(fname,'w') as f:
			f.write('iterations,fitness,time,fevals\n')
		gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
		ga = StandardGeneticAlgorithm(pop, mate, mutate, gap)
		fit = FixedIterationTrainer(ga, 100)
		times =[0]
		for i in range(0,maxIters,100):
			start = clock()
			fit.train()
			elapsed = time.clock()-start
			times.append(times[-1]+elapsed)
			fevals = ef.fevals
			score = ef.value(ga.getOptimal())
			ef.fevals -= 1
			st = '{},{},{},{}\n'.format(i,score,times[-1],fevals)
			print st
			with open(fname,'a+') as f:
				f.write(st)

quit()

#RHC
for t in range(numTrials):
	fname = outfile.replace('@ALG@','RHC').replace('@N@',str(t+1))
	with open(fname,'w') as f:
		f.write('iterations, fitness, time, fevals\n')
	hcp = GenericHillClimbingProblem(ef, odd, nf)
	rhc = RandomizedHillClimbing(hcp)
	fit = FixedIterationTrainer(rhc, 100)
	times =[0]
	for i in range(0, maxIters, 100):
		start = clock()
		fit.train()
		elapsed = time.clock()-start
		times.append(times[-1]+elapsed)
		fevals = ef.fevals
		#exit()
		score = ef.value(rhc.getOptimal())
		ef.fevals -= 1
		st = '{},{},{},{}\n'.format(i,score,times[-1],fevals)
		print st	
		with open(fname,'a+') as f:
			f.write(st)
 

# SA
for t in range(numTrials):
	for CE in [0.75]:
		fname = outfile.replace('@ALG@','SA{}'.format(CE)).replace('@N@',str(t+1))
		with open(fname,'w') as f:
			f.write('iterations,fitness,time,fevals\n')
		hcp = GenericHillClimbingProblem(ef, odd, nf)
		sa = SimulatedAnnealing(1E10, CE, hcp)
		fit = FixedIterationTrainer(sa, 100)
		times =[0]
		for i in range(0,maxIters,100):
			start = clock()
			fit.train()
			elapsed = time.clock()-start
			times.append(times[-1]+elapsed)
			fevals = ef.fevals
			score = ef.value(sa.getOptimal())
			ef.fevals -= 1
			st = '{},{},{},{}\n'.format(i,score,times[-1],fevals)
			print st
			with open(fname,'a+') as f:
				f.write(st)

quit()



