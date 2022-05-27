# The segmentation game - for napari

[![License](https://img.shields.io/pypi/l/the-segmentation-game.svg?color=green)](https://github.com/haesleinhuepf/the-segmentation-game/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/the-segmentation-game.svg?color=green)](https://pypi.org/project/the-segmentation-game)
[![Python Version](https://img.shields.io/pypi/pyversions/the-segmentation-game.svg?color=green)](https://python.org)
[![tests](https://github.com/haesleinhuepf/the-segmentation-game/workflows/tests/badge.svg)](https://github.com/haesleinhuepf/the-segmentation-game/actions)
[![codecov](https://codecov.io/gh/haesleinhuepf/the-segmentation-game/branch/main/graph/badge.svg)](https://codecov.io/gh/haesleinhuepf/the-segmentation-game)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/the-segmentation-game)](https://napari-hub.org/plugins/the-segmentation-game)

Gamified image segmentation quality estimation

![img.png](https://github.com/haesleinhuepf/the-segmentation-game/raw/main/images/screenshot.png)

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

![](https://github.com/haesleinhuepf/the-segmentation-game/raw/main/images/algorithm_comparison.gif)

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
