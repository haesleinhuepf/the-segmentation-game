import the_segmentation_game.metrics as met
import numpy as np

def test_jaccard_index_sparse():
    reference_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 2, 2, 0, 0, 0, 0, 0],
        [0, 1, 1, 2, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    test_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 2, 2, 3, 3, 4, 4, 0],
        [0, 1, 1, 2, 2, 3, 3, 4, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert abs(met.jaccard_index_sparse(reference_labels, test_labels) - 1.0) < 0.001

    test_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 2, 2, 1, 1, 0, 0, 0],
        [0, 3, 3, 2, 2, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert abs(met.jaccard_index_sparse(reference_labels, test_labels) - 1.0) < 0.001

    test_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 2, 2, 0, 0, 0, 0, 0],
        [0, 1, 1, 2, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert abs(met.jaccard_index_sparse(reference_labels, test_labels) - 1.0) < 0.001

    test_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert abs(met.jaccard_index_sparse(reference_labels, test_labels) - 0.5) < 0.001

    test_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert abs(met.jaccard_index_sparse(reference_labels, test_labels) - 0.5) < 0.001
    
def test_ROC_binary():
    reference_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    
    test_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    
    assert abs(met.roc_accuracy_binary(reference_labels, test_labels) - 0.9) < 0.001
    assert abs(met.roc_balanced_accuracy_binary(reference_labels, test_labels) - 0.75) < 0.001
    assert abs(met.roc_f1score_binary(reference_labels, test_labels) - 2/3) < 0.001
    
    assert abs(met.roc_true_negative_rate_binary(reference_labels, test_labels) - 1.0) < 0.001
    assert abs(met.roc_true_positive_rate_binary(reference_labels, test_labels) - 0.5) < 0.001
    assert abs(met.roc_positive_predictive_value_binary(reference_labels, test_labels) - 1.0) < 0.001
    assert abs(met.roc_threat_score_binary(reference_labels, test_labels) - 0.5) < 0.001
