import warnings

from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit
from napari_tools_menu import register_dock_widget
from magicgui.widgets import create_widget
from napari.layers import Labels
from napari._qt.qthreading import thread_worker
import numpy as np
import time

@register_dock_widget(menu = "Games > The Segmentation Game")
class TheSegmentationGameWidget(QWidget):
    def __init__(self, napari_viewer, _for_testing:bool = False):
        super().__init__()
        self._viewer = napari_viewer
        self.setLayout(QVBoxLayout())

        # widgets for the selection of labels layers
        ground_truth_annotation_container = QWidget()
        ground_truth_annotation_container.setLayout(QHBoxLayout())
        ground_truth_annotation_container.layout().addWidget(QLabel("Ground truth annotation"))
        self.ground_truth_annotation_select = create_widget(annotation=Labels, label="labels_layer")
        ground_truth_annotation_container.layout().addWidget(self.ground_truth_annotation_select.native)
        self.layout().addWidget(ground_truth_annotation_container)

        segmentation_result_container = QWidget()
        segmentation_result_container.setLayout(QHBoxLayout())
        segmentation_result_container.layout().addWidget(QLabel("Segmentation result"))
        self.segmentation_result_select = create_widget(annotation=Labels, label="labels_layer")
        segmentation_result_container.layout().addWidget(self.segmentation_result_select.native)
        self.layout().addWidget(segmentation_result_container)

        # widgets for comparison method selection
        from .metrics import Metrics
        comparison_method_container = QWidget()
        comparison_method_container.setLayout(QHBoxLayout())
        comparison_method_container.layout().addWidget(QLabel("Comparison Method"))
        self.comparison_method_select = create_widget(
            widget_type="ComboBox",
            name="comparison_method",
            value=Metrics.Jaccard_Index_sparse,
            options={"choices": [e for e in Metrics]},
        )
        comparison_method_container.layout().addWidget(
            self.comparison_method_select.native
        )
        self.layout().addWidget(comparison_method_container)

        # widget for quality visualization
        self.quality_text = QLabel("")
        font = self.quality_text.font()
        font.setPointSize(30)
        self.quality_text.setFont(font)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.quality_text)

        self.description_field = QLineEdit("")
        self.description_field.setPlaceholderText("Enter player name or segmentation description here")
        self.layout().addWidget(self.description_field)

        btn = QPushButton("Save to highscore table")
        btn.clicked.connect(self._save_clicked)
        self.layout().addWidget(btn)

        # go through all widgets and change spacing
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i).widget()
            if item.layout() is not None:
                item.layout().setSpacing(0)
                item.layout().setContentsMargins(1, 1, 1, 1)

        # ----------------------------------------------------------
        # Thread worker for updating memory consumption threading
        # https://napari.org/guides/stable/threading.html
        # adapted from https://github.com/haesleinhuepf/napari-image-quality-analyzer/blob/9dbf6162df1d93fff3b9e7b4a67a1a173db58ea2/napari_image_quality_analyzer/_dock_widget.py#L48
        @thread_worker
        def loop_run():
            while self._viewer.window.qt_viewer:  # loop until napari closes
                yield self.determine_quality(self.comparison_method_select.value.value)
                time.sleep(0.5)

        # Start the loop
        worker = loop_run()
        worker.yielded.connect(self._update_quality)
        if _for_testing:
            self._update_quality(self.determine_quality(self.comparison_method_select.value.value))
        else:
            worker.start()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.reset_choices()

    def reset_choices(self, event=None):
        self.ground_truth_annotation_select.reset_choices(event)
        self.segmentation_result_select.reset_choices(event)

    def _save_clicked(self):
        if self.ground_truth_annotation_select.value is None:
            warnings.warn("No ground truth annotation was selected!")
            return
        if self.segmentation_result_select.value is None:
            warnings.warn("No segmentation result was selected!")
            return
        if self.segmentation_result_select.value is self.ground_truth_annotation_select.value:
            warnings.warn("No ground truth annotation and segmentation result must not be the same!")
            return None

        features = self.ground_truth_annotation_select.value.features
        if features is None:
            features = {}

        if not isinstance(features, dict):
            features = features.to_dict(orient='list')

        # store description
        if "description" not in features.keys():
            features["description"] = []
        features["description"].append(self.description_field.text())

        # store metrics
        from .metrics import Metrics
        for metric in Metrics:
            function = metric.value
            name = str(metric)

            quality = self.determine_quality(function)

            if name not in features.keys():
                features[name] = []
            features[name].append(quality)

        self.ground_truth_annotation_select.value.features = features

        from napari_skimage_regionprops import add_table
        add_table(self.ground_truth_annotation_select.value, self._viewer)

    def _update_quality(self, quality:float):
        """Receive a quality measurement and store it in the user interface"""
        if quality is not None:
            self.quality_text.setText(str(quality)[0:5])
            if quality > 0.9:
                self.quality_text.setStyleSheet("QLabel { color : green }")
            elif quality > 0.5:
                self.quality_text.setStyleSheet("QLabel { color : yellow }")
            else:
                self.quality_text.setStyleSheet("QLabel { color : red }")
        else:
            self.quality_text.setText("")

    def determine_quality(self, function):
        """Determine quality of the currently selected label images considering the currently selected metric."""
        if self.ground_truth_annotation_select.value is None:
            return None
        if self.segmentation_result_select.value is None:
            return None
        if self.segmentation_result_select.value is self.ground_truth_annotation_select.value:
            return None

        quality = function(self.ground_truth_annotation_select.value.data, self.segmentation_result_select.value.data)

        return quality


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [TheSegmentationGameWidget]
