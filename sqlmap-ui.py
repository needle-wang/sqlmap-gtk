#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 08月 26日 星期日 16:54:41 CST
# sqlmap gui gtk-3 by needle wang

from gtk3_header import Gtk as g


class UI_Window(g.Window):
  def __init__(self):
    super().__init__(title='sqlmap-ui')
    # self.set_default_size(700, 0)

    self.notebook = g.Notebook()
    self.add(self.notebook)

    self._build_page1()
    self._build_page2()
    self._build_page3()
    self._build_page4()

    self.notebook.append_page(self.page1, g.Label('功能'))
    self.notebook.append_page(self.page2, g.Label('查看记录'))
    self.notebook.append_page(self.page3, g.Label('帮助'))
    self.notebook.append_page(self.page4, g.Label('关于'))

  def _build_page1(self):
    self.page1 = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)
    self.page1.set_border_width(10)

    # 目标url
    name_store = g.ListStore(int, str)
    name_store.append([1, "www.baidu.com"])
    name_store.append([11, "www.sina.com"])

    _url_area = g.Frame.new('目标url')
    _url_area.set_border_width(0)

    _url_combobox = g.ComboBox.new_with_model_and_entry(name_store)
    _url_combobox.set_size_request(0, 0)
    # _url_combobox.connect('changed', None)
    _url_combobox.set_entry_text_column(1)
    _url_area.add(_url_combobox)

    self.page1.pack_start(_url_area, False, True, 0)

    # sqlmap命令语句
    _cmd_area = g.Frame.new('sqlmap命令语句:')

    _cmd_str = g.Entry()
    _cmd_area.add(_cmd_str)

    self.page1.pack_start(_cmd_area, False, True, 0)

    # 主构造区
    _notebook = g.Notebook()

    # 功能 - 设置, 请求, 枚举, 文件
    self._build_page1_setting()
    self._build_page1_request()
    self._build_page1_enumeration()
    self._build_page1_file()

    _notebook.append_page(self.page1_setting, g.Label('设置'))
    _notebook.append_page(self.page1_request, g.Label('请求'))
    _notebook.append_page(self.page1_enumeration, g.Label('枚举'))
    _notebook.append_page(self.page1_file, g.Label('文件'))

    self.page1.pack_start(_notebook, True, True, 0)

    # 执行
    _exec_area = g.Box()
    _exec_area.pack_start(g.Button('构造命令语句'), False, True, 0)
    _exec_area.pack_end(g.Button('开始'), False, True, 0)

    self.page1.pack_start(_exec_area, True, True, 0)

  def _build_page1_setting(self):
    self.page1_setting = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box(orientation=g.Orientation.HORIZONTAL)

    self._build_page1_setting_inject()
    self._build_page1_setting_tamper()
    self._build_page1_setting_optimize()
    self._build_page1_setting_misc()

    _row1.pack_start(self._inject_area, False, True, 0)
    _row1.pack_start(self._tamper_area, False, True, 0)
    _row1.pack_start(self._optimize_area, False, True, 0)
    _row1.pack_start(self._misc_area, False, True, 0)

    self.page1_setting.pack_start(_row1, True, True, 0)

    _row2 = g.Box(orientation=g.Orientation.HORIZONTAL)

    self._build_page1_setting_check()
    self._build_page1_setting_tech()

    _row2.pack_start(self._check_area, False, True, 0)
    _row2.pack_start(self._tech_area, False, True, 0)

    self.page1_setting.pack_start(_row2, True, True, 0)

  def _build_page1_setting_tech(self):
    # self._tech_area = g.Box(orientation=g.Orientation.VERTICAL)
    self._tech_area = g.Frame.new('技术')

    _tech_area_opts = g.ListBox()

    # 行1
    _row1 = g.Box()
    _tech_store = g.ListStore(int, str)
    _tech_store.append([1, "B"])
    _tech_store.append([2, "E"])

    _ckbtn1 = g.CheckButton('注入技术')
    _tech_combobox = g.ComboBox.new_with_model_and_entry(_tech_store)
    _tech_combobox.set_entry_text_column(1)  # 设成0, 会出现段错误~~, NB!

    _row1.pack_start(_ckbtn1, False, True, 0)
    _row1.pack_end(_tech_combobox, False, True, 0)
    _tech_area_opts.add(_row1)

    # 行2
    _row2 = g.Box()
    _ckbtn2 = g.CheckButton('union数')
    _entry = g.Entry()

    _row2.pack_start(_ckbtn2, False, True, 0)
    _row2.pack_end(_entry, False, True, 0)
    _tech_area_opts.add(_row2)

    # 行3
    _row3 = g.Box()
    _ckbtn3 = g.CheckButton('union字符')
    _entry = g.Entry()

    _row3.pack_start(_ckbtn3, False, True, 0)
    _row3.pack_end(_entry, False, True, 0)
    _tech_area_opts.add(_row3)

    # 行4
    _row4 = g.Box()
    _ckbtn4 = g.CheckButton('查询延迟时间')
    _entry = g.Entry()

    _row4.pack_start(_ckbtn4, False, True, 0)
    _row4.pack_end(_entry, False, True, 0)
    _tech_area_opts.add(_row4)

    self._tech_area.add(_tech_area_opts)

  def _build_page1_setting_check(self):
    self._check_area = g.Frame.new('检测')

    _check_area_opts = g.ListBox()

    # 行1
    _row1 = g.Box()
    _ckbtn1 = g.CheckButton('字符串')
    _entry = g.Entry()

    _row1.pack_start(_ckbtn1, True, True, 0)
    _row1.pack_end(_entry, True, True, 0)
    _check_area_opts.add(_row1)

    # 行2
    _row2 = g.Box()
    _ckbtn2 = g.CheckButton('正则')
    _entry = g.Entry()

    _row2.pack_start(_ckbtn2, True, True, 0)
    _row2.pack_end(_entry, True, True, 0)
    _check_area_opts.add(_row2)

    # 行3
    _row3 = g.Box()
    _ckbtn3 = g.CheckButton('代码')
    _entry = g.Entry()

    _row3.pack_start(_ckbtn3, True, True, 0)
    _row3.pack_end(_entry, True, True, 0)
    _check_area_opts.add(_row3)

    # 行4
    _row4 = g.Box()
    _level_store = g.ListStore(int, str)
    _level_store.append([1, "1"])
    _level_store.append([2, "2"])

    _ckbtn4 = g.CheckButton('等级')
    _level = g.ComboBox.new_with_model_and_entry(_level_store)
    _level.set_entry_text_column(1)  # 设成0, 会出现段错误~~, NB!

    _ckbtn5 = g.CheckButton('仅文本')

    _row4.pack_start(_ckbtn4, False, True, 0)
    _row4.pack_end(_ckbtn5, False, True, 0)
    _row4.pack_end(_level, False, True, 10)
    _check_area_opts.add(_row4)

    # 行5
    _row5 = g.Box()
    _level_store = g.ListStore(int, str)
    _level_store.append([1, "1"])
    _level_store.append([2, "2"])

    _ckbtn5 = g.CheckButton('风险度')
    _risk_combobox = g.ComboBox.new_with_model_and_entry(_level_store)
    _risk_combobox.set_entry_text_column(1)  # 设成0, 会出现段错误~~, NB!

    _ckbtn6 = g.CheckButton('标题')

    _row5.pack_start(_ckbtn5, False, True, 0)
    _row5.pack_end(_ckbtn6, False, True, 0)
    _row5.pack_end(_risk_combobox, False, True, 10)
    _check_area_opts.add(_row5)

    self._check_area.add(_check_area_opts)

  def _build_page1_setting_misc(self):
    self._misc_area = g.Frame.new('其他')

    _misc_area_opts = g.ListBox()

    _misc_area_opts.add(g.CheckButton('详细检测数据库类型'))
    _misc_area_opts.add(g.CheckButton('数据库版本信息'))
    _misc_area_opts.add(g.CheckButton('hex'))
    _misc_area_opts.add(g.CheckButton('无交互模式'))

    _detail_vv_row = g.Box()
    _detail_vv_store = g.ListStore(int, str)
    _detail_vv_store.append([1, "1"])
    _detail_vv_store.append([2, "2"])
    _detail_vv = g.ComboBox.new_with_model_and_entry(_detail_vv_store)
    _detail_vv.set_entry_text_column(1)  # 设成0, 会出现段错误~~, NB!

    _detail_vv_row.pack_start(g.CheckButton('输出详细度'), False, True, 0)
    _detail_vv_row.pack_end(_detail_vv, False, True, 0)
    _misc_area_opts.add(_detail_vv_row)

    self._misc_area.add(_misc_area_opts)

  def _build_page1_setting_optimize(self):
    self._optimize_area = g.Frame.new('优化')

    _optimize_area_opts = g.ListBox()

    _optimize_area_opts.add(g.CheckButton('打开所有优化选项'))
    _optimize_area_opts.add(g.CheckButton('预测输出结果'))
    _optimize_area_opts.add(g.CheckButton('持续连接'))
    _optimize_area_opts.add(g.CheckButton('只比较响应包长度'))
    _thread_num_row = g.Box()

    _thread_num_store = g.ListStore(int, str)
    _thread_num_store.append([1, "1"])
    _thread_num_store.append([2, "2"])
    _thread_num = g.ComboBox.new_with_model_and_entry(_thread_num_store)
    _thread_num.set_entry_text_column(1)  # 设成0, 会出现段错误~~, NB!
    _thread_num_row.pack_start(g.CheckButton('线程数'), False, True, 0)
    _thread_num_row.pack_end(_thread_num, False, True, 0)
    _optimize_area_opts.add(_thread_num_row)

    self._optimize_area.add(_optimize_area_opts)

  def _build_page1_setting_tamper(self):
    self._tamper_area = g.Frame.new('tamper脚本')

    _tamper_area_list = g.ListBox()
    # 最小尺寸
    _tamper_area_list.set_size_request(300, 0)

    _items = '这.py 是 个 啥 ? a d b e e s w e'.split()
    for _item in _items:
      _tamper_area_list.add(g.Label(_item))

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(_tamper_area_list)

    self._tamper_area.add(_scrolled)

  def _build_page1_setting_inject(self):
    self._inject_area = g.Frame.new('注入')

    _inject_area_opts = g.ListBox()

    # 行1
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

    self._inject_area.add(_inject_area_opts)

  def _build_page1_request(self):
    self.page1_request = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    # 行1
    _row1 = g.Box()
    _row1.pack_start(g.Label('POST数据'), False, True, 10)

    # 行2
    _row2 = g.Box()
    _ckbtn_row2 = g.CheckButton()
    _entry_row2 = g.Entry()

    _row2.pack_start(_ckbtn_row2, False, True, 10)
    _row2.pack_start(_entry_row2, True, True, 10)

    # 行3
    _row3 = g.Box()
    _row3.pack_start(g.Label('Cookie'), False, True, 10)

    # 行4
    _row4 = g.Box()
    _ckbtn_row4 = g.CheckButton()
    _entry_row4 = g.Entry()

    _row4.pack_start(_ckbtn_row4, False, True, 10)
    _row4.pack_start(_entry_row4, True, True, 10)

    self.page1_request.pack_start(_row1, False, True, 10)
    self.page1_request.pack_start(_row2, False, True, 10)
    self.page1_request.pack_start(_row3, False, True, 10)
    self.page1_request.pack_start(_row4, False, True, 10)

  def _build_page1_enumeration(self):
    '''
    完全用Gtk.Box和Frame写吧
    '''
    self.page1_enumeration = g.Box(
      orientation=g.Orientation.VERTICAL, spacing=0)

    # 行1
    _row1 = g.Box()
    _row1.props.margin = 10

    self._build_page1_enumeration_enum()
    self._build_page1_enumeration_dump()
    self._build_page1_enumeration_blind()
    self._build_page1_enumeration_limit()

    _row1.pack_start(self._enum_area, False, True, 10)
    _row1.pack_start(self._dump_area, False, True, 10)
    _row1.pack_start(self._blind_area, False, True, 10)
    _row1.pack_start(self._limit_area, False, True, 10)

    self.page1_enumeration.add(_row1)

    # 行2
    _row2 = g.Box()
    _row2.props.margin = 10

    self._build_page1_enumeration_meta()

    _row2.pack_start(self._meta_area, True, True, 10)
    self.page1_enumeration.add(_row2)

    # 行3
    _row3 = g.Box()
    _row3.props.margin = 10
    self._build_page1_enumeration_runsql()

    _row3.pack_start(self._runsql_area, True, True, 10)
    self.page1_enumeration.add(_row3)

  def _build_page1_enumeration_runsql(self):
    self._runsql_area = g.Frame.new('执行SQL语句')

    _runsql_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    # 行1
    _runsql_area_opts_row1 = g.Box()
    _runsql_area_opts_row1.pack_start(g.CheckButton(), False, True, 10)
    _runsql_area_opts_row1.pack_start(g.Entry(), True, True, 10)

    _runsql_area_opts.pack_start(_runsql_area_opts_row1, False, True, 5)
    self._runsql_area.add(_runsql_area_opts)

  def _build_page1_enumeration_meta(self):
    self._meta_area = g.Frame.new('数据库名, 表名, 列名')

    _meta_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    # 行1
    _meta_area_opts_row1 = g.Box()
    _meta_area_opts_row1.pack_start(g.CheckButton('指定数据库名'), False, True, 10)
    _meta_area_opts_row1.pack_start(g.Entry(), True, True, 10)

    # 行2
    _meta_area_opts_row2 = g.Box()
    _meta_area_opts_row2.pack_start(g.CheckButton('指定表名'), False, True, 10)
    _meta_area_opts_row2.pack_start(g.Entry(), True, True, 10)

    # 行3
    _meta_area_opts_row3 = g.Box()
    _meta_area_opts_row3.pack_start(g.CheckButton('指定列名'), False, True, 10)
    _meta_area_opts_row3.pack_start(g.Entry(), True, True, 10)

    _meta_area_opts.pack_start(_meta_area_opts_row1, False, True, 5)
    _meta_area_opts.pack_start(_meta_area_opts_row2, False, True, 5)
    _meta_area_opts.pack_start(_meta_area_opts_row3, False, True, 5)

    self._meta_area.add(_meta_area_opts)

  def _build_page1_enumeration_limit(self):
    self._limit_area = g.Frame.new('limit(限制)')

    _limit_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    # 行1
    _limit_area_opts_row1 = g.Box()
    _limit_area_opts_row1.pack_start(g.CheckButton('始'), False, True, 5)
    _limit_area_opts_row1.pack_start(g.Entry(), False, True, 10)

    # 行2
    _limit_area_opts_row2 = g.Box()
    _limit_area_opts_row2.pack_start(g.CheckButton('末'), False, True, 5)
    _limit_area_opts_row2.pack_start(g.Entry(), False, True, 10)

    _limit_area_opts.pack_start(_limit_area_opts_row1, False, True, 10)
    _limit_area_opts.pack_start(_limit_area_opts_row2, False, True, 10)

    self._limit_area.add(_limit_area_opts)

  def _build_page1_enumeration_blind(self):
    self._blind_area = g.Frame.new('盲注选项')

    _blind_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    # 行1
    _blind_area_opts_row1 = g.Box()
    _blind_area_opts_row1.pack_start(g.CheckButton('第一字符'), False, True, 5)
    _blind_area_opts_row1.pack_start(g.Entry(), False, True, 10)

    # 行2
    _blind_area_opts_row2 = g.Box()
    _blind_area_opts_row2.pack_start(g.CheckButton('最末字符'), False, True, 5)
    _blind_area_opts_row2.pack_start(g.Entry(), False, True, 10)

    _blind_area_opts.pack_start(_blind_area_opts_row1, False, True, 10)
    _blind_area_opts.pack_start(_blind_area_opts_row2, False, True, 10)

    self._blind_area.add(_blind_area_opts)

  def _build_page1_enumeration_dump(self):
    self._dump_area = g.Frame.new('Dump(转储)')

    _dump_area_opts = g.Box(spacing=6)

    _dump_area_opts_cols = g.Box(orientation=g.Orientation.VERTICAL)

    _ckbtn1 = g.CheckButton('dump(拖库)')
    _ckbtn2 = g.CheckButton('全部dump')
    _ckbtn3 = g.CheckButton('搜索')
    _ckbtn4 = g.CheckButton('不包含系统数据库')

    _dump_area_opts_cols.add(_ckbtn1)
    _dump_area_opts_cols.add(_ckbtn2)
    _dump_area_opts_cols.add(_ckbtn3)
    _dump_area_opts_cols.add(_ckbtn4)

    _dump_area_opts.pack_start(_dump_area_opts_cols, False, True, 10)

    self._dump_area.add(_dump_area_opts)

  def _build_page1_enumeration_enum(self):
    self._enum_area = g.Frame.new('枚举')

    _enu_area_opts = g.Box(spacing=6)  # 添加三列, 方便对齐...
    _enu_area_opts_list = (
      ('当前用户' , '当前数据库' , '是否是DBA' , '用户')   ,
      ('密码'     , '权限'       , '角色'      , '数据库') ,
      ('表'       , '字段'       , '架构'      , '计数')   ,
    )

    # Do not use: [g.Box()] * 3, 会有闭包现象
    _enu_area_opts_cols = []
    for _x in range(len(_enu_area_opts_list)):
      _enu_area_opts_cols.append(g.Box(orientation=g.Orientation.VERTICAL))
      for _y in _enu_area_opts_list[_x]:
        _enu_area_opts_cols[_x].add(g.CheckButton(_y))
      _enu_area_opts.pack_start(_enu_area_opts_cols[_x], False, True, 10)

    self._enum_area.add(_enu_area_opts)

  def _build_page1_file(self):
    self.page1_file = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    # 行1
    _row1 = g.Box(orientation=g.Orientation.HORIZONTAL)
    _row1.props.margin = 10

    self._build_page1_file_read()

    _row1.pack_start(self._file_read_area, True, True, 10)

    self.page1_file.add(_row1)

    # 行2
    _row2 = g.Box(orientation=g.Orientation.HORIZONTAL)
    _row2.props.margin = 10

    self._build_page1_file_type()
    self._build_page1_file_logfile()

    _row2.pack_start(self._file_type_area, False, True, 10)
    _row2.pack_start(self._file_logfile_area, True, True, 10)

    self.page1_file.add(_row2)

  def _build_page1_file_logfile(self):
    self._file_logfile_area = g.Frame.new('默认*log, *config')

  def _build_page1_file_type(self):
    self._file_type_area = g.Frame.new('类别')

    # _file_type_area_list = g.ListBox()
    # _file_type_area_list.set_size_request(300, 200)

    # _file_type_area_list.add(g.TextView())

    _file_type_area_list = g.TextView()
    _file_type_area_list.set_size_request(300, 200)

    self._file_type_area.add(_file_type_area_list)

  def _build_page1_file_read(self):
    self._file_read_area = g.Frame.new('读文件')

    _file_read_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    # 行1
    _file_read_area_opts_row1 = g.Box()

    _file_read_area_opts_row1.pack_start(g.CheckButton(), False, True, 10)
    _file_read_area_opts_row1.pack_start(g.Entry(), True, True, 10)
    _file_read_area_opts_row1.pack_start(g.Button('在记录中查看'), False, True, 10)

    _file_read_area_opts.pack_start(_file_read_area_opts_row1, False, True, 5)

    self._file_read_area.add(_file_read_area_opts)

  def _build_page2(self):
    self.page2 = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)
    self.page2.set_border_width(10)

    # 行1
    _row1 = g.Frame()

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(g.TextView())

    _row1.add(_scrolled)

    self.page2.pack_start(_row1, True, True, 10)

    # 行2
    _row2 = g.Box()

    _row2.pack_end(g.Button(' log '), False, True, 0)
    _row2.pack_end(g.Button(' session '), False, True, 30)

    self.page2.pack_end(_row2, False, True, 0)

  def _build_page3(self):
    self.page3 = g.Box(orientation=g.Orientation.VERTICAL)
    self.page3.set_border_width(10)

    # 行1
    _row1 = g.Frame()

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(g.TextView())

    _row1.add(_scrolled)

    self.page3.pack_start(_row1, True, True, 10)

  def _build_page4(self):
    self.page4 = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)
    self.page4.set_border_width(10)

    _about_str = '''
    0. VERSION: 0.1\n
    1. 作者: needle wang ( needlewang2011@gmail.com )\n\n
    2. 使用PyGObject(Gtk-3: python3-gi)重写sqm.py的界面\n
    3. Gtk-3教程: https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html\n
    4. Gtk-3 API: https://lazka.github.io/pgi-docs/Gtk-3.0/\n\n
    5. 感谢sqm的原作者, sqm UI 使用的是tkinter\n
    6. 界面上的中文参考的是 ettack ( ettack@gmail.com ) 汉化的sqm.py\n
    '''
    self.page4.pack_start(g.Label(_about_str), True, False, 0)


def main():
  win = UI_Window()
  win.connect('destroy', g.main_quit)
  win.show_all()
  g.main()


if __name__ == '__main__':
  main()
