#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 08月 26日 星期日 16:54:41 CST
# sqlmap gui(gtk+3 by needle wang)
# required: python3.5+, python3-gi, sqlmap
# sqlmap requires python 2.6.x and 2.7.x

# python3.5+
from pathlib import Path
from subprocess import Popen, PIPE
from threading import Thread

from gtk3_header import Gdk as d
from gtk3_header import GLib
from gtk3_header import Gtk as g
from sqlmap_ui_handlers import Singal_Handlers as Handlers
from sqlmap_ui_tooltips import Widget_Mesg as Init_Mesg

# from basis_and_tool.logging_needle import get_console_logger
# logger = get_console_logger()


class UI_Window(g.Window):
  def __init__(self):
    super().__init__(title='sqlmap-ui')
    self.connect('key_press_event', self.on_window_key_press_event)

    self._handlers = Handlers(self)

    _main_box = g.Box.new(orientation = g.Orientation.VERTICAL, spacing = 0)

    self._build_page_target()

    _main_box.pack_start(self._target_notbook, False, True, 0)

    _notebook = g.Notebook()
    self._build_page1()
    self._build_page2()
    self._build_page3()
    self._build_page4()

    _notebook.append_page(self.page1, g.Label.new_with_mnemonic('选项区(_Q)'))
    _notebook.append_page(self.page2, g.Label.new_with_mnemonic('显示区(_W)'))
    _notebook.append_page(self.page3, g.Label.new_with_mnemonic('帮助(_H)'))
    _notebook.append_page(self.page4, g.Label.new_with_mnemonic('关于(_A)'))

    _main_box.pack_start(_notebook, True, True, 0)
    self.add(_main_box)

    # 添加tooltips, placeholders等
    Init_Mesg(self)

  def unselect_all_ckbtn(self, button):
    for _i in dir(self):
      if 'ckbtn' in _i:
        _tmp_ckbtn = getattr(self, _i)
        if isinstance(_tmp_ckbtn, g.CheckButton):
          _tmp_ckbtn.set_active(False)
    for _i in self._enum_area_opts_ckbtns:
      for _j in _i:
        _j.set_active(False)

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

  def _build_page_target(self):
    # 目标url
    name_store = g.ListStore(int, str)
    name_store.append([1, "http://www.site.com/vuln.php?id=1"])

    self._target_notbook = g.Notebook()

    _url_area = g.Box()

    self._url_combobox = g.ComboBox.new_with_model_and_entry(name_store)
    self._url_combobox.set_entry_text_column(1)

    _url_area.pack_start(self._url_combobox, True, True, 0)

    _burp_area = g.Box()

    self._burp_logfile = g.Entry()
    self._burp_logfile_chooser = g.FileChooserButton()

    self._burp_logfile_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._burp_logfile
    )

    _burp_area.pack_start(self._burp_logfile, True, True, 0)
    _burp_area.pack_start(self._burp_logfile_chooser, False, True, 0)

    _request_area = g.Box()

    self._request_file = g.Entry()
    self._request_file_chooser = g.FileChooserButton()

    self._request_file_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._request_file
    )

    _request_area.pack_start(self._request_file, True, True, 0)
    _request_area.pack_start(self._request_file_chooser, False, True, 0)

    _bulkfile_area = g.Box()

    self._bulkfile = g.Entry()
    self._bulkfile_chooser = g.FileChooserButton()

    self._bulkfile_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._bulkfile
    )

    _bulkfile_area.pack_start(self._bulkfile, True, True, 0)
    _bulkfile_area.pack_start(self._bulkfile_chooser, False, True, 0)

    _configfile_area = g.Box()

    self._configfile = g.Entry()
    self._configfile_chooser = g.FileChooserButton()

    self._configfile_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._configfile
    )

    _configfile_area.pack_start(self._configfile, True, True, 0)
    _configfile_area.pack_start(self._configfile_chooser, False, True, 0)

    _sitemap_url_area = g.Box()

    self._sitemap_url = g.Entry()

    _sitemap_url_area.pack_start(self._sitemap_url, True, True, 0)

    _google_dork_area = g.Box()

    self._google_dork = g.Entry()

    _google_dork_area.pack_start(self._google_dork, True, True, 0)

    self._target_notbook.append_page(_url_area, g.Label('目标url'))
    self._target_notbook.append_page(_burp_area, g.Label('burp日志'))
    self._target_notbook.append_page(_request_area, g.Label('HTTP请求'))
    self._target_notbook.append_page(_bulkfile_area, g.Label('BULKFILE'))
    self._target_notbook.append_page(_configfile_area, g.Label('ini文件'))
    self._target_notbook.append_page(_sitemap_url_area, g.Label('xml_url'))
    self._target_notbook.append_page(_google_dork_area, g.Label('GOOGLEDORK'))

  def _build_page1(self):
    self.page1 = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)
    self.page1.set_border_width(10)

    # sqlmap命令语句
    _cmd_area = g.Frame.new('sqlmap命令语句:')

    self._cmd_entry = g.Entry()

    _cmd_area.add(self._cmd_entry)

    self.page1.pack_start(_cmd_area, False, True, 0)

    # 主构造区
    _notebook = g.Notebook()

    # 选项区 - 设置, 请求, 枚举, 文件
    self._build_page1_setting()
    self._build_page1_request()
    self._build_page1_enumeration()
    self._build_page1_file()
    self._build_page1_other()

    _notebook.append_page(self.page1_setting, g.Label.new_with_mnemonic('测试(_1)'))
    _notebook.append_page(self.page1_request, g.Label.new_with_mnemonic('请求(_2)'))
    _notebook.append_page(self.page1_enumeration, g.Label.new_with_mnemonic('枚举(_3)'))
    _notebook.append_page(self.page1_file, g.Label.new_with_mnemonic('文件(_4)'))
    _notebook.append_page(self.page1_other, g.Label.new_with_mnemonic('其他(_5)'))

    self.page1.pack_start(_notebook, True, True, 0)

    # 构造与执行
    _exec_area = g.Box()

    _build_button = g.Button.new_with_mnemonic('构造命令语句(_E)')
    _build_button.connect('clicked', self._handlers.build_all)

    # 与sqlmap无关, 用于改善ui的使用体验!
    _unselect_all_btn = g.Button.new_with_mnemonic('反选所有复选框(_C)')
    _unselect_all_btn.connect('clicked', self.unselect_all_ckbtn)

    _run_button = g.Button.new_with_mnemonic('开始(_R)')
    _run_button.connect('clicked', self._handlers.run_cmdline)

    _exec_area.pack_start(_build_button, False, True, 0)
    _exec_area.pack_start(_unselect_all_btn, True, False, 0)
    _exec_area.pack_end(_run_button, False, True, 0)

    self.page1.pack_end(_exec_area, False, True, 0)

  def _build_page1_other(self):
    _page1_other = g.Box(orientation=g.Orientation.VERTICAL)

    self._build_page1_other_general()
    self._build_page1_other_misc()

    _row1 = g.Box()
    _row1.pack_start(self.page1_other_general_area, True, True, 5)

    _row2 = g.Box()
    _row2.pack_start(self.page1_other_misc_area, True, True, 5)

    _page1_other.add(_row1)
    _page1_other.add(_row2)

    self.page1_other = g.ScrolledWindow()
    self.page1_other.set_policy(g.PolicyType.NEVER, g.PolicyType.AUTOMATIC)
    self.page1_other.add(_page1_other)

  def _build_page1_other_misc(self):
    self.page1_other_misc_area = g.Frame.new('杂项')
    _page1_other_misc_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._page1_misc_web_root_ckbtn = g.CheckButton('远程web的root目录')
    self._page1_misc_web_root_entry = g.Entry()
    self._page1_misc_tmp_dir_ckbtn = g.CheckButton('本地临时目录')
    self._page1_misc_tmp_dir_entry = g.Entry()
    self._page1_misc_tmp_dir_chooser = g.FileChooserButton()

    # TODO, 应该选择目录, 而不是文件
    self._page1_misc_tmp_dir_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._page1_misc_tmp_dir_entry
    )

    _row1.pack_start(self._page1_misc_web_root_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_misc_web_root_entry, True, True, 5)
    _row1.pack_start(self._page1_misc_tmp_dir_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_misc_tmp_dir_entry, True, True, 0)
    _row1.pack_start(self._page1_misc_tmp_dir_chooser, False, True, 5)

    _row2 = g.Box()
    self._page1_misc_identify_waf_ckbtn = g.CheckButton('鉴别WAF')
    self._page1_misc_skip_waf_ckbtn = g.CheckButton('跳过对WAF/IPS保护的启发式侦测')
    self._page1_misc_smart_ckbtn = g.CheckButton('进行详细测试(当启动正面启发式时)')
    self._page1_misc_list_tampers_ckbtn = g.CheckButton('显示可用的tamper脚本列表')
    self._page1_misc_disable_color_ckbtn = g.CheckButton('禁用终端输出的颜色')

    _row2.pack_start(self._page1_misc_identify_waf_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_misc_skip_waf_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_misc_smart_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_misc_list_tampers_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_misc_disable_color_ckbtn, False, True, 5)

    _row3 = g.Box()
    self._page1_misc_offline_ckbtn = g.CheckButton('离线模式(只使用保存的会话数据)')
    self._page1_misc_mobile_ckbtn = g.CheckButton('模拟手机请求')
    self._page1_misc_beep_ckbtn = g.CheckButton('响铃')
    # TODO, 要加个alert嘛?
    self._page1_misc_purge_ckbtn = g.CheckButton('彻底清除所有记录')
    self._page1_misc_dependencies_ckbtn = g.CheckButton('检查丢失的(非核心的)sqlmap依赖')
    self._page1_general_update_ckbtn = g.CheckButton('更新sqlmap')

    _row3.pack_start(self._page1_misc_offline_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_misc_mobile_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_misc_beep_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_misc_purge_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_misc_dependencies_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_general_update_ckbtn, False, True, 5)

    _row4 = g.Box()
    self._page1_misc_answers_ckbtn = g.CheckButton('设置交互时的问题答案:')
    self._page1_misc_answers_entry = g.Entry()
    self._page1_misc_answers_entry.set_text('quit=N,follow=N')
    self._page1_misc_alert_ckbtn = g.CheckButton('当发现注入时运行OS命令:')
    self._page1_misc_alert_entry = g.Entry()
    self._page1_misc_gpage_ckbtn = g.CheckButton('GOOGLEDORK时的页码')
    self._page1_misc_gpage_spinbtn = g.SpinButton.new_with_range(1, 100, 1)

    _row4.pack_start(self._page1_misc_answers_ckbtn, False, True, 5)
    _row4.pack_start(self._page1_misc_answers_entry, True, True, 5)
    _row4.pack_start(self._page1_misc_alert_ckbtn, False, True, 5)
    _row4.pack_start(self._page1_misc_alert_entry, True, True, 5)
    _row4.pack_start(self._page1_misc_gpage_ckbtn, False, True, 5)
    _row4.pack_start(self._page1_misc_gpage_spinbtn, False, True, 5)

    _row5 = g.Box()
    self._page1_misc_z_ckbtn = g.CheckButton('使用短的助记符')
    self._page1_misc_z_entry = g.Entry()
    self._page1_misc_z_entry.set_text('flu,bat,ban,tec=EU...')

    _row5.pack_start(self._page1_misc_z_ckbtn, False, True, 5)
    _row5.pack_start(self._page1_misc_z_entry, True, True, 5)

    _page1_other_misc_opts.add(_row1)
    _page1_other_misc_opts.add(_row2)
    _page1_other_misc_opts.add(_row3)
    _page1_other_misc_opts.add(_row4)
    _page1_other_misc_opts.add(_row5)
    # _page1_other_misc_opts.add(g.Separator.new(g.Orientation.HORIZONTAL))
    self.page1_other_misc_area.add(_page1_other_misc_opts)

  def _build_page1_other_general(self):
    self.page1_other_general_area = g.Frame.new('通用项')
    _page1_other_general_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._page1_general_check_internet_ckbtn = g.CheckButton('检查与目标的网络连接')
    self._page1_general_fresh_queries_ckbtn = g.CheckButton('刷新此次查询')
    self._page1_general_flush_session_ckbtn = g.CheckButton('清空目标的会话文件')
    self._page1_general_eta_ckbtn = g.CheckButton('显示剩余时间')
    self._page1_general_binary_fields_ckbtn = g.CheckButton('生成有二进制值的字段')
    self._page1_general_binary_fields_entry = g.Entry()

    _row1.pack_start(self._page1_general_check_internet_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_general_fresh_queries_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_general_flush_session_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_general_eta_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_general_binary_fields_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_general_binary_fields_entry, False, True, 5)

    _row2 = g.Box()
    self._page1_general_forms_ckbtn = g.CheckButton('解析和测试目标url内的表单')
    self._page1_general_parse_errors_ckbtn = g.CheckButton('解析并显示DB错误信息')
    self._page1_misc_cleanup_ckbtn = g.CheckButton('清理DBMS中sqlmap产生的UDF和表')

    _row2.pack_start(self._page1_general_forms_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_general_parse_errors_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_misc_cleanup_ckbtn, False, True, 5)

    _row3 = g.Box()
    self._page1_general_crawl_ckbtn = g.CheckButton('爬网站(的层级/深度)')
    self._page1_general_crawl_entry = g.Entry()

    self._page1_general_crawl_exclude_ckbtn = g.CheckButton('爬站时排除(正则)页面')
    self._page1_general_crawl_exclude_entry = g.Entry()

    _row3.pack_start(self._page1_general_crawl_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_general_crawl_entry, True, True, 5)
    _row3.pack_start(self._page1_general_crawl_exclude_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_general_crawl_exclude_entry, True, True, 5)

    _row4 = g.Box()
    self._page1_general_charset_ckbtn = g.CheckButton('盲注所用的字符集合')
    self._page1_general_charset_entry = g.Entry()
    self._page1_general_charset_entry.set_text('0123456789abcdef')
    self._page1_general_encoding_ckbtn = g.CheckButton('字符编码(用于数据获取)')
    self._page1_general_encoding_entry = g.Entry()
    self._page1_general_encoding_entry.set_text('GBK')

    _row4.pack_start(self._page1_general_charset_ckbtn, False, True, 5)
    _row4.pack_start(self._page1_general_charset_entry, True, True, 5)
    _row4.pack_start(self._page1_general_encoding_ckbtn, False, True, 5)
    _row4.pack_start(self._page1_general_encoding_entry, False, True, 5)

    _row5 = g.Box()
    self._page1_general_session_file_ckbtn = g.CheckButton('指定会话文件')
    self._page1_general_session_file_entry = g.Entry()
    self._page1_general_session_file_chooser = g.FileChooserButton()

    self._page1_general_session_file_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._page1_general_session_file_entry
    )

    self._page1_general_output_dir_ckbtn = g.CheckButton('输出的保存目录')
    self._page1_general_output_dir_entry = g.Entry()
    self._page1_general_output_dir_chooser = g.FileChooserButton()

    self._page1_general_output_dir_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._page1_general_output_dir_entry
    )

    _row5.pack_start(self._page1_general_session_file_ckbtn, False, True, 5)
    _row5.pack_start(self._page1_general_session_file_entry, True, True, 0)
    _row5.pack_start(self._page1_general_session_file_chooser, False, True, 5)
    _row5.pack_start(self._page1_general_output_dir_ckbtn, False, True, 5)
    _row5.pack_start(self._page1_general_output_dir_entry, True, True, 0)
    _row5.pack_start(self._page1_general_output_dir_chooser, False, True, 5)

    _row6 = g.Box()
    self._page1_general_dump_format_ckbtn = g.CheckButton('dump结果的文件格式')
    self._page1_general_dump_format_entry = g.Entry()
    self._page1_general_dump_format_entry.set_max_width_chars(40)
    self._page1_general_csv_del_ckbtn = g.CheckButton('(csv文件的)分隔符')
    self._page1_general_csv_del_entry = g.Entry()
    self._page1_general_csv_del_entry.set_text(',')

    _row6.pack_start(self._page1_general_dump_format_ckbtn, False, True, 5)
    _row6.pack_start(self._page1_general_dump_format_entry, False, True, 5)
    _row6.pack_start(self._page1_general_csv_del_ckbtn, False, True, 5)
    _row6.pack_start(self._page1_general_csv_del_entry, False, True, 5)

    _row7 = g.Box()
    self._page1_general_traffic_file_ckbtn = g.CheckButton('转存所有http流量到文本')
    self._page1_general_traffic_file_entry = g.Entry()
    self._page1_general_traffic_file_chooser = g.FileChooserButton()

    self._page1_general_traffic_file_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._page1_general_traffic_file_entry
    )

    self._page1_general_har_ckbtn = g.CheckButton('转存至HAR文件')
    self._page1_general_har_entry = g.Entry()
    self._page1_general_har_chooser = g.FileChooserButton()

    self._page1_general_har_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._page1_general_har_entry
    )

    _row7.pack_start(self._page1_general_traffic_file_ckbtn, False, True, 5)
    _row7.pack_start(self._page1_general_traffic_file_entry, True, True, 0)
    _row7.pack_start(self._page1_general_traffic_file_chooser, False, True, 5)
    _row7.pack_start(self._page1_general_har_ckbtn, False, True, 5)
    _row7.pack_start(self._page1_general_har_entry, True, True, 0)
    _row7.pack_start(self._page1_general_har_chooser, False, True, 5)

    _row8 = g.Box()
    self._page1_general_save_ckbtn = g.CheckButton('保存选项至INI文件')
    self._page1_general_save_entry = g.Entry()
    self._page1_general_save_chooser = g.FileChooserButton()

    self._page1_general_save_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._page1_general_save_entry
    )

    self._page1_general_scope_ckbtn = g.CheckButton('从代理日志过滤出目标(正则)')
    self._page1_general_scope_entry = g.Entry()
    self._page1_general_scope_chooser = g.FileChooserButton()

    self._page1_general_scope_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._page1_general_scope_entry
    )

    _row8.pack_start(self._page1_general_save_ckbtn, False, True, 5)
    _row8.pack_start(self._page1_general_save_entry, True, True, 0)
    _row8.pack_start(self._page1_general_save_chooser, False, True, 5)
    _row8.pack_start(self._page1_general_scope_ckbtn, False, True, 5)
    _row8.pack_start(self._page1_general_scope_entry, True, True, 0)
    _row8.pack_start(self._page1_general_scope_chooser, False, True, 5)

    _row9 = g.Box()
    self._page1_general_test_filter_ckbtn = g.CheckButton('测试过滤器(从payload/title选择)')
    self._page1_general_test_filter_entry = g.Entry()
    self._page1_general_test_skip_ckbtn = g.CheckButton('测试跳过(从payload/title选择)')
    self._page1_general_test_skip_entry = g.Entry()

    _row9.pack_start(self._page1_general_test_filter_ckbtn, False, True, 5)
    _row9.pack_start(self._page1_general_test_filter_entry, True, True, 5)
    _row9.pack_start(self._page1_general_test_skip_ckbtn, False, True, 5)
    _row9.pack_start(self._page1_general_test_skip_entry, True, True, 5)

    # 添加行: _row1 - _row9
    for _i in range(1, 10):
      _page1_other_general_opts.add(locals()[''.join(('_row', str(_i)))])
    self.page1_other_general_area.add(_page1_other_general_opts)

  def _build_page1_setting(self):
    _page1_setting = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()
    self._build_page1_setting_inject()
    self._build_page1_setting_detection()
    self._build_page1_setting_tech()

    _row1.pack_start(self._inject_area, False, True, 5)
    _row1.pack_start(self._detection_area, True, True, 5)
    _row1.pack_start(self._tech_area, False, True, 5)

    _row2 = g.Box()
    self._build_page1_setting_tamper()
    self._build_page1_setting_optimize()
    self._build_page1_setting_general()

    _row2.pack_start(self._tamper_area, False, True, 5)
    _row2.pack_start(self._optimize_area, False, True, 5)
    _row2.pack_start(self._general_area, False, True, 5)

    _page1_setting.pack_start(_row1, True, True, 5)
    _page1_setting.pack_start(_row2, True, True, 5)

    self.page1_setting = g.ScrolledWindow()
    self.page1_setting.set_policy(g.PolicyType.NEVER, g.PolicyType.AUTOMATIC)
    self.page1_setting.add(_page1_setting)

  def _build_page1_setting_tech(self):
    self._tech_area = g.Frame.new('各注入技术的选项')

    _tech_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._tech_area_tech_ckbtn = g.CheckButton('注入技术')
    self._tech_area_tech_entry = g.Entry()

    _row1.pack_start(self._tech_area_tech_ckbtn, False, True, 5)
    _row1.pack_end(self._tech_area_tech_entry, False, True, 5)

    _row2 = g.Box()
    self._tech_area_time_sec_ckbtn = g.CheckButton('指定DB延迟多少秒响应')
    self._tech_area_time_sec_entry = g.Entry()

    _row2.pack_start(self._tech_area_time_sec_ckbtn, False, True, 5)
    _row2.pack_end(self._tech_area_time_sec_entry, False, True, 5)

    _row3 = g.Box()
    self._tech_area_union_col_ckbtn = g.CheckButton('指定最大union列数')
    self._tech_area_union_col_entry = g.Entry()

    _row3.pack_start(self._tech_area_union_col_ckbtn, False, True, 5)
    _row3.pack_end(self._tech_area_union_col_entry, False, True, 5)

    _row4 = g.Box()
    self._tech_area_union_chr_ckbtn = g.CheckButton('指定枚举列数时所用字符')
    self._tech_area_union_chr_entry = g.Entry()

    _row4.pack_start(self._tech_area_union_chr_ckbtn, False, True, 5)
    _row4.pack_end(self._tech_area_union_chr_entry, False, True, 5)

    _row5 = g.Box()
    self._tech_area_union_from_ckbtn = g.CheckButton('指定枚举列数时from的表名')
    self._tech_area_union_from_entry = g.Entry()

    _row5.pack_start(self._tech_area_union_from_ckbtn, False, True, 5)
    _row5.pack_end(self._tech_area_union_from_entry, False, True, 5)

    _row6 = g.Box()
    self._tech_area_dns_ckbtn = g.CheckButton('指定DNS')
    self._tech_area_dns_entry = g.Entry()

    _row6.pack_start(self._tech_area_dns_ckbtn, True, True, 5)
    _row6.pack_end(self._tech_area_dns_entry, True, True, 5)

    _row7 = g.Box()
    self._tech_area_second_url_ckbtn = g.CheckButton('指定二阶响应的url')
    self._tech_area_second_url_entry = g.Entry()

    _row7.pack_start(self._tech_area_second_url_ckbtn, True, True, 5)
    _row7.pack_end(self._tech_area_second_url_entry, True, True, 5)

    _row8 = g.Box()
    self._tech_area_second_req_ckbtn = g.CheckButton('指定含二阶HTTP请求的文件')
    self._tech_area_second_req_entry = g.Entry()

    _row8.pack_start(self._tech_area_second_req_ckbtn, True, True, 5)
    _row8.pack_end(self._tech_area_second_req_entry, True, True, 5)

    # 添加行: _row1 - _row8
    for _i in range(1, 9):
      _tech_area_opts.add(locals()[''.join(('_row', str(_i)))])
    self._tech_area.add(_tech_area_opts)

  def _build_page1_setting_detection(self):
    self._detection_area = g.Frame.new('探测选项')

    _detection_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._detection_area_level_ckbtn = g.CheckButton('探测等级(范围)')
    self._detection_area_level_scale = g.Scale.new_with_range(g.Orientation.HORIZONTAL, 1, 5, 1)

    self._detection_area_text_only_ckbtn = g.CheckButton('仅对比文本')

    _row1.pack_start(self._detection_area_level_ckbtn, False, True, 5)
    _row1.pack_start(self._detection_area_level_scale, True, True, 5)
    _row1.pack_end(self._detection_area_text_only_ckbtn, False, True, 5)

    _row2 = g.Box()
    self._detection_area_risk_ckbtn = g.CheckButton('payload危险等级')
    self._detection_area_risk_scale = g.Scale.new_with_range(g.Orientation.HORIZONTAL, 1, 3, 1)

    self._detection_area_titles_ckbtn = g.CheckButton('仅对比title')

    _row2.pack_start(self._detection_area_risk_ckbtn, False, True, 5)
    _row2.pack_start(self._detection_area_risk_scale, True, True, 10)
    _row2.pack_start(self._detection_area_titles_ckbtn, False, True, 5)

    _row3 = g.Box()
    self._detection_area_str_ckbtn = g.CheckButton('指定字符串')
    self._detection_area_str_entry = g.Entry()

    _row3.pack_start(self._detection_area_str_ckbtn, False, True, 5)
    _row3.pack_end(self._detection_area_str_entry, True, True, 5)

    _row4 = g.Box()
    self._detection_area_not_str_ckbtn = g.CheckButton('指定字符串')
    self._detection_area_not_str_entry = g.Entry()

    _row4.pack_start(self._detection_area_not_str_ckbtn, False, True, 5)
    _row4.pack_end(self._detection_area_not_str_entry, True, True, 5)

    _row5 = g.Box()
    self._detection_area_re_ckbtn = g.CheckButton('指定正则')
    self._detection_area_re_entry = g.Entry()

    _row5.pack_start(self._detection_area_re_ckbtn, False, True, 5)
    _row5.pack_end(self._detection_area_re_entry, True, True, 5)

    _row6 = g.Box()
    self._detection_area_code_ckbtn = g.CheckButton('指定http状态码')
    self._detection_area_code_entry = g.Entry()

    _row6.pack_start(self._detection_area_code_ckbtn, False, True, 5)
    _row6.pack_end(self._detection_area_code_entry, True, True, 5)

    # 添加行: _row1 - _row6
    for _i in range(1, 7):
      _detection_area_opts.add(locals()[''.join(('_row', str(_i)))])
    self._detection_area.add(_detection_area_opts)

  def _build_page1_setting_general(self):
    self._general_area = g.Frame.new('常用选项')
    _general_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._general_area_verbose_ckbtn = g.CheckButton('输出详细程度')
    self._general_area_verbose_scale = g.Scale.new_with_range(g.Orientation.HORIZONTAL, 0, 6, 1)
    self._general_area_verbose_scale.set_value(1.0)

    _row1.pack_start(self._general_area_verbose_ckbtn, False, True, 5)
    _row1.pack_start(self._general_area_verbose_scale, True, True, 5)

    _row2 = g.Box()
    self._general_area_finger_ckbtn = g.CheckButton('执行宽泛的DB版本检测')

    _row2.pack_start(self._general_area_finger_ckbtn, False, True, 5)

    _row3 = g.Box()
    self._general_area_hex_ckbtn = g.CheckButton('获取数据时使用hex转换')

    _row3.pack_start(self._general_area_hex_ckbtn, False, True, 5)

    _row4 = g.Box()
    self._general_area_batch_ckbtn = g.CheckButton('非交互模式, 一切皆默认')

    _row4.pack_start(self._general_area_batch_ckbtn, False, True, 5)

    _general_area_opts.add(_row1)
    _general_area_opts.add(_row2)
    _general_area_opts.add(_row3)
    _general_area_opts.add(_row4)
    self._general_area.add(_general_area_opts)

  def _build_page1_setting_optimize(self):
    self._optimize_area = g.Frame.new('性能优化')

    _optimize_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._optimize_area_turn_all_ckbtn = g.CheckButton('启用所有优化选项')
    self._optimize_area_turn_all_ckbtn.connect('clicked', self._handlers.optimize_area_controller)

    _row1.pack_start(self._optimize_area_turn_all_ckbtn, False, True, 5)

    _row2 = g.Box()
    self._optimize_area_thread_num_ckbtn = g.CheckButton('使用线程数:')
    self._optimize_area_thread_num_spinbtn = g.SpinButton.new_with_range(2, 1000, 2)

    _row2.pack_start(self._optimize_area_thread_num_ckbtn, False, True, 5)
    _row2.pack_start(self._optimize_area_thread_num_spinbtn, True, True, 5)

    _row3 = g.Box()
    self._optimize_area_predict_ckbtn = g.CheckButton('预测通常的查询结果')

    _row3.pack_start(self._optimize_area_predict_ckbtn, False, True, 5)

    _row4 = g.Box()
    self._optimize_area_keep_alive_ckbtn = g.CheckButton('http连接使用keep-alive')

    _row4.pack_start(self._optimize_area_keep_alive_ckbtn, False, True, 5)

    _row5 = g.Box()
    self._optimize_area_null_connect_ckbtn = g.CheckButton('只用页面长度报头来比较, 不去获取实际的响应体')

    _row5.pack_start(self._optimize_area_null_connect_ckbtn, False, True, 5)

    # 添加行: _row1 - _row5
    for _i in range(1, 6):
      _optimize_area_opts.add(locals()[''.join(('_row', str(_i)))])
    self._optimize_area.add(_optimize_area_opts)

  def _build_page1_setting_tamper(self):
    self._tamper_area = g.Frame.new('tamper脚本')

    _tamper_area_list = g.Box()

    _tamper_area_tamper_view = g.TextView()
    self._tamper_area_tamper_textbuffer = _tamper_area_tamper_view.get_buffer()

    _tamper_area_list.pack_start(_tamper_area_tamper_view, True, True, 0)

    _scrolled = g.ScrolledWindow()
    _scrolled.set_size_request(300, 0)
    _scrolled.set_policy(g.PolicyType.ALWAYS, g.PolicyType.ALWAYS)
    _scrolled.add(_tamper_area_list)

    self._tamper_area.add(_scrolled)

  def _build_page1_setting_inject(self):
    self._inject_area = g.Frame.new('注入选项')

    _row1 = g.Box()
    self._inject_area_param_ckbtn = g.CheckButton('可测试的参数')
    self._inject_area_param_entry = g.Entry()

    _row1.pack_start(self._inject_area_param_ckbtn, False, True, 5)
    _row1.pack_start(self._inject_area_param_entry, True, True, 5)

    _row2 = g.Box()
    self._inject_area_skip_static_ckbtn = g.CheckButton('跳过无动态特性的参数')
    self._inject_area_skip_static_ckbtn.set_active(True)

    _row2.pack_start(self._inject_area_skip_static_ckbtn, True, True, 5)

    _row3 = g.Box()
    self._inject_area_prefix_ckbtn = g.CheckButton('payload前缀')
    self._inject_area_prefix_entry = g.Entry()

    _row3.pack_start(self._inject_area_prefix_ckbtn, False, True, 5)
    _row3.pack_start(self._inject_area_prefix_entry, True, True, 5)

    _row4 = g.Box()
    self._inject_area_suffix_ckbtn = g.CheckButton('payload后缀')
    self._inject_area_suffix_entry = g.Entry()

    _row4.pack_start(self._inject_area_suffix_ckbtn, False, True, 5)
    _row4.pack_start(self._inject_area_suffix_entry, True, True, 5)

    _row5 = g.Box()
    self._inject_area_skip_ckbtn = g.CheckButton('排除参数')
    self._inject_area_skip_entry = g.Entry()

    _row5.pack_start(self._inject_area_skip_ckbtn, False, True, 5)
    _row5.pack_start(self._inject_area_skip_entry, True, True, 5)

    _row6 = g.Box()
    self._inject_area_param_exclude_ckbtn = g.CheckButton('排除参数(正则)')
    self._inject_area_param_exclude_entry = g.Entry()

    _row6.pack_start(self._inject_area_param_exclude_ckbtn, False, True, 5)
    _row6.pack_start(self._inject_area_param_exclude_entry, True, True, 5)

    _row7 = g.Box()
    _db_store = g.ListStore(int, str)
    _db_store.append([1, "mysql"])
    _db_store.append([2, "sqlite"])
    _db_store.append([3, "sqlserver"])

    self._inject_area_dbms_ckbtn = g.CheckButton('固定DB类型为')
    self._inject_area_dbms_combobox = g.ComboBox.new_with_model_and_entry(
      _db_store)
    self._inject_area_dbms_combobox.set_entry_text_column(1)

    _row7.pack_start(self._inject_area_dbms_ckbtn, False, True, 5)
    _row7.pack_start(self._inject_area_dbms_combobox, True, True, 5)

    _row8 = g.Box()
    self._inject_area_dbms_cred_ckbtn = g.CheckButton('DB认证')
    self._inject_area_dbms_cred_entry = g.Entry()

    _row8.pack_start(self._inject_area_dbms_cred_ckbtn, False, True, 5)
    _row8.pack_start(self._inject_area_dbms_cred_entry, True, True, 5)

    _row9 = g.Box()
    self._inject_area_os_ckbtn = g.CheckButton('固定OS为')
    self._inject_area_os_entry = g.Entry()

    _row9.pack_start(self._inject_area_os_ckbtn, False, True, 5)
    _row9.pack_start(self._inject_area_os_entry, True, True, 5)

    _row10 = g.Box()
    self._inject_area_no_cast_ckbtn = g.CheckButton('关掉payload变形机制')
    self._inject_area_no_escape_ckbtn = g.CheckButton('关掉string转义')

    _row10.pack_start(self._inject_area_no_cast_ckbtn, False, True, 5)
    _row10.pack_start(self._inject_area_no_escape_ckbtn, False, True, 5)

    _row11 = g.Box()
    _invalid_label = g.Label('对payload中的废值:')
    self._inject_area_invalid_logic_ckbtn = g.CheckButton('使用逻辑运算符')

    _row11.pack_start(_invalid_label, False, True, 5)
    _row11.pack_end(self._inject_area_invalid_logic_ckbtn, False, True, 5)

    _row12 = g.Box()
    self._inject_area_invalid_bignum_ckbtn = g.CheckButton('使用大数')
    self._inject_area_invalid_str_ckbtn = g.CheckButton('使用随机字符串')

    _row12.pack_end(self._inject_area_invalid_str_ckbtn, False, True, 5)
    _row12.pack_end(self._inject_area_invalid_bignum_ckbtn, False, True, 5)

    _inject_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)
    # 添加行: _row1 - _row12
    for _i in range(1, 13):
      _inject_area_opts.add(locals()[''.join(('_row', str(_i)))])
    self._inject_area.add(_inject_area_opts)

  def _build_page1_request(self):
    _page1_request = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()
    self._build_page1_request_header()

    _row1.pack_start(self._request_header_area, True, True, 5)

    _row2 = g.Box()
    self._build_page1_request_data()

    _row2.pack_start(self._request_data_area, True, True, 5)

    _row3 = g.Box()
    self._build_page1_request_custom()

    _row3.pack_start(self._request_custom_area, True, True, 5)

    _row4 = g.Box()
    self._build_page1_request_proxy()

    _row4.pack_start(self._request_proxy_area, True, True, 5)

    _page1_request.pack_start(_row1, False, True, 5)
    _page1_request.pack_start(_row2, False, True, 5)
    _page1_request.pack_start(_row3, False, True, 5)
    _page1_request.pack_start(_row4, False, True, 5)

    self.page1_request = g.ScrolledWindow()
    self.page1_request.set_policy(g.PolicyType.NEVER, g.PolicyType.AUTOMATIC)
    self.page1_request.add(_page1_request)

  def _build_page1_request_proxy(self):
    self._request_proxy_area = g.Frame.new('隐匿/代理')
    _request_proxy_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing = 5)

    _row1 = g.Box()
    self._request_area_safe_url_ckbtn = g.CheckButton('顺便掺杂地访问一个安全url')
    self._request_area_safe_url_entry = g.Entry()
    self._request_area_safe_post_ckbtn = g.CheckButton('提交到安全url的post数据')
    self._request_area_safe_post_entry = g.Entry()

    _row1.pack_start(self._request_area_safe_url_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_safe_url_entry, True, True, 5)
    _row1.pack_start(self._request_area_safe_post_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_safe_post_entry, True, True, 5)

    _row2 = g.Box()
    self._request_area_safe_req_ckbtn = g.CheckButton('从文件载入safe HTTP请求')
    self._request_area_safe_req_entry = g.Entry()
    self._request_area_safe_req_chooser = g.FileChooserButton()

    self._request_area_safe_req_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._request_area_safe_req_entry
    )

    self._request_area_safe_freq_ckbtn = g.CheckButton('访问安全url的频率')
    self._request_area_safe_freq_entry = g.Entry()

    _row2.pack_start(self._request_area_safe_req_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_safe_req_entry, True, True, 0)
    _row2.pack_start(self._request_area_safe_req_chooser, False, True, 0)
    _row2.pack_start(self._request_area_safe_freq_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_safe_freq_entry, False, True, 5)

    _row3 = g.Separator.new(g.Orientation.HORIZONTAL)

    _row4 = g.Box()
    self._request_area_ignore_proxy_ckbtn = g.CheckButton('忽略系统默认代理')
    self._request_area_proxy_ckbtn = g.CheckButton('使用代理')
    self._request_area_proxy_file_ckbtn = g.CheckButton('代理列表文件')
    self._request_area_proxy_file_entry = g.Entry()
    self._request_area_proxy_file_chooser = g.FileChooserButton()

    self._request_area_proxy_file_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._request_area_proxy_file_entry
    )

    _row4.pack_start(self._request_area_ignore_proxy_ckbtn, False, True, 5)
    _row4.pack_start(self._request_area_proxy_ckbtn, False, True, 5)
    _row4.pack_start(self._request_area_proxy_file_ckbtn, False, True, 5)
    _row4.pack_start(self._request_area_proxy_file_entry, True, True, 0)
    _row4.pack_start(self._request_area_proxy_file_chooser, False, True, 5)

    _row5 = g.Box()
    self._request_area_proxy_ip_label = g.Label('IP:')
    self._request_area_proxy_ip_entry = g.Entry()
    self._request_area_proxy_port_label = g.Label('PORT:')
    self._request_area_proxy_port_entry = g.Entry()

    self._request_area_proxy_username_label = g.Label('username:')
    self._request_area_proxy_username_entry = g.Entry()
    self._request_area_proxy_password_label = g.Label('password:')
    self._request_area_proxy_password_entry = g.Entry()

    _row5.pack_start(self._request_area_proxy_ip_label, False, True, 5)
    _row5.pack_start(self._request_area_proxy_ip_entry, True, True, 5)
    _row5.pack_start(self._request_area_proxy_port_label, False, True, 5)
    _row5.pack_start(self._request_area_proxy_port_entry, False, True, 5)
    _row5.pack_start(self._request_area_proxy_username_label, False, True, 5)
    _row5.pack_start(self._request_area_proxy_username_entry, True, True, 5)
    _row5.pack_start(self._request_area_proxy_password_label, False, True, 5)
    _row5.pack_start(self._request_area_proxy_password_entry, True, True, 5)

    _row6 = g.Box()
    self._request_area_tor_ckbtn = g.CheckButton('使用Tor匿名网络')
    self._request_area_tor_port_ckbtn = g.CheckButton('Tor端口')
    self._request_area_tor_port_entry = g.Entry()
    self._request_area_tor_type_ckbtn = g.CheckButton('Tor代理类型')
    self._request_area_tor_type_entry = g.Entry()
    self._request_area_check_tor_ckbtn = g.CheckButton('检查Tor连接')

    _row6.pack_start(self._request_area_tor_ckbtn, False, True, 5)
    _row6.pack_start(self._request_area_tor_port_ckbtn, False, True, 5)
    _row6.pack_start(self._request_area_tor_port_entry, False, True, 5)
    _row6.pack_start(self._request_area_tor_type_ckbtn, False, True, 5)
    _row6.pack_start(self._request_area_tor_type_entry, False, True, 5)
    _row6.pack_start(self._request_area_check_tor_ckbtn, False, True, 5)

    # 添加行: _row1 - _row6
    for _i in range(1, 7):
      _request_proxy_opts.add(locals()[''.join(('_row', str(_i)))])
    self._request_proxy_area.add(_request_proxy_opts)

  def _build_page1_request_custom(self):
    self._request_custom_area = g.Frame.new('request定制')
    _request_custom_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing = 5)

    _row1 = g.Box()
    self._request_area_ignore_redirects_ckbtn = g.CheckButton('忽略重定向')
    self._request_area_ignore_timeouts_ckbtn = g.CheckButton('忽略连接超时')
    self._request_area_ignore_code_ckbtn = g.CheckButton('忽略错误型状态码:')
    self._request_area_ignore_code_entry = g.Entry()
    self._request_area_ignore_code_entry.set_text('401')
    self._request_area_skip_urlencode_ckbtn = g.CheckButton('payload不使用url编码')
    self._request_area_force_ssl_ckbtn = g.CheckButton('强制使用HTTPS')
    self._request_area_hpp_ckbtn = g.CheckButton('使用HTTP参数污染')

    _row1.pack_start(self._request_area_ignore_redirects_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_ignore_timeouts_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_ignore_code_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_ignore_code_entry, True, True, 5)
    _row1.pack_start(self._request_area_skip_urlencode_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_force_ssl_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_hpp_ckbtn, False, True, 5)

    _row2 = g.Box()
    self._request_area_delay_ckbtn = g.CheckButton('请求间隔(秒)')
    self._request_area_delay_entry = g.Entry()
    self._request_area_timeout_ckbtn = g.CheckButton('几秒超时')
    self._request_area_timeout_entry = g.Entry()
    self._request_area_timeout_entry.set_text('30')
    self._request_area_retries_ckbtn = g.CheckButton('超时重试次数')
    self._request_area_retries_entry = g.Entry()
    self._request_area_retries_entry.set_text('3')
    self._request_area_randomize_ckbtn = g.CheckButton('指定要随机改变值的参数')
    self._request_area_randomize_entry = g.Entry()

    _row2.pack_start(self._request_area_delay_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_delay_entry, False, True, 5)
    _row2.pack_start(self._request_area_timeout_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_timeout_entry, False, True, 5)
    _row2.pack_start(self._request_area_retries_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_retries_entry, False, True, 5)
    _row2.pack_start(self._request_area_randomize_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_randomize_entry, True, True, 5)

    _row3 = g.Box()
    self._request_area_eval_ckbtn = g.CheckButton('--eval=')
    self._request_area_eval_entry = g.Entry()

    _row3.pack_start(self._request_area_eval_ckbtn, False, True, 5)
    _row3.pack_start(self._request_area_eval_entry, True, True, 5)

    _request_custom_opts.add(_row1)
    _request_custom_opts.add(_row2)
    _request_custom_opts.add(_row3)
    self._request_custom_area.add(_request_custom_opts)

  def _build_page1_request_data(self):
    self._request_data_area = g.Frame.new('HTTP data')
    _request_data_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing = 5)

    _row1 = g.Box()
    self._request_area_method_ckbtn = g.CheckButton('HTTP请求方式')
    self._request_area_method_entry = g.Entry()
    self._request_area_param_del_ckbtn = g.CheckButton('指定分隔data参数值的字符')
    self._request_area_param_del_entry = g.Entry()

    _row1.pack_start(self._request_area_method_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_method_entry, False, True, 5)
    _row1.pack_start(self._request_area_param_del_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_param_del_entry, False, True, 5)

    _row2 = g.Box()
    self._request_area_post_ckbtn = g.CheckButton('通过POST提交data:')
    self._request_area_post_entry = g.Entry()
    _row2.pack_start(self._request_area_post_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_post_entry, True, True, 5)

    _row3 = g.Separator.new(g.Orientation.HORIZONTAL)

    _row4 = g.Box()
    self._request_area_cookie_ckbtn = g.CheckButton('请求中要包含的Cookie:')
    self._request_area_cookie_entry = g.Entry()
    self._request_area_cookie_del_ckbtn = g.CheckButton('指定cookie分隔符')
    self._request_area_cookie_del_entry = g.Entry()

    _row4.pack_start(self._request_area_cookie_ckbtn, False, True, 5)
    _row4.pack_start(self._request_area_cookie_entry, True, True, 5)
    _row4.pack_start(self._request_area_cookie_del_ckbtn, False, True, 5)
    _row4.pack_start(self._request_area_cookie_del_entry, False, True, 5)

    _row5 = g.Box()
    self._request_area_load_cookies_ckbtn = g.CheckButton('本地Cookie文件')
    self._request_area_load_cookies_entry = g.Entry()
    self._request_area_load_cookies_chooser = g.FileChooserButton()
    self._request_area_load_cookies_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._request_area_load_cookies_entry
    )
    self._request_area_drop_set_cookie_ckbtn = g.CheckButton('丢弃Set-Cookie头')

    _row5.pack_start(self._request_area_load_cookies_ckbtn, False, True, 10)
    _row5.pack_start(self._request_area_load_cookies_entry, True, True, 0)
    _row5.pack_start(self._request_area_load_cookies_chooser, False, True, 0)
    _row5.pack_start(self._request_area_drop_set_cookie_ckbtn, False, True, 10)

    _row6 = g.Separator.new(g.Orientation.HORIZONTAL)

    _row7 = g.Box()
    self._request_area_auth_type_ckbtn = g.CheckButton('http认证类型')
    self._request_area_auth_type_entry = g.Entry()
    self._request_area_auth_type_entry.set_max_width_chars(25)
    self._request_area_auth_cred_ckbtn = g.CheckButton('http认证账密')
    self._request_area_auth_cred_entry = g.Entry()
    self._request_area_auth_file_ckbtn = g.CheckButton('http认证文件')
    self._request_area_auth_file_entry = g.Entry()
    self._request_area_auth_file_entry.set_max_width_chars(25)
    self._request_area_auth_file_chooser = g.FileChooserButton()

    self._request_area_auth_file_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._request_area_auth_file_entry
    )

    _row7.pack_start(self._request_area_auth_type_ckbtn, False, True, 5)
    _row7.pack_start(self._request_area_auth_type_entry, True, True, 5)
    _row7.pack_start(self._request_area_auth_cred_ckbtn, False, True, 5)
    _row7.pack_start(self._request_area_auth_cred_entry, True, True, 5)
    _row7.pack_start(self._request_area_auth_file_ckbtn, False, True, 5)
    _row7.pack_start(self._request_area_auth_file_entry, True, True, 0)
    _row7.pack_start(self._request_area_auth_file_chooser, False, True, 5)

    _row8 = g.Box()
    self._request_area_csrf_token_ckbtn = g.CheckButton('csrf_token')
    self._request_area_csrf_token_entry = g.Entry()
    self._request_area_csrf_url_ckbtn = g.CheckButton('获取csrf_token的url')
    self._request_area_csrf_url_entry = g.Entry()

    _row8.pack_start(self._request_area_csrf_token_ckbtn, False, True, 5)
    _row8.pack_start(self._request_area_csrf_token_entry, True, True, 5)
    _row8.pack_start(self._request_area_csrf_url_ckbtn, False, True, 5)
    _row8.pack_start(self._request_area_csrf_url_entry, True, True, 5)

    # 添加行: _row1 - _row8
    for _i in range(1, 9):
      _request_data_opts.add(locals()[''.join(('_row', str(_i)))])
    self._request_data_area.add(_request_data_opts)

  def _build_page1_request_header(self):
    self._request_header_area = g.Frame.new('HTTP header')
    _request_header_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing = 5)

    _row1 = g.Box()
    self._request_area_random_agent_ckbtn = g.CheckButton('随机User-Agent头')
    self._request_area_random_agent_ckbtn.set_active(True)
    self._request_area_user_agent_ckbtn = g.CheckButton('指定User-Agent头')
    self._request_area_user_agent_entry = g.Entry()

    _row1.pack_start(self._request_area_random_agent_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_user_agent_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_user_agent_entry, True, True, 5)

    _row2 = g.Box()
    self._request_area_host_ckbtn = g.CheckButton('Host头')
    self._request_area_host_entry = g.Entry()
    self._request_area_referer_ckbtn = g.CheckButton('referer头')
    self._request_area_referer_entry = g.Entry()

    _row2.pack_start(self._request_area_host_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_host_entry, True, True, 5)
    _row2.pack_start(self._request_area_referer_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_referer_entry, True, True, 5)

    _row3 = g.Box()
    self._request_area_header_ckbtn = g.CheckButton('额外的header(-H)')
    self._request_area_header_entry = g.Entry()
    self._request_area_headers_ckbtn = g.CheckButton('额外的headers')
    self._request_area_headers_entry = g.Entry()

    _row3.pack_start(self._request_area_header_ckbtn, False, True, 5)
    _row3.pack_start(self._request_area_header_entry, True, True, 5)
    _row3.pack_start(self._request_area_headers_ckbtn, False, True, 5)
    _row3.pack_start(self._request_area_headers_entry, True, True, 5)

    _request_header_opts.add(_row1)
    _request_header_opts.add(_row2)
    _request_header_opts.add(_row3)
    self._request_header_area.add(_request_header_opts)

  def _build_page1_enumeration(self):
    '''
    完全用Gtk.Box和Frame写吧
    '''
    self.page1_enumeration = g.Box(orientation=g.Orientation.VERTICAL)

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

    _row2 = g.Box()
    _row2.props.margin = 10

    self._build_page1_enumeration_meta()

    _row2.pack_start(self._meta_area, True, True, 10)

    _row3 = g.Box()
    _row3.props.margin = 10
    self._build_page1_enumeration_runsql()

    _row3.pack_start(self._runsql_area, True, True, 10)

    _row4 = g.Box()
    _row4.props.margin = 10
    self._build_page1_enumeration_brute_force()

    _row4.pack_start(self._brute_force_area, False, True, 10)

    self.page1_enumeration.add(_row1)
    self.page1_enumeration.add(_row2)
    self.page1_enumeration.add(_row3)
    self.page1_enumeration.add(_row4)

    # self.page1_enumeration = g.ScrolledWindow()
    # self.page1_enumeration.set_policy(g.PolicyType.NEVER, g.PolicyType.AUTOMATIC)
    # self.page1_enumeration.add(_page1_enumeration)

  def _build_page1_enumeration_brute_force(self):
    self._brute_force_area = g.Frame.new('暴破表名/列名')

    _brute_force_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()
    self._brute_force_area_common_tables_ckbtn = g.CheckButton('常用表名')
    self._brute_force_area_common_columns_ckbtn = g.CheckButton('常用列名')

    _row1.pack_start(self._brute_force_area_common_tables_ckbtn, True, True, 10)
    _row1.pack_start(self._brute_force_area_common_columns_ckbtn, True, True, 10)

    _brute_force_area_opts.pack_start(_row1, False, True, 5)
    self._brute_force_area.add(_brute_force_area_opts)

  def _build_page1_enumeration_runsql(self):
    self._runsql_area = g.Frame.new('执行SQL语句')

    _runsql_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()
    self._runsql_area_sql_query_ckbtn = g.CheckButton('SQL语句:')
    self._runsql_area_sql_query_entry = g.Entry()
    _row1.pack_start(self._runsql_area_sql_query_ckbtn, False, True, 10)
    _row1.pack_start(self._runsql_area_sql_query_entry, True, True, 10)

    _row2 = g.Box()
    self._runsql_area_sql_file_ckbtn = g.CheckButton('本地SQL文件:')
    self._runsql_area_sql_file_entry = g.Entry()
    self._runsql_area_sql_file_chooser = g.FileChooserButton()

    self._runsql_area_sql_file_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._runsql_area_sql_file_entry
    )

    _row2.pack_start(self._runsql_area_sql_file_ckbtn, False, True, 10)
    _row2.pack_start(self._runsql_area_sql_file_entry, True, True, 0)
    _row2.pack_start(self._runsql_area_sql_file_chooser, False, True, 10)

    _runsql_area_opts.pack_start(_row1, False, True, 5)
    _runsql_area_opts.pack_start(_row2, False, True, 5)
    self._runsql_area.add(_runsql_area_opts)

  def _build_page1_enumeration_meta(self):
    self._meta_area = g.Frame.new('数据库名, 表名, 列名...')

    _meta_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()

    _col1 = g.Box()

    self._meta_area_D_ckbtn = g.CheckButton('指定库名')
    self._meta_area_D_entry = g.Entry()

    _col1.pack_start(self._meta_area_D_ckbtn, False, True, 10)
    _col1.pack_start(self._meta_area_D_entry, True, True, 10)

    _col2 = g.Box()

    self._meta_area_T_ckbtn = g.CheckButton('指定表名')
    self._meta_area_T_entry = g.Entry()

    _col2.pack_start(self._meta_area_T_ckbtn, False, True, 10)
    _col2.pack_start(self._meta_area_T_entry, True, True, 10)

    _col3 = g.Box()

    self._meta_area_C_ckbtn = g.CheckButton('指定列名')
    self._meta_area_C_entry = g.Entry()

    _col3.pack_start(self._meta_area_C_ckbtn, False, True, 10)
    _col3.pack_start(self._meta_area_C_entry, True, True, 10)

    _col4 = g.Box()

    self._meta_area_U_ckbtn = g.CheckButton('指定用户')
    self._meta_area_U_entry = g.Entry()

    _col4.pack_start(self._meta_area_U_ckbtn, False, True, 10)
    _col4.pack_start(self._meta_area_U_entry, True, True, 10)

    _row1.pack_start(_col1, False, True, 5)
    _row1.pack_start(_col2, False, True, 5)
    _row1.pack_start(_col3, False, True, 5)
    _row1.pack_start(_col4, False, True, 5)

    _row2 = g.Box()

    _col1 = g.Box()

    self._meta_area_X_ckbtn = g.CheckButton('排除标志符')
    self._meta_area_X_entry = g.Entry()

    _col1.pack_start(self._meta_area_X_ckbtn, False, True, 10)
    _col1.pack_start(self._meta_area_X_entry, True, True, 10)

    _col2 = g.Box()

    self._meta_area_pivot_ckbtn = g.CheckButton('指定Pivot列名')
    self._meta_area_pivot_entry = g.Entry()

    _col2.pack_start(self._meta_area_pivot_ckbtn, False, True, 10)
    _col2.pack_start(self._meta_area_pivot_entry, True, True, 10)

    _row2.pack_start(_col1, False, True, 5)
    _row2.pack_start(_col2, False, True, 5)

    _row3 = g.Box()
    self._meta_area_where_ckbtn = g.CheckButton('where子句')
    self._meta_area_where_entry = g.Entry()

    _row3.pack_start(self._meta_area_where_ckbtn, False, True, 10)
    _row3.pack_start(self._meta_area_where_entry, True, True, 10)

    _meta_area_opts.pack_start(_row1, False, True, 5)
    _meta_area_opts.pack_start(_row2, False, True, 5)
    _meta_area_opts.pack_start(_row3, False, True, 5)

    self._meta_area.add(_meta_area_opts)

  def _build_page1_enumeration_limit(self):
    self._limit_area = g.Frame.new('limit(dump时的限制)')

    _limit_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()
    self._limit_area_start_ckbtn = g.CheckButton('始于第')
    self._limit_area_start_entry = g.Entry()

    _row1.pack_start(self._limit_area_start_ckbtn, False, True, 5)
    _row1.pack_start(self._limit_area_start_entry, False, True, 0)
    _row1.pack_start(g.Label('条'), False, True, 5)

    _row2 = g.Box()
    self._limit_area_stop_ckbtn = g.CheckButton('止于第')
    self._limit_area_stop_entry = g.Entry()

    _row2.pack_start(self._limit_area_stop_ckbtn, False, True, 5)
    _row2.pack_start(self._limit_area_stop_entry, False, True, 0)
    _row2.pack_start(g.Label('条'), False, True, 5)

    _limit_area_opts.pack_start(_row1, False, True, 10)
    _limit_area_opts.pack_start(_row2, False, True, 10)

    self._limit_area.add(_limit_area_opts)

  def _build_page1_enumeration_blind(self):
    self._blind_area = g.Frame.new('盲注选项')

    _blind_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()
    self._blind_area_first_ckbtn = g.CheckButton('首字符')
    self._blind_area_first_entry = g.Entry()

    _row1.pack_start(self._blind_area_first_ckbtn, False, True, 5)
    _row1.pack_start(self._blind_area_first_entry, False, True, 10)

    _blind_area_opts.pack_start(_row1, False, True, 10)

    _row2 = g.Box()
    self._blind_area_last_ckbtn = g.CheckButton('末字符')
    self._blind_area_last_entry = g.Entry()

    _row2.pack_start(self._blind_area_last_ckbtn, False, True, 5)
    _row2.pack_start(self._blind_area_last_entry, False, True, 10)

    _blind_area_opts.pack_start(_row2, False, True, 10)

    self._blind_area.add(_blind_area_opts)

  def _build_page1_enumeration_dump(self):
    self._dump_area = g.Frame.new('Dump(转储)')

    _dump_area_opts = g.Box(spacing=6)

    # 加这一层, 只是为了横向上有padding
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
      ('表', '字段', '架构', '计数', '备注'),
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

    self._build_page1_file_read()
    self._build_page1_file_write()
    self._build_page1_file_os_access()
    self._build_page1_file_os_registry()

    _row1 = g.Box(orientation=g.Orientation.HORIZONTAL)
    _row1.props.margin = 10
    _row1.pack_start(self._file_read_area, True, True, 10)

    _row2 = g.Box(orientation=g.Orientation.HORIZONTAL)
    _row2.props.margin = 10
    _row2.pack_start(self._file_write_area, True, True, 10)

    _row3 = g.Box(orientation=g.Orientation.HORIZONTAL)
    _row3.props.margin = 10
    _row3.pack_start(self._file_os_access_area, True, True, 10)

    _row4 = g.Box(orientation=g.Orientation.HORIZONTAL)
    _row4.props.margin = 10
    _row4.pack_start(self._file_os_registry_area, True, True, 10)

    self.page1_file.add(_row1)
    self.page1_file.add(_row2)
    self.page1_file.add(_row3)
    self.page1_file.add(_row4)
    # 如果全是ScrolledWindow, UI大小不会自动扩展
    # self.page1_file = g.ScrolledWindow()
    # self.page1_file.set_policy(g.PolicyType.NEVER, g.PolicyType.AUTOMATIC)
    # self.page1_file.add(_page1_file)

  def _build_page1_file_os_registry(self):
    self._file_os_registry_area = g.Frame.new('访问WIN下注册表')

    _file_os_registry_opts = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()
    self._file_os_registry_reg_ckbtn = g.CheckButton('键值操作:')
    self._file_os_registry_reg_combobox = g.ComboBoxText.new()
    self._file_os_registry_reg_combobox.append('--reg-read', '读取')
    self._file_os_registry_reg_combobox.append('--reg-add', '新增')
    self._file_os_registry_reg_combobox.append('--reg-del', '删除')
    self._file_os_registry_reg_combobox.set_active(0)

    _row1.pack_start(self._file_os_registry_reg_ckbtn, False, True, 5)
    _row1.pack_start(self._file_os_registry_reg_combobox, False, True, 5)

    _row2 = g.Box()
    self._file_os_registry_reg_key_label = g.Label('键')
    self._file_os_registry_reg_key_entry = g.Entry()
    self._file_os_registry_reg_value_label = g.Label('值')
    self._file_os_registry_reg_value_entry = g.Entry()

    _row2.pack_start(self._file_os_registry_reg_key_label, False, True, 5)
    _row2.pack_start(self._file_os_registry_reg_key_entry, True, True, 5)
    _row2.pack_start(self._file_os_registry_reg_value_label, False, True, 5)
    _row2.pack_start(self._file_os_registry_reg_value_entry, True, True, 5)

    _row3 = g.Box()
    self._file_os_registry_reg_data_label = g.Label('数据')
    self._file_os_registry_reg_data_entry = g.Entry()
    self._file_os_registry_reg_type_label = g.Label('类型')
    self._file_os_registry_reg_type_entry = g.Entry()

    _row3.pack_start(self._file_os_registry_reg_data_label, False, True, 5)
    _row3.pack_start(self._file_os_registry_reg_data_entry, True, True, 5)
    _row3.pack_start(self._file_os_registry_reg_type_label, False, True, 5)
    _row3.pack_start(self._file_os_registry_reg_type_entry, True, True, 5)

    _file_os_registry_opts.add(_row1)
    _file_os_registry_opts.add(_row2)
    _file_os_registry_opts.add(_row3)

    self._file_os_registry_area.add(_file_os_registry_opts)

  def _build_page1_file_os_access(self):
    self._file_os_access_area = g.Frame.new('访问后端OS')

    _file_os_access_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._file_os_access_os_cmd_ckbtn = g.CheckButton('执行CLI命令')
    self._file_os_access_os_cmd_entry = g.Entry()

    _row1.pack_start(self._file_os_access_os_cmd_ckbtn, False, True, 5)
    _row1.pack_start(self._file_os_access_os_cmd_entry, True, True, 5)

    _row2 = g.Box()
    self._file_os_access_os_shell_ckbtn = g.CheckButton('获取交互shell')
    self._file_os_access_os_pwn_ckbtn = g.CheckButton('--os-pwn')
    self._file_os_access_os_smbrelay_ckbtn = g.CheckButton('--os-smbrelay')
    self._file_os_access_os_bof_ckbtn = g.CheckButton('--os-bof')
    self._file_os_access_priv_esc_ckbtn = g.CheckButton('--priv-esc')

    _row2.pack_start(self._file_os_access_os_shell_ckbtn, False, True, 5)
    _row2.pack_start(self._file_os_access_os_pwn_ckbtn, False, True, 5)
    _row2.pack_start(self._file_os_access_os_smbrelay_ckbtn, False, True, 5)
    _row2.pack_start(self._file_os_access_os_bof_ckbtn, False, True, 5)
    _row2.pack_start(self._file_os_access_priv_esc_ckbtn, False, True, 5)

    _row3 = g.Box()
    self._file_os_access_msf_path_ckbtn = g.CheckButton('本地Metasploit安装路径')
    self._file_os_access_msf_path_entry = g.Entry()
    self._file_os_access_msf_path_chooser = g.FileChooserButton()

    # TODO, 应该选择目录, 而不是文件
    self._file_os_access_msf_path_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._file_os_access_msf_path_entry
    )

    self._file_os_access_tmp_path_ckbtn = g.CheckButton('远程临时目录(绝对路径)')
    self._file_os_access_tmp_path_entry = g.Entry()

    _row3.pack_start(self._file_os_access_msf_path_ckbtn, False, True, 5)
    _row3.pack_start(self._file_os_access_msf_path_entry, True, True, 0)
    _row3.pack_start(self._file_os_access_msf_path_chooser, False, True, 5)
    _row3.pack_start(self._file_os_access_tmp_path_ckbtn, False, True, 5)
    _row3.pack_start(self._file_os_access_tmp_path_entry, True, True, 5)

    _file_os_access_opts.add(_row1)
    _file_os_access_opts.add(_row2)
    _file_os_access_opts.add(_row3)
    self._file_os_access_area.add(_file_os_access_opts)

  def _build_page1_file_write(self):
    self._file_write_area = g.Frame.new('文件上传')

    _file_write_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._file_write_area_udf_ckbtn = g.CheckButton('注入(默认sqlmap自带的)用户定义函数')

    self._file_write_area_shared_lib_ckbtn = g.CheckButton('本地共享库路径(--shared-lib=)')
    self._file_write_area_shared_lib_entry = g.Entry()
    self._file_write_area_shared_lib_chooser = g.FileChooserButton()

    self._file_write_area_shared_lib_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._file_write_area_shared_lib_entry
    )

    _row1.pack_start(self._file_write_area_udf_ckbtn, False, True, 5)
    _row1.pack_start(self._file_write_area_shared_lib_ckbtn, False, True, 5)
    _row1.pack_start(self._file_write_area_shared_lib_entry, True, True, 0)
    _row1.pack_start(self._file_write_area_shared_lib_chooser, False, True, 5)

    _row2 = g.Box()
    self._file_write_area_file_write_ckbtn = g.CheckButton('本地文件路径(--file-write=)')
    self._file_write_area_file_write_entry = g.Entry()
    self._file_write_area_file_write_chooser = g.FileChooserButton()

    self._file_write_area_file_write_chooser.connect(
      'file-set',
      self._handlers.set_file_entry_text,
      self._file_write_area_file_write_entry
    )

    _row2.pack_start(self._file_write_area_file_write_ckbtn, False, True, 5)
    _row2.pack_start(self._file_write_area_file_write_entry, True, True, 0)
    _row2.pack_start(self._file_write_area_file_write_chooser, False, True, 5)

    _row3 = g.Box()
    self._file_write_area_file_dest_ckbtn = g.CheckButton('远程文件路径(--file-dest=)')
    self._file_write_area_file_dest_entry = g.Entry()

    _row3.pack_start(self._file_write_area_file_dest_ckbtn, False, True, 5)
    _row3.pack_start(self._file_write_area_file_dest_entry, True, True, 5)

    _file_write_area_opts.pack_start(_row1, False, True, 5)
    _file_write_area_opts.pack_start(_row2, False, True, 5)
    _file_write_area_opts.pack_start(_row3, False, True, 5)
    self._file_write_area.add(_file_write_area_opts)

  def _build_page1_file_read(self):
    self._file_read_area = g.Frame.new('读取远程文件')

    _file_read_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._file_read_area_file_read_ckbtn = g.CheckButton('远程文件路径(--file-read=)')
    self._file_read_area_file_read_entry = g.Entry()
    self._file_read_area_file_read_entry.set_text('/etc/passwd')
    self._file_read_area_file_btn = g.Button('查看')
    self._file_read_area_file_btn.connect('clicked', self._handlers.read_dumped_file)

    _row1.pack_start(self._file_read_area_file_read_ckbtn, False, True, 10)
    _row1.pack_start(self._file_read_area_file_read_entry, True, True, 10)
    _row1.pack_start(self._file_read_area_file_btn, False, True, 10)

    _file_read_area_opts.pack_start(_row1, False, True, 5)
    self._file_read_area.add(_file_read_area_opts)

  def _build_page2(self):
    self.page2 = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)
    self.page2.set_border_width(10)

    _row1 = g.Frame()
    _log_view = g.TextView()

    self._log_view_textbuffer = _log_view.get_buffer()
    self._log_view_textbuffer.set_text(''.join(
      ('sqlmap的运行记录都放在这: ', str(Path.home() / '.sqlmap/output\n'))
    ))

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.ALWAYS, g.PolicyType.ALWAYS)
    _scrolled.add(_log_view)

    _row1.add(_scrolled)

    _row2 = g.Box()
    self._page2_read_target_btn = g.Button('查看target文件')
    self._page2_read_target_btn.connect('clicked', self._handlers.read_target_file)

    _row2.pack_start(self._page2_read_target_btn, True, False, 0)

    self._page2_clear_btn = g.Button.new_with_mnemonic('清空(_C)')
    self._page2_clear_btn.connect('clicked', self._handlers.clear_buffer)

    _row2.pack_start(self._page2_clear_btn, True, False, 0)

    self._page2_read_log_btn = g.Button('查看log文件')
    self._page2_read_log_btn.connect('clicked', self._handlers.read_log_file)

    _row2.pack_start(self._page2_read_log_btn, True, False, 0)

    self.page2.pack_start(_row1, True, True, 5)
    self.page2.pack_end(_row2, False, True, 0)

  def _build_page3(self):
    self.page3 = g.Box(orientation=g.Orientation.VERTICAL)
    self.page3.set_border_width(10)

    _row1 = g.Frame()
    _manual_view = g.TextView()
    _manual_view.set_editable(False)

    self._manual_view_textbuffer = _manual_view.get_buffer()

    # 启动线程, 填充帮助标签, 加快启动速度
    t = Thread(target = self._set_manual_view)
    t.daemon = True
    t.start()

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.ALWAYS, g.PolicyType.ALWAYS)
    _scrolled.add(_manual_view)

    _row1.add(_scrolled)

    self.page3.pack_start(_row1, True, True, 10)

  def _set_manual_view(self):
    '''
    不用多线程能行嘛? 想要获得输出结果就一定会有阻塞的可能!
    https://www.jianshu.com/p/11090e197648
    https://wiki.gnome.org/Projects/PyGObject/Threading
    '''
    _end_iter = self._manual_view_textbuffer.get_end_iter()
    # _manual_hh = '/home/needle/bin/output_interval.sh'
    _manual_hh = ['/usr/bin/env', 'sqlmap', '-hh']
    try:
      _subprocess = Popen(_manual_hh, stdout=PIPE, bufsize=1)

      for _an_bytes_line_tmp in iter(_subprocess.stdout.readline, b''):
        GLib.idle_add(self._manual_view_textbuffer.insert, _end_iter, _an_bytes_line_tmp.decode('utf8'))
      _subprocess.stdout.close()
      _subprocess.wait()
    except FileNotFoundError as e:
      GLib.idle_add(self._manual_view_textbuffer.insert, _end_iter, str(e))

  def _build_page4(self):
    self.page4 = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)
    self.page4.set_border_width(10)

    _about_str = '''
    1. VERSION: 0.2
       2018年 10月 22日 星期一 16:24:05 CST
       required: python3.5+, python3-gi, sqlmap(require: python2.6+)
       作者: needle wang ( needlewang2011@gmail.com )\n
    2. 使用PyGObject(Gtk+3: python3-gi)重写sqm.py\n
    3. Gtk+3教程: https://python-gtk-3-tutorial.readthedocs.io/en/latest\n
    4. Gtk+3 API: https://lazka.github.io/pgi-docs/Gtk-3.0/\n\n
    5. 感谢sqm的作者 KINGX ( https://github.com/kxcode ), sqm UI 使用的是python2 + tkinter
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
