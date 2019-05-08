#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 08月 26日 星期日 16:54:41 CST
# sqlmap gui(gtk+3 by needle wang)
# required: python3.5+, python3-gi, sqlmap
# sqlmap requires: python 2.6.x and 2.7.x

# python3.5+
from pathlib import Path
from subprocess import Popen, PIPE
from threading import Thread

from gtk3_header import GLib, Vte, d, g
from model import Model
from handlers import Handler
from session import Session
from tooltips import Widget_Mesg as INIT_MESG

# from basis_and_tool.logging_needle import get_console_logger
# logger = get_console_logger()

# 从左往右
HORIZONTAL = g.Orientation.HORIZONTAL
# 从上至下
VERTICAL = g.Orientation.VERTICAL
# Model()与对象有关, 按照OOP原则, 理应是实例属性
# 但只有一个实例, 所以就这么写吧
m = Model()


class UI_Window(g.Window):
  # @profile
  def __init__(self):
    super().__init__(title='sqlmap-gtk')
    self.connect('key_press_event', self.on_window_key_press_event)

    self._handlers = Handler(self, m)

    # g.Box默认的orientation是HORIZONTAL
    _main_box = g.Box.new(orientation = VERTICAL, spacing = 0)

    self._build_page_target()

    _main_box.pack_start(self._target_notebook, False, True, 0)

    self.main_notebook = g.Notebook()
    self.main_notebook.add_events(d.EventMask.SCROLL_MASK | d.EventMask.SMOOTH_SCROLL_MASK)
    self.main_notebook.connect('scroll-event', self.scroll_page)
    self._build_page1()
    self._build_page2()
    self._build_page3()
    self._build_page4()
    self._build_page5()
    self._build_page6()

    self.main_notebook.append_page(self.page1, g.Label.new_with_mnemonic('选项区(_1)'))
    self.main_notebook.append_page(self.page2, g.Label.new_with_mnemonic('输出区(_2)'))
    self.main_notebook.append_page(self.page3, g.Label.new_with_mnemonic('日志区(_3)'))
    self.main_notebook.append_page(self.page4, g.Label.new_with_mnemonic('API区(_4)'))
    self.main_notebook.append_page(self.page5, g.Label.new_with_mnemonic('帮助(_H)'))
    self.main_notebook.append_page(self.page6, g.Label.new('关于'))

    _main_box.pack_start(self.main_notebook, True, True, 0)
    self.add(_main_box)
    # 初始化完后, 必须要有焦点, 不然按任何键都会报错, 直到操作一次UI:
    # gtk_widget_event: assertion 'WIDGET_REALIZED_FOR_EVENT (widget, event)' failed`
    m._inject_area_param_ckbtn.grab_focus()

    # 添加tooltips, placeholders等
    INIT_MESG(self, m)

    # 读取 上次所有选项
    self.session = Session(m)
    self.session.load_from_tmp()

  def on_window_destroy(self):
    # 保存 此次所有选项
    self.session.save_to_tmp()
    g.main_quit()

  def scroll_page(self, notebook, event):
    '''
    https://stackoverflow.com/questions/11773132/gtk-notebook-change-page-with-scrolling-and-alt1-like-firefox-chrome-epipha
    '''
    if event.get_scroll_deltas()[2] < 0:
      notebook.prev_page()
    else:
      notebook.next_page()
    # returns True, so it should stop the emission.
    # 返回True, 会停止向上(父容器)传递信号,
    # 不然page1的_notebook处理完信号后, 会传递给父容器的main_notebook
    return True

  def set_file_entry_text(self, button, data):
    '''
    data: [file_entry, 'title of chooser']
    '''
    if len(data) > 1:   # 选择目录
      dialog = g.FileChooserDialog(data[1], self,
                                   g.FileChooserAction.SELECT_FOLDER,
                                   ('_Cancel', g.ResponseType.CANCEL,
                                    '_Select', g.ResponseType.OK))
    else:
      # 点击左侧的 最近使用 可以选择目录, 小问题, 不用管.
      dialog = g.FileChooserDialog("选择文件", self,
                                   g.FileChooserAction.OPEN,
                                   ('_Cancel', g.ResponseType.CANCEL,
                                    '_OK', g.ResponseType.OK))
    try:
      if dialog.run() == g.ResponseType.OK:
        data[0].set_text(dialog.get_filename())
        data[0].grab_focus()
    finally:
      dialog.destroy()

  def _show_warn(self, button):
    if button.get_active():
      _warn_dialog = g.MessageDialog(parent = self,
                                     flags = g.DialogFlags.MODAL,
                                     type = g.MessageType.WARNING,
                                     buttons = g.ButtonsType.OK_CANCEL,
                                     message_format = '这将清除所有记录!\n确定勾选?')
      _response = _warn_dialog.run()
      if _response in (g.ResponseType.CANCEL, g.ResponseType.DELETE_EVENT):
        button.set_active(False)

      _warn_dialog.destroy()

  def clear_all_entry(self, button):
    for _i in dir(m):
      if _i.endswith('entry'):
        _tmp_entry = getattr(m, _i)
        if isinstance(_tmp_entry, g.Entry):
          _tmp_entry.set_text('')

  def unselect_all_ckbtn(self, button):
    for _i in dir(m):
      if _i.endswith('ckbtn'):
        _tmp_ckbtn = getattr(m, _i)
        if isinstance(_tmp_ckbtn, g.CheckButton):
          _tmp_ckbtn.set_active(False)
    for _i in m._enum_area_opts_ckbtns:
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
      self.on_window_destroy()
      return True

  def _build_page_target(self):
    self._target_notebook = g.Notebook()
    self._target_notebook.add_events(d.EventMask.SCROLL_MASK | d.EventMask.SMOOTH_SCROLL_MASK)
    self._target_notebook.connect('scroll-event', self.scroll_page)
    # 目标url
    name_store = g.ListStore(int, str)
    name_store.append([1, "http://www.site.com/vuln.php?id=1"])

    _url_area = g.Box()
    m._url_combobox.set_model(name_store)
    m._url_combobox.set_entry_text_column(1)

    _url_area.pack_start(m._url_combobox, True, True, 0)

    _burp_area = g.Box()
    m._burp_logfile_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._burp_logfile]
    )

    _burp_area.pack_start(m._burp_logfile, True, True, 0)
    _burp_area.pack_start(m._burp_logfile_chooser, False, True, 0)

    _request_area = g.Box()

    m._request_file_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._request_file]
    )

    _request_area.pack_start(m._request_file, True, True, 0)
    _request_area.pack_start(m._request_file_chooser, False, True, 0)

    _bulkfile_area = g.Box()
    m._bulkfile_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._bulkfile]
    )

    _bulkfile_area.pack_start(m._bulkfile, True, True, 0)
    _bulkfile_area.pack_start(m._bulkfile_chooser, False, True, 0)

    _configfile_area = g.Box()
    m._configfile_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._configfile]
    )

    _configfile_area.pack_start(m._configfile, True, True, 0)
    _configfile_area.pack_start(m._configfile_chooser, False, True, 0)

    _sitemap_url_area = g.Box()
    _sitemap_url_area.pack_start(m._sitemap_url, True, True, 0)

    _google_dork_area = g.Box()
    _google_dork_area.pack_start(m._google_dork, True, True, 0)

    self._target_notebook.append_page(_url_area, g.Label.new('目标url'))
    self._target_notebook.append_page(_burp_area, g.Label.new('burp日志'))
    self._target_notebook.append_page(_request_area, g.Label.new('HTTP请求'))
    self._target_notebook.append_page(_bulkfile_area, g.Label.new('BULKFILE'))
    self._target_notebook.append_page(_configfile_area, g.Label.new('ini文件'))
    self._target_notebook.append_page(_sitemap_url_area, g.Label.new('xml_url'))
    self._target_notebook.append_page(_google_dork_area, g.Label.new('GOOGLEDORK'))

  def _build_page1(self):
    self.page1 = g.Box(orientation=VERTICAL, spacing=6)
    self.page1.set_border_width(10)

    # sqlmap命令语句
    _cmd_area = g.Frame.new('A.收集选项 的结果显示在这:')

    _cmd_area.add(m._cmd_entry)

    self.page1.pack_start(_cmd_area, False, True, 0)

    # 主构造区
    _notebook = g.Notebook()
    _notebook.add_events(d.EventMask.SCROLL_MASK | d.EventMask.SMOOTH_SCROLL_MASK)
    _notebook.connect('scroll-event', self.scroll_page)

    # 选项区 - 设置, 请求, 枚举, 文件, 其他
    self._build_page1_setting()
    self._build_page1_request()
    self._build_page1_enumeration()
    self._build_page1_file()
    self._build_page1_other()

    _notebook.append_page(self.page1_setting, g.Label.new_with_mnemonic('测试(_Q)'))
    _notebook.append_page(self.page1_request, g.Label.new_with_mnemonic('请求(_W)'))
    _notebook.append_page(self.page1_enumeration, g.Label.new_with_mnemonic('枚举(_E)'))
    _notebook.append_page(self.page1_file, g.Label.new_with_mnemonic('文件(_R)'))
    _notebook.append_page(self.page1_other, g.Label.new_with_mnemonic('其他(_T)'))

    self.page1.pack_start(_notebook, True, True, 0)

    # 构造与执行
    _exec_area = g.Box()

    _build_button = g.Button.new_with_mnemonic('A.收集选项(_A)')
    _build_button.connect('clicked', self._handlers.build_all)
    # 用于改善ui的使用体验
    _unselect_all_btn = g.Button.new_with_mnemonic('反选所有复选框(_S)')
    _unselect_all_btn.connect('clicked', self.unselect_all_ckbtn)
    _clear_all_entry = g.Button.new_with_mnemonic('清空所有输入框(_D)')
    _clear_all_entry.connect('clicked', self.clear_all_entry)

    _run_button = g.Button.new_with_mnemonic('B.开始(_F)')
    _run_button.connect('clicked', self._handlers.run_cmdline)

    _exec_area.pack_start(_build_button, False, True, 0)
    _exec_area.pack_start(_unselect_all_btn, True, False, 0)
    _exec_area.pack_start(_clear_all_entry, True, False, 0)
    _exec_area.pack_end(_run_button, False, True, 0)

    self.page1.pack_end(_exec_area, False, True, 0)

  def _build_page1_other(self):
    '''
    最大的宽应该是由最长的 request定制的第一行 决定

    如果所有标签页全用ScrolledWindow的话, UI的尺寸(size)会变得很小
    以"其他"标签的height作为标准高,
    高于此height的标签页使用ScrolledWindow, 显示滚动条
    '''
    self.page1_other = g.Box(orientation=VERTICAL)

    self._build_page1_other_general()
    self._build_page1_other_misc()

    _row1 = g.Box()
    _row1.pack_start(self.page1_other_general_area, True, True, 5)

    _row2 = g.Box()
    _row2.pack_start(self.page1_other_misc_area, True, True, 5)

    self.page1_other.add(_row1)
    self.page1_other.add(_row2)

  def _build_page1_other_misc(self):
    self.page1_other_misc_area = g.Frame.new('杂项')
    _page1_other_misc_opts = g.Box(orientation=VERTICAL, spacing=6)

    _row1 = g.Box()
    m._page1_misc_tmp_dir_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._page1_misc_tmp_dir_entry, '选择 本地临时目录']
    )

    _row1.pack_start(m._page1_misc_web_root_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_misc_web_root_entry, True, True, 5)
    _row1.pack_start(m._page1_misc_tmp_dir_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_misc_tmp_dir_entry, True, True, 0)
    _row1.pack_start(m._page1_misc_tmp_dir_chooser, False, True, 5)

    _row2 = g.Box()
    _row2.pack_start(m._page1_misc_identify_waf_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_skip_waf_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_smart_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_list_tampers_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_sqlmap_shell_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_disable_color_ckbtn, False, True, 5)

    _row3 = g.Box()
    m._page1_misc_purge_ckbtn.connect('toggled', self._show_warn)

    _row3.pack_start(m._page1_misc_offline_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_misc_mobile_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_misc_beep_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_misc_purge_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_misc_dependencies_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_general_update_ckbtn, False, True, 5)

    _row4 = g.Box()
    m._page1_misc_answers_entry.set_text('quit=N,follow=N')

    _row4.pack_start(m._page1_misc_answers_ckbtn, False, True, 5)
    _row4.pack_start(m._page1_misc_answers_entry, True, True, 5)
    _row4.pack_start(m._page1_misc_alert_ckbtn, False, True, 5)
    _row4.pack_start(m._page1_misc_alert_entry, True, True, 5)
    _row4.pack_start(m._page1_misc_gpage_ckbtn, False, True, 5)
    _row4.pack_start(m._page1_misc_gpage_spinbtn, False, True, 5)

    _row5 = g.Box()
    m._page1_misc_z_entry.set_text('flu,bat,ban,tec=EU...')

    _row5.pack_start(m._page1_misc_z_ckbtn, False, True, 5)
    _row5.pack_start(m._page1_misc_z_entry, True, True, 5)

    _page1_other_misc_opts.add(_row1)
    _page1_other_misc_opts.add(_row2)
    _page1_other_misc_opts.add(_row3)
    _page1_other_misc_opts.add(_row4)
    _page1_other_misc_opts.add(_row5)
    # _page1_other_misc_opts.add(g.Separator.new(HORIZONTAL))
    self.page1_other_misc_area.add(_page1_other_misc_opts)

  def _build_page1_other_general(self):
    self.page1_other_general_area = g.Frame.new('通用项')
    _page1_other_general_opts = g.Box(orientation=VERTICAL, spacing=6)

    _row1 = g.Box()
    _row1.pack_start(m._page1_general_check_internet_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_general_fresh_queries_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_general_flush_session_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_general_eta_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_general_binary_fields_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_general_binary_fields_entry, False, True, 5)

    _row2 = g.Box()
    m._page1_general_preprocess_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._page1_general_preprocess_entry]
    )

    _row2.pack_start(m._page1_general_forms_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_general_parse_errors_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_cleanup_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_general_preprocess_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_general_preprocess_entry, True, True, 5)
    _row2.pack_start(m._page1_general_preprocess_chooser, False, True, 5)

    _row3 = g.Box()
    _row3.pack_start(m._page1_general_crawl_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_general_crawl_entry, True, True, 5)
    _row3.pack_start(m._page1_general_crawl_exclude_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_general_crawl_exclude_entry, True, True, 5)

    _row4 = g.Box()
    m._page1_general_charset_entry.set_text('0123456789abcdef')
    m._page1_general_encoding_entry.set_text('GBK')

    _row4.pack_start(m._page1_general_charset_ckbtn, False, True, 5)
    _row4.pack_start(m._page1_general_charset_entry, True, True, 5)
    _row4.pack_start(m._page1_general_encoding_ckbtn, False, True, 5)
    _row4.pack_start(m._page1_general_encoding_entry, False, True, 5)

    _row5 = g.Box()
    m._page1_general_session_file_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._page1_general_session_file_entry]
    )

    m._page1_general_output_dir_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._page1_general_output_dir_entry, '选择 结果保存在哪']
    )

    _row5.pack_start(m._page1_general_session_file_ckbtn, False, True, 5)
    _row5.pack_start(m._page1_general_session_file_entry, True, True, 0)
    _row5.pack_start(m._page1_general_session_file_chooser, False, True, 5)
    _row5.pack_start(m._page1_general_output_dir_ckbtn, False, True, 5)
    _row5.pack_start(m._page1_general_output_dir_entry, True, True, 0)
    _row5.pack_start(m._page1_general_output_dir_chooser, False, True, 5)

    _row6 = g.Box()
    m._page1_general_dump_format_entry.set_max_width_chars(40)
    m._page1_general_csv_del_entry.set_max_length(1)
    m._page1_general_csv_del_entry.set_text(',')

    _row6.pack_start(m._page1_general_dump_format_ckbtn, False, True, 5)
    _row6.pack_start(m._page1_general_dump_format_entry, False, True, 5)
    _row6.pack_start(m._page1_general_csv_del_ckbtn, False, True, 5)
    _row6.pack_start(m._page1_general_csv_del_entry, False, True, 5)

    _row7 = g.Box()
    m._page1_general_traffic_file_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._page1_general_traffic_file_entry]
    )

    m._page1_general_har_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._page1_general_har_entry]
    )

    _row7.pack_start(m._page1_general_traffic_file_ckbtn, False, True, 5)
    _row7.pack_start(m._page1_general_traffic_file_entry, True, True, 0)
    _row7.pack_start(m._page1_general_traffic_file_chooser, False, True, 5)
    _row7.pack_start(m._page1_general_har_ckbtn, False, True, 5)
    _row7.pack_start(m._page1_general_har_entry, True, True, 0)
    _row7.pack_start(m._page1_general_har_chooser, False, True, 5)

    _row8 = g.Box()
    m._page1_general_save_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._page1_general_save_entry]
    )

    m._page1_general_scope_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._page1_general_scope_entry]
    )

    _row8.pack_start(m._page1_general_save_ckbtn, False, True, 5)
    _row8.pack_start(m._page1_general_save_entry, True, True, 0)
    _row8.pack_start(m._page1_general_save_chooser, False, True, 5)
    _row8.pack_start(m._page1_general_scope_ckbtn, False, True, 5)
    _row8.pack_start(m._page1_general_scope_entry, True, True, 0)
    _row8.pack_start(m._page1_general_scope_chooser, False, True, 5)

    _row9 = g.Box()
    _row9.pack_start(m._page1_general_test_filter_ckbtn, False, True, 5)
    _row9.pack_start(m._page1_general_test_filter_entry, True, True, 5)
    _row9.pack_start(m._page1_general_test_skip_ckbtn, False, True, 5)
    _row9.pack_start(m._page1_general_test_skip_entry, True, True, 5)

    # 添加行: _row1 - _row9
    for _i in range(1, 10):
      _page1_other_general_opts.add(locals()[''.join(('_row', str(_i)))])
    self.page1_other_general_area.add(_page1_other_general_opts)

  def _build_page1_setting(self):
    _page1_setting = g.Box(orientation=VERTICAL)

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

    _page1_setting.pack_start(_row1, False, True, 5)
    _page1_setting.pack_start(_row2, False, True, 5)

    self.page1_setting = g.ScrolledWindow()
    self.page1_setting.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    self.page1_setting.add(_page1_setting)

  def _build_page1_setting_tech(self):
    self._tech_area = g.Frame.new('各注入技术的选项')

    _tech_area_opts = g.Box(orientation=VERTICAL, spacing=6)

    _row1 = g.Box()
    _row1.pack_start(m._tech_area_tech_ckbtn, False, True, 5)
    _row1.pack_end(m._tech_area_tech_entry, False, True, 5)

    _row2 = g.Box()
    _row2.pack_start(m._tech_area_time_sec_ckbtn, False, True, 5)
    _row2.pack_end(m._tech_area_time_sec_entry, False, True, 5)

    _row3 = g.Box()
    _row3.pack_start(m._tech_area_union_col_ckbtn, False, True, 5)
    _row3.pack_end(m._tech_area_union_col_entry, False, True, 5)

    _row4 = g.Box()
    _row4.pack_start(m._tech_area_union_chr_ckbtn, False, True, 5)
    _row4.pack_end(m._tech_area_union_chr_entry, False, True, 5)

    _row5 = g.Box()
    _row5.pack_start(m._tech_area_union_from_ckbtn, False, True, 5)
    _row5.pack_end(m._tech_area_union_from_entry, False, True, 5)

    _row6 = g.Box()
    _row6.pack_start(m._tech_area_dns_ckbtn, True, True, 5)
    _row6.pack_end(m._tech_area_dns_entry, True, True, 5)

    _row7 = g.Box()
    _row7.pack_start(m._tech_area_second_url_ckbtn, True, True, 5)
    _row7.pack_end(m._tech_area_second_url_entry, True, True, 5)

    _row8 = g.Box()
    _row8.pack_start(m._tech_area_second_req_ckbtn, True, True, 5)

    _row9 = g.Box()
    m._tech_area_second_req_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._tech_area_second_req_entry]
    )

    _row9.pack_end(m._tech_area_second_req_chooser, False, True, 5)
    _row9.pack_end(m._tech_area_second_req_entry, True, True, 5)

    # 添加行: _row1 - _row9
    for _i in range(1, 10):
      _tech_area_opts.add(locals()[''.join(('_row', str(_i)))])
    self._tech_area.add(_tech_area_opts)

  def _build_page1_setting_detection(self):
    self._detection_area = g.Frame.new('探测选项')

    _detection_area_opts = g.Box(orientation=VERTICAL, spacing=6)

    _row1 = g.Box()
    _row1.pack_start(m._detection_area_level_ckbtn, False, True, 5)
    _row1.pack_start(m._detection_area_level_scale, True, True, 5)

    _row2 = g.Box()
    _row2.pack_start(m._detection_area_risk_ckbtn, False, True, 5)
    _row2.pack_start(m._detection_area_risk_scale, True, True, 10)

    _row3 = g.Box()
    _row3.pack_start(m._detection_area_str_ckbtn, False, True, 5)
    _row3.pack_end(m._detection_area_str_entry, True, True, 5)

    _row4 = g.Box()
    _row4.pack_start(m._detection_area_not_str_ckbtn, False, True, 5)
    _row4.pack_end(m._detection_area_not_str_entry, True, True, 5)

    _row5 = g.Box()
    _row5.pack_start(m._detection_area_re_ckbtn, False, True, 5)
    _row5.pack_end(m._detection_area_re_entry, True, True, 5)

    _row6 = g.Box()
    _row6.pack_start(m._detection_area_code_ckbtn, False, True, 5)
    _row6.pack_start(m._detection_area_code_entry, False, True, 5)

    _row7 = g.Box()
    _row7.pack_start(m._detection_area_text_only_ckbtn, True, True, 5)
    _row7.pack_start(m._detection_area_titles_ckbtn, True, True, 5)

    # 添加行: _row1 - _row7
    for _i in range(1, 8):
      _detection_area_opts.add(locals()[''.join(('_row', str(_i)))])
    self._detection_area.add(_detection_area_opts)

  def _build_page1_setting_general(self):
    self._general_area = g.Frame.new('常用选项')
    _general_area_opts = g.Box(orientation=VERTICAL, spacing=6)

    _row1 = g.Box()
    m._general_area_verbose_scale.set_value(1.0)

    _row1.pack_start(m._general_area_verbose_ckbtn, False, True, 5)
    _row1.pack_start(m._general_area_verbose_scale, True, True, 5)

    _row2 = g.Box()
    _row2.pack_start(m._general_area_finger_ckbtn, False, True, 5)

    _row3 = g.Box()
    _row3.pack_start(m._general_area_hex_ckbtn, False, True, 5)

    _row4 = g.Box()
    _row4.pack_start(m._general_area_batch_ckbtn, False, True, 5)

    _row5 = g.Box()
    _row5.pack_start(m._page1_misc_wizard_ckbtn, False, True, 5)

    _general_area_opts.add(_row1)
    _general_area_opts.add(_row2)
    _general_area_opts.add(_row3)
    _general_area_opts.add(_row4)
    _general_area_opts.add(_row5)
    self._general_area.add(_general_area_opts)

  def _build_page1_setting_optimize(self):
    self._optimize_area = g.Frame.new('性能优化')

    _optimize_area_opts = g.Box(orientation=VERTICAL, spacing=6)

    _row1 = g.Box()
    m._optimize_area_turn_all_ckbtn.connect('clicked', self._handlers.optimize_area_controller)

    _row1.pack_start(m._optimize_area_turn_all_ckbtn, False, True, 5)

    _row2 = g.Box()
    _row2.pack_start(m._optimize_area_thread_num_ckbtn, False, True, 5)
    _row2.pack_start(m._optimize_area_thread_num_spinbtn, True, True, 5)

    _row3 = g.Box()
    _row3.pack_start(m._optimize_area_predict_ckbtn, False, True, 5)

    _row4 = g.Box()
    _row4.pack_start(m._optimize_area_keep_alive_ckbtn, False, True, 5)

    _row5 = g.Box()
    _row5.pack_start(m._optimize_area_null_connect_ckbtn, False, True, 5)

    # 添加行: _row1 - _row5
    for _i in range(1, 6):
      _optimize_area_opts.add(locals()[''.join(('_row', str(_i)))])
    self._optimize_area.add(_optimize_area_opts)

  def _build_page1_setting_tamper(self):
    '''
    frame套box, box再套scroll会出现:
    一直按回车出现滚动条后, 光标会下移 直到移出可见区, 原内容不会上移
    即内容的显示没有 下滑 滚轮的效果.
    '''
    self._tamper_area = g.Frame.new('tamper脚本')

    self._tamper_area_tamper_view = g.TextView()
    self._tamper_area_tamper_view.set_wrap_mode(g.WrapMode.CHAR)

    _scrolled = g.ScrolledWindow()
    _scrolled.set_size_request(300, -1)
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(self._tamper_area_tamper_view)

    self._tamper_area.add(_scrolled)

  def _build_page1_setting_inject(self):
    self._inject_area = g.Frame.new('注入选项')

    _row1 = g.Box()
    _row1.pack_start(m._inject_area_param_ckbtn, False, True, 5)
    _row1.pack_start(m._inject_area_param_entry, True, True, 5)

    _row2 = g.Box()
    # set_active(True)为选中状态
    m._inject_area_skip_static_ckbtn.set_active(True)

    _row2.pack_start(m._inject_area_skip_static_ckbtn, True, True, 5)

    _row3 = g.Box()
    _row3.pack_start(m._inject_area_prefix_ckbtn, False, True, 5)
    _row3.pack_start(m._inject_area_prefix_entry, True, True, 5)

    _row4 = g.Box()
    _row4.pack_start(m._inject_area_suffix_ckbtn, False, True, 5)
    _row4.pack_start(m._inject_area_suffix_entry, True, True, 5)

    _row5 = g.Box()
    _row5.pack_start(m._inject_area_skip_ckbtn, False, True, 5)
    _row5.pack_start(m._inject_area_skip_entry, True, True, 5)

    _row6 = g.Box()
    _row6.pack_start(m._inject_area_param_exclude_ckbtn, False, True, 5)
    _row6.pack_start(m._inject_area_param_exclude_entry, True, True, 5)

    _row7 = g.Box()
    _db_store = g.ListStore(str)
    _db_store.append(["mysql"])
    _db_store.append(["sqlite"])
    _db_store.append(["sqlserver"])

    m._inject_area_dbms_combobox.set_model(_db_store)
    m._inject_area_dbms_combobox.set_entry_text_column(0)

    _row7.pack_start(m._inject_area_dbms_ckbtn, False, True, 5)
    _row7.pack_start(m._inject_area_dbms_combobox, True, True, 5)

    _row8 = g.Box()
    _row8.pack_start(m._inject_area_dbms_cred_ckbtn, False, True, 5)
    _row8.pack_start(m._inject_area_dbms_cred_entry, True, True, 5)

    _row9 = g.Box()
    _row9.pack_start(m._inject_area_os_ckbtn, False, True, 5)
    _row9.pack_start(m._inject_area_os_entry, True, True, 5)

    _row10 = g.Box()
    _row10.pack_start(m._inject_area_no_cast_ckbtn, False, True, 5)
    _row10.pack_start(m._inject_area_no_escape_ckbtn, False, True, 5)

    _row11 = g.Box()
    _invalid_label = g.Label.new('对payload中的废值:')

    _row11.pack_start(_invalid_label, False, True, 5)
    _row11.pack_end(m._inject_area_invalid_logic_ckbtn, False, True, 5)

    _row12 = g.Box()
    _row12.pack_end(m._inject_area_invalid_str_ckbtn, False, True, 5)
    _row12.pack_end(m._inject_area_invalid_bignum_ckbtn, False, True, 5)

    _inject_area_opts = g.Box(orientation=VERTICAL, spacing=6)
    # 添加行: _row1 - _row12
    for _i in range(1, 13):
      _inject_area_opts.add(locals()[''.join(('_row', str(_i)))])
    self._inject_area.add(_inject_area_opts)

  def _build_page1_request(self):
    _page1_request = g.Box(orientation=VERTICAL)

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
    self.page1_request.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    self.page1_request.add(_page1_request)

  def _build_page1_request_proxy(self):
    self._request_proxy_area = g.Frame.new('隐匿/代理')
    _request_proxy_opts = g.Box(orientation=VERTICAL, spacing = 5)

    _row1 = g.Box()
    _row1.pack_start(m._request_area_safe_url_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_safe_url_entry, True, True, 5)
    _row1.pack_start(m._request_area_safe_post_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_safe_post_entry, True, True, 5)

    _row2 = g.Box()
    m._request_area_safe_req_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._request_area_safe_req_entry]
    )

    _row2.pack_start(m._request_area_safe_req_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_safe_req_entry, True, True, 0)
    _row2.pack_start(m._request_area_safe_req_chooser, False, True, 0)
    _row2.pack_start(m._request_area_safe_freq_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_safe_freq_entry, False, True, 5)

    _row3 = g.Separator.new(HORIZONTAL)

    _row4 = g.Box()
    m._request_area_proxy_file_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._request_area_proxy_file_entry]
    )

    _row4.pack_start(m._request_area_ignore_proxy_ckbtn, False, True, 5)
    _row4.pack_start(m._request_area_proxy_ckbtn, False, True, 5)
    _row4.pack_start(m._request_area_proxy_file_ckbtn, False, True, 5)
    _row4.pack_start(m._request_area_proxy_file_entry, True, True, 0)
    _row4.pack_start(m._request_area_proxy_file_chooser, False, True, 5)

    _row5 = g.Box()
    _row5.pack_start(m._request_area_proxy_ip_label, False, True, 5)
    _row5.pack_start(m._request_area_proxy_ip_entry, True, True, 5)
    _row5.pack_start(m._request_area_proxy_port_label, False, True, 5)
    _row5.pack_start(m._request_area_proxy_port_entry, False, True, 5)
    _row5.pack_start(m._request_area_proxy_username_label, False, True, 5)
    _row5.pack_start(m._request_area_proxy_username_entry, True, True, 5)
    _row5.pack_start(m._request_area_proxy_password_label, False, True, 5)
    _row5.pack_start(m._request_area_proxy_password_entry, True, True, 5)

    _row6 = g.Box()
    _row6.pack_start(m._request_area_tor_ckbtn, False, True, 5)
    _row6.pack_start(m._request_area_tor_port_ckbtn, False, True, 5)
    _row6.pack_start(m._request_area_tor_port_entry, False, True, 5)
    _row6.pack_start(m._request_area_tor_type_ckbtn, False, True, 5)
    _row6.pack_start(m._request_area_tor_type_entry, False, True, 5)
    _row6.pack_start(m._request_area_check_tor_ckbtn, False, True, 5)

    # 添加行: _row1 - _row6
    for _i in range(1, 7):
      _request_proxy_opts.add(locals()[''.join(('_row', str(_i)))])
    self._request_proxy_area.add(_request_proxy_opts)

  def _build_page1_request_custom(self):
    self._request_custom_area = g.Frame.new('request定制')
    _request_custom_opts = g.Box(orientation=VERTICAL, spacing = 5)

    _row1 = g.Box()
    m._request_area_ignore_code_entry.set_text('401')

    _row1.pack_start(m._request_area_ignore_redirects_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_ignore_timeouts_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_ignore_code_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_ignore_code_entry, True, True, 5)
    _row1.pack_start(m._request_area_skip_urlencode_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_force_ssl_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_chunked_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_hpp_ckbtn, False, True, 5)

    _row2 = g.Box()
    m._request_area_timeout_entry.set_text('30')
    m._request_area_retries_entry.set_text('3')

    _row2.pack_start(m._request_area_delay_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_delay_entry, False, True, 5)
    _row2.pack_start(m._request_area_timeout_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_timeout_entry, False, True, 5)
    _row2.pack_start(m._request_area_retries_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_retries_entry, False, True, 5)
    _row2.pack_start(m._request_area_randomize_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_randomize_entry, True, True, 5)

    _row3 = g.Box()
    _row3.pack_start(m._request_area_eval_ckbtn, False, True, 5)
    _row3.pack_start(m._request_area_eval_entry, True, True, 5)

    _request_custom_opts.add(_row1)
    _request_custom_opts.add(_row2)
    _request_custom_opts.add(_row3)
    self._request_custom_area.add(_request_custom_opts)

  def _build_page1_request_data(self):
    self._request_data_area = g.Frame.new('HTTP data')
    _request_data_opts = g.Box(orientation=VERTICAL, spacing = 5)

    _row1 = g.Box()
    m._request_area_param_del_entry.set_max_length(1)

    _row1.pack_start(m._request_area_method_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_method_entry, False, True, 5)
    _row1.pack_start(m._request_area_param_del_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_param_del_entry, False, True, 5)

    _row2 = g.Box()
    _row2.pack_start(m._request_area_post_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_post_entry, True, True, 5)

    _row3 = g.Separator.new(HORIZONTAL)

    _row4 = g.Box()
    _row4.pack_start(m._request_area_cookie_ckbtn, False, True, 5)
    _row4.pack_start(m._request_area_cookie_entry, True, True, 5)
    _row4.pack_start(m._request_area_cookie_del_ckbtn, False, True, 5)
    _row4.pack_start(m._request_area_cookie_del_entry, False, True, 5)

    _row5 = g.Box()
    m._request_area_load_cookies_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._request_area_load_cookies_entry]
    )

    _row5.pack_start(m._request_area_load_cookies_ckbtn, False, True, 10)
    _row5.pack_start(m._request_area_load_cookies_entry, True, True, 0)
    _row5.pack_start(m._request_area_load_cookies_chooser, False, True, 0)
    _row5.pack_start(m._request_area_drop_set_cookie_ckbtn, False, True, 10)

    _row6 = g.Separator.new(HORIZONTAL)

    _row7 = g.Box()
    m._request_area_auth_type_entry.set_max_width_chars(25)
    m._request_area_auth_file_entry.set_max_width_chars(25)

    m._request_area_auth_file_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._request_area_auth_file_entry]
    )

    _row7.pack_start(m._request_area_auth_type_ckbtn, False, True, 5)
    _row7.pack_start(m._request_area_auth_type_entry, True, True, 5)
    _row7.pack_start(m._request_area_auth_cred_ckbtn, False, True, 5)
    _row7.pack_start(m._request_area_auth_cred_entry, True, True, 5)
    _row7.pack_start(m._request_area_auth_file_ckbtn, False, True, 5)
    _row7.pack_start(m._request_area_auth_file_entry, True, True, 0)
    _row7.pack_start(m._request_area_auth_file_chooser, False, True, 5)

    _row8 = g.Box()
    _row8.pack_start(m._request_area_csrf_token_ckbtn, False, True, 5)
    _row8.pack_start(m._request_area_csrf_token_entry, True, True, 5)
    _row8.pack_start(m._request_area_csrf_url_ckbtn, False, True, 5)
    _row8.pack_start(m._request_area_csrf_url_entry, True, True, 5)

    # 添加行: _row1 - _row8
    for _i in range(1, 9):
      _request_data_opts.add(locals()[''.join(('_row', str(_i)))])
    self._request_data_area.add(_request_data_opts)

  def _build_page1_request_header(self):
    self._request_header_area = g.Frame.new('HTTP header')
    _request_header_opts = g.Box(orientation=VERTICAL, spacing = 5)

    _row1 = g.Box()
    m._request_area_random_agent_ckbtn.set_active(True)

    _row1.pack_start(m._request_area_random_agent_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_user_agent_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_user_agent_entry, True, True, 5)

    _row2 = g.Box()
    _row2.pack_start(m._request_area_host_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_host_entry, True, True, 5)
    _row2.pack_start(m._request_area_referer_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_referer_entry, True, True, 5)

    _row3 = g.Box()
    _row3.pack_start(m._request_area_header_ckbtn, False, True, 5)
    _row3.pack_start(m._request_area_header_entry, True, True, 5)
    _row3.pack_start(m._request_area_headers_ckbtn, False, True, 5)
    _row3.pack_start(m._request_area_headers_entry, True, True, 5)

    _request_header_opts.add(_row1)
    _request_header_opts.add(_row2)
    _request_header_opts.add(_row3)
    self._request_header_area.add(_request_header_opts)

  def _build_page1_enumeration(self):
    '''
    完全用Gtk.Box和Frame写吧
    '''
    self.page1_enumeration = g.Box(orientation=VERTICAL)

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

  def _build_page1_enumeration_brute_force(self):
    self._brute_force_area = g.Frame.new('暴破表名/列名')

    _brute_force_area_opts = g.Box(orientation=VERTICAL)

    _row1 = g.Box()

    _row1.pack_start(g.Label.new('检查是否存在:'), False, True, 10)
    _row1.pack_start(m._brute_force_area_common_tables_ckbtn, False, True, 0)
    _row1.pack_start(m._brute_force_area_common_columns_ckbtn, False, True, 10)

    _brute_force_area_opts.pack_start(_row1, False, True, 5)
    self._brute_force_area.add(_brute_force_area_opts)

  def _build_page1_enumeration_runsql(self):
    self._runsql_area = g.Frame.new('执行SQL语句')

    _runsql_area_opts = g.Box(orientation=VERTICAL)

    _row1 = g.Box()
    _row1.pack_start(m._runsql_area_sql_query_ckbtn, False, True, 10)
    _row1.pack_start(m._runsql_area_sql_query_entry, True, True, 10)

    _row2 = g.Box()
    m._runsql_area_sql_file_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._runsql_area_sql_file_entry]
    )

    _row2.pack_start(m._runsql_area_sql_shell_ckbtn, False, True, 10)
    _row2.pack_start(m._runsql_area_sql_file_ckbtn, False, True, 10)
    _row2.pack_start(m._runsql_area_sql_file_entry, True, True, 0)
    _row2.pack_start(m._runsql_area_sql_file_chooser, False, True, 10)

    _runsql_area_opts.pack_start(_row1, False, True, 5)
    _runsql_area_opts.pack_start(_row2, False, True, 5)
    self._runsql_area.add(_runsql_area_opts)

  def _build_page1_enumeration_meta(self):
    self._meta_area = g.Frame.new('数据库名, 表名, 列名...')

    _meta_area_opts = g.Box(orientation=VERTICAL)

    _row1 = g.Box()

    _col1 = g.Box()     # It's row actually.
    _col1.pack_start(m._meta_area_D_ckbtn, False, True, 10)
    _col1.pack_start(m._meta_area_D_entry, True, True, 10)

    _col2 = g.Box()
    _col2.pack_start(m._meta_area_T_ckbtn, False, True, 10)
    _col2.pack_start(m._meta_area_T_entry, True, True, 10)

    _col3 = g.Box()
    _col3.pack_start(m._meta_area_C_ckbtn, False, True, 10)
    _col3.pack_start(m._meta_area_C_entry, True, True, 10)

    _col4 = g.Box()
    _col4.pack_start(m._meta_area_U_ckbtn, False, True, 10)
    _col4.pack_start(m._meta_area_U_entry, True, True, 10)

    _row1.pack_start(_col1, False, True, 5)
    _row1.pack_start(_col2, False, True, 5)
    _row1.pack_start(_col3, False, True, 5)
    _row1.pack_start(_col4, False, True, 5)

    _row2 = g.Box()

    _col1 = g.Box()
    _col1.pack_start(m._meta_area_X_ckbtn, False, True, 10)
    _col1.pack_start(m._meta_area_X_entry, True, True, 10)

    _col2 = g.Box()
    _col2.pack_start(m._meta_area_pivot_ckbtn, False, True, 10)
    _col2.pack_start(m._meta_area_pivot_entry, True, True, 10)

    _row2.pack_start(_col1, False, True, 5)
    _row2.pack_start(_col2, False, True, 5)

    _row3 = g.Box()
    _row3.pack_start(m._meta_area_where_ckbtn, False, True, 10)
    _row3.pack_start(m._meta_area_where_entry, True, True, 10)

    _meta_area_opts.pack_start(_row1, False, True, 5)
    _meta_area_opts.pack_start(_row2, False, True, 5)
    _meta_area_opts.pack_start(_row3, False, True, 5)

    self._meta_area.add(_meta_area_opts)

  def _build_page1_enumeration_blind(self):
    self._blind_area = g.Frame.new('盲注选项')

    _blind_area_opts = g.Box(orientation=VERTICAL)

    _row1 = g.Box()
    _row1.pack_start(m._blind_area_first_ckbtn, False, True, 5)
    _row1.pack_start(m._blind_area_first_entry, False, True, 10)

    _blind_area_opts.pack_start(_row1, False, True, 10)

    _row2 = g.Box()
    _row2.pack_start(m._blind_area_last_ckbtn, False, True, 5)
    _row2.pack_start(m._blind_area_last_entry, False, True, 10)

    _blind_area_opts.pack_start(_row2, False, True, 10)

    self._blind_area.add(_blind_area_opts)

  def _build_page1_enumeration_limit(self):
    self._limit_area = g.Frame.new('limit(dump时的限制)')

    _limit_area_opts = g.Box(orientation=VERTICAL)

    _row1 = g.Box()
    _row1.pack_start(m._limit_area_start_ckbtn, False, True, 5)
    _row1.pack_start(m._limit_area_start_entry, False, True, 0)
    _row1.pack_start(g.Label.new('条'), False, True, 5)

    _row2 = g.Box()
    _row2.pack_start(m._limit_area_stop_ckbtn, False, True, 5)
    _row2.pack_start(m._limit_area_stop_entry, False, True, 0)
    _row2.pack_start(g.Label.new('条'), False, True, 5)

    _limit_area_opts.pack_start(_row1, False, True, 10)
    _limit_area_opts.pack_start(_row2, False, True, 10)

    self._limit_area.add(_limit_area_opts)

  def _build_page1_enumeration_dump(self):
    self._dump_area = g.Frame.new('Dump(转储)')

    _dump_area_opts = g.Box(spacing=6)

    # 加这一层, 只是为了横向上有padding
    _dump_area_opts_cols = g.Box(orientation=VERTICAL)

    _dump_area_opts_cols.add(m._dump_area_dump_ckbtn)
    _dump_area_opts_cols.add(m._dump_area_dump_all_ckbtn)
    _dump_area_opts_cols.add(m._dump_area_search_ckbtn)
    _dump_area_opts_cols.add(m._dump_area_no_sys_db_ckbtn)
    _dump_area_opts_cols.add(m._dump_area_repair_ckbtn)

    _dump_area_opts.pack_start(_dump_area_opts_cols, False, True, 10)

    self._dump_area.add(_dump_area_opts)

  def _build_page1_enumeration_enum(self):
    self._enum_area = g.Frame.new('枚举')

    _enum_area_opts = g.Box(spacing=6)

    # Do not use: [g.Box()] * 3, 会有闭包现象
    _enu_area_opts_cols = [g.Box(orientation=VERTICAL),
                           g.Box(orientation=VERTICAL),
                           g.Box(orientation=VERTICAL)]

    for _x in range(len(m._enum_area_opts_ckbtns)):
      for _y in m._enum_area_opts_ckbtns[_x]:
        # 每列, 至上往下add
        _enu_area_opts_cols[_x].add(_y)
      # 添加三列, 方便对齐...
      _enum_area_opts.pack_start(_enu_area_opts_cols[_x], False, True, 10)

    self._enum_area.add(_enum_area_opts)

  def _build_page1_file(self):
    self.page1_file = g.Box(orientation=VERTICAL, spacing=6)

    self._build_page1_file_read()
    self._build_page1_file_write()
    self._build_page1_file_os_access()
    self._build_page1_file_os_registry()

    _row1 = g.Box()
    _row1.props.margin = 10
    _row1.pack_start(self._file_read_area, True, True, 10)

    _row2 = g.Box()
    _row2.props.margin = 10
    _row2.pack_start(self._file_write_area, True, True, 10)

    _row3 = g.Box()
    _row3.props.margin = 10
    _row3.pack_start(self._file_os_access_area, True, True, 10)

    _row4 = g.Box()
    _row4.props.margin = 10
    _row4.pack_start(self._file_os_registry_area, True, True, 10)

    self.page1_file.add(_row1)
    self.page1_file.add(_row2)
    self.page1_file.add(_row3)
    self.page1_file.add(_row4)

  def _build_page1_file_os_registry(self):
    self._file_os_registry_area = g.Frame.new('访问WIN下注册表')

    _file_os_registry_opts = g.Box(orientation=VERTICAL)

    _row1 = g.Box()
    m._file_os_registry_reg_combobox.append('--reg-read', '读取')
    m._file_os_registry_reg_combobox.append('--reg-add', '新增')
    m._file_os_registry_reg_combobox.append('--reg-del', '删除')
    m._file_os_registry_reg_combobox.set_active(0)

    _row1.pack_start(m._file_os_registry_reg_ckbtn, False, True, 5)
    _row1.pack_start(m._file_os_registry_reg_combobox, False, True, 5)

    _row2 = g.Box()
    _row2.pack_start(m._file_os_registry_reg_key_label, False, True, 5)
    _row2.pack_start(m._file_os_registry_reg_key_entry, True, True, 5)
    _row2.pack_start(m._file_os_registry_reg_value_label, False, True, 5)
    _row2.pack_start(m._file_os_registry_reg_value_entry, True, True, 5)

    _row3 = g.Box()
    _row3.pack_start(m._file_os_registry_reg_data_label, False, True, 5)
    _row3.pack_start(m._file_os_registry_reg_data_entry, True, True, 5)
    _row3.pack_start(m._file_os_registry_reg_type_label, False, True, 5)
    _row3.pack_start(m._file_os_registry_reg_type_entry, True, True, 5)

    _file_os_registry_opts.add(_row1)
    _file_os_registry_opts.add(_row2)
    _file_os_registry_opts.add(_row3)

    self._file_os_registry_area.add(_file_os_registry_opts)

  def _build_page1_file_os_access(self):
    self._file_os_access_area = g.Frame.new('访问后端OS')

    _file_os_access_opts = g.Box(orientation=VERTICAL, spacing=6)

    _row1 = g.Box()
    _row1.pack_start(m._file_os_access_os_cmd_ckbtn, False, True, 5)
    _row1.pack_start(m._file_os_access_os_cmd_entry, True, True, 5)

    _row2 = g.Box()
    _row2.pack_start(m._file_os_access_os_shell_ckbtn, False, True, 5)
    _row2.pack_start(m._file_os_access_os_pwn_ckbtn, False, True, 5)
    _row2.pack_start(m._file_os_access_os_smbrelay_ckbtn, False, True, 5)
    _row2.pack_start(m._file_os_access_os_bof_ckbtn, False, True, 5)
    _row2.pack_start(m._file_os_access_priv_esc_ckbtn, False, True, 5)

    _row3 = g.Box()
    m._file_os_access_msf_path_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._file_os_access_msf_path_entry, '选择 本地Metasploit安装目录']
    )

    _row3.pack_start(m._file_os_access_msf_path_ckbtn, False, True, 5)
    _row3.pack_start(m._file_os_access_msf_path_entry, True, True, 0)
    _row3.pack_start(m._file_os_access_msf_path_chooser, False, True, 5)
    _row3.pack_start(m._file_os_access_tmp_path_ckbtn, False, True, 5)
    _row3.pack_start(m._file_os_access_tmp_path_entry, True, True, 5)

    _file_os_access_opts.add(_row1)
    _file_os_access_opts.add(_row2)
    _file_os_access_opts.add(_row3)
    self._file_os_access_area.add(_file_os_access_opts)

  def _build_page1_file_write(self):
    self._file_write_area = g.Frame.new('文件上传')

    _file_write_area_opts = g.Box(orientation=VERTICAL, spacing=6)

    _row1 = g.Box()
    m._file_write_area_shared_lib_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._file_write_area_shared_lib_entry]
    )

    _row1.pack_start(m._file_write_area_udf_ckbtn, False, True, 5)
    _row1.pack_start(m._file_write_area_shared_lib_ckbtn, False, True, 5)
    _row1.pack_start(m._file_write_area_shared_lib_entry, True, True, 0)
    _row1.pack_start(m._file_write_area_shared_lib_chooser, False, True, 5)

    _row2 = g.Box()
    m._file_write_area_file_write_chooser.connect(
      'clicked',
      self.set_file_entry_text,
      [m._file_write_area_file_write_entry]
    )

    _row2.pack_start(m._file_write_area_file_write_ckbtn, False, True, 5)
    _row2.pack_start(m._file_write_area_file_write_entry, True, True, 0)
    _row2.pack_start(m._file_write_area_file_write_chooser, False, True, 5)

    _row3 = g.Box()
    _row3.pack_start(m._file_write_area_file_dest_ckbtn, False, True, 5)
    _row3.pack_start(m._file_write_area_file_dest_entry, True, True, 5)

    _file_write_area_opts.pack_start(_row1, False, True, 5)
    _file_write_area_opts.pack_start(_row2, False, True, 5)
    _file_write_area_opts.pack_start(_row3, False, True, 5)
    self._file_write_area.add(_file_write_area_opts)

  def _build_page1_file_read(self):
    self._file_read_area = g.Frame.new('读取远程文件')

    _file_read_area_opts = g.Box(orientation=VERTICAL, spacing=6)

    _row1 = g.Box()
    m._file_read_area_file_read_entry.set_text('/etc/passwd')
    m._file_read_area_file_btn.connect('clicked', self._handlers.read_dumped_file)

    _row1.pack_start(m._file_read_area_file_read_ckbtn, False, True, 10)
    _row1.pack_start(m._file_read_area_file_read_entry, True, True, 10)
    _row1.pack_start(m._file_read_area_file_btn, False, True, 10)

    _file_read_area_opts.pack_start(_row1, False, True, 5)
    self._file_read_area.add(_file_read_area_opts)

  def _build_page2(self):
    '''
    用subprocess不可实现与sqlap的交互!
    不管是多线程, 同步还是异步, 都不行, 只能使用pty
    '''
    self.page2 = g.Box(orientation=VERTICAL, spacing=6)
    self.page2.set_border_width(10)

    _row1 = g.Box(spacing = 6)
    # m._page2_cmdline_str_label.set_alignment(0, 0.5)    # 怎么没有垂直居中?
    m._page2_respwan_btn.connect('clicked', self._handlers.respawn_terminal)

    # _row1.pack_start(m._page2_cmdline_str_label, True, True, 0)
    _row1.pack_start(m._page2_respwan_btn, False, True, 0)

    _row2 = g.Frame()
    # 等价于_pty = m._page2_terminal.pty_new_sync(Vte.PtyFlags.DEFAULT)
    _pty = Vte.Pty.new_sync(Vte.PtyFlags.DEFAULT)
    m._page2_terminal.set_pty(_pty)

    # https://stackoverflow.com/questions/55105447/virtual-python-shell-with-vte-pty-spawn-async
    # https://gtk-d.dpldocs.info/vte.Pty.Pty.spawnAsync.html
    # API手册上的该方法签名有问题, 与实际的对不上
    # 最后一个参数为回调函数, 是必填项
    _pty.spawn_async(str(Path.home()),
                     [self._handlers.shell],
                     None,
                     GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                     None,
                     None,
                     -1,
                     None,
                     lambda pty, task: None)

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(m._page2_terminal)
    _row2.add(_scrolled)

    self.page2.pack_start(_row1, False, True, 5)
    self.page2.pack_end(_row2, True, True, 0)

  def _build_page3(self):
    self.page3 = g.Box(orientation=VERTICAL, spacing=6)
    self.page3.set_border_width(10)

    _row1 = g.Frame()
    m._page3_log_view.set_editable(False)
    m._page3_log_view.set_wrap_mode(g.WrapMode.WORD)

    _log_view_textbuffer = m._page3_log_view.get_buffer()
    self._handlers.clear_log_view_buffer(None)

    _end = _log_view_textbuffer.get_end_iter()
    _log_view_textbuffer.create_mark('end', _end, False)

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(m._page3_log_view)
    _row1.add(_scrolled)

    _row2 = g.Box()
    m._page3_read_target_btn.connect('clicked', self._handlers.read_target_file)
    m._page3_clear_btn.connect('clicked', self._handlers.clear_log_view_buffer)
    m._page3_read_log_btn.connect('clicked', self._handlers.read_log_file)

    _row2.pack_start(m._page3_read_target_btn, True, False, 0)
    _row2.pack_start(m._page3_clear_btn, True, False, 0)
    _row2.pack_start(m._page3_read_log_btn, True, False, 0)

    self.page3.pack_start(_row1, True, True, 5)
    self.page3.pack_end(_row2, False, True, 0)

  def _build_page4(self):
    self.page4 = g.Box(orientation=VERTICAL)
    self.page4.set_border_width(10)

    _row1 = g.Box(spacing = 6)
    m._page4_api_server_entry.set_text('127.0.0.1:8775')
    # set_width_chars: 设置entry长度
    # set_max_length: 设置entry可输入的字符长度(admin token只有32位)
    m._page4_admin_token_entry.set_max_length(32)
    _row1.pack_start(m._page4_api_server_label, False, True, 0)
    _row1.pack_start(m._page4_api_server_entry, True, True, 0)
    _row1.pack_start(m._page4_admin_token_label, False, True, 0)
    _row1.pack_start(m._page4_admin_token_entry, True, True, 0)

    _row2 = g.Box(spacing = 6)
    _arrow_down = g.Image.new_from_icon_name('pan-down-symbolic', 1)
    m._page4_admin_list_btn.set_image(_arrow_down)
    m._page4_admin_list_btn.set_image_position(g.PositionType.RIGHT)
    m._page4_admin_list_btn.set_always_show_image(True)

    m._page4_task_new_btn.connect('clicked', self._handlers.api_task_new)
    m._page4_admin_list_btn.connect('clicked', self._handlers.api_admin_list)
    m._page4_admin_flush_btn.connect('clicked', self._handlers.api_admin_flush)
    m._page4_clear_task_view_btn.connect('clicked', self._handlers.clear_task_view_buffer)

    _row2.pack_start(m._page4_task_new_btn, False, True, 0)
    _row2.pack_start(m._page4_admin_list_btn, False, True, 0)
    _row2.pack_start(m._page4_admin_flush_btn, False, True, 0)
    _row2.pack_start(m._page4_clear_task_view_btn, False, True, 0)

    _row3 = g.Frame()
    _paned = g.Paned()

    self._api_admin_list_rows = g.ListBox.new()
    self._api_admin_list_rows.set_selection_mode(g.SelectionMode.NONE)

    _lscrolled = g.ScrolledWindow()
    _lscrolled.set_size_request(400, -1)
    _lscrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _lscrolled.add(self._api_admin_list_rows)

    _rbox = g.Box(orientation = VERTICAL)
    m._page4_option_get_entry.set_text('url risk level')

    m._page4_option_set_view.set_wrap_mode(g.WrapMode.CHAR)
    _option_set_view_textbuffer = m._page4_option_set_view.get_buffer()
    _options_example = ("{\n"
                        "  'url': 'http://www.site.com/vuln.php?id=1',\n"
                        "  'level': 1, 'risk': 1,\n\n"
                        "}\n# 所有选项见sqlmap目录中的optiondict.py\n")
    _option_set_view_textbuffer.set_text(_options_example, len(_options_example.encode('utf8')))
    # 貌似scrollwindow要直接包含textview,
    # 不然一直回车后, 页面不会向上滚
    _option_set_scrolled = g.ScrolledWindow()
    _option_set_scrolled.set_size_request(400, -1)
    _option_set_scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _option_set_scrolled.add(m._page4_option_set_view)

    _rbox.pack_start(m._page4_option_get_entry, False, True, 2)
    _rbox.pack_start(_option_set_scrolled, True, True, 2)

    # Warning: don't edit pack1(), pack2() again, or it would be strange.
    _paned.pack1(_lscrolled, False, False)
    _paned.pack2(_rbox, False, True)
    _row3.add(_paned)

    _row4 = g.Frame()
    m._page4_task_view.set_editable(False)
    m._page4_task_view.set_wrap_mode(g.WrapMode.WORD)

    _task_view_textbuffer = m._page4_task_view.get_buffer()
    _end = _task_view_textbuffer.get_end_iter()
    _task_view_textbuffer.create_mark('end', _end, False)
    self._handlers._task_view_append('此处显示反馈的结果:')

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(m._page4_task_view)

    _row4.add(_scrolled)

    self.page4.pack_start(_row1, False, True, 5)
    self.page4.pack_start(_row2, False, True, 5)
    self.page4.pack_start(_row3, True, True, 5)
    self.page4.pack_start(_row4, True, True, 5)

  def _build_page5(self):
    self.page5 = g.Box(orientation=VERTICAL)
    self.page5.set_border_width(10)

    _row1 = g.Frame()
    m._page5_manual_view.set_editable(False)
    m._page5_manual_view.set_wrap_mode(g.WrapMode.WORD)

    # 使用线程 填充 帮助标签, 加快启动速度
    t = Thread(target = self._set_manual_view,
               args = (m._page5_manual_view.get_buffer(),))
    # t.daemon = True   # 死了也会存在
    t.start()

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(m._page5_manual_view)

    _row1.add(_scrolled)

    self.page5.pack_start(_row1, True, True, 5)

  def _set_manual_view(self, textbuffer):
    '''
    不用多线程能行嘛? 想要获得输出结果就一定会有阻塞的可能!
    https://www.jianshu.com/p/11090e197648
    https://wiki.gnome.org/Projects/PyGObject/Threading
    '''
    _end = textbuffer.get_end_iter()
    # _manual_hh = '/home/needle/bin/output_interval.sh'
    # WIN下不能用此行
    # _manual_hh = ['/usr/bin/env', 'sqlmap', '-hh']
    _manual_hh = 'echo y|sqlmap -hh'
    try:
      _subprocess = Popen(_manual_hh, stdout=PIPE, bufsize=1, shell = True)

      for _an_bytes_line_tmp in iter(_subprocess.stdout.readline, b''):
        GLib.idle_add(textbuffer.insert, _end, _an_bytes_line_tmp.decode('utf8'))
      _subprocess.stdout.close()
      _subprocess.wait()
    except FileNotFoundError as e:
      GLib.idle_add(textbuffer.insert, _end, str(e))

  def _build_page6(self):
    self.page6 = g.Box()

    _about_str = '''
    update at 2019-05-03 16:13:47
    1. VERSION: 0.3.2
       2019年 04月 29日 星期一 21:20:07 CST
       required: python3.5+, python3-gi, sqlmap(require: python2.6+)
       作者: needle wang ( needlewang2011@gmail.com )\n
    2. 使用PyGObject(Gtk+3: python3-gi)重写sqm.py\n
    3. Gtk+3教程: https://python-gtk-3-tutorial.readthedocs.io/en/latest\n
    4. Gtk+3 API: https://lazka.github.io/pgi-docs/Gtk-3.0/\n\n
    5. 感谢sqm带来的灵感, 其作者: KINGX ( https://github.com/kxcode ), sqm UI 使用的是python2 + tkinter
    '''
    self.page6.pack_start(g.Label.new(_about_str), True, False, 0)


def main():
  win = UI_Window()
  win.connect('destroy', lambda x: win.on_window_destroy())
  # win.maximize()
  win.show_all()

  g.main()


if __name__ == '__main__':
  main()
