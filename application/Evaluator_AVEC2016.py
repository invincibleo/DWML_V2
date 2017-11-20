#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 20.11.17 11:50
# @Author  : Duowei Tang
# @Site    : https://iiw.kuleuven.be/onderzoek/emedia/people/phd-students/duoweitang
# @File    : Evaluator_AVEC2016
# @Software: PyCharm Community Edition

import numpy as np

class Evaluator_AVEC2016(object):
    def __init__(self):
        self.results = dict()

    def evaluate(self, truth, prediction):
        pred_mean = np.mean(prediction, -1);
        ref_mean = np.mean(truth, -1);

        pred_var = np.var(prediction, -1);
        ref_var = np.var(truth, -1);

        covariance = np.mean(np.multiply((prediction - pred_mean), (truth - ref_mean)), -1);

        CCC = (2 * covariance) / (pred_var + ref_var + (pred_mean - ref_mean) ** 2);
        self.results["CCC"] = CCC

    def results(self):
        return self.results