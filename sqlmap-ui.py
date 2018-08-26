#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 08月 26日 星期日 16:54:41 CST
# sqlmap gui gtk-3

from gtk3_header import Gtk as g


class UI_Window(g.Window):
  def __init__(self):
    super().__init__(title='sqlmap-ui by needlewang')
    # self.set_default_size(700, 0)

    self.notebook = g.Notebook()
    self.add(self.notebook)

    self._build_page1()
    self.notebook.append_page(self.page1, g.Label('功能'))
    self._build_page2()
    self.notebook.append_page(self.page2, g.Label('查看记录'))
    self._build_page3()
    self.notebook.append_page(self.page3, g.Label('帮助'))
    self._build_page4()
    self.notebook.append_page(self.page4, g.Label('感谢'))

  def _build_page1(self):
    self.page1 = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)
    self.page1.set_border_width(10)

    # 目标url
    name_store = g.ListStore(int, str)
    name_store.append([1, "www.baidu.com"])
    name_store.append([11, "www.sina.com"])

    _url_area = g.Stack()

    _combobox = g.ComboBox.new_with_model_and_entry(name_store)
    _combobox.set_size_request(0, 0)
    # _combobox.connect('changed', None)
    _combobox.set_entry_text_column(1)
    _url_area.add_titled(_combobox, '_combobox', '目标url')

    _stack_switcher1 = g.StackSwitcher()
    _stack_switcher1.set_stack(_url_area)

    self.page1.pack_start(_stack_switcher1, False, True, 0)
    self.page1.pack_start(_url_area, False, True, 0)

    # sqlmap命令语句
    _cmd_area = g.Stack()

    _cmd_str = g.Entry()
    _cmd_area.add_titled(_cmd_str, '_cmd_str', 'sqlmap命令语句:')

    _stack_switcher2 = g.StackSwitcher()
    _stack_switcher2.set_stack(_cmd_area)

    self.page1.pack_start(_stack_switcher2, False, True, 0)
    self.page1.pack_start(_cmd_area, False, True, 0)

    # 主构造区
    _notebook = g.Notebook()
    self.page1.pack_start(_notebook, True, True, 0)

    # 功能 - 设置, 请求, 枚举, 文件
    self._build_page1_setting()
    self._build_page1_request()
    self._build_page1_enumeration()
    self._build_page1_file()

    _notebook.append_page(self.page1_setting, g.Label('设置'))
    _notebook.append_page(self.page1_request, g.Label('请求'))
    _notebook.append_page(self.page1_enumeration, g.Label('枚举'))
    _notebook.append_page(self.page1_file, g.Label('文件'))

  def _build_page1_setting(self):
    self.page1_setting = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box(orientation=g.Orientation.HORIZONTAL)

    self._build_page1_setting_inject()
    self._build_page1_setting_tamper()
    self._build_page1_setting_optimize()

    _row1.pack_start(self._inject_area, False, True, 0)
    _row1.pack_start(self._tamper_area, False, True, 0)
    _row1.pack_start(self._optimize_area, False, True, 0)

    self.page1_setting.pack_start(_row1, True, True, 0)

    _row2 = g.Box(orientation=g.Orientation.HORIZONTAL)

    pass

    self.page1_setting.pack_start(_row2, True, True, 0)

  def _build_page1_setting_optimize(self):
    self._optimize_area = g.Box(orientation=g.Orientation.VERTICAL)

    _optimize_area_stack = g.Stack()
    _optimize_area_opts = g.ListBox()

    _optimize_area_opts.add(g.CheckButton('打开所有优化选项'))
    _optimize_area_opts.add(g.CheckButton('预测输出结果'))
    _optimize_area_opts.add(g.CheckButton('持续连接'))
    _optimize_area_opts.add(g.CheckButton('只比较响应包长度'))

    _optimize_area_stack.add_titled(_optimize_area_opts, '_optimize_area_opts', '优化')

    _optimize_area_switcher = g.StackSwitcher()
    _optimize_area_switcher.set_stack(_optimize_area_stack)

    self._optimize_area.pack_start(_optimize_area_switcher, False, True, 0)
    self._optimize_area.pack_end(_optimize_area_stack, True, True, 0)

  def _build_page1_setting_tamper(self):
    self._tamper_area = g.Box(orientation=g.Orientation.VERTICAL)

    _tamper_area_stack = g.Stack()
    _tamper_area_list = g.ListBox()
    # 最小尺寸
    _tamper_area_list.set_size_request(300, 0)

    _items = '这.py 是 个 啥 ? a d b e e s w e'.split()
    for _item in _items:
      _tamper_area_list.add(g.Label(_item))

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(_tamper_area_list)

    _tamper_area_stack.add_titled(_scrolled, '_tamper_area_list', 'tamper脚本')

    _tamper_area_switcher = g.StackSwitcher()
    _tamper_area_switcher.set_stack(_tamper_area_stack)

    self._tamper_area.pack_start(_tamper_area_switcher, False, True, 0)
    self._tamper_area.pack_end(_tamper_area_stack, True, True, 0)

  def _build_page1_setting_inject(self):
    self._inject_area = g.Box(orientation=g.Orientation.VERTICAL)

    _inject_area_stack = g.Stack()
    _inject_area_opts = g.ListBox()

    # 行1
    # _row1 = g.Box(orientation=g.Orientation.HORIZONTAL, spacing=50)
    _row1 = g.Box()
    _db_store = g.ListStore(int, str)
    _db_store.append([1, "access"])
    _db_store.append([11, "mysql"])

    _ckbtn1 = g.CheckButton('数据库类型')
    _db_combobox = g.ComboBox.new_with_model_and_entry(_db_store)
    _db_combobox.set_entry_text_column(1)

    _row1.pack_start(_ckbtn1, True, True, 0)
    _row1.pack_end(_db_combobox, True, True, 0)
    _inject_area_opts.add(_row1)

    # 行2
    _ckbtn2 = g.CheckButton('待测试参数')
    _entry = g.Entry()

    _row2 = g.Box()
    _row2.pack_start(_ckbtn2, True, True, 0)
    _row2.pack_end(_entry, True, True, 0)
    _inject_area_opts.add(_row2)

    # 行3
    _row3 = g.Box()
    _ckbtn3 = g.CheckButton('前缀')
    _entry = g.Entry()

    _row3.pack_start(_ckbtn3, True, True, 0)
    _row3.pack_end(_entry, True, True, 0)
    _inject_area_opts.add(_row3)

    # 行4
    _row4 = g.Box()
    _ckbtn4 = g.CheckButton('后缀')
    _entry = g.Entry()

    _row4.pack_start(_ckbtn4, True, True, 0)
    _row4.pack_end(_entry, True, True, 0)
    _inject_area_opts.add(_row4)

    # 行5
    _row5 = g.Box()
    _ckbtn5 = g.CheckButton('操作系统')
    _entry = g.Entry()

    _row5.pack_start(_ckbtn5, True, True, 0)
    _row5.pack_end(_entry, True, True, 0)
    _inject_area_opts.add(_row5)

    # 行6
    _row6 = g.Box()
    _ckbtn6 = g.CheckButton('跳过某参数')
    _entry = g.Entry()

    _row6.pack_start(_ckbtn6, True, True, 0)
    _row6.pack_end(_entry, True, True, 0)
    _inject_area_opts.add(_row6)

    # 行7
    _row7 = g.Box()
    _ckbtn7 = g.CheckButton('使用逻辑选项')

    _row7.pack_start(_ckbtn7, True, True, 0)
    _inject_area_opts.add(_row7)

    _inject_area_stack.add_titled(_inject_area_opts, '_inject_area_opts', '注入')

    _inject_area_switcher = g.StackSwitcher()
    _inject_area_switcher.set_stack(_inject_area_stack)

    self._inject_area.pack_start(_inject_area_switcher, False, True, 0)
    self._inject_area.pack_end(_inject_area_stack, True, True, 0)

  def _build_page1_request(self):
    self.page1_request = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

  def _build_page1_enumeration(self):
    self.page1_enumeration = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

  def _build_page1_file(self):
    self.page1_file = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

  def _build_page2(self):
    self.page2 = g.Box()
    self.page2.set_border_width(10)
    self.page2.add(g.Label('带图片的页面'))

  def _build_page3(self):
    self.page3 = g.Box()
    self.page3.set_border_width(10)
    self.page3.add(g.Label('带图片的页面'))

  def _build_page4(self):
    self.page4 = g.Box()
    self.page4.set_border_width(10)
    self.page4.add(g.Label('带图片的页面'))


def main():
  win = UI_Window()
  win.connect('destroy', g.main_quit)
  win.show_all()
  g.main()


if __name__ == '__main__':
  main()
