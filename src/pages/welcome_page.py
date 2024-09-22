"""
欢迎页面

"""
from flet_core import Row, ImageFit, Container


class WelcomePage(Row):
    """
    欢迎页面

    """

    def __init__(self):
        super().__init__()

        self.welcome_page_image_path: str = '/images/welcome_page.jpg'
        self._active_view = self.set_welcome_page()

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view

    def set_welcome_page(self):
        """
        设置欢迎页面

        :return:
        """
        return Container(image_src=self.welcome_page_image_path, image_fit=ImageFit.COVER, expand=True)
