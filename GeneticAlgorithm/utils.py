from GeneticAlgorithm.genes import Genes
import configparser
import logging
import csv


def get_config():
    config = configparser.ConfigParser()
    config.read('GeneticAlgorithm/Config/training_parameters.ini')
    return config


def config_min_max_interval(config_name):
    config = get_config()
    config = config[config_name]
    minimum = int(config['minimum'])
    maximum = int(config['maximum'])
    interval = int(config['interval'])
    return minimum, maximum, interval


def check_valid_geneset(genes, logger=logging.getLogger(__name__)):
    """
    function to check if the mutated geneset has
    valid dimensions after pooling is altered
    it does this by calculating the smallest dimension of the 
    geneset at the last convolutional layer
    """

    current_dimension = genes.input_shape[0]
    logger.info("checking for valid geneset; conv dimensions %d", current_dimension)
    for layer in genes.iterate_layers():
        if layer[0] == 2:
            if layer[7] == 'same':
                padding = 1
            else:
                padding = 0
            current_dimension=conv_layer_output_size(current_dimension, layer[3], layer[2], padding)
            if layer[5] is not 0:
                current_dimension = pooling_layer_output_size(current_dimension, layer[6], layer[8])
        elif layer[0] == 3:
            break
    if current_dimension < 1:
        logger.info("Invalid geneset, dimensions less than 0, Dimension: %d", current_dimension)
        return False  # invalid geneset
    else:
        logger.info("valid geneset found, min dimension: %d", current_dimension)
        return True  # valid geneset


def conv_layer_output_size(input_width, kernel_size, stride_size, padding_amount):
    return (input_width-kernel_size + (2 * padding_amount))/stride_size + 1


def pooling_layer_output_size(input_width, kernel_size, stride_size):
    return (input_width - kernel_size)/stride_size + 1


def load_known_architecture(file_name, input_shape):
    chromosome = Genes(input_shape)
    with open(file_name, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            line = line
            for j, x in enumerate(line):
                line[j] = convert(x)

            if i == 0:
                chromosome.hyperparameters = line
            else:
                chromosome.add_layer(line)
    return chromosome


def convert(x):
    """
    Converts string to int, float or leaves  it as a string
    :param x:
    :return:
    """

    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x


def intermittent_logging(chromosome, generation_num):
    with open('GeneticAlgorithm/logs/trend.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([generation_num, ',',
                             chromosome.id, ',',
                             chromosome.age, ',',
                             chromosome.accuracy, ',',
                             chromosome.fitness, ',',
                             chromosome.parameters, ',',
                             chromosome.__len__(), ',',
                             chromosome.num_conv_layers(), ',',
                             chromosome.num_dense_layers(), ',',
                             chromosome.num_incep_layers(), ',',
                             ])


def setup_csvlogger():
    with open('GeneticAlgorithm/logs/trend.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['generation', ',',
                             'id', ',',
                             'Age', ',',
                             'Fitness', ',',
                             'Accuracy', ',',
                             'Parameters', ',',
                             'Num Layers', ',',
                             'Num Conv Layers', ',',
                             'Num Dense Layers', ',',
                             'Num Incep Layers'])
