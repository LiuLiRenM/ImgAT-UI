"""
本地图库布局

"""
from pathlib import Path
from typing import List

from flet_core import (Row, GridView, Image, ImageFit, ImageRepeat, border_radius, Page, TextField, Column, Text,
                       TextThemeStyle, MainAxisAlignment, FloatingActionButton, icons, FilePickerResultEvent,
                       FilePicker, Checkbox, Container, ElevatedButton, AlertDialog, TextButton)

from src.common import constants


class SelectDirPage(Column):
    """
    选择图库路径页面

    """

    def __init__(self, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

        self.width = 800

        # 用于判断是否已经添加过确认按钮
        self.is_add_confirm_button = False

        self.get_directory_dialog = FilePicker(on_result=self.select_folder)
        self.page.overlay.append(self.get_directory_dialog)

        self.checkbox_list: Column = Column()

        # 占位，不显示实际内容
        self.empty_container = Container(height=50)
        # 标题
        self.title = Row(
            [Text(value=constants.LOCAL_GALLERY_CONFIGURATION_TITLE, theme_style=TextThemeStyle.HEADLINE_LARGE)],
            alignment=MainAxisAlignment.CENTER)
        # 提示框
        self.prompt_box = TextField(hint_text=constants.GALLERY_PATH_CONFIGURATION_PROMPT,
                                    expand=True)
        # 已选择内容的提示标题
        self.selected_title = Row(
            controls=[Text(value=constants.SELECTED_DIR_PROMPT, theme_style=TextThemeStyle.TITLE_MEDIUM)],
            alignment=MainAxisAlignment.START)
        self.controls = [
            self.empty_container,
            self.title,
            Row(controls=[self.prompt_box, FloatingActionButton(icon=icons.FOLDER_OPEN, on_click=self.add_clicked,
                                                                disabled=self.page.web)]),
            self.selected_title,
            self.checkbox_list
        ]

        self.dlg_modal = None

    def select_folder(self, e: FilePickerResultEvent):
        """
        提供选择文件夹功能

        :return:
        """
        if e.path:
            checkbox = Checkbox(label=e.path, value=True)
            self.checkbox_list.controls.append(checkbox)
            # 添加确认按钮
            if not self.is_add_confirm_button:
                confirm_button = ElevatedButton(constants.CONFIRM_BUTTON, on_click=self.open_dlg_modal)
                button_in_row = Row(controls=[confirm_button], alignment=MainAxisAlignment.CENTER)
                self.controls.append(button_in_row)
                self.is_add_confirm_button = True
            self.update()

    def add_clicked(self, e):
        """
        点击按钮事件

        :return:
        """
        self.get_directory_dialog.get_directory_path()

    def open_dlg_modal(self, e):
        """
        打开模式对话框

        :param e:
        :return:
        """
        self.dlg_modal = AlertDialog(modal=True, title=Text(constants.ADD_LOCAL_GALLERY),
                                     content=Text(constants.CONTENT_OF_THE_PROMPT),
                                     actions=[
                                         TextButton(constants.YES, on_click=self.close_dlg_modal_with_yes),
                                         TextButton(constants.NO, on_click=self.close_dlg_modal_with_no)
                                     ],
                                     actions_alignment=MainAxisAlignment.END)
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()

    def close_dlg_modal_with_yes(self, e):
        """
        关闭模式对话框（点击“是”场景下）

        :param e:
        :return:
        """
        dir_path_list = list()
        # 读取已勾选的checkbox并获取其label值
        for checkbox in self.checkbox_list.controls:
            if checkbox.value:
                dir_path_list.append(checkbox.label)
        print(dir_path_list)
        self.page.client_storage.set(constants.GALLERY_DIR_PATH_LIST, dir_path_list)
        self.close_dlg_modal_with_no(e)


    def close_dlg_modal_with_no(self, e):
        """
        关闭模式对话框（点击“否”场景下）

        :param e:
        :return:
        """
        self.dlg_modal.open = False
        self.page.update()


class LocalGalleryLayout(Row):
    """
    本地图库布局

    """

    def __init__(self, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self._active_view = self.set_view()

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view

    @staticmethod
    def set_image_grid_view(gallery_dir_path_list: List[str]):
        """
        加载网格图

        :param gallery_dir_path_list: 图库路径列表
        :return:
        """
        images = GridView(expand=True, runs_count=1, max_extent=960,
                          child_aspect_ratio=1.89, spacing=5, run_spacing=5, padding=5)
        extensions_pattern = '|'.join(constants.IMAGE_SUFFIX_LIST)
        pattern = '*[{}]'.format(extensions_pattern)
        for dir_path in gallery_dir_path_list:
            for file in Path(dir_path).rglob(pattern):
                image = Image(src=file.as_posix(), fit=ImageFit.COVER, repeat=ImageRepeat.NO_REPEAT,
                              border_radius=border_radius.all(10))
                images.controls.append(image)
        return images

    def set_dir_select_view(self):
        """
        加载图库路径配置页面

        :return:
        """
        select_dir_page = SelectDirPage(page=self.page)
        # 通过增加明确宽度的Container以及alignment=MainAxisAlignment.SPACE_BETWEEN参数来保证select_dir_page水平居中显示
        return Row(controls=[Container(width=100), select_dir_page, Container(width=100)], expand=True,
                   alignment=MainAxisAlignment.SPACE_BETWEEN)

    def set_view(self):
        """
        加载用户点击本地图库后要展示的页面

        :return:
        """
        gallery_dir_path_list = self.page.client_storage.get(constants.GALLERY_DIR_PATH_LIST)
        if gallery_dir_path_list:
            return self.set_image_grid_view(gallery_dir_path_list=gallery_dir_path_list)
        else:
            return self.set_dir_select_view()
