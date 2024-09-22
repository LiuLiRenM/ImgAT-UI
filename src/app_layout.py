"""
定义应用程序的布局

"""
from flet_core import Row, Page, Control, MainAxisAlignment

from src.pages.local_gallery import LocalGalleryLayout
from src.pages.online_gallery import OnlineGalleryLayout
from src.pages.welcome_page import WelcomePage
from src.sidebar import Sidebar


class AppLayout(Row):
    """
    应用程序布局

    """

    def __init__(
            self,
            app,
            page: Page,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.sidebar = Sidebar(page)
        self._active_view: Control = self.set_welcome_page()
        self.controls = [self.sidebar, self.active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.update()

    @staticmethod
    def set_welcome_page():
        """
        设置欢迎页面

        :return:
        """
        return WelcomePage().active_view

    def set_local_gallery_view(self):
        """
        将active_view换成本地图库的页面

        :return:
        """
        local_gallery = LocalGalleryLayout(page=self.page)
        self.active_view = local_gallery.active_view
        self.alignment = MainAxisAlignment.CENTER
        self.sidebar.wallpaper_center_nav_rail.selected_index = 0
        self.sidebar.down_center_nav_rail.selected_index = None
        self.sidebar.update()
        self.page.update()

    def set_online_gallery_view(self):
        """
        将active_view换成在线图库的页面

        :return:
        """
        online_gallery = OnlineGalleryLayout()
        self.active_view = online_gallery.active_view
        self.sidebar.wallpaper_center_nav_rail.selected_index = 1
        self.sidebar.down_center_nav_rail.selected_index = None
        self.sidebar.update()
        self.page.update()
