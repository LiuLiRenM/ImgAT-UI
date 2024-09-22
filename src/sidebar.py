"""
导航菜单

"""
from typing import Optional

from flet_core import (UserControl, NavigationRailDestination, Text, icons, NavigationRail, colors, Container, Column,
                       Row, border_radius, alignment, padding, margin, NavigationRailLabelType, Page)

from src.common import constants


class Sidebar(UserControl):
    """
    导航菜单

    """

    def __init__(self, page: Page):
        super().__init__()
        self.view: Optional[Container] = None
        # self.page = page
        self.wallpaper_center_nav_items = [
            NavigationRailDestination(label_content=Text(constants.LOCAL_GALLERY), label="LocalGallery",
                                      icon=icons.IMAGE, selected_icon=icons.IMAGE),
            NavigationRailDestination(label_content=Text(constants.ONLINE_GALLERY), label="OnlineGallery",
                                      icon=icons.IMAGE_SEARCH, selected_icon=icons.IMAGE_SEARCH)
        ]
        self.wallpaper_center_nav_rail = NavigationRail(label_type=NavigationRailLabelType.ALL,
                                                        on_change=self.wallpaper_center_nav_change,
                                                        destinations=self.wallpaper_center_nav_items,
                                                        bgcolor=colors.BLUE_GREY_100, extended=True,
                                                        height=100)
        self.down_center_nav_items = [
            NavigationRailDestination(label_content=Text(constants.DOWNLOAD_LIST), label="DownloadList",
                                      icon=icons.DOWNLOAD, selected_icon=icons.DOWNLOAD),
            NavigationRailDestination(label_content=Text(constants.LOCAL_LIST), label="LocalList",
                                      icon=icons.LIST, selected_icon=icons.LIST)
        ]
        self.down_center_nav_rail = NavigationRail(label_type=NavigationRailLabelType.ALL,
                                                   on_change=self.down_center_nav_change,
                                                   destinations=self.down_center_nav_items,
                                                   bgcolor=colors.BLUE_GREY_100,
                                                   extended=True,
                                                   expand=True)

    def build(self):
        column_controls = [
            Row([Text(constants.WALLPAPER_CENTER)]),
            # 横线
            Container(bgcolor=colors.BLACK26, border_radius=border_radius.all(30), height=1,
                      alignment=alignment.center_right, width=220),
            self.wallpaper_center_nav_rail,
            Row([Text(constants.DOWNLOAD_CENTER)]),
            # 横线
            Container(bgcolor=colors.BLACK26, border_radius=border_radius.all(30), height=1,
                      alignment=alignment.center_right, width=220),
            self.down_center_nav_rail,
        ]
        self.view = Container(
            content=Column(column_controls, tight=True),
            padding=padding.all(15),
            margin=margin.all(0),
            width=250,
            bgcolor=colors.BLUE_GREY_100,
            expand=True
        )
        return self.view

    def wallpaper_center_nav_change(self, e):
        """
        壁纸中心导航栏的点击事件

        :param e:
        :return:
        """
        index = e.control.selected_index
        self.wallpaper_center_nav_rail.selected_index = index
        # 其他导航栏的selected_index设置为None，不然会出现选中多个的情况
        self.down_center_nav_rail.selected_index = None
        self.view.update()
        if index == 0:
            self.page.route = '/local_gallery'
        elif index == 1:
            self.page.route = '/online_gallery'
        self.page.update()

    def down_center_nav_change(self, e):
        """
        下载中心导航栏的点击事件

        :param e:
        :return:
        """
        self.down_center_nav_rail.selected_index = e.control.selected_index
        # 其他导航栏的selected_index设置为None，不然会出现选中多个的情况
        self.wallpaper_center_nav_rail.selected_index = None
        self.update()
