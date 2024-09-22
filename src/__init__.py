import logging
from typing import Optional

from flet_core import Page, PopupMenuItem, AppBar, icons, colors, Text, Container, PopupMenuButton, margin, \
    UserControl, View, padding, TemplateRoute, Icon, MainAxisAlignment

from src.app_layout import AppLayout
from src.common import constants


class ImgATApp(UserControl):
    """
    应用程序基类

    """

    def __init__(self, page: Page):
        super().__init__()
        self.layout: Optional[AppLayout] = None
        self.page = page
        self.page.on_route_change = self.route_change
        self.appbar_items = [
            PopupMenuItem(text=constants.SETTINGS, icon=icons.SETTINGS),
            # divider
            PopupMenuItem(),
            PopupMenuItem(text=constants.USERS, icon=icons.PERSON)
        ]
        self.appbar = AppBar(
            leading=Icon(icons.HOME),
            exclude_header_semantics=True,
            title=Text(constants.APP_NAME, size=16),
            center_title=False,
            toolbar_height=50,
            bgcolor=colors.BLUE_GREY_50,
            actions=[
                Container(content=PopupMenuButton(items=self.appbar_items), margin=margin.only(left=50, right=25))
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()

    def build(self):
        self.layout = AppLayout(self, self.page, tight=True, expand=True, vertical_alignment=MainAxisAlignment.START)
        return self.layout

    def initialize(self):
        self.page.views.append(
            View(
                "/",
                [
                    self.appbar,
                    self.layout
                ],
                padding=padding.all(0),
                bgcolor=colors.WHITE,
            )
        )
        self.page.update()
        self.page.go("/")

    def route_change(self, e):
        """
        路由变动

        :param e:
        :return:
        """
        template_route = TemplateRoute(self.page.route)
        # 展示本地图库选项的页面
        if template_route.match('/local_gallery'):
            logging.info('Navigate to the local gallery page.')
            self.layout.set_local_gallery_view()
        elif template_route.match('/online_gallery/'):
            logging.info('Navigate to the online gallery page.')
            self.layout.set_online_gallery_view()
        self.page.update()
