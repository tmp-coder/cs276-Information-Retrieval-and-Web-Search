
# You can add additional imports here

import sys
import pickle as pkl
import array
import os
import timeit
import contextlib
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from collections import Counter
from collections import OrderedDict
import math

import xgboost as xgb

from base_classes.load_train_data import load_train_data
from base_classes.id_map import IdMap
from base_classes.ndcg import NDCG
from base_classes.query import Query
from base_classes.document import Document