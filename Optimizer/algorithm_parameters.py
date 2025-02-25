import numpy as np
from skopt.space import Integer, Real

# CDRec parameters
CDREC_RANK_RANGE = [i for i in range(10)]  # replace with actual range
CDREC_EPS_RANGE = np.logspace(-6, 0, num=10)  # log scale for eps
# array([1.e-06, 3.59381366e-06, 1.29154967e-05, 4.64158883e-05,
#        1.66810054e-04, 5.99484250e-04, 2.15443469e-03, 7.74263683e-03,
#        2.78255940e-02, 1.e-01, 1.e+00])
CDREC_ITERS_RANGE = [i * 100 for i in range(1, 11)]  # replace with actual range

# IIM parameters
IIM_LEARNING_NEIGHBOR_RANGE = [i for i in range(1, 100)]  # Test up to 100 learning neighbors
# IIM_ADAPTIVE_RANGE = [True, False]  # Test with and without adaptive learning
# IIM_METRIC_RANGE = ['euclidean', 'cosine']  # Test with euclidean and cosine distance, could be more

# MRNN parameters
MRNN_LEARNING_RATE_CHANGE = np.logspace(-6, 0, num=20)  # log scale for learning rate
MRNN_HIDDEN_DIM_RANGE = [i for i in range(10)]  # hidden dimension
# MRNN_SEQ_LEN_RANGE = [i for i in range(100)]  # sequence length
MRNN_NUM_ITER_RANGE = [i for i in range(0, 100, 5)]  # number of epochs
MRNN_KEEP_PROB_RANGE = np.logspace(-6, 0, num=10)  # dropout keep probability

# STMVL parameters
STMVL_WINDOW_SIZE_RANGE = [i for i in range(2, 100)]  # window size
STMVL_GAMMA_RANGE = np.logspace(-6, 0, num=10, endpoint=False)  # smoothing parameter gamma
STMVL_ALPHA_RANGE = [i for i in range(1, 10)]  # smoothing parameter alpha

# Define the search space for each algorithm separately
SEARCH_SPACES = {
    'cdrec': [Integer(0, 9, name='rank'), Real(1e-6, 1, "log-uniform", name='eps'), Integer(100, 1000, name='iters')],
    'iim': [Integer(1, 100, name='learning_neighbours')],
    'mrnn': [Integer(0, 9, name='hidden_dim'), Real(1e-6, 1, "log-uniform", name='learning_rate'),
             Integer(0, 95, name='iterations'), Real(1e-6, 1, "log-uniform", name='keep_prob'),
             # Integer(0, 99, name='seq_len')
             ],
    'stmvl': [Integer(2, 99, name='window_size'), Real(1e-6, 0.999999, "log-uniform", name='gamma'),
              Integer(1, 9, name='alpha')],
}

# Define the search space for each algorithm separately for PSO
SEARCH_SPACES_PSO = {
    'cdrec': [(1, 10), (1e-6, 1), (100, 1000)],
    'iim': [(1, 100)],
    'mrnn': [(1, 100), (1e-6, 1e-2), (1, 100), (0.1, 1.0),
             # (1, 100)
             ],
    'stmvl': [(2, 100), (1e-6, 1e-2), (1, 100)]
}

# Define the parameter names for each algorithm
PARAM_NAMES = {
    'cdrec': ['rank', 'eps', 'iters'],
    'iim': ['learning_neighbours'],
    'mrnn': ['hidden_dim', 'learning_rate', 'iterations', 'keep_prob',
             # 'seq_len'
             ],
    'stmvl': ['window_size', 'gamma', 'alpha']
}

DEFAULT_PARAMS = {
    'cdrec': [0, 1e-6, 100],
    'iim': [10],
    'mrnn': [10, 0.01, 1000, 1.0,
                # 50
                ],
    'stmvl': [2, 0.85, 7]
}