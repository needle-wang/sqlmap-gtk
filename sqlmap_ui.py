#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 08月 26日 星期日 16:54:41 CST
# sqlmap gui gtk-3 by needle wang

from gtk3_header import Gdk as d
from gtk3_header import Gtk as g

from sqlmap_ui_handlers import Singal_Handlers as handlers


class UI_Window(g.Window):
  def __init__(self):
    super().__init__(title='sqlmap-ui')
    self.connect('key_press_event', self.on_window_key_press_event)
    self._handlers = handlers(self)

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

  # 如果是实现do_key_press_event, 那事件就传不出去了, why?
  def on_window_key_press_event(self, widget, event: d.EventKey):
    keysym = event.keyval  # see: gdk/gdkkeysyms.h
    # key_name = d.keyval_name(keysym)
    # print('(keysym %s, %s)' % (keysym, key_name))

    state = event.state
    _ctrl = (state & d.ModifierType.CONTROL_MASK)

    if _ctrl and(keysym == d.KEY_q or keysym == d.KEY_w):
      g.main_quit()
      return True

  def _build_page1(self):
    self.page1 = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)
    self.page1.set_border_width(10)

    # 目标url
    name_store = g.ListStore(int, str)
    name_store.append([1, "www.google.com?id=1"])

    _target_notbook = g.Notebook()

    _url_area = g.Box()

    self._url_combobox = g.ComboBox.new_with_model_and_entry(name_store)
    self._url_combobox.set_size_request(0, 0)
    self._url_combobox.set_entry_text_column(1)
    _url_area.pack_start(self._url_combobox, True, True, 0)

    _target_notbook.append_page(_url_area, g.Label('目标url'))

    _burp_area = g.Box()

    self._burp_logfile = g.Entry()
    self._burp_logfile.set_text('-l: Burp或WebScarab代理的日志文件路径(用来解析目标)')

    _burp_area.pack_start(self._burp_logfile, True, True, 0)

    _target_notbook.append_page(_burp_area, g.Label('burp日志'))

    _request_area = g.Box()

    self._request_file = g.Entry()
    self._request_file.set_text('-r: 包含HTTP请求的的文件路径')

    _request_area.pack_start(self._request_file, True, True, 0)

    _target_notbook.append_page(_request_area, g.Label('HTTP请求'))

    self.page1.pack_start(_target_notbook, False, True, 0)

    # sqlmap命令语句
    _cmd_area = g.Frame.new('sqlmap命令语句:')

    self._cmd_entry = g.Entry()

    # 没用呢?
    # _scrolled = g.ScrolledWindow()
    # _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.NEVER)
    # _scrolled.add(self._cmd_entry)
    # _cmd_area.add(_scrolled)
    _cmd_area.add(self._cmd_entry)

    self.page1.pack_start(_cmd_area, False, True, 0)

    # 主构造区
    _notebook = g.Notebook()

    # 功能 - 设置, 请求, 枚举, 文件
    self._build_page1_setting()
    self._build_page1_request()
    self._build_page1_enumeration()
    self._build_page1_file()

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(self.page1_setting)
    _notebook.append_page(_scrolled, g.Label('设置'))

    # _notebook.append_page(self.page1_setting, g.Label('设置'))
    _notebook.append_page(self.page1_request, g.Label('请求'))
    _notebook.append_page(self.page1_enumeration, g.Label('枚举'))
    _notebook.append_page(self.page1_file, g.Label('文件'))

    self.page1.pack_start(_notebook, True, True, 0)

    # 构造与执行
    _exec_area = g.Box()

    _build_button = g.Button('构造命令语句')
    _build_button.connect('clicked', self._handlers.build_all)

    _run_button = g.Button('开始')
    _run_button.connect('clicked', self._handlers.run_cmd)

    _exec_area.pack_start(_build_button, False, True, 0)
    _exec_area.pack_end(_run_button, False, True, 0)

    self.page1.pack_end(_exec_area, False, True, 0)

  def _build_page1_setting(self):
    self.page1_setting = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box(orientation=g.Orientation.HORIZONTAL)

    self._build_page1_setting_inject()
    self._build_page1_setting_detection()
    self._build_page1_setting_tech()

    _row1.pack_start(self._inject_area, False, True, 0)
    _row1.pack_start(self._detection_area, False, True, 0)
    _row1.pack_start(self._tech_area, False, True, 0)

    self.page1_setting.pack_start(_row1, True, True, 0)

    _row2 = g.Box(orientation=g.Orientation.HORIZONTAL)

    self._build_page1_setting_tamper()
    self._build_page1_setting_optimize()
    self._build_page1_setting_general()

    _row2.pack_start(self._tamper_area, False, True, 0)
    _row2.pack_start(self._optimize_area, False, True, 0)
    _row2.pack_start(self._general_area, False, True, 0)

    self.page1_setting.pack_start(_row2, True, True, 0)

  def _build_page1_setting_tech(self):
    # self._tech_area = g.Box(orientation=g.Orientation.VERTICAL)
    self._tech_area = g.Frame.new('各注入技术的选项')

    _tech_area_opts = g.ListBox()

    # 行1
    _row1 = g.Box()

    self._tech_area_tech_ckbtn = g.CheckButton('注入技术')
    self._tech_area_tech_entry = g.Entry()
    self._tech_area_tech_entry.set_text('BEUSTQ')

    _row1.pack_start(self._tech_area_tech_ckbtn, False, True, 0)
    _row1.pack_end(self._tech_area_tech_entry, False, True, 0)
    _tech_area_opts.add(_row1)

    # 行2
    _row2 = g.Box()
    self._tech_area_time_sec_ckbtn = g.CheckButton('指定DB响应的延迟秒数')
    self._tech_area_time_sec_entry = g.Entry()
    self._tech_area_time_sec_entry.set_text('(时间盲注时)')

    _row2.pack_start(self._tech_area_time_sec_ckbtn, False, True, 0)
    _row2.pack_end(self._tech_area_time_sec_entry, False, True, 0)
    _tech_area_opts.add(_row2)

    # 行3
    _row3 = g.Box()
    self._tech_area_union_col_ckbtn = g.CheckButton('指定最大union列数')
    self._tech_area_union_col_entry = g.Entry()
    self._tech_area_union_col_entry.set_text('(union查询时)')

    _row3.pack_start(self._tech_area_union_col_ckbtn, False, True, 0)
    _row3.pack_end(self._tech_area_union_col_entry, False, True, 0)
    _tech_area_opts.add(_row3)

    # 行4
    _row4 = g.Box()
    self._tech_area_union_chr_ckbtn = g.CheckButton('指定枚举列数时所用字符')
    self._tech_area_union_chr_entry = g.Entry()
    self._tech_area_union_chr_entry.set_text('(union查询时)')

    _row4.pack_start(self._tech_area_union_chr_ckbtn, False, True, 0)
    _row4.pack_end(self._tech_area_union_chr_entry, False, True, 0)
    _tech_area_opts.add(_row4)

    # 行5
    _row5 = g.Box()
    self._tech_area_union_table_ckbtn = g.CheckButton('指定枚举列数时from的表名')
    self._tech_area_union_table_entry = g.Entry()
    self._tech_area_union_table_entry.set_text('(union查询时)')

    _row5.pack_start(self._tech_area_union_table_ckbtn, False, True, 0)
    _row5.pack_end(self._tech_area_union_table_entry, False, True, 0)
    _tech_area_opts.add(_row5)

    # 行6
    _row6 = g.Box()
    self._tech_area_dns_ckbtn = g.CheckButton('指定DNS')
    self._tech_area_dns_entry = g.Entry()
    self._tech_area_dns_entry.set_text('(DNS exfiltration)')

    _row6.pack_start(self._tech_area_dns_ckbtn, True, True, 0)
    _row6.pack_end(self._tech_area_dns_entry, True, True, 0)
    _tech_area_opts.add(_row6)

    # 行7
    _row7 = g.Box()
    self._tech_area_second_url_ckbtn = g.CheckButton('指定秒序响应的url')
    self._tech_area_second_url_entry = g.Entry()

    _row7.pack_start(self._tech_area_second_url_ckbtn, True, True, 0)
    _row7.pack_end(self._tech_area_second_url_entry, True, True, 0)
    _tech_area_opts.add(_row7)

    # 行8
    _row8 = g.Box()
    self._tech_area_second_req_url_ckbtn = g.CheckButton('指定含秒序HTTP请求的文件')
    self._tech_area_second_req_url_entry = g.Entry()

    _row8.pack_start(self._tech_area_second_req_url_ckbtn, True, True, 0)
    _row8.pack_end(self._tech_area_second_req_url_entry, True, True, 0)
    _tech_area_opts.add(_row8)

    self._tech_area.add(_tech_area_opts)

  def _build_page1_setting_detection(self):
    self._detection_area = g.Frame.new('探测选项')

    _check_area_opts = g.ListBox()

    # 行1
    _row1 = g.Box()
    _level_store = g.ListStore(int, str)
    _level_store.append([1, "1"])
    _level_store.append([2, "2"])

    self._check_area_level_ckbtn = g.CheckButton('探测等级(范围)')
    self._check_area_level_combobox = g.ComboBox.new_with_model_and_entry(_level_store)
    self._check_area_level_combobox.set_entry_text_column(1)  # 设成0, 会出现段错误~~, NB!
    self._check_area_level_combobox.get_child().set_text('默认为1')

    self._check_area_text_only_ckbtn = g.CheckButton('仅对比文本')

    _row1.pack_start(self._check_area_level_ckbtn, False, True, 0)
    _row1.pack_start(self._check_area_level_combobox, True, False, 10)
    _row1.pack_start(self._check_area_text_only_ckbtn, False, True, 0)
    _check_area_opts.add(_row1)

    # 行2
    _row2 = g.Box()
    _level_store = g.ListStore(int, str)
    _level_store.append([1, "1"])
    _level_store.append([2, "2"])

    self._check_area_risk_ckbtn = g.CheckButton('payload危险等级')
    self._check_area_risk_combobox = g.ComboBox.new_with_model_and_entry(_level_store)
    self._check_area_risk_combobox.set_entry_text_column(1)  # 设成0, 会出现段错误~~, NB!
    self._check_area_risk_combobox.get_child().set_text('默认为1')

    self._check_area_titles_ckbtn = g.CheckButton('仅对比title')

    _row2.pack_start(self._check_area_risk_ckbtn, False, True, 0)
    _row2.pack_start(self._check_area_risk_combobox, True, False, 10)
    _row2.pack_start(self._check_area_titles_ckbtn, False, True, 0)
    _check_area_opts.add(_row2)

    # 行3
    _row3 = g.Box()
    self._check_area_str_ckbtn = g.CheckButton('指定字符串')
    self._check_area_str_entry = g.Entry()
    self._check_area_str_entry.set_text('(查询为真时的)')

    _row3.pack_start(self._check_area_str_ckbtn, False, True, 0)
    _row3.pack_end(self._check_area_str_entry, True, True, 5)
    _check_area_opts.add(_row3)

    # 行4
    _row4 = g.Box()
    self._check_area_re_ckbtn = g.CheckButton('指定正则')
    self._check_area_re_entry = g.Entry()
    self._check_area_re_entry.set_text('(查询为真时的)')

    _row4.pack_start(self._check_area_re_ckbtn, False, True, 0)
    _row4.pack_end(self._check_area_re_entry, True, True, 5)
    _check_area_opts.add(_row4)

    # 行5
    _row5 = g.Box()
    self._check_area_code_ckbtn = g.CheckButton('指定http状态码')
    self._check_area_code_entry = g.Entry()
    self._check_area_code_entry.set_text('(查询为真时)')

    _row5.pack_start(self._check_area_code_ckbtn, False, True, 0)
    _row5.pack_end(self._check_area_code_entry, True, True, 5)
    _check_area_opts.add(_row5)

    self._detection_area.add(_check_area_opts)

  def _build_page1_setting_general(self):
    self._general_area = g.Frame.new('通用选项')

    # _general_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=10)
    _general_area_opts = g.ListBox()

    self._general_area_finger_chkbtn = g.CheckButton('执行宽泛的DB版本检测(--fingerprint)')
    self._general_area_batch_ckbtn = g.CheckButton('非交互模式(--batch), 使用默认行为')
    self._general_area_hex_ckbtn = g.CheckButton('获取数据时使用hex转换(--hex)')

    _general_area_opts.add(self._general_area_finger_chkbtn)
    _general_area_opts.add(self._general_area_batch_ckbtn)
    _general_area_opts.add(self._general_area_hex_ckbtn)

    _detail_vv_row = g.Box()

    self._general_area_verbose_ckbtn = g.CheckButton('输出详细度')

    _detail_vv_store = g.ListStore(int, str)
    _detail_vv_store.append([1, "1"])
    _detail_vv_store.append([2, "2"])

    self._detail_vv_combobox = g.ComboBox.new_with_model_and_entry(_detail_vv_store)
    self._detail_vv_combobox.set_entry_text_column(1)  # 设成0, 会出现段错误~~, NB!

    _detail_vv_row.pack_start(self._general_area_verbose_ckbtn, False, True, 0)
    _detail_vv_row.pack_end(self._detail_vv_combobox, False, True, 0)

    _general_area_opts.add(_detail_vv_row)

    self._general_area.add(_general_area_opts)

  def _build_page1_setting_optimize(self):
    self._optimize_area = g.Frame.new('性能优化')

    _optimize_area_opts = g.ListBox()

    self._optimize_area_turn_all_ckbtn = g.CheckButton('启用所有优化选项')
    _optimize_area_opts.add(self._optimize_area_turn_all_ckbtn)

    self._optimize_area_predict_ckbtn = g.CheckButton('预测通常的查询结果')
    _optimize_area_opts.add(self._optimize_area_predict_ckbtn)

    self._optimize_area_keep_alive_ckbtn = g.CheckButton('http连接使用keep-alive')
    _optimize_area_opts.add(self._optimize_area_keep_alive_ckbtn)

    self._optimize_area_null_connect_ckbtn = g.CheckButton('只比较页面长度, 而非内容')
    _optimize_area_opts.add(self._optimize_area_null_connect_ckbtn)

    _thread_num_row = g.Box()

    self._optimize_area_thread_num_ckbtn = g.CheckButton('启用多线程(数量):')
    _thread_num_row.pack_start(self._optimize_area_thread_num_ckbtn, False, True, 0)

    _thread_num_store = g.ListStore(int, str)
    _thread_num_store.append([1, "2"])
    _thread_num_store.append([2, "4"])
    self._optimize_area_thread_num_combobox = g.ComboBox.new_with_model_and_entry(_thread_num_store)
    # set_entry_text_column(0)会出现段错误~~, NB!
    self._optimize_area_thread_num_combobox.set_entry_text_column(1)
    self._optimize_area_thread_num_combobox.get_child().set_text('默认为1')

    _thread_num_row.pack_end(self._optimize_area_thread_num_combobox, False, True, 0)

    _optimize_area_opts.add(_thread_num_row)

    self._optimize_area.add(_optimize_area_opts)

  def _build_page1_setting_tamper(self):
    self._tamper_area = g.Frame.new('tamper脚本')

    _tamper_area_list = g.Box()
    # 最小尺寸
    _tamper_area_list.set_size_request(300, 0)

    _tamper_area_list.pack_start(g.TextView(), True, True, 0)

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(_tamper_area_list)

    self._tamper_area.add(_scrolled)

  def _build_page1_setting_inject(self):
    self._inject_area = g.Frame.new('注入选项')

    _inject_area_opts = g.ListBox()

    # 行1
    self._inject_area_param_ckbtn = g.CheckButton('可测试的参数')
    self._inject_area_param_entry = g.Entry()
    self._inject_area_param_entry.set_text('id')

    _row1 = g.Box()
    _row1.pack_start(self._inject_area_param_ckbtn, True, True, 0)
    _row1.pack_end(self._inject_area_param_entry, True, True, 0)
    _inject_area_opts.add(_row1)

    # 行2
    _row2 = g.Box()
    self._inject_area_skip_ckbtn = g.CheckButton('排除参数')
    self._inject_area_skip_entry = g.Entry()
    self._inject_area_skip_entry.set_text('...,...')

    _row2.pack_start(self._inject_area_skip_ckbtn, True, True, 0)
    _row2.pack_end(self._inject_area_skip_entry, True, True, 0)
    _inject_area_opts.add(_row2)

    # 行3
    _row3 = g.Box()
    self._inject_area_skip_static_ckbtn = g.CheckButton('跳过无动态特性的参数')

    _row3.pack_start(self._inject_area_skip_static_ckbtn, True, True, 0)
    _inject_area_opts.add(_row3)

    # 行4
    _row4 = g.Box()
    _db_store = g.ListStore(int, str)
    _db_store.append([1, "access"])
    _db_store.append([11, "mysql"])

    self._inject_area_dbms_ckbtn = g.CheckButton('固定DB类型为')
    self._inject_area_dbms_combobox = g.ComboBox.new_with_model_and_entry(
      _db_store)
    self._inject_area_dbms_combobox.set_entry_text_column(1)

    _row4.pack_start(self._inject_area_dbms_ckbtn, True, True, 0)
    _row4.pack_end(self._inject_area_dbms_combobox, True, True, 0)
    _inject_area_opts.add(_row4)

    # 行5
    _row5 = g.Box()
    self._inject_area_os_ckbtn = g.CheckButton('固定OS为')
    self._inject_area_os_entry = g.Entry()

    _row5.pack_start(self._inject_area_os_ckbtn, True, True, 0)
    _row5.pack_end(self._inject_area_os_entry, True, True, 0)
    _inject_area_opts.add(_row5)

    # 行6
    _row6 = g.Box()
    self._inject_area_logic_ckbtn = g.CheckButton('对payload中的废值使用逻辑运算符')

    _row6.pack_start(self._inject_area_logic_ckbtn, True, True, 0)
    _inject_area_opts.add(_row6)

    # 行7
    _row7 = g.Box()
    self._inject_area_logic_ckbtn = g.CheckButton('关掉payload变形机制')

    _row7.pack_start(self._inject_area_logic_ckbtn, True, True, 0)
    _inject_area_opts.add(_row7)

    # 行8
    _row8 = g.Box()
    self._inject_area_logic_ckbtn = g.CheckButton('关掉string转义')

    _row8.pack_start(self._inject_area_logic_ckbtn, True, True, 0)
    _inject_area_opts.add(_row8)

    # 行9
    _row9 = g.Box()
    self._inject_area_prefix_ckbtn = g.CheckButton('payload前缀')
    self._inject_area_prefix_entry = g.Entry()
    self._inject_area_prefix_entry.set_text('用于闭合')

    _row9.pack_start(self._inject_area_prefix_ckbtn, True, True, 0)
    _row9.pack_end(self._inject_area_prefix_entry, True, True, 0)
    _inject_area_opts.add(_row9)

    # 行10
    _row10 = g.Box()
    self._inject_area_suffix_ckbtn = g.CheckButton('payload后缀')
    self._inject_area_suffix_entry = g.Entry()

    _row10.pack_start(self._inject_area_suffix_ckbtn, True, True, 0)
    _row10.pack_end(self._inject_area_suffix_entry, True, True, 0)
    _inject_area_opts.add(_row10)

    self._inject_area.add(_inject_area_opts)

  def _build_page1_request(self):
    self.page1_request = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    # 行1
    _row1 = g.Box()
    _row1.pack_start(g.Label('POST数据'), False, True, 10)

    # 行2
    _row2 = g.Box()
    self.page1_request_post_ckbtn = g.CheckButton()
    self.page1_request_post_entry = g.Entry()

    _row2.pack_start(self.page1_request_post_ckbtn, False, True, 10)
    _row2.pack_start(self.page1_request_post_entry, True, True, 10)

    # 行3
    _row3 = g.Box()
    _row3.pack_start(g.Label('Cookie'), False, True, 10)

    # 行4
    _row4 = g.Box()
    self._cookie_ckbtn = g.CheckButton()
    self._cookie_entry = g.Entry()

    _row4.pack_start(self._cookie_ckbtn, False, True, 10)
    _row4.pack_start(self._cookie_entry, True, True, 10)

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
    self._build_page1_enumeration_limit()
    self._build_page1_enumeration_blind()

    _row1.pack_start(self._enum_area, False, True, 10)
    _row1.pack_start(self._dump_area, False, True, 10)
    _row1.pack_start(self._limit_area, False, True, 10)
    _row1.pack_start(self._blind_area, False, True, 10)

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
    self._runsql_area_runsql_ckbtn = g.CheckButton()
    self._runsql_area_runsql_entry = g.Entry()
    _runsql_area_opts_row1.pack_start(self._runsql_area_runsql_ckbtn, False, True, 10)
    _runsql_area_opts_row1.pack_start(self._runsql_area_runsql_entry, True, True, 10)

    _runsql_area_opts.pack_start(_runsql_area_opts_row1, False, True, 5)
    self._runsql_area.add(_runsql_area_opts)

  def _build_page1_enumeration_meta(self):
    self._meta_area = g.Frame.new('数据库名, 表名, 列名')

    _meta_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    # 行1
    _meta_area_opts_row1 = g.Box()

    self._meta_area_D_ckbtn = g.CheckButton('指定数据库名')
    self._meta_area_D_entry = g.Entry()

    _meta_area_opts_row1.pack_start(self._meta_area_D_ckbtn, False, True, 10)
    _meta_area_opts_row1.pack_start(self._meta_area_D_entry, True, True, 10)

    _meta_area_opts.pack_start(_meta_area_opts_row1, False, True, 5)

    # 行2
    _meta_area_opts_row2 = g.Box()

    self._meta_area_T_ckbtn = g.CheckButton('指定表名')
    self._meta_area_T_entry = g.Entry()

    _meta_area_opts_row2.pack_start(self._meta_area_T_ckbtn, False, True, 10)
    _meta_area_opts_row2.pack_start(self._meta_area_T_entry, True, True, 10)

    _meta_area_opts.pack_start(_meta_area_opts_row2, False, True, 5)

    # 行3
    _meta_area_opts_row3 = g.Box()

    self._meta_area_C_ckbtn = g.CheckButton('指定列名')
    self._meta_area_C_entry = g.Entry()

    _meta_area_opts_row3.pack_start(self._meta_area_C_ckbtn, False, True, 10)
    _meta_area_opts_row3.pack_start(self._meta_area_C_entry, True, True, 10)

    _meta_area_opts.pack_start(_meta_area_opts_row3, False, True, 5)

    # 行4
    _meta_area_opts_row4 = g.Box()

    self._meta_area_where_ckbtn = g.CheckButton('where子句')
    self._meta_area_where_entry = g.Entry()

    _meta_area_opts_row4.pack_start(self._meta_area_where_ckbtn, False, True, 10)
    _meta_area_opts_row4.pack_start(self._meta_area_where_entry, True, True, 10)

    _meta_area_opts.pack_start(_meta_area_opts_row4, False, True, 5)

    self._meta_area.add(_meta_area_opts)

  def _build_page1_enumeration_limit(self):
    self._limit_area = g.Frame.new('limit(dump时的限制)')

    _limit_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    # 行1
    _limit_area_opts_row1 = g.Box()

    self._limit_area_start_ckbtn = g.CheckButton('始于第')
    self._limit_area_start_entry = g.Entry()

    _limit_area_opts_row1.pack_start(self._limit_area_start_ckbtn, False, True, 5)
    _limit_area_opts_row1.pack_start(self._limit_area_start_entry, False, True, 0)
    _limit_area_opts_row1.pack_start(g.Label('条'), False, True, 5)

    # 行2
    _limit_area_opts_row2 = g.Box()

    self._limit_area_stop_ckbtn = g.CheckButton('止于第')
    self._limit_area_stop_entry = g.Entry()

    _limit_area_opts_row2.pack_start(self._limit_area_stop_ckbtn, False, True, 5)
    _limit_area_opts_row2.pack_start(self._limit_area_stop_entry, False, True, 0)
    _limit_area_opts_row2.pack_start(g.Label('条'), False, True, 5)

    _limit_area_opts.pack_start(_limit_area_opts_row1, False, True, 10)
    _limit_area_opts.pack_start(_limit_area_opts_row2, False, True, 10)

    self._limit_area.add(_limit_area_opts)

  def _build_page1_enumeration_blind(self):
    self._blind_area = g.Frame.new('盲注选项')

    _blind_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    # 行1
    _blind_area_opts_row1 = g.Box()

    self._blind_area_first_ckbtn = g.CheckButton('首字符')
    self._blind_area_first_entry = g.Entry()

    _blind_area_opts_row1.pack_start(self._blind_area_first_ckbtn, False, True, 5)
    _blind_area_opts_row1.pack_start(self._blind_area_first_entry, False, True, 10)

    _blind_area_opts.pack_start(_blind_area_opts_row1, False, True, 10)

    # 行2
    _blind_area_opts_row2 = g.Box()

    self._blind_area_last_ckbtn = g.CheckButton('末字符')
    self._blind_area_last_entry = g.Entry()

    _blind_area_opts_row2.pack_start(self._blind_area_last_ckbtn, False, True, 5)
    _blind_area_opts_row2.pack_start(self._blind_area_last_entry, False, True, 10)

    _blind_area_opts.pack_start(_blind_area_opts_row2, False, True, 10)

    self._blind_area.add(_blind_area_opts)

  def _build_page1_enumeration_dump(self):
    self._dump_area = g.Frame.new('Dump(转储)')

    _dump_area_opts = g.Box(spacing=6)

    _dump_area_opts_cols = g.Box(orientation=g.Orientation.VERTICAL)

    self._dump_area_dump_ckbtn = g.CheckButton('dump(某库某表的条目)')
    self._dump_area_dump_all_ckbtn = g.CheckButton('全部dump(拖库)')
    self._dump_area_search_ckbtn = g.CheckButton('搜索')
    self._dump_area_no_sys_db_ckbtn = g.CheckButton('排除系统库')

    _dump_area_opts_cols.add(self._dump_area_dump_ckbtn)
    _dump_area_opts_cols.add(self._dump_area_dump_all_ckbtn)
    _dump_area_opts_cols.add(self._dump_area_search_ckbtn)
    _dump_area_opts_cols.add(self._dump_area_no_sys_db_ckbtn)

    _dump_area_opts.pack_start(_dump_area_opts_cols, False, True, 10)

    self._dump_area.add(_dump_area_opts)

  def _build_page1_enumeration_enum(self):
    self._enum_area = g.Frame.new('枚举')

    _enum_area_opts = g.Box(spacing=6)  # 添加三列, 方便对齐...
    _enum_area_opts_list = (
      ('DB banner', '当前用户', '当前数据库', '主机名', '是否是DBA'),
      ('用户', '密码', '权限', '角色', '数据库'),
      ('表', '字段', '架构', '计数'),
    )
    self._enum_area_opts_ckbtns = []

    # Do not use: [g.Box()] * 3, 会有闭包现象
    _enu_area_opts_cols = []
    for _x in range(len(_enum_area_opts_list)):
      self._enum_area_opts_ckbtns.append([])
      _enu_area_opts_cols.append(g.Box(orientation=g.Orientation.VERTICAL))

      for _y in _enum_area_opts_list[_x]:
        _tmp = g.CheckButton(_y)
        self._enum_area_opts_ckbtns[_x].append(_tmp)
        _enu_area_opts_cols[_x].add(_tmp)

      _enum_area_opts.pack_start(_enu_area_opts_cols[_x], False, True, 10)

    self._enum_area.add(_enum_area_opts)

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

    self._build_page1_file_write()

    _row2.pack_start(self._file_write_area, True, True, 10)

    self.page1_file.add(_row2)

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

  def _build_page1_file_write(self):
    self._file_write_area = g.Frame.new('文件上传')

    _file_write_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    # 行1
    _file_write_area_opts_row1 = g.Box()

    self._file_read_area_udf_ckbtn = g.CheckButton('注入sqlmap自带的用户定义函数(--udf-inject)')

    _file_write_area_opts_row1.pack_start(self._file_read_area_udf_ckbtn, False, True, 5)

    self._file_read_area_shared_lib_ckbtn = g.CheckButton('本地共享库路径(--shared-lib)')
    self._file_read_area_shared_lib_entry = g.Entry()
    self._file_read_area_shared_lib_entry.set_text('与--udf-inject配套使用, 可选')

    _file_write_area_opts_row1.pack_start(self._file_read_area_shared_lib_ckbtn, False, True, 5)
    _file_write_area_opts_row1.pack_start(self._file_read_area_shared_lib_entry, True, True, 5)

    _file_write_area_opts.pack_start(_file_write_area_opts_row1, False, True, 5)

    # 行2
    _file_write_area_opts_row2 = g.Box()

    self._file_read_area_file_write_ckbtn = g.CheckButton('本地文件路径(--file-write=)')
    self._file_read_area_file_write_entry = g.Entry()
    self._file_read_area_file_write_entry.set_text('若使用此选项, 则--file-dest为必选项')

    _file_write_area_opts_row2.pack_start(self._file_read_area_file_write_ckbtn, False, True, 5)
    _file_write_area_opts_row2.pack_start(self._file_read_area_file_write_entry, True, True, 5)

    _file_write_area_opts.pack_start(_file_write_area_opts_row2, False, True, 5)

    # 行3
    _file_write_area_opts_row3 = g.Box()

    self._file_read_area_file_dest_ckbtn = g.CheckButton('远程文件路径(--file-dest=)')
    self._file_read_area_file_dest_entry = g.Entry()
    self._file_read_area_file_dest_entry.set_text('与本地文件路径配套使用, 单独勾选无意义(要求是绝对路径, 构造后会有引号!)')

    _file_write_area_opts_row3.pack_start(self._file_read_area_file_dest_ckbtn, False, True, 5)
    _file_write_area_opts_row3.pack_start(self._file_read_area_file_dest_entry, True, True, 5)

    _file_write_area_opts.pack_start(_file_write_area_opts_row3, False, True, 5)

    self._file_write_area.add(_file_write_area_opts)

  def _build_page1_file_read(self):
    self._file_read_area = g.Frame.new('读取远程文件')

    _file_read_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    # 行1
    _file_read_area_opts_row1 = g.Box()

    self._file_read_area_file_read_ckbtn = g.CheckButton('远程文件路径(--file-read=)')
    self._file_read_area_file_read_entry = g.Entry()
    self._file_read_area_file_read_entry.set_text('远程DB所在服务器上的文件路径')
    self._file_read_area_file_btn = g.Button('在记录中查看')

    _file_read_area_opts_row1.pack_start(self._file_read_area_file_read_ckbtn, False, True, 10)
    _file_read_area_opts_row1.pack_start(self._file_read_area_file_read_entry, True, True, 10)
    _file_read_area_opts_row1.pack_start(self._file_read_area_file_btn, False, True, 10)

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
    1. VERSION: 0.1
       2018年 08月 31日 星期五 18:22:06 CST
       作者: needle wang ( needlewang2011@gmail.com )\n
    2. 使用PyGObject(Gtk-3: python3-gi)重写sqm.py\n
    3. Gtk-3教程: https://python-gtk-3-tutorial.readthedocs.io/en/latest\n
    4. Gtk-3 API: https://lazka.github.io/pgi-docs/Gtk-3.0/\n\n
    5. 感谢sqm的作者 KINGX ( https://github.com/kxcode ), sqm UI 使用的是tkinter
    '''
    self.page4.pack_start(g.Label(_about_str), True, False, 0)


def main():
  win = UI_Window()
  win.connect('destroy', g.main_quit)
  # win.maximize()
  win.show_all()
  g.main()


if __name__ == '__main__':
  main()
