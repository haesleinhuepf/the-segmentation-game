import the_segmentation_game
import pytest

# this is your plugin name declared in your napari.plugins entry point
MY_PLUGIN_NAME = "the-segmentation-game"
# the name of your widget(s)
MY_WIDGET_NAMES = ["The Segmentation Game Widget"]


@pytest.mark.parametrize("widget_name", MY_WIDGET_NAMES)
def test_something_with_viewer(widget_name, make_napari_viewer, napari_plugin_manager):
    napari_plugin_manager.register(the_segmentation_game, name=MY_PLUGIN_NAME)
    viewer = make_napari_viewer()

    import numpy as np
    image = np.random.random((100, 100))
    viewer.add_image(image)

    num_dw = len(viewer.window._dock_widgets)
    viewer.window.add_dock_widget(the_segmentation_game._dock_widget.TheSegmentationGameWidget(viewer, _for_testing=True))
    ## makes test an endless loop
    # viewer.window.add_plugin_dock_widget(
    #    plugin_name=MY_PLUGIN_NAME, widget_name=widget_name
    # )
    assert len(viewer.window._dock_widgets) == num_dw + 1
