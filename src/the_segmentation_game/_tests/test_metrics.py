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
