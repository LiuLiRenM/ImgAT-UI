"""
程序主入口

"""
import logging

import flet
from flet_core import Page, colors, theme

from src import ImgATApp
from src.common import constants


def main(page: Page):
    """
    主入口

    :param page:
    :return:
    """
    page.title = constants.APP_NAME
    page.padding = 0
    page.window.height = 1080
    page.window.width = 1920
    page.theme = theme.Theme(font_family="Verdana")
    page.theme.page_transitions.windows = "cupertino"
    # page.bgcolor = colors.WHITE
    app = ImgATApp(page=page)
    page.add(app)
    page.update()
    app.initialize()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    flet.app(main)
