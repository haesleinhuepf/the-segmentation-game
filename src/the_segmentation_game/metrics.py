import numpy as np
from functools import partial
from enum import Enum

def jaccard_index_sparse(reference_label_image, test_label_image) -> float:

    # adapted from https://github.com/haesleinhuepf/napari-workflow-optimizer/blob/20c3baaf3009caf26909b57f08181108a731e67e/src/napari_workflow_optimizer/_optimizer.py#L288
    from sklearn.metrics import confusion_matrix
    import numpy as np

    reference_label_image = np.asarray(reference_label_image)
    test_label_image = np.asarray(test_label_image)

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

def jaccard_index_binary(reference_label_image, test_label_image) -> float:
    """
    Determine how correct a given test segmentation is.
    As metric we use the Jaccard index.
    Assumtion: test and reference are binary images or
    label images with values 0=False, otherwise: True.
    """
    tp, tn, fp, fn = compute_tp_tn_fp_fn(reference_label_image, test_label_image)

    # return Jaccard Index
    return tp / (tp + fn + fp)


def jaccard_index_binary_sparse(reference_label_image, test_label_image) -> float:
    """
    Determine how correct a given test segmentation is.
    As metric we use the Jaccard index.
    Assumtion: the test images has values 0=unknown, 1=False, 2=True.
    The reference image can be a binary or label image with 0=False, otherwise:True
    """
    ### adapted from https://github.com/haesleinhuepf/napari-workflow-optimizer/blob/20c3baaf3009caf26909b57f08181108a731e67e/src/napari_workflow_optimizer/_optimizer.py#L248
    try:
        import pyclesperanto_prototype as cle
        binary_and = cle.binary_and

        reference_label_image = cle.push(reference_label_image)
        test_label_image = cle.push(test_label_image)
    except ImportError:
        binary_and = np.logical_and

        reference_label_image = np.asarray(reference_label_image)
        test_label_image = np.asarray(test_label_image)

    test_label_image_max = test_label_image.max()

    negative_reference = reference_label_image == 0
    positive_reference = reference_label_image != 0
    negative_test = test_label_image != test_label_image_max
    positive_test = test_label_image == test_label_image_max

    # true positive:
    tp = binary_and(positive_reference, positive_test).sum()

    # true negative:
    tn = binary_and(negative_reference, negative_test).sum()

    # false positive
    fp = binary_and(negative_reference, positive_test).sum()

    # false negative
    fn = binary_and(positive_reference, negative_test).sum()

    # return Jaccard Index
    return tp / (tp + fn + fp)
    
def roc_f1score_binary(reference_label_image, test_label_image) -> float:
    """
    Determine how correct a given test segmentation is.
    As metric we use F1 score which is the harmonic mean of precision and sensitivity.
    Assumtion: test and reference are binary images or
    label images with values 0=False, otherwise: True.
    """
    tp, tn, fp, fn = compute_tp_tn_fp_fn(reference_label_image, test_label_image)

    # return F1 score
    return 2*tp / (2*tp + fn + fp)
    
def roc_accuracy_binary(reference_label_image, test_label_image) -> float:
    """
    Determine how correct a given test segmentation is.
    As metric we use accuracy ROC metric.
    Assumtion: test and reference are binary images or
    label images with values 0=False, otherwise: True.
    """
    tp, tn, fp, fn = compute_tp_tn_fp_fn(reference_label_image, test_label_image)

    # return accuracy
    return  (tp + tn)/(tp + tn + fp + fn)
    
def roc_balanced_accuracy_binary(reference_label_image, test_label_image) -> float:
    """
    Determine how correct a given test segmentation is.
    As metric we use balance accuracy ROC metric.
    Assumtion: test and reference are binary images or
    label images with values 0=False, otherwise: True.
    """
    tp, tn, fp, fn = compute_tp_tn_fp_fn(reference_label_image, test_label_image)
    
    # true positive ratr
    tpr = tp / (tp + fn) 
    
    # true negative rate
    tnr = tn / (tn + fp) 

    # return balanced accuracy
    return (tpr + tnr) / 2

