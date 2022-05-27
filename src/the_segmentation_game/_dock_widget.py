import warnings

from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
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

        self.quality_text = QLabel("")
        font = self.quality_text.font()
        font.setPointSize(30)
        self.quality_text.setFont(font)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Jaccard Index (sparse):"))
        self.layout().addWidget(self.quality_text)

        btn = QPushButton("Save to highscore table")
        btn.clicked.connect(self._save_clicked)
        self.layout().addWidget(btn)

        # go through all widgets and change spacing
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i).widget()
            if item.layout() is not None:
                item.layout().setSpacing(0)
                item.layout().setContentsMargins(3, 3, 3, 3)

        # ----------------------------------------------------------
        # Thread worker for updating memory consumption threading
        # https://napari.org/guides/stable/threading.html
        # adapted from https://github.com/haesleinhuepf/napari-image-quality-analyzer/blob/9dbf6162df1d93fff3b9e7b4a67a1a173db58ea2/napari_image_quality_analyzer/_dock_widget.py#L48
        @thread_worker
        def loop_run():
            while self._viewer.window.qt_viewer:  # loop until napari closes
                yield self.determine_quality()
                time.sleep(0.5)

        # Start the loop
        worker = loop_run()
        worker.yielded.connect(self._update_quality)
        if _for_testing:
            self._update_quality(self.determine_quality())
        else:
            worker.start()


    def _save_clicked(self):
        if self.ground_truth_annotation_select.value is None:
            warnings.warn("No ground truth annotation was selected!")
            return
        if self.segmentation_result_select.value is None:
            warnings.warn("No segmentation result was selected!")
            return

    def _update_quality(self, quality:float):
        """Receive a quality measurement and store it in the user interface"""
        self.quality_text.setText(str(quality))
        if quality is not None:
            if quality > 0.9:
                self.quality_text.setStyleSheet("QLabel { color : green }")
            elif quality > 0.5:
                self.quality_text.setStyleSheet("QLabel { color : yellow }")
            else:
                self.quality_text.setStyleSheet("QLabel { color : red }")

    def determine_quality(self):
        """Determine quality of the currently selected label images considering the currently selected metric."""
        if self.ground_truth_annotation_select.value is None:
            return None
        if self.segmentation_result_select.value is None:
            return None

        from .metrics import jaccard_index_sparse
        function = jaccard_index_sparse

        quality = function(self.ground_truth_annotation_select.value, self.segmentation_result_select.value)

        return quality


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [TheSegmentationGameWidget]
