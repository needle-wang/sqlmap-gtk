#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 08月 29日 星期三 15:34:10 CST

import ast
import time
from os import environ, name as OS_NAME
# python3.5+
from pathlib import Path
from subprocess import Popen
from urllib.parse import urlparse
import requests

from gtk3_header import g, GLib, Vte
# from basis_and_too.logging_needle import get_console_logger
# logger = get_console_logger()

IS_POSIX = True if OS_NAME == 'posix' else False
QUOTE = "'%s'" if OS_NAME == 'posix' else '"%s"'  # dos下只能用双引号


class Singal_Handlers(object):
  def __init__(self, w, m):
    '''
    w: sqlmap_ui.UI_Window
    m: model.Model
    还不能用注解, 会相互import
    '''
    self.w = w
    self.m = m
    self.shell = environ["SHELL"]

  def build_all(self, button):
    _target = self._get_target()

    self._collect_opts()
    _opts_list = (
      self._setting_opts + self._request_opts +
      self._enumeration_opts + self._file_opts + self._other_opts
    )

    _final_line = _target + ''.join(_opts_list)

    if _final_line is not None:
      self.m._cmd_entry.set_text(_final_line.strip())

  def api_task_new(self, button):
    '''
    rest api获取自: https://github.com/PyxYuYu/MyBlog/issues/69
    @get("/task/new") 创建新任务
    '''
    _host = self.m._page4_api_server_entry.get_text()
    if _host:
      try:
        _resp = requests.get('http://%s/task/new' % _host)
        _resp = _resp.json()
        if _resp['success']:
          self._task_view_append('%s: 创建成功.' % _resp['taskid'])
      except Exception as e:
        self._task_view_append(e)

  def api_admin_list(self, button):
    '''
    @get("/admin/<taskid>/list") 查看所有任务，并显示运行状态
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _token = self.m._page4_admin_token_entry.get_text()
    if _host and _token:
      try:
        _resp = requests.get('http://%s/admin/%s/list' % (_host, _token))
        _resp = _resp.json()
        # print(_resp)
        if _resp['success']:
          # self._task_view_append('总任务数: %s' % _resp['tasks_num'])
          # 清空之前的任务列表
          for _a_child in self.w._api_admin_list_rows.get_children():
            # self.w._api_admin_list_rows.remove(_a_child)
            _a_child.destroy()
          # 填充任务列表
          _id = 0
          for _taskid, _status in _resp['tasks'].items():
            _a_task_row = g.ListBoxRow()
            _a_row_box_tmp = g.Box()
            _a_task_row.add(_a_row_box_tmp)

            _task_del_btn = g.Button.new_with_label('删除')
            _task_del_btn.connect('clicked', self.api_task_delete, _a_task_row, _taskid)
            _scan_kill_btn = g.Button.new_with_label('杀死')
            _scan_kill_btn.connect('clicked', self.api_scan_kill, _taskid)
            _scan_stop_btn = g.Button.new_with_label('停止')
            _scan_stop_btn.connect('clicked', self.api_scan_stop, _taskid)
            _scan_start_btn = g.Button.new_with_label('启动')
            _scan_start_btn.connect('clicked', self.api_scan_start, _taskid)
            _scan_data_btn = g.Button.new_with_label('data')
            _scan_data_btn.connect('clicked', self.api_scan_data, _taskid)
            _scan_log_btn = g.Button.new_with_label('log')
            _scan_log_btn.connect('clicked', self.api_scan_log, _taskid)
            _option_list_btn = g.Button.new_with_label('所有选项')
            _option_list_btn.connect('clicked', self.api_option_list, _taskid)
            _option_get_btn = g.Button.new_with_label('选项:')
            _option_get_btn.connect('clicked', self.api_option_get, _taskid)
            _option_set_btn = g.Button.new_with_label('设置:')
            _option_set_btn.connect('clicked', self.api_option_set, _taskid)

            _id += 1
            _a_row_box_tmp.pack_start(g.Label.new('%s. %s' % (_id, _taskid)), False, True, 5)
            _a_row_box_tmp.pack_start(g.Label.new('(%s)' % _status), False, True, 0)
            _a_row_box_tmp.pack_start(_task_del_btn, False, True, 1)
            _a_row_box_tmp.pack_start(_scan_kill_btn, False, True, 1)
            _a_row_box_tmp.pack_start(_scan_stop_btn, False, True, 1)
            _a_row_box_tmp.pack_start(_scan_start_btn, False, True, 1)
            _a_row_box_tmp.pack_start(g.Label.new('查看:('), False, True, 1)
            _a_row_box_tmp.pack_start(_scan_data_btn, False, True, 1)
            _a_row_box_tmp.pack_start(_scan_log_btn, False, True, 1)
            _a_row_box_tmp.pack_start(_option_list_btn, False, True, 1)
            _a_row_box_tmp.pack_start(_option_get_btn, False, True, 1)
            _a_row_box_tmp.pack_start(g.Label.new(')'), False, True, 1)
            _a_row_box_tmp.pack_start(_option_set_btn, False, True, 1)

            self.w._api_admin_list_rows.add(_a_task_row)

          self.w._api_admin_list_rows.show_all()
      except Exception as e:
        self._task_view_append(e)

  def api_option_list(self, button, taskid):
    '''
    @get("/option/<taskid>/list") 获取指定任务的options
    '''
    _host = self.m._page4_api_server_entry.get_text()
    if _host:
      try:
        _resp = requests.get('http://%s/option/%s/list' % (_host, taskid))
        _resp = _resp.json()
        if _resp['success']:
          for _key, _value in _resp['options'].items():
            if _value:
              self._task_view_append('%s: %s' % (_key, _value))
      except Exception as e:
        self._task_view_append(e)

  def api_option_get(self, button, taskid):
    '''
    @post("/option/<taskid>/get") 获取指定任务的option(s)
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _buffer_text = self.m._page4_option_get_entry.get_text()
    _options = {}
    for _tmp in _buffer_text.split():
      _options[_tmp] = None
    if _host and _options:
      _mesg = '%s:\n' % taskid
      try:
        _headers = {'Content-Type': 'application/json'}
        _resp = requests.post('http://%s/option/%s/get' % (_host, taskid),
                              json = _options,
                              headers = _headers)
        _resp = _resp.json()
        if _resp['success']:
          if _resp['options'].items():
            for _key, _value in _resp['options'].items():
              _mesg += '%s: %s, ' % (_key, _value)
          else:
            _mesg += 'None'
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)
      self._task_view_append(_mesg.strip())

  def api_option_set(self, button, taskid):
    '''
    @post("/option/<taskid>/set") 设置指定任务的option(s)
    Warning: any option can be set, even a invalid option which
             is unable to remove, except deleting the task.
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _buffer_text = self._get_buffer_text(self.m._page4_option_set_view)
    try:
      _json = ast.literal_eval(_buffer_text)
    except Exception as e:
      _json = str(e)

    _mesg = '%s: ' % taskid
    if _json and isinstance(_json, dict):
      if _host:
        try:
          _headers = {'Content-Type': 'application/json'}
          _resp = requests.post('http://%s/option/%s/set' % (_host, taskid),
                                json = _json,
                                headers = _headers)
          _resp = _resp.json()
          if _resp['success']:
            _mesg += '设置成功'
        except Exception as e:
          _mesg += str(e)
    else:
      _mesg += '需要一个有效的python dict'

    self._task_view_append(_mesg)

  def api_admin_flush(self, button):
    '''
    @get("/admin/<taskid>/flush") 删除所有任务
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _token = self.m._page4_admin_token_entry.get_text()
    if _host and _token:
      try:
        _resp = requests.get('http://%s/admin/%s/flush' % (_host, _token))
        _resp = _resp.json()
        if _resp['success']:
          for _a_child in self.w._api_admin_list_rows.get_children():
            self.w._api_admin_list_rows.remove(_a_child)
          self._task_view_append('清空全部任务: 成功')
      except Exception as e:
        self._task_view_append(e)

  def api_task_delete(self, button, *data):
    '''
    @get("/task/<taskid>/delete") 删除指定任务
    '''
    _host = self.m._page4_api_server_entry.get_text()
    if _host:
      try:
        _resp = requests.get('http://%s/task/%s/delete' % (_host, data[1]))
        _resp = _resp.json()
        if _resp['success']:
          self.w._api_admin_list_rows.remove(data[0])
          self._task_view_append('%s: 删除成功' % data[1])
      except Exception as e:
        self._task_view_append(e)

  def api_scan_start(self, button, taskid):
    '''
    @post("/scan/<taskid>/start") 指定任务 开始扫描
    要求发送json, 会执行/option/<taskid>/set
    '''
    _host = self.m._page4_api_server_entry.get_text()
    if _host:
      _mesg = '%s: ' % taskid
      try:
        _headers = {'Content-Type': 'application/json'}
        _resp = requests.post('http://%s/scan/%s/start' % (_host, taskid),
                              json = {},
                              headers = _headers)
        _resp = _resp.json()
        if _resp['success']:
          _mesg = '%sengineid: %s' % (_mesg, _resp['engineid'])
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)

      self._task_view_append(_mesg)

  def api_scan_stop(self, button, taskid):
    '''
    @get("/scan/<taskid>/stop") 指定任务 停止扫描
    '''
    _host = self.m._page4_api_server_entry.get_text()
    if _host:
      _mesg = '%s: ' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/stop' % (_host, taskid))
        _resp = _resp.json()
        if _resp['success']:
          _mesg += 'ok, stoped.'
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)
      self._task_view_append(_mesg)

  def api_scan_kill(self, button, taskid):
    '''
    @get("/scan/<taskid>/kill") kill -9 指定任务
    '''
    _host = self.m._page4_api_server_entry.get_text()
    if _host:
      _mesg = '%s: ' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/kill' % (_host, taskid))
        _resp = _resp.json()
        if _resp['success']:
          _mesg += 'ok, killed.'
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)
      self._task_view_append(_mesg)

  def api_scan_data(self, button, taskid):
    '''
    @get("/scan/<taskid>/data") 查看指定任务的扫描数据,
                                data若有内容说明存在注入
    '''
    _host = self.m._page4_api_server_entry.get_text()
    if _host:
      _mesg = '%s:\n' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/data' % (_host, taskid))
        _resp = _resp.json()
        # print(_resp)    # _resp['data'], _resp['error'] are list
        if _resp['success']:
          del[_resp['success']]
          _mesg = '%s%s' % (_mesg, _resp)
      except Exception as e:
        _mesg += str(e)
      self._task_view_append(_mesg)

  def api_scan_log(self, button, taskid):
    '''
    @get("/scan/<taskid>/log") 查看指定任务的扫描日志
    '''
    _host = self.m._page4_api_server_entry.get_text()
    if _host:
      _mesg = '%s:\n' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/log' % (_host, taskid))
        _resp = _resp.json()
        if _resp['success']:
          _logs = ''
          for _tmp in _resp['log']:
            _log = '%s %s: %s\n' % (_tmp['time'], _tmp['level'], _tmp['message'])
            _logs = ''.join((_logs, _log))
          if _logs:
            _mesg += _logs.strip()
          else:
            _mesg += "没有log."
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)
      self._task_view_append(_mesg)

  def _get_buffer_text(self, textview):
    _buffer = textview.get_buffer()
    _start = _buffer.get_start_iter()
    _end = _buffer.get_end_iter()
    return _buffer.get_text(_start, _end, False).strip()

  def _task_view_append(self, output):
    _task_view_textbuffer = self.m._page4_task_view.get_buffer()

    _mark = _task_view_textbuffer.get_mark('end')
    _end = _task_view_textbuffer.get_iter_at_mark(_mark)

    _task_view_textbuffer.insert(_end, '%s\n' % output)

    # 获取焦点
    # self.w.set_focus(self.m._page4_task_view)
    self.m._page4_task_view.grab_focus()
    # https://stackoverflow.com/questions/48934458/gtk-sourceview-scroll-to-mark-not-working
    GLib.idle_add(self.m._page4_task_view.scroll_mark_onscreen, _mark)

  def run_cmdline(self, button):
    '''
    only for posix, won't code it for win now.
    '''
    _sqlmap_opts = self.m._cmd_entry.get_text().strip()
    if IS_POSIX:
      self.w.main_notebook.next_page()
      _cmdline_str = ''.join(('sqlmap ', _sqlmap_opts, '\n'))
      # print(_cmdline_str)
      if _cmdline_str:
        # self.m._page2_cmdline_str_label.set_text("running: " + _cmdline_str)
        self.m._page2_terminal.feed_child(_cmdline_str, len(_cmdline_str))
        self.m._page2_terminal.grab_focus()

  def respawn_terminal(self, button):
    '''
    不管pty是不是还活着, 都重新生成一个
    没有close方法, 无法删掉旧pty, 用top -Hp pid显示, 好像会残留线程
    '''
    _pty = Vte.Pty.new_sync(Vte.PtyFlags.DEFAULT)
    self.m._page2_terminal.set_pty(_pty)

    _pty.spawn_async(str(Path.home()),
                     [self.shell],
                     None,
                     GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                     None,
                     None,
                     -1,
                     None,
                     lambda pty, task: None)
    self.m._page2_terminal.grab_focus()

  def run_cmdline_old(self, button):
    '''
     -  -  -  - 废弃 -  -  -  -
    '''
    _sqlmap_opts = self.m._cmd_entry.get_text().strip()

    if _sqlmap_opts:
      if IS_POSIX:
        _cmdline_str = ''.join(('/usr/bin/env xterm -hold -e sqlmap ', _sqlmap_opts))
      else:
        # msys2
        _cmdline_str = ''.join(('start cmd /k sqlmap ', _sqlmap_opts))

      # print(_cmdline_str)
      Popen(_cmdline_str, shell = True)

  def clear_log_view_buffer(self, button):
    _log_view_textbuffer = self.w._log_view.get_buffer()
    _log_view_textbuffer.set_text(''.join(
      ('sqlmap的运行记录都放在这: ', str(Path.home() / '.sqlmap/output\n'))
    ))

  def clear_task_view_buffer(self, button):
    _task_view_textbuffer = self.m._page4_task_view.get_buffer()
    _task_view_textbuffer.set_text('')

  def optimize_area_controller(self, button):
    m = self.m
    if m._optimize_area_turn_all_ckbtn.get_active():
      m._optimize_area_predict_ckbtn.set_active(False)
      m._optimize_area_keep_alive_ckbtn.set_active(False)
      m._optimize_area_null_connect_ckbtn.set_active(False)

      m._optimize_area_predict_ckbtn.set_sensitive(False)
      m._optimize_area_keep_alive_ckbtn.set_sensitive(False)
      m._optimize_area_null_connect_ckbtn.set_sensitive(False)
    else:
      m._optimize_area_predict_ckbtn.set_sensitive(True)
      m._optimize_area_keep_alive_ckbtn.set_sensitive(True)
      m._optimize_area_null_connect_ckbtn.set_sensitive(True)

  def _get_url_dir(self):
    '''
    return: pathlib.Path
    '''
    _load_url = self.m._url_combobox.get_child().get_text()

    if _load_url:
      if not _load_url.startswith('http'):
        _load_url = 'http://' + _load_url

      _load_host = urlparse(_load_url).netloc

      return Path.home() / '.sqlmap/output' / _load_host

  def _log_view_insert(self, file_path):
    '''
    file_path: pathlib.Path
               sqlmap库中dataToOutFile默认utf8写入
    '''
    _log_view_textbuffer = self.w._log_view.get_buffer()

    _mark = _log_view_textbuffer.get_mark('end')
    _end = _log_view_textbuffer.get_iter_at_mark(_mark)

    try:
      with file_path.open(encoding = 'utf8') as _f:
        _line_list_tmp = _f.readlines()
        if _line_list_tmp:
          for _line_tmp in _line_list_tmp:
            _log_view_textbuffer.insert(_end, _line_tmp)
        else:
          _log_view_textbuffer.insert(_end, str(file_path) + ': 空文件')
    except EnvironmentError as e:
      _log_view_textbuffer.insert(_end, str(e))
    finally:
      _log_view_textbuffer.insert(
        _end,
        time.strftime('\n%Y-%m-%d %R:%S: ----------我是分割线----------\n',
                      time.localtime()))

    self.w._log_view.grab_focus()
    GLib.idle_add(self.w._log_view.scroll_mark_onscreen, _mark)

  def read_log_file(self, button):
    _base_dir = self._get_url_dir()

    if _base_dir:
      _log_file_path = _base_dir / 'log'
      self._log_view_insert(_log_file_path)

  def read_target_file(self, button):
    _base_dir = self._get_url_dir()

    if _base_dir:
      _target_file_path = _base_dir / 'target.txt'
      self._log_view_insert(_target_file_path)

  def read_dumped_file(self, button):
    self.w.main_notebook.next_page()
    self.w.main_notebook.next_page()

    _base_dir = self._get_url_dir()
    _load_file = self.m._file_read_area_file_read_entry.get_text()

    if _base_dir and _load_file:
      # 不能用os.sep, 因为是依据远程OS的sep而定
      # 沿用sqlmap库中的filePathToSafeString函数
      _load_file = (_load_file.replace("/", "_").replace("\\", "_")
                              .replace(" ", "_").replace(":", "_"))

      _dumped_file_path = _base_dir / 'files' / _load_file
      self._log_view_insert(_dumped_file_path)

  def _get_target(self):
    m = self.m
    _current_pagenum = self.w._target_notebook.get_current_page()
    _target_list = [("-u ", m._url_combobox.get_child().get_text),
                    ("-l ", m._burp_logfile.get_text),
                    ("-r ", m._request_file.get_text),
                    ("-m ", m._bulkfile.get_text),
                    ("-c ", m._configfile.get_text),
                    ("-x ", m._sitemap_url.get_text),
                    ("-g ", m._google_dork.get_text)]

    _target_tmp = _target_list[_current_pagenum][1]().strip()
    if _target_tmp:
      return _target_list[_current_pagenum][0] + QUOTE % _target_tmp
    else:
      return ''

  def _collect_opts(self):
    m = self.m

    self._other_opts = [
      self._get_text_only_ckbtn("--check-internet",
                                m._page1_general_check_internet_ckbtn),
      self._get_text_only_ckbtn("--fresh-queries",
                                m._page1_general_fresh_queries_ckbtn),
      self._get_text_only_ckbtn("--flush-session",
                                m._page1_general_flush_session_ckbtn),
      self._get_text_only_ckbtn("--eta",
                                m._page1_general_eta_ckbtn),
      self._get_text_from_entry("--binary-fields=",
                                m._page1_general_binary_fields_ckbtn,
                                m._page1_general_binary_fields_entry),
      self._get_text_only_ckbtn("--forms",
                                m._page1_general_forms_ckbtn),
      self._get_text_only_ckbtn("--parse-errors",
                                m._page1_general_parse_errors_ckbtn),
      self._get_text_only_ckbtn("--cleanup",
                                m._page1_misc_cleanup_ckbtn),
      self._get_text_from_entry("--preprocess=",
                                m._page1_general_preprocess_ckbtn,
                                m._page1_general_preprocess_entry),
      self._get_text_from_entry("--crawl=",
                                m._page1_general_crawl_ckbtn,
                                m._page1_general_crawl_entry),
      self._get_text_from_entry("--crawl-exclude=",
                                m._page1_general_crawl_exclude_ckbtn,
                                m._page1_general_crawl_exclude_entry),
      self._get_text_from_entry("--charset=",
                                m._page1_general_charset_ckbtn,
                                m._page1_general_charset_entry),
      self._get_text_from_entry("--encoding=",
                                m._page1_general_encoding_ckbtn,
                                m._page1_general_encoding_entry),
      self._get_text_from_entry("-s ",
                                m._page1_general_session_file_ckbtn,
                                m._page1_general_session_file_entry),
      self._get_text_from_entry("--output-dir=",
                                m._page1_general_output_dir_ckbtn,
                                m._page1_general_output_dir_entry),
      self._get_text_from_entry("--dump-format=",
                                m._page1_general_dump_format_ckbtn,
                                m._page1_general_dump_format_entry),
      self._get_text_from_entry("--csv-del=",
                                m._page1_general_csv_del_ckbtn,
                                m._page1_general_csv_del_entry),
      self._get_text_from_entry("-t ",
                                m._page1_general_traffic_file_ckbtn,
                                m._page1_general_traffic_file_entry),
      self._get_text_from_entry("--har=",
                                m._page1_general_har_ckbtn,
                                m._page1_general_har_entry),
      self._get_text_from_entry("--save=",
                                m._page1_general_save_ckbtn,
                                m._page1_general_save_entry),
      self._get_text_from_entry("--scope=",
                                m._page1_general_scope_ckbtn,
                                m._page1_general_scope_entry),
      self._get_text_from_entry("--test-filter=",
                                m._page1_general_test_filter_ckbtn,
                                m._page1_general_test_filter_entry),
      self._get_text_from_entry("--test-skip=",
                                m._page1_general_test_skip_ckbtn,
                                m._page1_general_test_skip_entry),
      self._get_text_from_entry("--web-root=",
                                m._page1_misc_web_root_ckbtn,
                                m._page1_misc_web_root_entry),
      self._get_text_from_entry("--tmp-dir=",
                                m._page1_misc_tmp_dir_ckbtn,
                                m._page1_misc_tmp_dir_entry),
      self._get_text_only_ckbtn("--identify-waf",
                                m._page1_misc_identify_waf_ckbtn),
      self._get_text_only_ckbtn("--skip-waf",
                                m._page1_misc_skip_waf_ckbtn),
      self._get_text_only_ckbtn("--smart",
                                m._page1_misc_smart_ckbtn),
      self._get_text_only_ckbtn("--list-tampers",
                                m._page1_misc_list_tampers_ckbtn),
      self._get_text_only_ckbtn("--sqlmap-shell",
                                m._page1_misc_sqlmap_shell_ckbtn),
      self._get_text_only_ckbtn("--disable-coloring",
                                m._page1_misc_disable_color_ckbtn),
      self._get_text_only_ckbtn("--offline",
                                m._page1_misc_offline_ckbtn),
      self._get_text_only_ckbtn("--mobile",
                                m._page1_misc_mobile_ckbtn),
      self._get_text_only_ckbtn("--beep",
                                m._page1_misc_beep_ckbtn),
      self._get_text_only_ckbtn("--purge",
                                m._page1_misc_purge_ckbtn),
      self._get_text_only_ckbtn("--dependencies",
                                m._page1_misc_dependencies_ckbtn),
      self._get_text_only_ckbtn("--update",
                                m._page1_general_update_ckbtn),
      self._get_text_from_entry("--answers=",
                                m._page1_misc_answers_ckbtn,
                                m._page1_misc_answers_entry),
      self._get_text_from_entry("--alert=",
                                m._page1_misc_alert_ckbtn,
                                m._page1_misc_alert_entry),
      self._get_text_from_entry("--gpage=",
                                m._page1_misc_gpage_ckbtn,
                                m._page1_misc_gpage_spinbtn, None),
      self._get_text_from_entry("-z ",
                                m._page1_misc_z_ckbtn,
                                m._page1_misc_z_entry),
    ]

    self._file_opts = [
      self._get_text_from_entry("--file-read=",
                                m._file_read_area_file_read_ckbtn,
                                m._file_read_area_file_read_entry),
      self._get_text_only_ckbtn("--udf-inject",
                                m._file_write_area_udf_ckbtn),
      self._get_text_from_entry("--shared-lib=",
                                m._file_write_area_shared_lib_ckbtn,
                                m._file_write_area_shared_lib_entry),
      self._get_text_from_entry("--file-write=",
                                m._file_write_area_file_write_ckbtn,
                                m._file_write_area_file_write_entry),
      self._get_text_from_entry("--file-dest=",
                                m._file_write_area_file_dest_ckbtn,
                                m._file_write_area_file_dest_entry),
      self._get_text_from_entry("--os-cmd=",
                                m._file_os_access_os_cmd_ckbtn,
                                m._file_os_access_os_cmd_entry),
      self._get_text_only_ckbtn("--os-shell",
                                m._file_os_access_os_shell_ckbtn),
      self._get_text_only_ckbtn("--os-pwn",
                                m._file_os_access_os_pwn_ckbtn),
      self._get_text_only_ckbtn("--os-smbrelay",
                                m._file_os_access_os_smbrelay_ckbtn),
      self._get_text_only_ckbtn("--os-bof",
                                m._file_os_access_os_bof_ckbtn),
      self._get_text_only_ckbtn("--priv-esc",
                                m._file_os_access_priv_esc_ckbtn),
      self._get_text_from_entry("--msf-path=",
                                m._file_os_access_msf_path_ckbtn,
                                m._file_os_access_msf_path_entry),
      self._get_text_from_entry("--tmp-path=",
                                m._file_os_access_tmp_path_ckbtn,
                                m._file_os_access_tmp_path_entry),
      self._get_text_only_ckbtn(m._file_os_registry_reg_combobox.get_active_id(),
                                m._file_os_registry_reg_ckbtn),
      self._get_text_from_entry("--reg-key=",
                                m._file_os_registry_reg_ckbtn,
                                m._file_os_registry_reg_key_entry),
      self._get_text_from_entry("--reg-value=",
                                m._file_os_registry_reg_ckbtn,
                                m._file_os_registry_reg_value_entry),
      self._get_text_from_entry("--reg-data=",
                                m._file_os_registry_reg_ckbtn,
                                m._file_os_registry_reg_data_entry),
      self._get_text_from_entry("--reg-type=",
                                m._file_os_registry_reg_ckbtn,
                                m._file_os_registry_reg_type_entry),
    ]

    self._enumeration_opts = [
      self._get_text_only_ckbtn("-b",
                                m._enum_area_opts_ckbtns[0][0]),
      self._get_text_only_ckbtn("--current-user",
                                m._enum_area_opts_ckbtns[0][1]),
      self._get_text_only_ckbtn("--current-db",
                                m._enum_area_opts_ckbtns[0][2]),
      self._get_text_only_ckbtn("--hostname",
                                m._enum_area_opts_ckbtns[0][3]),
      self._get_text_only_ckbtn("--is-dba",
                                m._enum_area_opts_ckbtns[0][4]),
      self._get_text_only_ckbtn("--users",
                                m._enum_area_opts_ckbtns[1][0]),
      self._get_text_only_ckbtn("--passwords",
                                m._enum_area_opts_ckbtns[1][1]),
      self._get_text_only_ckbtn("--privileges",
                                m._enum_area_opts_ckbtns[1][2]),
      self._get_text_only_ckbtn("--roles",
                                m._enum_area_opts_ckbtns[1][3]),
      self._get_text_only_ckbtn("--dbs",
                                m._enum_area_opts_ckbtns[1][4]),
      self._get_text_only_ckbtn("--tables",
                                m._enum_area_opts_ckbtns[2][0]),
      self._get_text_only_ckbtn("--columns",
                                m._enum_area_opts_ckbtns[2][1]),
      self._get_text_only_ckbtn("--schema",
                                m._enum_area_opts_ckbtns[2][2]),
      self._get_text_only_ckbtn("--count",
                                m._enum_area_opts_ckbtns[2][3]),
      self._get_text_only_ckbtn("--comments",
                                m._enum_area_opts_ckbtns[2][4]),
      self._get_text_only_ckbtn("--dump",
                                m._dump_area_dump_ckbtn),
      self._get_text_only_ckbtn("--dump-all",
                                m._dump_area_dump_all_ckbtn),
      self._get_text_only_ckbtn("--search",
                                m._dump_area_search_ckbtn),
      self._get_text_only_ckbtn("--exclude-sysdb",
                                m._dump_area_no_sys_db_ckbtn),
      self._get_text_only_ckbtn("--repair",
                                m._dump_area_repair_ckbtn),
      self._get_text_from_entry("--start=",
                                m._limit_area_start_ckbtn,
                                m._limit_area_start_entry, None),
      self._get_text_from_entry("--stop=",
                                m._limit_area_stop_ckbtn,
                                m._limit_area_stop_entry, None),
      self._get_text_from_entry("--first=",
                                m._blind_area_first_ckbtn,
                                m._blind_area_first_entry),
      self._get_text_from_entry("--last=",
                                m._blind_area_last_ckbtn,
                                m._blind_area_last_entry),
      self._get_text_from_entry("-D ",
                                m._meta_area_D_ckbtn,
                                m._meta_area_D_entry),
      self._get_text_from_entry("-T ",
                                m._meta_area_T_ckbtn,
                                m._meta_area_T_entry),
      self._get_text_from_entry("-C ",
                                m._meta_area_C_ckbtn,
                                m._meta_area_C_entry),
      self._get_text_from_entry("-U ",
                                m._meta_area_U_ckbtn,
                                m._meta_area_U_entry),
      self._get_text_from_entry("-X ",
                                m._meta_area_X_ckbtn,
                                m._meta_area_X_entry),
      self._get_text_from_entry("--pivot-column=",
                                m._meta_area_pivot_ckbtn,
                                m._meta_area_pivot_entry),
      self._get_text_from_entry("--where=",
                                m._meta_area_where_ckbtn,
                                m._meta_area_where_entry),
      self._get_text_from_entry("--sql-query=",
                                m._runsql_area_sql_query_ckbtn,
                                m._runsql_area_sql_query_entry),
      self._get_text_only_ckbtn("--sql-shell",
                                m._runsql_area_sql_shell_ckbtn),
      self._get_text_from_entry("--sql-file=",
                                m._runsql_area_sql_file_ckbtn,
                                m._runsql_area_sql_file_entry),
      self._get_text_only_ckbtn("--common-tables",
                                m._brute_force_area_common_tables_ckbtn),
      self._get_text_only_ckbtn("--common-columns",
                                m._brute_force_area_common_columns_ckbtn),
    ]

    self._request_opts = [
      self._get_text_only_ckbtn("--random-agent",
                                m._request_area_random_agent_ckbtn),
      self._get_text_from_entry("--user-agent=",
                                m._request_area_user_agent_ckbtn,
                                m._request_area_user_agent_entry),
      self._get_text_from_entry("--host=",
                                m._request_area_host_ckbtn,
                                m._request_area_host_entry),
      self._get_text_from_entry("--referer=",
                                m._request_area_referer_ckbtn,
                                m._request_area_referer_entry),
      self._get_text_from_entry("--header=",
                                m._request_area_header_ckbtn,
                                m._request_area_header_entry),
      self._get_text_from_entry("--headers=",
                                m._request_area_headers_ckbtn,
                                m._request_area_headers_entry),
      self._get_text_from_entry("--method=",
                                m._request_area_method_ckbtn,
                                m._request_area_method_entry, None),
      self._get_text_from_entry("--param-del=",
                                m._request_area_param_del_ckbtn,
                                m._request_area_param_del_entry),
      self._get_text_from_entry("--data=",
                                m._request_area_post_ckbtn,
                                m._request_area_post_entry),
      self._get_text_from_entry("--cookie=",
                                m._request_area_cookie_ckbtn,
                                m._request_area_cookie_entry),
      self._get_text_from_entry("--cookie-del=",
                                m._request_area_cookie_del_ckbtn,
                                m._request_area_cookie_del_entry),
      self._get_text_from_entry("--load-cookies=",
                                m._request_area_load_cookies_ckbtn,
                                m._request_area_load_cookies_entry),
      self._get_text_only_ckbtn("--drop-set-cookie",
                                m._request_area_drop_set_cookie_ckbtn),
      self._get_text_from_entry("--auth-type=",
                                m._request_area_auth_type_ckbtn,
                                m._request_area_auth_type_entry),
      self._get_text_from_entry("--auth-cred=",
                                m._request_area_auth_cred_ckbtn,
                                m._request_area_auth_cred_entry),
      self._get_text_from_entry("--auth-file=",
                                m._request_area_auth_file_ckbtn,
                                m._request_area_auth_file_entry),
      self._get_text_from_entry("--csrf-token=",
                                m._request_area_csrf_token_ckbtn,
                                m._request_area_csrf_token_entry),
      self._get_text_from_entry("--csrf-url=",
                                m._request_area_csrf_url_ckbtn,
                                m._request_area_csrf_url_entry),
      self._get_text_only_ckbtn("--ignore-redirects",
                                m._request_area_ignore_redirects_ckbtn),
      self._get_text_only_ckbtn("--ignore-timeouts",
                                m._request_area_ignore_timeouts_ckbtn),
      self._get_text_from_entry("--ignore-code=",
                                m._request_area_ignore_code_ckbtn,
                                m._request_area_ignore_code_entry, None),
      self._get_text_only_ckbtn("--skip-urlencode",
                                m._request_area_skip_urlencode_ckbtn),
      self._get_text_only_ckbtn("--force-ssl",
                                m._request_area_force_ssl_ckbtn),
      self._get_text_only_ckbtn("--chunked",
                                m._request_area_chunked_ckbtn),
      self._get_text_only_ckbtn("--hpp",
                                m._request_area_hpp_ckbtn),
      self._get_text_from_entry("--delay=",
                                m._request_area_delay_ckbtn,
                                m._request_area_delay_entry, None),
      self._get_text_from_entry("--timeout=",
                                m._request_area_timeout_ckbtn,
                                m._request_area_timeout_entry, None),
      self._get_text_from_entry("--retries=",
                                m._request_area_retries_ckbtn,
                                m._request_area_retries_entry, None),
      self._get_text_from_entry("--randomize=",
                                m._request_area_randomize_ckbtn,
                                m._request_area_randomize_entry),
      self._get_text_from_entry("--eval=",
                                m._request_area_eval_ckbtn,
                                m._request_area_eval_entry),
      self._get_text_from_entry("--safe-url=",
                                m._request_area_safe_url_ckbtn,
                                m._request_area_safe_url_entry),
      self._get_text_from_entry("--safe-post=",
                                m._request_area_safe_post_ckbtn,
                                m._request_area_safe_post_entry),
      self._get_text_from_entry("--safe-req=",
                                m._request_area_safe_req_ckbtn,
                                m._request_area_safe_req_entry),
      self._get_text_from_entry("--safe-freq=",
                                m._request_area_safe_freq_ckbtn,
                                m._request_area_safe_freq_entry),
      self._get_text_only_ckbtn("--ignore-proxy",
                                m._request_area_ignore_proxy_ckbtn),
      self._get_http_proxy(),
      self._get_http_proxy_cred(),
      self._get_text_from_entry("--proxy-file=",
                                m._request_area_proxy_file_ckbtn,
                                m._request_area_proxy_file_entry),
      self._get_text_only_ckbtn("--tor",
                                m._request_area_tor_ckbtn),
      self._get_text_from_entry("--tor-port=",
                                m._request_area_tor_port_ckbtn,
                                m._request_area_tor_port_entry),
      self._get_text_from_entry("--tor-type=",
                                m._request_area_tor_type_ckbtn,
                                m._request_area_tor_type_entry),
      self._get_text_only_ckbtn("--check-tor",
                                m._request_area_check_tor_ckbtn),
    ]

    self._setting_opts = [
      self._get_text_from_entry("-p ",
                                m._inject_area_param_ckbtn,
                                m._inject_area_param_entry),
      self._get_text_only_ckbtn("--skip-static",
                                m._inject_area_skip_static_ckbtn),
      self._get_text_from_entry("--prefix=",
                                m._inject_area_prefix_ckbtn,
                                m._inject_area_prefix_entry),
      self._get_text_from_entry("--suffix=",
                                m._inject_area_suffix_ckbtn,
                                m._inject_area_suffix_entry),
      self._get_text_from_entry("--skip=",
                                m._inject_area_skip_ckbtn,
                                m._inject_area_skip_entry),
      self._get_text_from_entry("--para-exclude=",
                                m._inject_area_param_exclude_ckbtn,
                                m._inject_area_param_exclude_entry),
      self._get_text_from_entry("--dbms=",
                                m._inject_area_dbms_ckbtn,
                                m._inject_area_dbms_combobox.get_child()),
      self._get_text_from_entry("--dbms-cred=",
                                m._inject_area_dbms_cred_ckbtn,
                                m._inject_area_dbms_cred_entry),
      self._get_text_from_entry("--os=",
                                m._inject_area_os_ckbtn,
                                m._inject_area_os_entry),
      self._get_text_only_ckbtn("--no-cast",
                                m._inject_area_no_cast_ckbtn),
      self._get_text_only_ckbtn("--no-escape",
                                m._inject_area_no_escape_ckbtn),
      self._get_text_only_ckbtn("--invalid-logic",
                                m._inject_area_invalid_logic_ckbtn),
      self._get_text_only_ckbtn("--invalid-bignum",
                                m._inject_area_invalid_bignum_ckbtn),
      self._get_text_only_ckbtn("--invalid-str",
                                m._inject_area_invalid_str_ckbtn),
      self._get_text_from_scale("--level=",
                                m._detection_area_level_ckbtn,
                                m._detection_area_level_scale),
      self._get_text_only_ckbtn("--text-only",
                                m._detection_area_text_only_ckbtn),
      self._get_text_from_scale("--risk=",
                                m._detection_area_risk_ckbtn,
                                m._detection_area_risk_scale),
      self._get_text_only_ckbtn("--titles",
                                m._detection_area_titles_ckbtn),
      self._get_text_from_entry("--string=",
                                m._detection_area_str_ckbtn,
                                m._detection_area_str_entry),
      self._get_text_from_entry("--not-string=",
                                m._detection_area_not_str_ckbtn,
                                m._detection_area_not_str_entry),
      self._get_text_from_entry("--regexp=",
                                m._detection_area_re_ckbtn,
                                m._detection_area_re_entry),
      self._get_text_from_entry("--code=",
                                m._detection_area_code_ckbtn,
                                m._detection_area_code_entry, None),
      self._get_text_from_entry("--technique=",
                                m._tech_area_tech_ckbtn,
                                m._tech_area_tech_entry, None),
      self._get_text_from_entry("--time-sec=",
                                m._tech_area_time_sec_ckbtn,
                                m._tech_area_time_sec_entry, None),
      self._get_text_from_entry("--union-cols=",
                                m._tech_area_union_col_ckbtn,
                                m._tech_area_union_col_entry, None),
      self._get_text_from_entry("--union-char=",
                                m._tech_area_union_chr_ckbtn,
                                m._tech_area_union_chr_entry),
      self._get_text_from_entry("--union-from=",
                                m._tech_area_union_from_ckbtn,
                                m._tech_area_union_from_entry),
      self._get_text_from_entry("--dns-domain=",
                                m._tech_area_dns_ckbtn,
                                m._tech_area_dns_entry),
      self._get_text_from_entry("--second-url=",
                                m._tech_area_second_url_ckbtn,
                                m._tech_area_second_url_entry),
      self._get_text_from_entry("--second-req=",
                                m._tech_area_second_req_ckbtn,
                                m._tech_area_second_req_entry),
      self._get_text_only_ckbtn("-o",
                                m._optimize_area_turn_all_ckbtn),
      self._get_text_from_entry("--threads=",
                                m._optimize_area_thread_num_ckbtn,
                                m._optimize_area_thread_num_spinbtn, None),
      self._get_text_only_ckbtn("--predict-output",
                                m._optimize_area_predict_ckbtn),
      self._get_text_only_ckbtn("--keep-alive",
                                m._optimize_area_keep_alive_ckbtn),
      self._get_text_only_ckbtn("--null-connection",
                                m._optimize_area_null_connect_ckbtn),
      self._get_text_from_scale("-v ",
                                m._general_area_verbose_ckbtn,
                                m._general_area_verbose_scale),
      self._get_text_only_ckbtn("--fingerprint",
                                m._general_area_finger_ckbtn),
      self._get_text_only_ckbtn("--hex",
                                m._general_area_hex_ckbtn),
      self._get_text_only_ckbtn("--batch",
                                m._general_area_batch_ckbtn),
      self._get_text_only_ckbtn("--wizard",
                                m._page1_misc_wizard_ckbtn),
      self._get_tampers(),
    ]

  def _get_http_proxy_cred(self):
    m = self.m
    _use_proxy = m._request_area_proxy_ckbtn.get_active()
    _username = m._request_area_proxy_username_entry.get_text()
    _pass = m._request_area_proxy_password_entry.get_text()

    if all((_use_proxy, _username, _pass)) :
      return ''.join((" --proxy-cred=", QUOTE % '{}:{}'.format(_username, _pass)))
    return ''

  def _get_http_proxy(self):
    m = self.m
    _use_proxy = m._request_area_proxy_ckbtn.get_active()
    _ip = m._request_area_proxy_ip_entry.get_text().strip()
    _port = m._request_area_proxy_port_entry.get_text()

    if _use_proxy and _ip:
      if _port:
        return "".join((" --proxy=", QUOTE % '{}:{}'.format(_ip, _port)))
      else:
        return "".join((" --proxy=", QUOTE % _ip))
    return ''

  def _get_tampers(self):
    ''' --tamper=TAMPER     Use given script(s) for tampering injection data '''
    _tamper_textbuffer = self.w._tamper_area_tamper_view.get_buffer()
    _tampers = ''

    _start = _tamper_textbuffer.get_start_iter()
    _end = _tamper_textbuffer.get_end_iter()
    for _tamper_tmp in _tamper_textbuffer.get_text(_start, _end, False).splitlines():
      if _tamper_tmp.strip():
        _tampers = _tampers + _tamper_tmp.strip() + ','

    if _tampers:
      return " --tamper=" + QUOTE % _tampers.rstrip(',')
    return ''

  def _get_text_from_scale(self, opt_str, ckbtn, scale):
    if ckbtn.get_active():
      return ''.join((' ', opt_str, str(int(scale.get_value()))))
    return ''

  def _get_text_only_ckbtn(self, opt_str, ckbtn):
    if ckbtn.get_active():
      return ''.join((' ', opt_str))
    return ''

  def _get_text_from_entry(self, opt_str, ckbtn, entry, quote = QUOTE):
    _entry_str = entry.get_text().strip()
    if ckbtn.get_active() and _entry_str:

      if quote:
        return ''.join((' ',
                        opt_str,
                        quote % self._escape_quote_in_QUOTE(_entry_str)))
      else:
        return ''.join((' ',
                        opt_str,
                        self._escape_quote(_entry_str)))
    return ''

  def _escape_quote_in_QUOTE(self, widget_text):
    '''
    注意bash中, 双单引号内无法使用'(即无法转义)
    '''
    if widget_text:
      if IS_POSIX:
        return widget_text.replace("'", r"'\''")
      else:
        return widget_text.replace('"', r"\"")
    return widget_text

  def _escape_quote(self, widget_text):
    if widget_text:
      return widget_text.replace("'", r"\'").replace('"', r'\"')
    return widget_text


def main():
  from sqlmap_ui import UI_Window

  win = UI_Window()
  win.connect('destroy', g.main_quit)
  win.show_all()
  g.main()


if __name__ == '__main__':
  main()
