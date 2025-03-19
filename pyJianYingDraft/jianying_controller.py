"""剪映自动化控制，主要与自动导出有关"""

import time
import shutil
import uiautomation as uia
import os
from typing import Optional, Literal

from . import exceptions
from .exceptions import AutomationError

class Jianying_controller:
    """剪映控制器"""

    app: uia.WindowControl
    """剪映窗口"""
    app_status: Literal["home", "edit", "pre_export"]

    def __init__(self):
        """初始化剪映控制器, 此时剪映应该处于目录页"""
        self.get_window()

    def export_draft(self, draft_name: str, output_dir: Optional[str] = None, timeout: float = 1200) -> None:
        """导出指定的剪映草稿

        **注意: 需要确认有导出草稿的权限(不使用VIP功能或已开通VIP), 否则可能陷入死循环**

        Args:
            draft_name (`str`): 要导出的剪映草稿名称
            output_path (`str`, optional): 导出路径, 导出完成后会将文件剪切到此, 不指定则使用剪映默认路径.
            timeout (`float`, optional): 导出超时时间(秒), 默认为20分钟.

        Raises:
            `DraftNotFound`: 未找到指定名称的剪映草稿
            `AutomationError`: 剪映操作失败
        """
        print(f"开始导出 {draft_name} 至 {output_dir}")
        self.get_window()
        self.switch_to_home()

        # 点击对应草稿
        draft_name_text = self.app.TextControl(searchDepth=2,
                                               Compare=lambda ctrl, depth: self.__draft_name_cmp(draft_name, ctrl, depth))
        if not draft_name_text.Exists(0):
            raise exceptions.DraftNotFound(f"未找到名为{draft_name}的剪映草稿")
        draft_btn = draft_name_text.GetParentControl()
        assert draft_btn is not None
        draft_btn.Click(simulateMove=False)
        time.sleep(10)
        self.get_window()

        # 点击导出按钮
        export_btn = self.app.TextControl(searchDepth=2, Compare=self.__edit_page_export_cmp)
        if not export_btn.Exists(0):
            raise AutomationError("未找到导出按钮")
        export_btn.Click(simulateMove=False)
        time.sleep(10)
        self.get_window()

        # 获取原始导出路径
        export_path_sib = self.app.TextControl(searchDepth=2, Compare=self.__export_path_cmp)
        if not export_path_sib.Exists(0):
            raise AutomationError("未找到导出路径框")
        export_path_text = export_path_sib.GetSiblingControl(lambda ctrl: True)
        assert export_path_text is not None
        export_path = export_path_text.GetPropertyValue(30159)

        # 点击导出
        export_btn = self.app.TextControl(searchDepth=2, Compare=self.__export_btn_cmp)
        if not export_btn.Exists(0):
            raise AutomationError("未找到导出按钮")
        export_btn.Click(simulateMove=False)
        time.sleep(5)

        # 等待导出完成
        st = time.time()
        while True:
            self.get_window()
            if self.app_status != "pre_export": continue

            succeed_close_btn = self.app.TextControl(searchDepth=2, Compare=self.__export_succeed_close_btn_cmp)
            if succeed_close_btn.Exists(0):
                succeed_close_btn.Click(simulateMove=False)
                break

            if time.time() - st > timeout:
                raise AutomationError("导出超时, 时限为%d秒" % timeout)

            time.sleep(1)
        time.sleep(2)

        # 回到目录页
        self.get_window()
        self.switch_to_home()
        time.sleep(2)

        # 复制导出的文件到指定目录
        if output_dir is not None:
            shutil.move(export_path, output_dir)

        print(f"导出 {draft_name} 至 {output_dir} 完成")

    def switch_to_home(self) -> None:
        """切换到剪映主页"""
        # 如果当前状态已经是主页，则直接返回
        if self.app_status == "home":
            return
        # 如果当前状态不是编辑模式，则抛出异常
        if self.app_status != "edit":
            raise AutomationError("仅支持从编辑模式切换到主页")
        # 获取关闭按钮
        close_btn = self.app.GroupControl(searchDepth=1, ClassName="TitleBarButton", foundIndex=3)
        # 点击关闭按钮
        close_btn.Click(simulateMove=False)
        # 等待2秒
        time.sleep(2)
        # 获取窗口
        self.get_window()

    def get_window(self) -> None:
        """寻找剪映窗口并置顶"""
        # 如果已经存在app属性且app存在，则将app置顶
        if hasattr(self, "app") and self.app.Exists(0):
            self.app.SetTopmost(False)

        # 寻找剪映窗口
        self.app = uia.WindowControl(searchDepth=1, Compare=self.__jianying_window_cmp)
        # 如果找不到剪映窗口，则抛出异常
        if not self.app.Exists(0):
            os.startfile(os.path.join(os.path.join(os.environ['USERPROFILE']), 'D:\\Software\\JianYin\\JianyingPro', 'JianyingPro.exe'))
            raise AutomationError("剪映窗口未找到")

        # 寻找可能存在的导出窗口
        export_window = self.app.WindowControl(searchDepth=1, Name="导出")
        # 如果找到了导出窗口，则将app置为导出窗口，并将app_status置为pre_export
        if export_window.Exists(0):
            self.app = export_window
            self.app_status = "pre_export"

        # 将app置为活动窗口
        self.app.SetActive()
        # 将app置顶
        self.app.SetTopmost()

    def __jianying_window_cmp(self, control: uia.WindowControl, depth: int) -> bool:
        # 判断窗口名称是否为"剪映专业版"
        if control.Name != "剪映专业版":
            return False
        # 判断窗口类名是否包含"HomePage"，如果包含，则将app_status设置为"home"
        if "HomePage".lower() in control.ClassName.lower():
            self.app_status = "home"
            return True
        # 判断窗口类名是否包含"MainWindow"，如果包含，则将app_status设置为"edit"
        if "MainWindow".lower() in control.ClassName.lower():
            self.app_status = "edit"
            return True
        # 如果以上条件都不满足，则返回False
        return False

    @staticmethod
    # 定义一个函数，用于比较草稿名称和UIA文本控件
    def __draft_name_cmp(draft_name: str, control: uia.TextControl, depth: int) -> bool:
        # 如果深度不等于2，则返回False
        if depth != 2:
            return False
        # 获取UIA文本控件的属性值
        full_desc: str = control.GetPropertyValue(30159)
        # 如果属性值中包含"Title:"和草稿名称，则返回True，否则返回False
        return "Title:".lower() in full_desc.lower() and draft_name in full_desc

    @staticmethod
    # 定义一个函数，用于编辑页面导出比较
    def __edit_page_export_cmp(control: uia.TextControl, depth: int) -> bool:
        # 如果深度不等于2，则返回False
        if depth != 2:
            return False
        # 获取控件的属性值，并将其转换为小写
        full_desc: str = control.GetPropertyValue(30159).lower()
        # 如果属性值中包含"title"和"export"，则返回True，否则返回False
        return "title" in full_desc and "export" in full_desc

    @staticmethod
    # 定义一个函数，用于比较控件和深度
    def __export_btn_cmp(control: uia.TextControl, depth: int) -> bool:
        # 如果深度不等于2，则返回False
        if depth != 2:
            return False
        # 获取控件的属性值，并将其转换为小写
        full_desc: str = control.GetPropertyValue(30159).lower()
        # 比较控件的属性值是否等于"ExportOkBtn"，并返回比较结果
        return "ExportOkBtn".lower() == full_desc

    @staticmethod
    # 定义一个函数，用于比较导出路径
    def __export_path_cmp(control: uia.TextControl, depth: int) -> bool:
        # 如果深度不等于2，则返回False
        if depth != 2:
            return False
        # 获取控件的属性值，并将其转换为小写
        full_desc: str = control.GetPropertyValue(30159).lower()
        # 如果属性值中包含"ExportPath"，则返回True，否则返回False
        return "ExportPath".lower() in full_desc

    @staticmethod
    # 定义一个函数，用于判断控件是否为导出成功关闭按钮
    def __export_succeed_close_btn_cmp(control: uia.TextControl, depth: int) -> bool:
        # 如果深度不等于2，则返回False
        if depth != 2:
            return False
        # 获取控件的完整描述，并将其转换为小写
        full_desc: str = control.GetPropertyValue(30159).lower()
        # 判断完整描述中是否包含"ExportSucceedCloseBtn"，如果包含，则返回True，否则返回False
        return "ExportSucceedCloseBtn".lower() in full_desc
