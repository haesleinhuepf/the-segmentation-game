# The segmentation game - for napari

[![License](https://img.shields.io/pypi/l/the-segmentation-game.svg?color=green)](https://github.com/haesleinhuepf/the-segmentation-game/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/the-segmentation-game.svg?color=green)](https://pypi.org/project/the-segmentation-game)
[![Python Version](https://img.shields.io/pypi/pyversions/the-segmentation-game.svg?color=green)](https://python.org)
[![tests](https://github.com/haesleinhuepf/the-segmentation-game/workflows/tests/badge.svg)](https://github.com/haesleinhuepf/the-segmentation-game/actions)
[![codecov](https://codecov.io/gh/haesleinhuepf/the-segmentation-game/branch/main/graph/badge.svg)](https://codecov.io/gh/haesleinhuepf/the-segmentation-game)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/the-segmentation-game)](https://napari-hub.org/plugins/the-segmentation-game)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6588373.svg)](https://doi.org/10.5281/zenodo.6588373)

Gamified image segmentation quality estimation

![img.png](https://github.com/haesleinhuepf/the-segmentation-game/raw/main/images/screencast.gif)

----------------------------------

## Usage

The Segmentation Game allows to quantitatively compare segmentation results to a given ground truth annotation.
This allows fine-tuning parameters of image processing workflows to get optimal segmentation quality. 
It also allows comparing different segmentation algorithms and identify which algorithm performs best objectively.

The game can be found in napari's `Tools > Games > The Segmentation Game` menu.

### Ground Truth Annotation

Before you can start playing the game, some annotated cells/nuclei are necessary to later compute segmentation quality from.
Depending on the used metric, it might be sufficient to annotate a hand full of objects. 
Use napari's annotation tools as shown below. 
Use the `+` and `-` keys on your keyboard to increase and decrease the label number that is currently drawn.
Note: Avoid label gaps. The labels must be continuously subsequent. If there are pixels annotated with value 2, there must be pixels annotated with value 1.

![](https://github.com/haesleinhuepf/the-segmentation-game/raw/main/images/annotation.gif)

### Parameter tuning

If you work with one of [napari's segmentation plugins](https://www.napari-hub.org/?search=segmentation&sort=relevance&page=1) that produce labels layers,
you can tune their parameters and see how this influences segmentation quality.

![](https://github.com/haesleinhuepf/the-segmentation-game/raw/main/images/parameter_tuning.gif)

### Segmentation algorithm comparison

If you aim at comparing different segmentation algorithms, you can collect their results in label layers in the napari viewer.
You can then select the segmentation result from the corresponding pulldown and save quantitative comparison results in the Highscore table.

![](https://github.com/haesleinhuepf/the-segmentation-game/raw/main/images/algorithm_comparison.gif)

## Metrics

Currently, these metrics are implemented:
* Jaccard Index (sparse): The [Jaccard Index](https://en.wikipedia.org/wiki/Jaccard_index) is a measure of overlap. 
  It lies between 0 (no overlap) and 1 (perfect overlap). 
  For each annotated ground truth label, the maximum overlap of any segmented label is determined. 
  The mean overlap of all annotated labels serves as metric result.
* Jaccard Index (binary): The annotated ground truth labels and the segmentation result are first binarized considering all annotated pixels as positive and all other labels as negative.
  Afterwards, the overlap between the two binary images is computed. This allows comparing binary segmentation algorithms, such as thresholding techniques.
* Jaccard Index (binary, sparse): The annotated ground truth image can contain values 1 (negative, false) and 2 (positive, true) and
  the segmentation result image will be binarized (0: False, otherwise: True). This allows comparing object/no-object annotations with label images.
 
 
Receiver operating characteristic ([ROC](https://en.wikipedia.org/wiki/Receiver_operating_characteristic))
  
Consider a two-class thresholding problem (binary pixel-wise classification object/background), in which the outcomes are labeled either as positive (p) or negative (n). There are four possible outcomes from a binary classifier. If the outcome from a prediction is p and the actual value is also p, then it is called a true positive (TP); however if the actual value is n then it is said to be a false positive (FP). Conversely, a true negative (TN) has occurred when both the prediction outcome and the actual value are n, and false negative (FN) is when the prediction outcome is n while the actual value is p. We can organize result in table called confusion matrix, based on positive/neagtive results in row and true and false result in columns. From the confucsion matrix we can get many metrics with various usefulness. The curently implemented used for classification evaluation are:

* Accuracy: (TP + TN)/ (TP + FP + TN + FN), Accuracy measures observational error. Accuracy is how close or far off a given set of measurements are to their true value. However, it usually fails in imbalanced sets.
* Balanced Accuracy: (TP/(TP+FN) + TN/(TN+FP))/2, Balanced Accuracy is trying to even out problems of accuracy in imbalanced sets.
* F1 Score: 2*TP/(2*TP + FP + TN + FN), In statistical analysis of binary classification, the F-score or F-measure is a measure of a test's accuracy. It is calculated from the precision and recall of the test, where the precision is the number of true positive results divided by the number of all positive results, including those not identified.
* Threat score (TS) or critical success index (CSI): TP/(TP + FP + TN + FN), TC is another name for Jaccard Index (binary).

The ROC measures or confusion matrix is invaluable in cases when when our binary classifier is not ideal (which is often) and we are aiming to not get a general good result but specified low error. In that case we usually need to decide for some trade off, for example we need all (as many as possible) classified true positive objects, but we do not mind getting (usually as few as possible) false positive objects.

Other ROC metrics will be implemented soon...

## Related plugins

If you aim at automatically optimizing segmentation quality, there are also napari plugins available with this capability:

* [napari-accelerated-pixel-and-object-classification](https://www.napari-hub.org/plugins/napari-accelerated-pixel-and-object-classification)
* [napari-workflow-optimizer](https://www.napari-hub.org/plugins/napari-workflow-optimizer)

## Installation

You can install `the-segmentation-game` via [pip]:

    pip install the-segmentation-game

## Contributing

Contributions - especially new image segmentation quality metrics - are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"the-segmentation-game" is free and open source software

## Issues

If you encounter any problems, please open a thread on [image.sc](https://image.sc) along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/haesleinhuepf/the-segmentation-game/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
