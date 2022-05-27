
def jaccard_index_sparse(reference_label_image, test_label_image) -> float:

    # adapted from https://github.com/haesleinhuepf/napari-workflow-optimizer/blob/20c3baaf3009caf26909b57f08181108a731e67e/src/napari_workflow_optimizer/_optimizer.py#L288
    from sklearn.metrics import confusion_matrix
    import numpy as np

    reference_label_image = np.asarray(reference_label_image)
    test_label_image = np.asarray(test_label_image)

    print(reference_label_image)
    print(test_label_image)

    # determine overlap
    overlap = confusion_matrix(reference_label_image.ravel(), test_label_image.ravel())

    # crop out region in confusion matrix where reference labels are
    num_labels_reference = reference_label_image.max()
    overlap = overlap[0:num_labels_reference+1, :]

    # Measure correctly labeled pixels
    n_pixels_pred = np.sum(overlap, axis=0, keepdims=True)
    n_pixels_true = np.sum(overlap, axis=1, keepdims=True)

    # Calculate intersection over union
    divisor = (n_pixels_pred + n_pixels_true - overlap)
    is_zero = divisor == 0
    divisor[is_zero] = 1
    overlap[is_zero] = 0
    iou = overlap / divisor

    # ignore background
    iou = iou[1:,1:]

    max_jacc = iou.max(axis=1)

    quality = max_jacc.mean()

    return quality