def roc_true_positive_rate_binary(reference_label_image, test_label_image) -> float:
    """
    Determine how correct a given test segmentation is.
    As metric we use true positive rate ROC metric.
    Assumtion: test and reference are binary images or
    label images with values 0=False, otherwise: True.
    """
    tp, tn, fp, fn = compute_tp_tn_fp_fn(reference_label_image, test_label_image)

    # true positive rate
    tpr = tp / (tp + fn)

    # return true positive rate
    return tpr


def roc_true_negative_rate_binary(reference_label_image, test_label_image) -> float:
    """
    Determine how correct a given test segmentation is.
    As metric we use true negative rate ROC metric.
    Assumtion: test and reference are binary images or
    label images with values 0=False, otherwise: True.
    """
    tp, tn, fp, fn = compute_tp_tn_fp_fn(reference_label_image, test_label_image)

    # true negative rate
    tnr = tn / (tn + fp)

    # return true negative rate
    return tnr

def roc_positive_predictive_value_binary(reference_label_image, test_label_image) -> float:
    """
    Determine how correct a given test segmentation is.
    As metric we use positive predictive value ROC metric.
    Assumtion: test and reference are binary images or
    label images with values 0=False, otherwise: True.
    """
    tp, tn, fp, fn = compute_tp_tn_fp_fn(reference_label_image, test_label_image)

    # positive predictive value
    ppv = tp / (tp + fp)

    return ppv

def roc_threat_score_binary(reference_label_image, test_label_image) -> float:
    """
    Determine how correct a given test segmentation is.
    As metric we use threat score ROC metric.
    Assumtion: test and reference are binary images or
    label images with values 0=False, otherwise: True.
    """
    tp, tn, fp, fn = compute_tp_tn_fp_fn(reference_label_image, test_label_image)

    # threat score
    ts = tp / (tp + fp + fn)

    return ts

def compute_tp_tn_fp_fn(reference_label_image, test_label_image):
    """Compute overlap statistics:
    * tp = true positives
    * tn = true negatives
    * fp = false positives
    * fn = false negatives

    Parameters
    ----------
    reference_label_image: Image, e.g. a manual ground truth annotation
    test_label_image: Image, e.g. an algorithm result to determine the quality of

    Returns
    -------
    tp, tn, fp, fn
    """
    ### adapted from https://github.com/haesleinhuepf/napari-workflow-optimizer/blob/20c3baaf3009caf26909b57f08181108a731e67e/src/napari_workflow_optimizer/_optimizer.py#L248
    try:
        import pyclesperanto_prototype as cle
        binary_and = cle.binary_and

        reference_label_image = cle.push(reference_label_image)
        test_label_image = cle.push(test_label_image)
    except ImportError:
        binary_and = np.logical_and

        reference_label_image = np.asarray(reference_label_image)
        test_label_image = np.asarray(test_label_image)

    negative_reference = reference_label_image == 0
    positive_reference = reference_label_image != 0
    negative_test = test_label_image == 0
    positive_test = test_label_image != 0

    # true positive:
    tp = binary_and(positive_reference, positive_test).sum()

    # true negative:
    tn = binary_and(negative_reference, negative_test).sum()

    # false positive
    fp = binary_and(negative_reference, positive_test).sum()

    # false negative
    fn = binary_and(positive_reference, negative_test).sum()

    return tp, tn, fp, fn

class Metrics(Enum):
    Jaccard_Index_sparse = partial(jaccard_index_sparse)
    Jaccard_Index_binary = partial(jaccard_index_binary)
    Jaccard_Index_binary_sparse = partial(jaccard_index_binary_sparse)
    ROC_F1Score_binary=partial(roc_f1score_binary)
    ROC_Accuracy_binary=partial(roc_accuracy_binary)
    ROC_Balanced_Accuracy_binary=partial(roc_balanced_accuracy_binary)
    ROC_True_Negative_Rate_binary = partial(roc_true_negative_rate_binary)
    ROC_True_Positive_Rate_binary = partial(roc_true_positive_rate_binary)
    ROC_Positive_Predictive_Value_binary = partial(roc_positive_predictive_value_binary)
    ROC_Threat_Score_binary = partial(roc_threat_score_binary)
