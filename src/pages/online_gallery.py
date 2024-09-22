"""
在线图库布局

"""
from flet_core import UserControl, Text

from src.common import constants


class OnlineGalleryLayout(UserControl):
    """
    在线图库布局

    """

    def __init__(self):
        super().__init__()
        self.view = Text(constants.ONLINE_GALLERY)
        self._active_view = None

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.update()
