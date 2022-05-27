from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from magicgui import magic_factory
from napari_tools_menu import register_dock_widget

@register_dock_widget(menu = "Utilities > Layer Details")
class LayerDetailsDisplay(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self.text = QLabel("")

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.text)

        btn = QPushButton("Refresh")
        btn.clicked.connect(self._on_selection)
        self.layout().addWidget(btn)

        napari_viewer.layers.selection.events.changed.connect(self._on_selection)

        self._on_selection()

    def _on_selection(self, event=None):
        text = ""
        for layer in self.viewer.layers.selection:
            text = text + \
                   "<b>" + layer.name + "</b>"
            if hasattr(layer, "data"):
                text = text + \
                       "<li>data:"

                text = text + ", ".join([attr_to_str(layer.data, attr) for attr in ["shape", "dtype"]])
                text = text + ", <br/>" + str(type(layer.data)).replace("<", "&lt;").replace(">", "&gt;") + \
                       "</li>"

                for attr in ["scale", "translate", "rotate", "shear", "opacity", "contrast_limits", "gamma", "multiscale", "cache", "metadata", "properties"]:
                    value = attr_to_str(layer, attr)
                    if value is not None:
                        text = text + \
                               "<li>" + attr + ":" + value + "</li>"
            text = text + \
                   "<br/><br>"

        self.text.setText(text)

def attr_to_str(object, attr):
    if hasattr(object, attr):
        value = getattr(object, attr)
        if isinstance(value, dict):
            return str(list(value.keys()))
        else:
            return str(value)
    return ""

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [LayerDetailsDisplay]
