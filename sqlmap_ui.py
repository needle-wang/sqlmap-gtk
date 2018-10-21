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
from sqlmap_ui_handlers import Singal_Handlers as handlers

# from basis_and_tool.logging_needle import get_console_logger
# logger = get_console_logger()


class UI_Window(g.Window):
  def __init__(self):
    super().__init__(title='sqlmap-ui')
    self.connect('key_press_event', self.on_window_key_press_event)

    self._handlers = handlers(self)

    self.main_box = g.Box.new(orientation = g.Orientation.VERTICAL, spacing = 0)
    self.add(self.main_box)

    self._build_page_target()

    self.main_box.pack_start(self._target_notbook, False, True, 0)

    self.notebook = g.Notebook()

    self._build_page1()
    self._build_page2()
    self._build_page3()
    self._build_page4()

    self.notebook.append_page(self.page1, g.Label.new_with_mnemonic('选项区(_Q)'))
    self.notebook.append_page(self.page2, g.Label.new_with_mnemonic('显示区(_W)'))
    self.notebook.append_page(self.page3, g.Label.new_with_mnemonic('帮助(_H)'))
    self.notebook.append_page(self.page4, g.Label.new_with_mnemonic('关于(_A)'))

    self.main_box.pack_start(self.notebook, True, True, 0)

  def unselect_all_ckbtn(self, button):
    for i in dir(self):
      if 'ckbtn' in i:
        _tmp_ckbtn = getattr(self, i)
        if isinstance(_tmp_ckbtn, g.CheckButton):
          _tmp_ckbtn.set_active(False)

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
    self._url_combobox.set_tooltip_text(
      '必填项, 从 目标url/burp日志/HTTP请求... 任选一项')

    _url_area.pack_start(self._url_combobox, True, True, 0)

    self._target_notbook.append_page(_url_area, g.Label('目标url'))

    _burp_area = g.Box()

    self._burp_logfile = g.Entry()
    self._burp_logfile.set_tooltip_text(
      '-l: Burp或WebScarab代理的日志文件路径(用来解析目标)')

    _burp_area.pack_start(self._burp_logfile, True, True, 0)

    self._target_notbook.append_page(_burp_area, g.Label('burp日志'))

    _request_area = g.Box()

    self._request_file = g.Entry()
    self._request_file.set_tooltip_text(
      '-r: 包含HTTP请求的的文件路径(如从fiddler中得来的)')

    _request_area.pack_start(self._request_file, True, True, 0)

    self._target_notbook.append_page(_request_area, g.Label('HTTP请求'))

    _sitemap_url_area = g.Box()

    self._sitemap_url = g.Entry()
    self._sitemap_url.set_tooltip_text(
      '-x: 远程sitemap(.xml)文件的url(用来解析目标)')

    _sitemap_url_area.pack_start(self._sitemap_url, True, True, 0)

    self._target_notbook.append_page(_sitemap_url_area, g.Label('xml_url'))

    _bulkfile_area = g.Box()

    self._bulkfile = g.Entry()
    self._bulkfile.set_tooltip_text(
      '-m: 给定一个包含多个目标的文本路径')

    _bulkfile_area.pack_start(self._bulkfile, True, True, 0)

    self._target_notbook.append_page(_bulkfile_area, g.Label('BULKFILE'))

    _google_dork_area = g.Box()

    self._google_dork = g.Entry()
    self._google_dork.set_tooltip_text(
      '-g: 处理google dork 结果为目标url')

    _google_dork_area.pack_start(self._google_dork, True, True, 0)

    self._target_notbook.append_page(_google_dork_area, g.Label('GOOGLEDORK'))

    _configfile_area = g.Box()

    self._configfile = g.Entry()
    self._configfile.set_tooltip_text(
      '-c: 从一个本地ini配置文件载入选项')

    _configfile_area.pack_start(self._configfile, True, True, 0)

    self._target_notbook.append_page(_configfile_area, g.Label('ini文件'))

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
    self._build_page1_OS()
    self._build_page1_general()
    self._build_page1_misc()

    _notebook.append_page(self.page1_setting, g.Label.new_with_mnemonic('设置(_1)'))
    _notebook.append_page(self.page1_request, g.Label.new_with_mnemonic('请求(_2)'))
    _notebook.append_page(self.page1_enumeration, g.Label.new_with_mnemonic('枚举(_3)'))
    _notebook.append_page(self.page1_file, g.Label.new_with_mnemonic('文件(_4)'))
    _notebook.append_page(self.page1_OS, g.Label.new_with_mnemonic('OS(_5)'))
    _notebook.append_page(self.page1_general, g.Label.new_with_mnemonic('通用(_6)'))
    _notebook.append_page(self.page1_misc, g.Label.new_with_mnemonic('杂项(_7)'))

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

  def _build_page1_misc(self):
    self.page1_misc = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()

    self._page1_misc_z_ckbtn = g.CheckButton('使用短的助记符')
    self._page1_misc_z_entry = g.Entry()

    _row1.pack_start(self._page1_misc_z_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_misc_z_entry, True, True, 5)

    _row2 = g.Box()

    self._page1_misc_beep_ckbtn = g.CheckButton('响铃')
    self._page1_misc_cleanup_ckbtn = g.CheckButton('清理DBMS?')
    self._page1_misc_dependencies_ckbtn = g.CheckButton('检查丢失的(非核心的)sqlmap依赖')
    self._page1_misc_disable_color_ckbtn = g.CheckButton('禁用终端输出的颜色')
    self._page1_misc_identify_waf_ckbtn = g.CheckButton('鉴别WAF')
    self._page1_misc_list_tampers_ckbtn = g.CheckButton('显示可用的tamper脚本列表')

    _row2.pack_start(self._page1_misc_beep_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_misc_cleanup_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_misc_dependencies_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_misc_disable_color_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_misc_identify_waf_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_misc_list_tampers_ckbtn, False, True, 5)

    _row3 = g.Box()

    self._page1_misc_mobile_ckbtn = g.CheckButton('模拟手机请求')
    self._page1_misc_offline_ckbtn = g.CheckButton('离线模式(只使用保存的会话数据)')
    self._page1_misc_purge_ckbtn = g.CheckButton('彻底清除所有记录')
    self._page1_misc_skip_waf_ckbtn = g.CheckButton('跳过WAF/IPS保护的启发式侦测')
    self._page1_misc_smart_ckbtn = g.CheckButton('进行详细测试(当启动正面启发式时)')

    _row3.pack_start(self._page1_misc_mobile_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_misc_offline_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_misc_purge_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_misc_skip_waf_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_misc_smart_ckbtn, False, True, 5)

    _row4 = g.Box()

    self._page1_misc_tmp_dir_ckbtn = g.CheckButton('本地临时目录')
    self._page1_misc_tmp_dir_entry = g.Entry()

    _row4.pack_start(self._page1_misc_tmp_dir_ckbtn, False, True, 5)
    _row4.pack_start(self._page1_misc_tmp_dir_entry, True, True, 5)

    _row5 = g.Box()

    self._page1_misc_web_root_ckbtn = g.CheckButton('远程web的root目录')
    self._page1_misc_web_root_entry = g.Entry()
    self._page1_misc_web_root_entry.set_text('/var/www')

    _row5.pack_start(self._page1_misc_web_root_ckbtn, False, True, 5)
    _row5.pack_start(self._page1_misc_web_root_entry, True, True, 5)

    _row6 = g.Box()

    self._page1_misc_answers_ckbtn = g.CheckButton('设置交互时的问题答案:')
    self._page1_misc_answers_entry = g.Entry()
    self._page1_misc_answers_entry.set_text('quit=N,follow=N')

    self._page1_misc_alert_ckbtn = g.CheckButton('当发现注入时运行OS命令:')
    self._page1_misc_alert_entry = g.Entry()

    self._page1_misc_gpage_ckbtn = g.CheckButton('GOOGLEDORK时的页码')
    self._page1_misc_gpage_entry = g.Entry()

    _row6.pack_start(self._page1_misc_answers_ckbtn, False, True, 5)
    _row6.pack_start(self._page1_misc_answers_entry, True, True, 5)
    _row6.pack_start(self._page1_misc_alert_ckbtn, False, True, 5)
    _row6.pack_start(self._page1_misc_alert_entry, True, True, 5)
    _row6.pack_start(self._page1_misc_gpage_ckbtn, False, True, 5)
    _row6.pack_start(self._page1_misc_gpage_entry, False, True, 5)

    self.page1_misc.add(_row1)
    self.page1_misc.add(_row2)
    self.page1_misc.add(_row3)
    self.page1_misc.add(_row4)
    self.page1_misc.add(_row5)
    self.page1_misc.add(_row6)

  def _build_page1_general(self):
    self.page1_general = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()

    self._page1_general_check_internet_ckbtn = g.CheckButton('检查与目标的网络连接')
    self._page1_general_binary_fields_ckbtn = g.CheckButton('生成有二进制值的字段')
    self._page1_general_binary_fields_entry = g.Entry()
    self._page1_general_eta_ckbtn = g.CheckButton('显示剩余时间')
    self._page1_general_update_ckbtn = g.CheckButton('更新sqlmap')

    _row1.pack_start(self._page1_general_check_internet_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_general_binary_fields_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_general_binary_fields_entry, False, True, 5)
    _row1.pack_start(self._page1_general_eta_ckbtn, False, True, 5)
    _row1.pack_start(self._page1_general_update_ckbtn, False, True, 5)

    _row2 = g.Box()

    self._page1_general_session_file_ckbtn = g.CheckButton('指定会话文件')
    self._page1_general_session_file_entry = g.Entry()

    self._page1_general_traffic_file_ckbtn = g.CheckButton('转存所有http流量到')
    self._page1_general_traffic_file_entry = g.Entry()

    _row2.pack_start(self._page1_general_session_file_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_general_session_file_entry, True, True, 5)
    _row2.pack_start(self._page1_general_traffic_file_ckbtn, False, True, 5)
    _row2.pack_start(self._page1_general_traffic_file_entry, True, True, 5)

    _row3 = g.Box()

    self._page1_general_crawl_ckbtn = g.CheckButton('爬网站(的层级/深度)')
    self._page1_general_crawl_entry = g.Entry()

    self._page1_general_crawl_exclude_ckbtn = g.CheckButton('爬站时排除(正则)页面')
    self._page1_general_crawl_exclude_entry = g.Entry()

    _row3.pack_start(self._page1_general_crawl_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_general_crawl_entry, False, True, 5)
    _row3.pack_start(self._page1_general_crawl_exclude_ckbtn, False, True, 5)
    _row3.pack_start(self._page1_general_crawl_exclude_entry, False, True, 5)

    _row4 = g.Box()

    self._page1_general_dump_format_ckbtn = g.CheckButton('dump结果的文件格式(默认CSV)')
    self._page1_general_dump_format_entry = g.Entry()

    self._page1_general_csv_del_ckbtn = g.CheckButton('(csv文件的)分隔符')
    self._page1_general_csv_del_entry = g.Entry()

    _row4.pack_start(self._page1_general_dump_format_ckbtn, False, True, 5)
    _row4.pack_start(self._page1_general_dump_format_entry, False, True, 5)
    _row4.pack_start(self._page1_general_csv_del_ckbtn, False, True, 5)
    _row4.pack_start(self._page1_general_csv_del_entry, False, True, 5)

    _row5 = g.Box()

    self._page1_general_charset_ckbtn = g.CheckButton('盲注所用的字符集合')
    self._page1_general_charset_entry = g.Entry()

    self._page1_general_encoding_ckbtn = g.CheckButton('字符编码(用于数据获取)')
    self._page1_general_encoding_entry = g.Entry()

    _row5.pack_start(self._page1_general_charset_ckbtn, False, True, 5)
    _row5.pack_start(self._page1_general_charset_entry, False, True, 5)
    _row5.pack_start(self._page1_general_encoding_ckbtn, False, True, 5)
    _row5.pack_start(self._page1_general_encoding_entry, False, True, 5)

    _row6 = g.Box()

    self._page1_general_flush_session_ckbtn = g.CheckButton('清空会话文件')
    self._page1_general_forms_ckbtn = g.CheckButton('解析和测试表单')
    self._page1_general_fresh_queries_ckbtn = g.CheckButton('刷新此次查询')

    _row6.pack_start(self._page1_general_flush_session_ckbtn, False, True, 5)
    _row6.pack_start(self._page1_general_forms_ckbtn, False, True, 5)
    _row6.pack_start(self._page1_general_fresh_queries_ckbtn, False, True, 5)

    _row7 = g.Box()

    self._page1_general_har_ckbtn = g.CheckButton('转存流量至HAR文件')
    self._page1_general_har_entry = g.Entry()
    self._page1_general_output_dir_ckbtn = g.CheckButton('输出目录')
    self._page1_general_output_dir_entry = g.Entry()

    _row7.pack_start(self._page1_general_har_ckbtn, False, True, 5)
    _row7.pack_start(self._page1_general_har_entry, True, True, 5)
    _row7.pack_start(self._page1_general_output_dir_ckbtn, False, True, 5)
    _row7.pack_start(self._page1_general_output_dir_entry, True, True, 5)

    _row8 = g.Box()

    self._page1_general_parse_errors_ckbtn = g.CheckButton('解析并显示DB错误信息')
    self._page1_general_save_ckbtn = g.CheckButton('保存选项至INI文件')
    self._page1_general_save_entry = g.Entry()
    self._page1_general_scope_ckbtn = g.CheckButton('从代理日志过滤出目标(正则)')
    self._page1_general_scope_entry = g.Entry()

    _row8.pack_start(self._page1_general_parse_errors_ckbtn, False, True, 5)
    _row8.pack_start(self._page1_general_save_ckbtn, False, True, 5)
    _row8.pack_start(self._page1_general_save_entry, True, True, 5)
    _row8.pack_start(self._page1_general_scope_ckbtn, False, True, 5)
    _row8.pack_start(self._page1_general_scope_entry, True, True, 5)

    _row9 = g.Box()

    self._page1_general_test_filter_ckbtn = g.CheckButton('测试过滤器(从payload/title选择)')
    self._page1_general_test_filter_entry = g.Entry()
    self._page1_general_test_skip_ckbtn = g.CheckButton('测试跳过(从payload/title选择)')
    self._page1_general_test_skip_entry = g.Entry()

    _row9.pack_start(self._page1_general_test_filter_ckbtn, False, True, 5)
    _row9.pack_start(self._page1_general_test_filter_entry, True, True, 5)
    _row9.pack_start(self._page1_general_test_skip_ckbtn, False, True, 5)
    _row9.pack_start(self._page1_general_test_skip_entry, True, True, 5)

    self.page1_general.add(_row1)
    self.page1_general.add(_row2)
    self.page1_general.add(_row3)
    self.page1_general.add(_row4)
    self.page1_general.add(_row5)
    self.page1_general.add(_row6)
    self.page1_general.add(_row7)
    self.page1_general.add(_row8)
    self.page1_general.add(_row9)

  def _build_page1_OS(self):
    self.page1_OS = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box(orientation=g.Orientation.VERTICAL)

    self._build_page1_OS_access()

    _row1.pack_start(self._OS_access_area, False, True, 0)
    self.page1_OS.add(_row1)

    _row2 = g.Box(orientation=g.Orientation.VERTICAL)

    self._build_page1_OS_registry()

    _row2.pack_start(self._OS_registry_area, False, True, 0)
    self.page1_OS.add(_row2)

  def _build_page1_OS_access(self):
    self._OS_access_area = g.Frame.new('访问后端OS')

    _OS_access_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()

    self._OS_access_area_os_cmd_ckbtn = g.CheckButton('执行CLI命令')
    self._OS_access_area_os_cmd_entry = g.Entry()

    _row1.pack_start(self._OS_access_area_os_cmd_ckbtn, False, True, 5)
    _row1.pack_start(self._OS_access_area_os_cmd_entry, True, True, 5)

    _OS_access_area_opts.add(_row1)

    _row2 = g.Box()

    self._OS_access_area_os_shell_ckbtn = g.CheckButton('获取交互shell')
    self._OS_access_area_os_pwn_ckbtn = g.CheckButton('--os-pwn')
    self._OS_access_area_os_pwn_ckbtn.set_tooltip_text('Prompt for an OOB shell, Meterpreter or VNC')
    self._OS_access_area_os_smbrelay_ckbtn = g.CheckButton('--os-smbrelay')
    self._OS_access_area_os_bof_ckbtn = g.CheckButton('--os-bof')
    self._OS_access_area_priv_esc_ckbtn = g.CheckButton('--priv-esc')

    _row2.pack_start(self._OS_access_area_os_shell_ckbtn, False, True, 5)
    _row2.pack_start(self._OS_access_area_os_pwn_ckbtn, False, True, 5)
    _row2.pack_start(self._OS_access_area_os_smbrelay_ckbtn, False, True, 5)
    _row2.pack_start(self._OS_access_area_os_bof_ckbtn, False, True, 5)
    _row2.pack_start(self._OS_access_area_priv_esc_ckbtn, False, True, 5)

    _OS_access_area_opts.add(_row2)

    _row3 = g.Box()

    self._OS_access_area_msf_path_ckbtn = g.CheckButton('本地Metasploit安装路径')
    self._OS_access_area_msf_path_entry = g.Entry()
    self._OS_access_area_msf_path_entry.set_tooltip_text('--msf-path=MSFPATH Local path where Metasploit Framework is installed')

    _row3.pack_start(self._OS_access_area_msf_path_ckbtn, False, True, 5)
    _row3.pack_start(self._OS_access_area_msf_path_entry, True, True, 5)

    self._OS_access_area_tmp_path_ckbtn = g.CheckButton('远程临时目录(绝对路径)')
    self._OS_access_area_tmp_path_entry = g.Entry()
    self._OS_access_area_tmp_path_entry.set_tooltip_text('--tmp-path=TMPPATH Remote absolute path of temporary files directory')

    _row3.pack_start(self._OS_access_area_tmp_path_ckbtn, False, True, 5)
    _row3.pack_start(self._OS_access_area_tmp_path_entry, True, True, 5)

    _OS_access_area_opts.add(_row3)

    self._OS_access_area.add(_OS_access_area_opts)

  def _build_page1_OS_registry(self):
    self._OS_registry_area = g.Frame.new('访问WIN下注册表')

    _OS_registry_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._OS_registry_area_reg_read_ckbtn = g.CheckButton('读取一个键值')
    self._OS_registry_area_reg_add_ckbtn = g.CheckButton('添加一个键值')
    self._OS_registry_area_reg_del_ckbtn = g.CheckButton('删除一个键值')

    _row1.pack_start(self._OS_registry_area_reg_read_ckbtn, False, True, 5)
    _row1.pack_start(self._OS_registry_area_reg_add_ckbtn, False, True, 5)
    _row1.pack_start(self._OS_registry_area_reg_del_ckbtn, False, True, 5)

    _OS_registry_area_opts.add(_row1)

    _row2 = g.Box()
    self._OS_registry_area_reg_key_ckbtn = g.CheckButton('键')
    self._OS_registry_area_reg_key_entry = g.Entry()
    self._OS_registry_area_reg_value_ckbtn = g.CheckButton('值')
    self._OS_registry_area_reg_value_entry = g.Entry()

    _row2.pack_start(self._OS_registry_area_reg_key_ckbtn, False, True, 5)
    _row2.pack_start(self._OS_registry_area_reg_key_entry, True, True, 5)

    _row2.pack_start(self._OS_registry_area_reg_value_ckbtn, False, True, 5)
    _row2.pack_start(self._OS_registry_area_reg_value_entry, True, True, 5)

    _OS_registry_area_opts.add(_row2)

    _row3 = g.Box()
    self._OS_registry_area_reg_data_ckbtn = g.CheckButton('数据')
    self._OS_registry_area_reg_data_entry = g.Entry()
    self._OS_registry_area_reg_type_ckbtn = g.CheckButton('类型')
    self._OS_registry_area_reg_type_entry = g.Entry()

    _row3.pack_start(self._OS_registry_area_reg_data_ckbtn, False, True, 5)
    _row3.pack_start(self._OS_registry_area_reg_data_entry, True, True, 5)

    _row3.pack_start(self._OS_registry_area_reg_type_ckbtn, False, True, 5)
    _row3.pack_start(self._OS_registry_area_reg_type_entry, True, True, 5)

    _OS_registry_area_opts.add(_row3)

    self._OS_registry_area.add(_OS_registry_area_opts)

  def _build_page1_setting(self):
    _page1_setting = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()
    self._build_page1_setting_inject()
    self._build_page1_setting_detection()
    self._build_page1_setting_tech()

    _row1.pack_start(self._inject_area, False, True, 0)
    _row1.pack_start(self._detection_area, False, True, 0)
    _row1.pack_start(self._tech_area, False, True, 0)

    _row2 = g.Box()
    self._build_page1_setting_tamper()
    self._build_page1_setting_optimize()
    self._build_page1_setting_general()

    _row2.pack_start(self._tamper_area, False, True, 0)
    _row2.pack_start(self._optimize_area, False, True, 0)
    _row2.pack_start(self._general_area, False, True, 0)

    _page1_setting.pack_start(_row1, True, True, 0)
    _page1_setting.pack_start(_row2, True, True, 0)

    self.page1_setting = g.ScrolledWindow()
    self.page1_setting.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    self.page1_setting.add(_page1_setting)

  def _build_page1_setting_tech(self):
    self._tech_area = g.Frame.new('各注入技术的选项')

    _tech_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    _row1.set_tooltip_text('--technique=')

    self._tech_area_tech_ckbtn = g.CheckButton('注入技术')
    self._tech_area_tech_entry = g.Entry()
    self._tech_area_tech_entry.set_text('BEUSTQ')

    _row1.pack_start(self._tech_area_tech_ckbtn, False, True, 5)
    _row1.pack_end(self._tech_area_tech_entry, False, True, 5)
    _tech_area_opts.add(_row1)

    _row2 = g.Box()
    _row2.set_tooltip_text('--time-sec=默认为5')

    self._tech_area_time_sec_ckbtn = g.CheckButton('指定DB延迟多少秒响应')
    self._tech_area_time_sec_entry = g.Entry()
    self._tech_area_time_sec_entry.set_text('(时间盲注时)')

    _row2.pack_start(self._tech_area_time_sec_ckbtn, False, True, 5)
    _row2.pack_end(self._tech_area_time_sec_entry, False, True, 5)
    _tech_area_opts.add(_row2)

    _row3 = g.Box()
    _row3.set_tooltip_text('--union-cols=')

    self._tech_area_union_col_ckbtn = g.CheckButton('指定最大union列数')
    self._tech_area_union_col_entry = g.Entry()
    self._tech_area_union_col_entry.set_text('(union查询时)')

    _row3.pack_start(self._tech_area_union_col_ckbtn, False, True, 5)
    _row3.pack_end(self._tech_area_union_col_entry, False, True, 5)
    _tech_area_opts.add(_row3)

    _row4 = g.Box()
    _row4.set_tooltip_text('--union-char=')

    self._tech_area_union_chr_ckbtn = g.CheckButton('指定枚举列数时所用字符')
    self._tech_area_union_chr_entry = g.Entry()
    self._tech_area_union_chr_entry.set_text('(union查询时)')

    _row4.pack_start(self._tech_area_union_chr_ckbtn, False, True, 5)
    _row4.pack_end(self._tech_area_union_chr_entry, False, True, 5)
    _tech_area_opts.add(_row4)

    _row5 = g.Box()
    _row5.set_tooltip_text('--union-from=')

    self._tech_area_union_table_ckbtn = g.CheckButton('指定枚举列数时from的表名')
    self._tech_area_union_table_entry = g.Entry()
    self._tech_area_union_table_entry.set_text('(union查询时)')

    _row5.pack_start(self._tech_area_union_table_ckbtn, False, True, 5)
    _row5.pack_end(self._tech_area_union_table_entry, False, True, 5)
    _tech_area_opts.add(_row5)

    _row6 = g.Box()
    _row6.set_tooltip_text('--dns-domain=')

    self._tech_area_dns_ckbtn = g.CheckButton('指定DNS')
    self._tech_area_dns_entry = g.Entry()
    self._tech_area_dns_entry.set_text('(DNS exfiltration)')

    _row6.pack_start(self._tech_area_dns_ckbtn, True, True, 5)
    _row6.pack_end(self._tech_area_dns_entry, True, True, 5)
    _tech_area_opts.add(_row6)

    _row7 = g.Box()
    _row7.set_tooltip_text('--second-url=')

    self._tech_area_second_url_ckbtn = g.CheckButton('指定二阶响应的url')
    self._tech_area_second_url_entry = g.Entry()

    _row7.pack_start(self._tech_area_second_url_ckbtn, True, True, 5)
    _row7.pack_end(self._tech_area_second_url_entry, True, True, 5)
    _tech_area_opts.add(_row7)

    _row8 = g.Box()
    _row8.set_tooltip_text('--second-req=')

    self._tech_area_second_req_url_ckbtn = g.CheckButton('指定含二阶HTTP请求的文件')
    self._tech_area_second_req_url_entry = g.Entry()

    _row8.pack_start(self._tech_area_second_req_url_ckbtn, True, True, 5)
    _row8.pack_end(self._tech_area_second_req_url_entry, True, True, 5)
    _tech_area_opts.add(_row8)

    self._tech_area.add(_tech_area_opts)

  def _build_page1_setting_detection(self):
    self._detection_area = g.Frame.new('探测选项')

    _detection_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()

    _level_store = g.ListStore(int, str)
    _level_store.append([1, "1"])
    _level_store.append([2, "2"])
    _level_store.append([3, "3"])
    _level_store.append([4, "4"])
    _level_store.append([5, "5"])

    self._detection_area_level_ckbtn = g.CheckButton('探测等级(范围)')
    self._detection_area_level_ckbtn.set_tooltip_text('--level=默认为1')

    self._detection_area_level_combobox = g.ComboBox.new_with_model_and_entry(_level_store)
    self._detection_area_level_combobox.set_entry_text_column(1)  # 设成0, 会出现段错误~~, NB!

    self._detection_area_text_only_ckbtn = g.CheckButton('仅对比文本')
    self._detection_area_text_only_ckbtn.set_tooltip_text('--text-only')

    _row1.pack_start(self._detection_area_level_ckbtn, False, True, 5)
    _row1.pack_start(self._detection_area_level_combobox, True, False, 10)
    _row1.pack_start(self._detection_area_text_only_ckbtn, False, True, 5)
    _detection_area_opts.add(_row1)

    _row2 = g.Box()

    _level_store = g.ListStore(int, str)
    _level_store.append([1, "1"])
    _level_store.append([2, "2"])
    _level_store.append([3, "3"])

    self._detection_area_risk_ckbtn = g.CheckButton('payload危险等级')
    self._detection_area_risk_ckbtn.set_tooltip_text('--risk=默认为1')

    self._detection_area_risk_combobox = g.ComboBox.new_with_model_and_entry(_level_store)
    self._detection_area_risk_combobox.set_entry_text_column(1)  # 设成0, 会出现段错误~~, NB!

    self._detection_area_titles_ckbtn = g.CheckButton('仅对比title')
    self._detection_area_titles_ckbtn.set_tooltip_text('--titles')

    _row2.pack_start(self._detection_area_risk_ckbtn, False, True, 5)
    _row2.pack_start(self._detection_area_risk_combobox, True, False, 10)
    _row2.pack_start(self._detection_area_titles_ckbtn, False, True, 5)
    _detection_area_opts.add(_row2)

    _row3 = g.Box()
    _row3.set_tooltip_text('--string=STRING     String to match when query is evaluated to True')

    self._detection_area_str_ckbtn = g.CheckButton('指定字符串')
    self._detection_area_str_entry = g.Entry()
    self._detection_area_str_entry.set_text('查询为真时页面出现的字串')

    _row3.pack_start(self._detection_area_str_ckbtn, False, True, 5)
    _row3.pack_end(self._detection_area_str_entry, True, True, 5)
    _detection_area_opts.add(_row3)

    _row4 = g.Box()
    _row4.set_tooltip_text('--not-string=NOT..  String to match when query is evaluated to False')

    self._detection_area_not_str_ckbtn = g.CheckButton('指定字符串')
    self._detection_area_not_str_entry = g.Entry()
    self._detection_area_not_str_entry.set_text('查询为假时的')

    _row4.pack_start(self._detection_area_not_str_ckbtn, False, True, 5)
    _row4.pack_end(self._detection_area_not_str_entry, True, True, 5)
    _detection_area_opts.add(_row4)

    _row5 = g.Box()
    _row5.set_tooltip_text('--regexp=')

    self._detection_area_re_ckbtn = g.CheckButton('指定正则')
    self._detection_area_re_entry = g.Entry()
    self._detection_area_re_entry.set_text('(查询为真时的)')

    _row5.pack_start(self._detection_area_re_ckbtn, False, True, 5)
    _row5.pack_end(self._detection_area_re_entry, True, True, 5)
    _detection_area_opts.add(_row5)

    _row6 = g.Box()
    _row6.set_tooltip_text('--code=')

    self._detection_area_code_ckbtn = g.CheckButton('指定http状态码')
    self._detection_area_code_entry = g.Entry()
    self._detection_area_code_entry.set_text('(查询为真时的)')

    _row6.pack_start(self._detection_area_code_ckbtn, False, True, 5)
    _row6.pack_end(self._detection_area_code_entry, True, True, 5)
    _detection_area_opts.add(_row6)

    self._detection_area.add(_detection_area_opts)

  def _build_page1_setting_general(self):
    self._general_area = g.Frame.new('通用选项')

    _general_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._general_area_finger_ckbtn = g.CheckButton('执行宽泛的DB版本检测')
    self._general_area_finger_ckbtn.set_tooltip_text('--fingerprint')

    _row1.pack_start(self._general_area_finger_ckbtn, False, True, 5)
    _general_area_opts.add(_row1)

    _row2 = g.Box()
    self._general_area_batch_ckbtn = g.CheckButton('非交互模式, 一切皆默认')
    self._general_area_batch_ckbtn.set_tooltip_text('--batch')

    _row2.pack_start(self._general_area_batch_ckbtn, False, True, 5)
    _general_area_opts.add(_row2)

    _row3 = g.Box()
    self._general_area_hex_ckbtn = g.CheckButton('获取数据时使用hex转换')
    self._general_area_hex_ckbtn.set_tooltip_text('--hex')

    _row3.pack_start(self._general_area_hex_ckbtn, False, True, 5)
    _general_area_opts.add(_row3)

    _row4 = g.Box()
    _row4.set_tooltip_text('-v 默认为1')

    self._general_area_verbose_ckbtn = g.CheckButton('输出详细程度')

    self._detail_vv_entry = g.Entry()
    self._detail_vv_entry.set_text('(0-6)')

    _row4.pack_start(self._general_area_verbose_ckbtn, False, True, 5)
    _row4.pack_start(self._detail_vv_entry, True, True, 5)
    _general_area_opts.add(_row4)

    self._general_area.add(_general_area_opts)

  def _build_page1_setting_optimize(self):
    self._optimize_area = g.Frame.new('性能优化')

    _optimize_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()
    self._optimize_area_turn_all_ckbtn = g.CheckButton('启用所有优化选项')
    self._optimize_area_turn_all_ckbtn.connect('clicked', self._handlers.optimize_area_controller)
    self._optimize_area_turn_all_ckbtn.set_tooltip_text('-o')

    _row1.pack_start(self._optimize_area_turn_all_ckbtn, False, True, 5)
    _optimize_area_opts.add(_row1)

    _row2 = g.Box()
    self._optimize_area_predict_ckbtn = g.CheckButton('预测通常的查询结果')
    self._optimize_area_predict_ckbtn.set_tooltip_text('--predict-output')

    _row2.pack_start(self._optimize_area_predict_ckbtn, False, True, 5)
    _optimize_area_opts.add(_row2)

    _row3 = g.Box()
    self._optimize_area_keep_alive_ckbtn = g.CheckButton('http连接使用keep-alive')
    self._optimize_area_keep_alive_ckbtn.set_tooltip_text('--keep-alive')

    _row3.pack_start(self._optimize_area_keep_alive_ckbtn, False, True, 5)
    _optimize_area_opts.add(_row3)

    _row4 = g.Box()
    self._optimize_area_null_connect_ckbtn = g.CheckButton('只用页面长度报头来比较, 不去获取实际的响应体')
    self._optimize_area_null_connect_ckbtn.set_tooltip_text('--null-connection')

    _row4.pack_start(self._optimize_area_null_connect_ckbtn, False, True, 5)
    _optimize_area_opts.add(_row4)

    _row5 = g.Box()
    _row5.set_tooltip_text('--threads=默认为1')

    self._optimize_area_thread_num_ckbtn = g.CheckButton('启用多线程(数量):')

    _thread_num_store = g.ListStore(int, str)
    _thread_num_store.append([1, "2"])
    _thread_num_store.append([2, "4"])
    self._optimize_area_thread_num_combobox = g.ComboBox.new_with_model_and_entry(_thread_num_store)
    # set_entry_text_column(0)会出现段错误~~, NB!
    self._optimize_area_thread_num_combobox.set_entry_text_column(1)

    _row5.pack_start(self._optimize_area_thread_num_ckbtn, False, True, 5)
    _row5.pack_end(self._optimize_area_thread_num_combobox, False, True, 5)

    _optimize_area_opts.add(_row5)

    self._optimize_area.add(_optimize_area_opts)

  def _build_page1_setting_tamper(self):
    self._tamper_area = g.Frame.new('tamper脚本')

    _tamper_area_list = g.Box()

    _tamper_area_tamper_view = g.TextView()
    _tamper_area_tamper_view.set_tooltip_text(
      '此处填写要使用的tamper脚本名\n详见: sqlmap --list-tamper\n回车或逗号拼接')

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
    _row1.set_tooltip_text('-p TESTPARAMETER\tTestable parameter(s)')

    self._inject_area_param_ckbtn = g.CheckButton('可测试的参数')
    self._inject_area_param_entry = g.Entry()
    self._inject_area_param_entry.set_text('id')

    _row1.pack_start(self._inject_area_param_ckbtn, True, True, 5)
    _row1.pack_end(self._inject_area_param_entry, True, True, 5)

    _row2 = g.Box()
    _row2.set_tooltip_text('--skip-static\tSkip testing parameters that not appear to be dynamic')
    self._inject_area_skip_static_ckbtn = g.CheckButton('跳过无动态特性的参数')

    _row2.pack_start(self._inject_area_skip_static_ckbtn, True, True, 5)

    _row3 = g.Box()
    _row3.set_tooltip_text('--skip=...,...\tSkip testing for given parameter(s)')

    self._inject_area_skip_ckbtn = g.CheckButton('排除参数')
    self._inject_area_skip_entry = g.Entry()

    _row3.pack_start(self._inject_area_skip_ckbtn, True, True, 5)
    _row3.pack_end(self._inject_area_skip_entry, True, True, 5)

    _row4 = g.Box()
    _row4.set_tooltip_text('--param-exclude=.. Regexp to exclude parameters from testing')

    self._param_exclude_ckbtn = g.CheckButton('排除参数(正则)')
    self._param_exclude_entry = g.Entry()

    _row4.pack_start(self._param_exclude_ckbtn, True, True, 5)
    _row4.pack_end(self._param_exclude_entry, True, True, 5)

    _row5 = g.Box()
    _row5.set_tooltip_text('--dbms=DBMS\tForce back-end DBMS to provided value')

    _db_store = g.ListStore(int, str)
    _db_store.append([1, "mysql"])
    _db_store.append([2, "sqlite"])
    _db_store.append([3, "sqlserver"])

    self._inject_area_dbms_ckbtn = g.CheckButton('固定DB类型为')
    self._inject_area_dbms_combobox = g.ComboBox.new_with_model_and_entry(
      _db_store)
    self._inject_area_dbms_combobox.set_entry_text_column(1)

    _row5.pack_start(self._inject_area_dbms_ckbtn, True, True, 5)
    _row5.pack_end(self._inject_area_dbms_combobox, True, True, 5)

    _row6 = g.Box()
    _row6.set_tooltip_text('--dbms-cred=DBMS..  DBMS authentication credentials (user:password)')

    self._inject_area_dbms_cred_ckbtn = g.CheckButton('DB认证:')
    self._inject_area_dbms_cred_entry = g.Entry()

    _row6.pack_start(self._inject_area_dbms_cred_ckbtn, True, True, 5)
    _row6.pack_end(self._inject_area_dbms_cred_entry, True, True, 5)

    _row7 = g.Box()
    _row7.set_tooltip_text('--os=OS\tForce back-end DBMS operating system to provided value')

    self._inject_area_os_ckbtn = g.CheckButton('固定OS为')
    self._inject_area_os_entry = g.Entry()

    _row7.pack_start(self._inject_area_os_ckbtn, True, True, 5)
    _row7.pack_end(self._inject_area_os_entry, True, True, 5)

    _row8 = g.Box()
    _row8.set_tooltip_text('--invalid-bignum    Use big numbers for invalidating values')

    self._inject_area_invalid_bignum_ckbtn = g.CheckButton('对payload中的废值使用大数')

    _row8.pack_start(self._inject_area_invalid_bignum_ckbtn, True, True, 5)

    _row9 = g.Box()
    _row9.set_tooltip_text('--invalid-logical\tUse logical operations for invalidating values')

    self._inject_area_invalid_logic_ckbtn = g.CheckButton('对payload中的废值使用逻辑运算符')

    _row9.pack_start(self._inject_area_invalid_logic_ckbtn, True, True, 5)

    _row10 = g.Box()
    _row10.set_tooltip_text('--invalid-string    Use random strings for invalidating values')

    self._inject_area_invalid_str_ckbtn = g.CheckButton('对payload中的废值使用随机字串')

    _row10.pack_start(self._inject_area_invalid_str_ckbtn, True, True, 5)

    _row11 = g.Box()
    _row11.set_tooltip_text('--no-cast\tTurn off payload casting mechanism')

    self._inject_area_no_cast_ckbtn = g.CheckButton('关掉payload变形机制')

    _row11.pack_start(self._inject_area_no_cast_ckbtn, True, True, 5)

    _row12 = g.Box()
    _row12.set_tooltip_text('--no-escape\tTurn off string escaping mechanism')

    self._inject_area_no_escape_ckbtn = g.CheckButton('关掉string转义')

    _row12.pack_start(self._inject_area_no_escape_ckbtn, True, True, 5)

    _row13 = g.Box()
    _row13.set_tooltip_text('--prefix=PREFIX\tInjection payload prefix string')

    self._inject_area_prefix_ckbtn = g.CheckButton('payload前缀')
    self._inject_area_prefix_entry = g.Entry()
    self._inject_area_prefix_entry.set_text('用于闭合')

    _row13.pack_start(self._inject_area_prefix_ckbtn, True, True, 5)
    _row13.pack_end(self._inject_area_prefix_entry, True, True, 5)

    _row14 = g.Box()
    _row14.set_tooltip_text('--suffix=SUFFIX\tInjection payload suffix string')

    self._inject_area_suffix_ckbtn = g.CheckButton('payload后缀')
    self._inject_area_suffix_entry = g.Entry()

    _row14.pack_start(self._inject_area_suffix_ckbtn, True, True, 5)
    _row14.pack_end(self._inject_area_suffix_entry, True, True, 5)

    _inject_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)
    # 添加行: _row1 - _row14
    for i in range(1, 15):
      _inject_area_opts.add(locals()[''.join(('_row', str(i)))])
    self._inject_area.add(_inject_area_opts)

  def _build_page1_request(self):
    _page1_request = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()
    self._request_area_method_ckbtn = g.CheckButton('指定HTTP请求方式')
    self._request_area_method_entry = g.Entry()

    self._request_area_random_agent_ckbtn = g.CheckButton('随机User-Agent头')
    self._request_area_random_agent_ckbtn.set_active(True)

    self._request_area_user_agent_ckbtn = g.CheckButton('指定User-Agent头')
    self._request_area_user_agent_entry = g.Entry()

    _row1.pack_start(self._request_area_method_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_method_entry, False, True, 5)
    _row1.pack_start(self._request_area_random_agent_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_user_agent_ckbtn, False, True, 5)
    _row1.pack_start(self._request_area_user_agent_entry, True, True, 5)

    _row2 = g.Box()
    self._request_area_post_ckbtn = g.CheckButton('通过POST请求要提交的data:')
    self._request_area_post_entry = g.Entry()
    self._request_area_post_entry.set_tooltip_text('--data=(填数据, 不是填文件路径哈)')
    self._request_area_param_del_ckbtn = g.CheckButton('指定参数分隔符')
    self._request_area_param_del_entry = g.Entry()

    _row2.pack_start(self._request_area_post_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_post_entry, True, True, 5)
    _row2.pack_start(self._request_area_param_del_ckbtn, False, True, 5)
    _row2.pack_start(self._request_area_param_del_entry, False, True, 5)

    _row3 = g.Box()
    self._request_area_cookie_ckbtn = g.CheckButton('设置请求中要包含的Cookie值:')
    self._request_area_cookie_entry = g.Entry()
    self._request_area_cookie_entry.set_tooltip_text('--cookie=填数据, 不是填文件名哈(另外, 请求选项太多了, 没时间写, #TODO)')
    self._request_area_cookie_del_ckbtn = g.CheckButton('指定cookie分隔符')
    self._request_area_cookie_del_entry = g.Entry()

    _row3.pack_start(self._request_area_cookie_ckbtn, False, True, 5)
    _row3.pack_start(self._request_area_cookie_entry, True, True, 5)
    _row3.pack_start(self._request_area_cookie_del_ckbtn, False, True, 5)
    _row3.pack_start(self._request_area_cookie_del_entry, False, True, 5)

    _row4 = g.Box()
    self._request_area_load_cookie_ckbtn = g.CheckButton('本地Cookie文件')
    self._request_area_load_cookie_entry = g.Entry()
    self._request_area_drop_set_cookie_ckbtn = g.CheckButton('丢弃Set-Cookie头')

    _row4.pack_start(self._request_area_load_cookie_ckbtn, False, True, 5)
    _row4.pack_start(self._request_area_load_cookie_entry, True, True, 5)
    _row4.pack_start(self._request_area_drop_set_cookie_ckbtn, True, True, 5)

    _row5 = g.Box()
    self._request_area_host_ckbtn = g.CheckButton('Host头')
    self._request_area_host_entry = g.Entry()
    self._request_area_referer_ckbtn = g.CheckButton('referer头')
    self._request_area_referer_entry = g.Entry()

    _row5.pack_start(self._request_area_host_ckbtn, False, True, 5)
    _row5.pack_start(self._request_area_host_entry, True, True, 5)
    _row5.pack_start(self._request_area_referer_ckbtn, False, True, 5)
    _row5.pack_start(self._request_area_referer_entry, True, True, 5)

    _row6 = g.Box()
    self._request_area_header_ckbtn = g.CheckButton('额外的header(-H)')
    self._request_area_header_entry = g.Entry()
    self._request_area_header_entry.set_text('X-Forwarded-For: 127.0.0.1')
    self._request_area_headers_ckbtn = g.CheckButton('额外的headers')
    self._request_area_headers_entry = g.Entry()
    self._request_area_headers_entry.set_text('Accept-Language: fr\\nETag: 123')

    _row6.pack_start(self._request_area_header_ckbtn, False, True, 5)
    _row6.pack_start(self._request_area_header_entry, True, True, 5)
    _row6.pack_start(self._request_area_headers_ckbtn, False, True, 5)
    _row6.pack_start(self._request_area_headers_entry, True, True, 5)

    _row7 = g.Box()
    self._request_area_auth_type_ckbtn = g.CheckButton('http认证类型')
    self._request_area_auth_type_entry = g.Entry()
    self._request_area_auth_cred_ckbtn = g.CheckButton('http认证密码')
    self._request_area_auth_cred_entry = g.Entry()
    self._request_area_auth_file_ckbtn = g.CheckButton('http认证文件')
    self._request_area_auth_file_entry = g.Entry()

    _row7.pack_start(self._request_area_auth_type_ckbtn, False, True, 5)
    _row7.pack_start(self._request_area_auth_type_entry, True, True, 5)
    _row7.pack_start(self._request_area_auth_cred_ckbtn, False, True, 5)
    _row7.pack_start(self._request_area_auth_cred_entry, True, True, 5)
    _row7.pack_start(self._request_area_auth_file_ckbtn, False, True, 5)
    _row7.pack_start(self._request_area_auth_file_entry, True, True, 5)

    _row8 = g.Box()
    self._request_area_ignore_redirects_ckbtn = g.CheckButton('忽略重定向')
    self._request_area_ignore_timeouts_ckbtn = g.CheckButton('忽略连接超时')
    self._request_area_ignore_code_ckbtn = g.CheckButton('忽略状态码:')
    self._request_area_ignore_code_entry = g.Entry()
    self._request_area_skip_urlencode_ckbtn = g.CheckButton('payload不使用url编码')
    self._request_area_force_ssl_ckbtn = g.CheckButton('强制使用HTTPS')
    self._request_area_hpp_ckbtn = g.CheckButton('使用HTTP参数污染')

    _row8.pack_start(self._request_area_ignore_redirects_ckbtn, False, True, 5)
    _row8.pack_start(self._request_area_ignore_timeouts_ckbtn, False, True, 5)
    _row8.pack_start(self._request_area_ignore_code_ckbtn, False, True, 5)
    _row8.pack_start(self._request_area_ignore_code_entry, False, True, 5)
    _row8.pack_start(self._request_area_skip_urlencode_ckbtn, False, True, 5)
    _row8.pack_start(self._request_area_force_ssl_ckbtn, False, True, 5)
    _row8.pack_start(self._request_area_hpp_ckbtn, False, True, 5)

    _row9 = g.Box()
    self._request_area_ignore_proxy_ckbtn = g.CheckButton('忽略系统默认代理')
    self._request_area_proxy_ckbtn = g.CheckButton('指定一个代理')
    self._request_area_proxy_cred_ckbtn = g.CheckButton('代理认证(name:passwd)')
    self._request_area_proxy_cred_entry = g.Entry()
    self._request_area_proxy_file_ckbtn = g.CheckButton('代理列表文件')
    self._request_area_proxy_file_entry = g.Entry()

    _row9.pack_start(self._request_area_ignore_proxy_ckbtn, False, True, 5)
    _row9.pack_start(self._request_area_proxy_ckbtn, False, True, 5)
    _row9.pack_start(self._request_area_proxy_cred_ckbtn, False, True, 5)
    _row9.pack_start(self._request_area_proxy_cred_entry, False, True, 5)
    _row9.pack_start(self._request_area_proxy_file_ckbtn, False, True, 5)
    _row9.pack_start(self._request_area_proxy_file_entry, True, True, 5)

    _row10 = g.Box()
    self._request_area_delay_ckbtn = g.CheckButton('请求间隔(秒)')
    self._request_area_delay_ckbtn.set_tooltip_text('隔几秒发送一个HTTP请求')
    self._request_area_delay_entry = g.Entry()
    self._request_area_timeout_ckbtn = g.CheckButton('超时几秒')
    self._request_area_timeout_entry = g.Entry()
    self._request_area_timeout_entry.set_text('30')
    self._request_area_retries_ckbtn = g.CheckButton('重试几次')
    self._request_area_retries_ckbtn.set_tooltip_text('连接超时后的重连次数')
    self._request_area_retries_entry = g.Entry()
    self._request_area_retries_entry.set_text('3')
    self._request_area_randomize_ckbtn = g.CheckButton('指定要随机改变值的参数')
    self._request_area_randomize_entry = g.Entry()

    _row10.pack_start(self._request_area_delay_ckbtn, False, True, 5)
    _row10.pack_start(self._request_area_delay_entry, False, True, 5)
    _row10.pack_start(self._request_area_timeout_ckbtn, False, True, 5)
    _row10.pack_start(self._request_area_timeout_entry, False, True, 5)
    _row10.pack_start(self._request_area_retries_ckbtn, False, True, 5)
    _row10.pack_start(self._request_area_retries_entry, False, True, 5)
    _row10.pack_start(self._request_area_randomize_ckbtn, False, True, 5)
    _row10.pack_start(self._request_area_randomize_entry, False, True, 5)

    _row11 = g.Box()
    self._request_area_safe_url_ckbtn = g.CheckButton('顺便掺杂地访问一个安全url')
    self._request_area_safe_url_entry = g.Entry()
    self._request_area_safe_post_ckbtn = g.CheckButton('提交到安全url的post数据')
    self._request_area_safe_post_entry = g.Entry()

    _row11.pack_start(self._request_area_safe_url_ckbtn, False, True, 5)
    _row11.pack_start(self._request_area_safe_url_entry, True, True, 5)
    _row11.pack_start(self._request_area_safe_post_ckbtn, False, True, 5)
    _row11.pack_start(self._request_area_safe_post_entry, True, True, 5)

    _row12 = g.Box()
    self._request_area_safe_req_ckbtn = g.CheckButton('从文件载入safe HTTP请求')
    self._request_area_safe_req_entry = g.Entry()
    self._request_area_safe_freq_ckbtn = g.CheckButton('安全url的访问频率')
    self._request_area_safe_freq_entry = g.Entry()

    _row12.pack_start(self._request_area_safe_req_ckbtn, False, True, 5)
    _row12.pack_start(self._request_area_safe_req_entry, True, True, 5)
    _row12.pack_start(self._request_area_safe_freq_ckbtn, False, True, 5)
    _row12.pack_start(self._request_area_safe_freq_entry, False, True, 5)

    _row13 = g.Box()
    self._request_area_csrf_token_ckbtn = g.CheckButton('csrf_token')
    self._request_area_csrf_token_entry = g.Entry()
    self._request_area_csrf_url_ckbtn = g.CheckButton('获取csrf_token的url')
    self._request_area_csrf_url_entry = g.Entry()

    _row13.pack_start(self._request_area_csrf_token_ckbtn, False, True, 5)
    _row13.pack_start(self._request_area_csrf_token_entry, True, True, 5)
    _row13.pack_start(self._request_area_csrf_url_ckbtn, False, True, 5)
    _row13.pack_start(self._request_area_csrf_url_entry, True, True, 5)

    _row14 = g.Box()
    self._request_area_eval_ckbtn = g.CheckButton('--eval=')
    self._request_area_eval_entry = g.Entry()
    self._request_area_eval_entry.set_tooltip_text('发送请求前先进行额外的处理(python code)')

    _row14.pack_start(self._request_area_eval_ckbtn, False, True, 5)
    _row14.pack_start(self._request_area_eval_entry, True, True, 5)

    _row15 = g.Box()
    self._request_area_tor_ckbtn = g.CheckButton('使用Tor匿名网络')
    self._request_area_tor_port_ckbtn = g.CheckButton('Tor端口')
    self._request_area_tor_port_entry = g.Entry()
    self._request_area_tor_type_ckbtn = g.CheckButton('Tor代理类型')
    self._request_area_tor_type_entry = g.Entry()
    self._request_area_check_tor_ckbtn = g.CheckButton('检查Tor连接')

    _row15.pack_start(self._request_area_tor_ckbtn, False, True, 5)
    _row15.pack_start(self._request_area_tor_port_ckbtn, False, True, 5)
    _row15.pack_start(self._request_area_tor_port_entry, False, True, 5)
    _row15.pack_start(self._request_area_tor_type_ckbtn, False, True, 5)
    _row15.pack_start(self._request_area_tor_type_entry, False, True, 5)
    _row15.pack_start(self._request_area_check_tor_ckbtn, False, True, 5)

    _page1_request.pack_start(_row1, False, True, 5)
    _page1_request.pack_start(_row2, False, True, 5)
    _page1_request.pack_start(_row3, False, True, 5)
    _page1_request.pack_start(_row4, False, True, 5)
    _page1_request.pack_start(_row5, False, True, 5)
    _page1_request.pack_start(_row6, False, True, 5)
    _page1_request.pack_start(_row7, False, True, 5)
    _page1_request.pack_start(_row8, False, True, 5)
    _page1_request.pack_start(_row9, False, True, 5)
    _page1_request.pack_start(_row10, False, True, 5)
    _page1_request.pack_start(_row11, False, True, 5)
    _page1_request.pack_start(_row12, False, True, 5)
    _page1_request.pack_start(_row13, False, True, 5)
    _page1_request.pack_start(_row14, False, True, 5)
    _page1_request.pack_start(_row15, False, True, 5)

    self.page1_request = g.ScrolledWindow()
    self.page1_request.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    self.page1_request.add(_page1_request)

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
    _row1.set_tooltip_text('--sql-query=QUERY')

    self._runsql_area_sql_query_ckbtn = g.CheckButton('SQL语句:')
    self._runsql_area_sql_query_entry = g.Entry()
    _row1.pack_start(self._runsql_area_sql_query_ckbtn, False, True, 10)
    _row1.pack_start(self._runsql_area_sql_query_entry, True, True, 10)

    _runsql_area_opts.pack_start(_row1, False, True, 5)

    _row2 = g.Box()
    _row2.set_tooltip_text('--sql-file=SQLFILE')

    self._runsql_area_sql_file_ckbtn = g.CheckButton('本地SQL文件:')
    self._runsql_area_sql_file_entry = g.Entry()
    _row2.pack_start(self._runsql_area_sql_file_ckbtn, False, True, 10)
    _row2.pack_start(self._runsql_area_sql_file_entry, True, True, 10)

    _runsql_area_opts.pack_start(_row2, False, True, 5)

    self._runsql_area.add(_runsql_area_opts)

  def _build_page1_enumeration_meta(self):
    self._meta_area = g.Frame.new('数据库名, 表名, 列名...')

    _meta_area_opts = g.Box(orientation=g.Orientation.VERTICAL)

    _row1 = g.Box()

    _col1 = g.Box()

    self._meta_area_D_ckbtn = g.CheckButton('指定库名')
    self._meta_area_D_entry = g.Entry()
    self._meta_area_D_ckbtn.set_tooltip_text('-D DB')

    _col1.pack_start(self._meta_area_D_ckbtn, False, True, 10)
    _col1.pack_start(self._meta_area_D_entry, True, True, 10)

    _row1.pack_start(_col1, False, True, 5)

    _col2 = g.Box()

    self._meta_area_T_ckbtn = g.CheckButton('指定表名')
    self._meta_area_T_entry = g.Entry()
    self._meta_area_T_ckbtn.set_tooltip_text('-T TBL')

    _col2.pack_start(self._meta_area_T_ckbtn, False, True, 10)
    _col2.pack_start(self._meta_area_T_entry, True, True, 10)

    _row1.pack_start(_col2, False, True, 5)

    _col3 = g.Box()

    self._meta_area_C_ckbtn = g.CheckButton('指定列名')
    self._meta_area_C_entry = g.Entry()
    self._meta_area_C_ckbtn.set_tooltip_text('-C COL')

    _col3.pack_start(self._meta_area_C_ckbtn, False, True, 10)
    _col3.pack_start(self._meta_area_C_entry, True, True, 10)

    _row1.pack_start(_col3, False, True, 5)

    _col4 = g.Box()

    self._meta_area_U_ckbtn = g.CheckButton('指定用户')
    self._meta_area_U_entry = g.Entry()
    self._meta_area_U_ckbtn.set_tooltip_text('-U USER')

    _col4.pack_start(self._meta_area_U_ckbtn, False, True, 10)
    _col4.pack_start(self._meta_area_U_entry, True, True, 10)

    _row1.pack_start(_col4, False, True, 5)

    _row2 = g.Box()
    _col1 = g.Box()

    self._meta_area_X_ckbtn = g.CheckButton('排除标志符')
    self._meta_area_X_entry = g.Entry()
    self._meta_area_X_ckbtn.set_tooltip_text('-X EXCLUDE')

    _col1.pack_start(self._meta_area_X_ckbtn, False, True, 10)
    _col1.pack_start(self._meta_area_X_entry, True, True, 10)

    _row2.pack_start(_col1, False, True, 5)

    _col2 = g.Box()

    self._meta_area_pivot_ckbtn = g.CheckButton('指定Pivot列名')
    self._meta_area_pivot_entry = g.Entry()
    self._meta_area_pivot_ckbtn.set_tooltip_text('--pivot-column=P..')

    _col2.pack_start(self._meta_area_pivot_ckbtn, False, True, 10)
    _col2.pack_start(self._meta_area_pivot_entry, True, True, 10)

    _row2.pack_start(_col2, False, True, 5)

    _row3 = g.Box()
    _row3.set_tooltip_text('--where=')

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

    _limit_area_opts_row1 = g.Box()
    _limit_area_opts_row1.set_tooltip_text('--start=')

    self._limit_area_start_ckbtn = g.CheckButton('始于第')
    self._limit_area_start_entry = g.Entry()

    _limit_area_opts_row1.pack_start(self._limit_area_start_ckbtn, False, True, 5)
    _limit_area_opts_row1.pack_start(self._limit_area_start_entry, False, True, 0)
    _limit_area_opts_row1.pack_start(g.Label('条'), False, True, 5)

    _limit_area_opts_row2 = g.Box()
    _limit_area_opts_row2.set_tooltip_text('--stop=')

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

    _blind_area_opts_row1 = g.Box()
    _blind_area_opts_row1.set_tooltip_text('--first=')

    self._blind_area_first_ckbtn = g.CheckButton('首字符')
    self._blind_area_first_entry = g.Entry()

    _blind_area_opts_row1.pack_start(self._blind_area_first_ckbtn, False, True, 5)
    _blind_area_opts_row1.pack_start(self._blind_area_first_entry, False, True, 10)

    _blind_area_opts.pack_start(_blind_area_opts_row1, False, True, 10)

    _blind_area_opts_row2 = g.Box()
    _blind_area_opts_row2.set_tooltip_text('--last=')

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
    self._dump_area_dump_ckbtn.set_tooltip_text('--dump')
    self._dump_area_dump_all_ckbtn = g.CheckButton('全部dump(拖库)')
    self._dump_area_dump_all_ckbtn.set_tooltip_text('--dump-all')
    self._dump_area_search_ckbtn = g.CheckButton('搜索')
    self._dump_area_search_ckbtn.set_tooltip_text('--search')
    self._dump_area_no_sys_db_ckbtn = g.CheckButton('排除系统库')
    self._dump_area_no_sys_db_ckbtn.set_tooltip_text('--exclude-sysdb')

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

    _row1 = g.Box(orientation=g.Orientation.HORIZONTAL)
    _row1.props.margin = 10

    self._build_page1_file_read()

    _row1.pack_start(self._file_read_area, True, True, 10)

    self.page1_file.add(_row1)

    _row2 = g.Box(orientation=g.Orientation.HORIZONTAL)
    _row2.props.margin = 10

    self._build_page1_file_write()

    _row2.pack_start(self._file_write_area, True, True, 10)

    self.page1_file.add(_row2)

  def _build_page1_file_write(self):
    self._file_write_area = g.Frame.new('文件上传')

    _file_write_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _row1 = g.Box()

    self._file_write_area_udf_ckbtn = g.CheckButton('注入(默认sqlmap自带的)用户定义函数')
    self._file_write_area_udf_ckbtn.set_tooltip_text('--udf-inject')

    _row1.pack_start(self._file_write_area_udf_ckbtn, False, True, 5)

    self._file_write_area_shared_lib_ckbtn = g.CheckButton('本地共享库路径(--shared-lib=)')
    self._file_write_area_shared_lib_ckbtn.set_tooltip_text('与--udf-inject配套使用, 可选')
    self._file_write_area_shared_lib_entry = g.Entry()

    _row1.pack_start(self._file_write_area_shared_lib_ckbtn, False, True, 5)
    _row1.pack_start(self._file_write_area_shared_lib_entry, True, True, 5)

    _file_write_area_opts.pack_start(_row1, False, True, 5)

    _row2 = g.Box()
    _row2.set_tooltip_text('若使用此选项, 则--file-dest为必选项')

    self._file_write_area_file_write_ckbtn = g.CheckButton('本地文件路径(--file-write=)')
    self._file_write_area_file_write_entry = g.Entry()

    _row2.pack_start(self._file_write_area_file_write_ckbtn, False, True, 5)
    _row2.pack_start(self._file_write_area_file_write_entry, True, True, 5)

    _file_write_area_opts.pack_start(_row2, False, True, 5)

    _row3 = g.Box()
    _row3.set_tooltip_text(
      '上传到DB服务器中的文件名, 要求是绝对路径, 构造后会有引号!\n'
      '与本地文件路径配套使用, 单独勾选无意义')

    self._file_write_area_file_dest_ckbtn = g.CheckButton('远程文件路径(--file-dest=)')
    self._file_write_area_file_dest_entry = g.Entry()

    _row3.pack_start(self._file_write_area_file_dest_ckbtn, False, True, 5)
    _row3.pack_start(self._file_write_area_file_dest_entry, True, True, 5)

    _file_write_area_opts.pack_start(_row3, False, True, 5)

    self._file_write_area.add(_file_write_area_opts)

  def _build_page1_file_read(self):
    self._file_read_area = g.Frame.new('读取远程文件')

    _file_read_area_opts = g.Box(orientation=g.Orientation.VERTICAL, spacing=6)

    _file_read_area_opts_row1 = g.Box()
    _file_read_area_opts_row1.set_tooltip_text('远程DB所在服务器上的文件路径')

    self._file_read_area_file_read_ckbtn = g.CheckButton('远程文件路径(--file-read=)')
    self._file_read_area_file_read_entry = g.Entry()
    self._file_read_area_file_read_entry.set_text('/etc/passwd')
    self._file_read_area_file_btn = g.Button('查看')
    self._file_read_area_file_btn.set_tooltip_text('只能查看已下载到本地的文件')
    self._file_read_area_file_btn.connect('clicked', self._handlers.read_dumped_file)

    _file_read_area_opts_row1.pack_start(self._file_read_area_file_read_ckbtn, False, True, 10)
    _file_read_area_opts_row1.pack_start(self._file_read_area_file_read_entry, True, True, 10)
    _file_read_area_opts_row1.pack_start(self._file_read_area_file_btn, False, True, 10)

    _file_read_area_opts.pack_start(_file_read_area_opts_row1, False, True, 5)

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

    self.page2.pack_start(_row1, True, True, 5)

    _row2 = g.Box()

    self._page3_read_target_btn = g.Button('查看target文件')
    self._page3_read_target_btn.connect('clicked', self._handlers.read_target_file)

    _row2.pack_start(self._page3_read_target_btn, True, False, 0)

    self._page3_clear_btn = g.Button.new_with_mnemonic('清空(_C)')
    self._page3_clear_btn.set_tooltip_text('不会动实际的文件')
    self._page3_clear_btn.connect('clicked', self._handlers.clear_buffer)

    _row2.pack_start(self._page3_clear_btn, True, False, 0)

    self._page3_read_log_btn = g.Button('查看log文件')
    self._page3_read_log_btn.connect('clicked', self._handlers.read_log_file)

    _row2.pack_start(self._page3_read_log_btn, True, False, 0)

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
    1. VERSION: 0.1
       2018年 09月 03日 星期一 03:34:31 CST
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
