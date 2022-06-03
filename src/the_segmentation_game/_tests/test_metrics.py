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
    assert met.jaccard_index_sparse(reference_labels, test_labels) == 1.0

    test_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 3, 2, 2, 1, 1, 0, 0, 0],
        [0, 3, 3, 2, 2, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert met.jaccard_index_sparse(reference_labels, test_labels) == 1.0

    test_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 2, 2, 0, 0, 0, 0, 0],
        [0, 1, 1, 2, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert met.jaccard_index_sparse(reference_labels, test_labels) == 1.0

    test_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert met.jaccard_index_sparse(reference_labels, test_labels) == 0.5

    test_labels = np.asarray([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])
    assert met.jaccard_index_sparse(reference_labels, test_labels) == 0.5
    
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
    
    assert met.roc_accuracy_binary(reference_labels, test_labels) == 0.9
    assert met.roc_balanced_accuracy_binary(reference_labels, test_labels) == 0.75
    assert met.ROC_F1Score_binary(reference_labels, test_labels) == 2/3
