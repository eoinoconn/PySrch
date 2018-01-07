from Python.Encoding.chromosome import Chromosome, LAYER_DEPTH, INPUT_SHAPE
import random
import logging


def mutate(chromosome):
    mutation_done = False

    while not mutation_done:
        rand = random.randrange(0, 2)
        logging.info("mutating chromosome, rand = %f", rand)

        # remove layer
        # there should always be at least 3 layers in the chromosome.
        # the input convolutional, the flatten layer and the dense layer.
        if chromosome.__len__() > 3 and rand == 0:
            logging.info("removing layer")
            remove_layer(chromosome)
            mutation_done = True
        # add layer
        elif rand == 1:
            logging.info("adding layer")
            add_layer(chromosome)
            mutation_done = True
        # change layer
        elif rand == 2:
            logging.warning("attempting unimplemented mutation")
            raise NotImplementedError
        # change hyperparameter
        elif rand == 3:
            logging.warning("attempting unimplemented mutation")
            raise NotImplementedError


def create_parent():
    logging.info("creating parent chromosome")
    chromosome = Chromosome()
    chromosome.add_layer(convolutional_layer(input_layer=True))
    chromosome.add_layer(flatten_layer())
    chromosome.add_layer(dense_layer())
    logging.info("parent chromosome created")
    return chromosome


# The first value of the layer array is 2 for a convolutional layer
# Other variables:
#   1   layer units
#   2   input layer
#   3   window size
#   4   activation
def convolutional_layer(input_layer=False):
    layer = [0 for x in range(0, LAYER_DEPTH)]
    layer[0] = 2    # Sets convolutional layer
    layer[1] = random.randrange(1, 16) * 16     # sets layer units
    if input_layer:
        layer[2] = 1    # Sets input layer
    else:
        layer[2] = 0    # Sets hidden layer
    layer[3] = random.randrange(1, 5)   # Sets slide size
    layer[4] = set_activation()
    logging.info("added conv layer")
    return layer


def flatten_layer():
    layer = [0 for x in range(0, LAYER_DEPTH)]
    layer[0] = 3
    return layer


# The first value of the layer array is 1 for a dense layer
# Other variables:
#   1   layer units
#   2   input layer
#   3   <unused>
#   4   activation
def dense_layer(input_layer=False):
    layer = [0 for x in range(LAYER_DEPTH)]
    layer[0] = 1
    layer[1] = random.randrange(1, 16) * 16  # sets layer units
    if input_layer:
        layer[2] = 1    # Sets input layer
    else:
        layer[2] = 0    # Sets hidden layer
    layer[4] = set_activation()
    logging.info("added dense layer")
    return layer


def set_activation():
    ran_active = random.randrange(0, 3)
    if ran_active == 0:
        return 'relu'
    elif ran_active == 1:
        return 'sigmoid'
    elif ran_active == 2:
        return 'linear'
    else:
        return 'elu'


def add_layer(chromosome):
    change_layer = False
    while not change_layer:
        rand = random.randrange(0, chromosome.__len__())
        logging.info("adding layer, rand = %d", rand)
        layer = chromosome.get_layer(rand)
        if layer[0] == 1:
            new_layer = dense_layer()
            change_layer = True
        elif layer[0] == 2:
            new_layer = convolutional_layer()
            change_layer = True
        else:
            continue

    for i in range(rand+1, chromosome.__len__()+1):
        temp_layer = chromosome.get_layer(i)
        chromosome.add_layer(new_layer, i)
        new_layer = temp_layer


def remove_layer(chromosome):
    while True:
        # randomly pick layer to remove
        rand = random.randrange(0, chromosome.__len__())
        layer = chromosome.get_layer(rand)
        # must not pick flatten layer which acts as border between convolutional and dense layers
        # must not pick dense or conv layer if only 1 is present
        if layer[0] == 3 or \
                (layer[0] == 2 and chromosome.num_conv() < 2) or \
                (layer[0] == 1 and chromosome.num_dense() < 2):
            continue
        logging.info("removed layer type %d", layer[0])
        chromosome.remove_layer(rand)
        for i in range(rand+1, chromosome.__len__()):
            temp_layer = chromosome.get_layer(i+1)
            chromosome.add_layer(temp_layer, i)
        break
