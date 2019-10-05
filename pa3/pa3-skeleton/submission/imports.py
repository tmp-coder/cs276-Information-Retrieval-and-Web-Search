
# You can add additional imports here
import sys
import pickle as pkl
import array
import os
import timeit
import contextlib
from collections import OrderedDict, Counter
import math

import sys
from base_classes.load_train_data import load_train_data
from base_classes.id_map import IdMap
from base_classes.ndcg import NDCG
from base_classes.query import Query
from base_classes.document import Document
import numpy as np