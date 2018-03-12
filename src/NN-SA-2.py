#! /Users/alexisdurocher/jython2.7.0/bin/jython
# jython script for nn backprop on Pima dataset"

import os
import csv
import time
import sys
# access the abagail library
sys.path.append("/Users/alexisdurocher/Docs/YouTheaSea/P18/cours/MachineLearning/AS2/adurocher3/ABAGAIL/ABAGAIL.jar")
from func.nn.backprop import BackPropagationNetworkFactory
from shared import SumOfSquaresError, DataSet, Instance
from opt.example import NeuralNetworkOptimizationProblem
from func.nn.backprop import RPROPUpdateRule
import opt.SimulatedAnnealing as SimulatedAnnealing

from func.nn.activation import RELU


# based on parameters tuning 
# we use RELU and (100,100,100)
INPUT_LAYER = 7
HIDDEN_LAYER1 = 60
HIDDEN_LAYER2 = 60
OUTPUT_LAYER = 1
TRAINING_ITERATIONS = 3300
OUTFILE = './output/NN/4_XXX_2_LOG.csv'

# Retrieving data and basic checks

# 1st classification problems : Pima binary classification probs
# Building subsets
def initialize_instances(infile):
    """Read the m_trg.csv CSV data into a list of instances."""
    instances = []

    # Read in the CSV file
    with open(infile, "r") as dat:
        reader = csv.reader(dat)

        for row in reader:
            instance = Instance([float(value) for value in row[:-1]])
            instance.setLabel(Instance(0 if float(row[-1]) < 2 else 1))
            instances.append(instance)

    return instances


def errorOnDataSet(network, ds, measure):
    N = len(ds)
    error = 0.
    correct = 0
    incorrect = 0
    for instance in ds:
        network.setInputValues(instance.getData())
        network.run()
        actual = instance.getLabel().getContinuous()
        predicted = network.getOutputValues().get(0)
        predicted = max(min(predicted,1),0)
        if abs(predicted - actual) < 0.5:
            correct += 1
        else:
            incorrect += 1
        output = instance.getLabel()
        output_values = network.getOutputValues()
        example = Instance(output_values, Instance(output_values.get(0)))
        error += measure.value(output, example)
    MSE = error/float(N)
    acc = correct/float(correct+incorrect)
    return MSE, acc


def train(oa, network, oaName, training_ints, testing_ints, measure):
    """Train a given network on a set of instances.
    """
    print "\nError results for %s\n---------------------------" % (oaName,)
    times = [0]
    for iteration in xrange(TRAINING_ITERATIONS):
        start = time.clock()
        oa.train()
        elapsed = time.clock()-start
        times.append(times[-1]+elapsed)
        if iteration % 10 == 0:
            MSE_train, acc_train = errorOnDataSet(network, training_ints, measure)
            MSE_test, acc_test = errorOnDataSet(network, testing_ints, measure)
            txt = '{},{},{},{},{},{}\n'.format(
                iteration,
                MSE_train, MSE_test,
                acc_train, acc_test,
                times[-1])
            print txt
            with open(OUTFILE.replace('XXX',oaName),'a+') as f:
                f.write(txt)


def main(CE):
    oa_name = "SA{}".format(CE)
    with open(OUTFILE.replace('XXX',oa_name),'w') as f:
        f.write('{},{},{},{},{},{}\n'.format('iteration','MSE_train','MSE_test','acc_train','acc_tst','elapsed'))
   
    
    training_data = initialize_instances('../data/Pima-train.csv')
    testing_data = initialize_instances('../data/Pima-test.csv')
    print(len(training_data))
    #testing_ints = initialize_instances('m_test.csv')
    #validation_ints = initialize_instances('m_val.csv')

    factory = BackPropagationNetworkFactory()
    measure = SumOfSquaresError()
    data_set = DataSet(training_data)
    relu = RELU()
    rule = RPROPUpdateRule()
    classification_network = factory.createClassificationNetwork(
        [INPUT_LAYER, HIDDEN_LAYER1, HIDDEN_LAYER2, OUTPUT_LAYER],
        relu
    )
    nnop = NeuralNetworkOptimizationProblem(data_set, classification_network, measure)
    oa = SimulatedAnnealing(1E10, CE, nnop)
    train(
        oa,
        classification_network,
        oa_name, 
        training_data,
        testing_data,
        measure
    )      


if __name__ == "__main__":
    for CE in [0.15,0.35,0.55,0.70,0.95]:
        main(CE)
