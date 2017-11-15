import unittest
import argparse
from hyperopt import fmin, tpe, hp

import os, sys
sys.path.append(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])

from application.Dataset_AVEC2016 import *
from application.LearnerInceptionV3 import LearnerInceptionV3
from core.evaluation import DCASE2016_EventDetection_SegmentBasedMetrics
import datetime
import tensorflow as tf

DATASET_DIR = "/media/invincibleo/Windows/Users/u0093839/Box Sync/PhD/Experiment/DWML_V2/AVEC2016"

class MyTestCase(unittest.TestCase):
    def test_something(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--data_dir',
            type=str,
            default='',
            help='Path to folders of labeled audios.'
        )
        parser.add_argument(
            '--learning_rate',
            type=float,
            default=0.001,
            help='How large a learning rate to use when training.'
        )
        parser.add_argument(
            '--testing_percentage',
            type=int,
            default=10,
            help='What percentage of images to use as a test set.'
        )
        parser.add_argument(
            '--validation_percentage',
            type=int,
            default=10,
            help='What percentage of images to use as a validation set.'
        )
        parser.add_argument(
            '--train_batch_size',
            type=int,
            default=256,
            help='How many images to train on at a time.'
        )
        parser.add_argument(
            '--test_batch_size',
            type=int,
            default=-1,
            help="""\
            How many images to test on. This test set is only used once, to evaluate
            the final accuracy of the model after training completes.
            A value of -1 causes the entire test set to be used, which leads to more
            stable results across runs.\
            """
        )
        parser.add_argument(
            '--validation_batch_size',
            type=int,
            default=100,
            help="""\
            How many images to use in an evaluation batch. This validation set is
            used much more often than the test set, and is an early indicator of how
            accurate the model is during training.
            A value of -1 causes the entire validation set to be used, which leads to
            more stable results across training iterations, but may be slower on large
            training sets.\
            """
        )
        parser.add_argument(
            '--time_resolution',
            type=float,
            default=1,
            help="""\
            The hop of the FFT in sec.\
            """
        )
        parser.add_argument(
            '--fs',
            type=int,
            default=44100,
            help="""\
            The sampling frequency if an time-series signal is given\
            """
        )
        parser.add_argument(
            '--num_second_last_layer',
            type=int,
            default=512,
            help="""\
            \
            """
        )
        parser.add_argument(
            '--drop_out_rate',
            type=float,
            default=0.9,
            help="""\
            \
            """
        )
        parser.add_argument(
            '--coding',
            type=str,
            default='number',
            help="""\
            one hot encoding: onehot, k hot encoding: khot, continues value: number
            \
            """
        )
        parser.add_argument(
            '--parameter_dir',
            type=str,
            default="parameters",
            help="""\
            parameter folder
            \
            """
        )
        FLAGS, unparsed = parser.parse_known_args()


        dataset = Dataset_AVEC2016(dataset_dir=DATASET_DIR, flag=FLAGS, normalization=True, dimension=40, using_existing_features=False)
        learner = LearnerInceptionV3(dataset=dataset, learner_name='InceptionV3', flag=FLAGS)
        evaluator = DCASE2016_EventDetection_SegmentBasedMetrics(class_list=dataset.label_list, time_resolution=FLAGS.time_resolution)

        # dataset.get_batch_data('training', 10, (-1, 40, 1))

        learner.learn()
        truth, prediction = learner.predict()
        evaluator.evaluate(truth, prediction)
        results = evaluator.results()
        print('F:' + str(results['class_wise_average']['F']) + '\n')
        print('ER' + str(results['class_wise_average']['ER']) + '\n')

        results_dir_addr = 'tmp/results/'
        current_time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        if not tf.gfile.Exists(results_dir_addr):
            tf.gfile.MakeDirs(results_dir_addr)
            hash_FLAGS = hashlib.sha1(str(FLAGS)).hexdigest()
            results_file_dir = os.path.join(results_dir_addr, dataset.dataset_name, hash_FLAGS)
            tf.gfile.MakeDirs(results_file_dir)
            json.dump(results, open(results_file_dir + '/results_' + current_time_str + '.json', 'wb'), indent=4)
            with open(results_file_dir + 'FLAGS_' + current_time_str + '.txt', 'wb') as f:
                f.write(str(FLAGS))

if __name__ == '__main__':
    unittest.main()