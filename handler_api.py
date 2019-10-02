#!/usr/bin/env python3
# encoding: utf-8
#
# 2019年 05月 14日 星期二 22:32:20 CST

import ast
import requests

from widgets import (g, GLib)


class Api(object):
  def __init__(self, window, m):
    '''
    w: Gtk.Window
    m: model.Model
    '''
    self.w = window
    self.m = m

  def task_new(self, button):
    '''
    rest api获取自: https://github.com/PyxYuYu/MyBlog/issues/69
    @get("/task/new") 创建新任务
    '''
    _host = self.m._page4_api_server_entry.get_text().strip()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    if _host:
      try:
        _resp = requests.get('http://%s/task/new' % _host,
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          self.task_view_append('%s: 创建成功.' % _resp['taskid'])
      except Exception as e:
        self.task_view_append(e)

  def admin_list(self, button):
    '''
    @get("/admin/<taskid>/list") 查看所有任务，并显示运行状态
    '''
    _host = self.m._page4_api_server_entry.get_text().strip()
    _token = self.m._page4_admin_token_entry.get_text().strip()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    if _host and _token:
      try:
        _resp = requests.get('http://%s/admin/%s/list' % (_host, _token),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        # print(_resp)
        if _resp['success']:
          # self.task_view_append('总任务数: %s' % _resp['tasks_num'])
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
            _task_del_btn.connect('clicked', self.task_delete, _a_task_row, _taskid)
            _scan_kill_btn = g.Button.new_with_label('杀死')
            _scan_kill_btn.connect('clicked', self.scan_kill, _taskid)
            _scan_stop_btn = g.Button.new_with_label('停止')
            _scan_stop_btn.connect('clicked', self.scan_stop, _taskid)
            _scan_start_btn = g.Button.new_with_label('启动')
            _scan_start_btn.connect('clicked', self.scan_start, _taskid)
            _scan_data_btn = g.Button.new_with_label('data')
            _scan_data_btn.connect('clicked', self.scan_data, _taskid)
            _scan_log_btn = g.Button.new_with_label('log')
            _scan_log_btn.connect('clicked', self.scan_log, _taskid)
            _option_list_btn = g.Button.new_with_label('所有选项')
            _option_list_btn.connect('clicked', self.option_list, _taskid)
            _option_get_btn = g.Button.new_with_label('选项:')
            _option_get_btn.connect('clicked', self.option_get, _taskid)
            _option_set_btn = g.Button.new_with_label('设置:')
            _option_set_btn.connect('clicked', self.option_set, _taskid)

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
        self.task_view_append(e)
    else:
        self.task_view_append('需要填写API server和admin token.')

  def option_list(self, button, taskid):
    '''
    @get("/option/<taskid>/list") 获取指定任务的options
    '''
    _host = self.m._page4_api_server_entry.get_text().strip()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    if _host:
      try:
        _resp = requests.get('http://%s/option/%s/list' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          for _key, _value in _resp['options'].items():
            if _value:
              self.task_view_append('%s: %s' % (_key, _value))
      except Exception as e:
        self.task_view_append(e)

  def option_get(self, button, taskid):
    '''
    @post("/option/<taskid>/get") 获取指定任务的option(s)
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _buffer_text = self.m._page4_option_get_entry.get_text()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    _options = {}
    for _tmp in _buffer_text.split():
      _options[_tmp] = None
    if _host and _options:
      _mesg = '%s:\n' % taskid
      try:
        _headers = {'Content-Type': 'application/json'}
        _resp = requests.post('http://%s/option/%s/get' % (_host, taskid),
                              json = _options,
                              headers = _headers,
                              auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

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
      self.task_view_append(_mesg.strip())

  def option_set(self, button, taskid):
    '''
    @post("/option/<taskid>/set") 设置指定任务的option(s)
    Warning: any option can be set, even a invalid option which
             is unable to remove, except deleting the task.
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _buffer_text = self._get_buffer_text(self.m._page4_option_set_view)
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    try:
      _json = ast.literal_eval(_buffer_text)
    except Exception as e:
      _json = str(e)

    _mesg = '%s: ' % taskid
    if _json and isinstance(_json, dict):
      if _host:
        try:
          _headers = {'Content-Type': 'application/json'}
          # data, json参数都要求是字典类型, 而非字符串
          # 另外, 字典的格式比json的宽松(json不能使用单引号, 不能多个逗号)
          _resp = requests.post('http://%s/option/%s/set' % (_host, taskid),
                                json = _json,
                                headers = _headers,
                                auth = (_username, _password))
          if not _resp:
            _resp.raise_for_status()

          _resp = _resp.json()
          if _resp['success']:
            _mesg += '设置成功'
        except Exception as e:
          _mesg += str(e)
    else:
      _mesg += '需要一个有效的python dict'

    self.task_view_append(_mesg)

  def admin_flush(self, button):
    '''
    @get("/admin/<taskid>/flush") 删除所有任务
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _token = self.m._page4_admin_token_entry.get_text()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    if _host and _token:
      try:
        _resp = requests.get('http://%s/admin/%s/flush' % (_host, _token),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          for _a_child in self.w._api_admin_list_rows.get_children():
            self.w._api_admin_list_rows.remove(_a_child)
          self.task_view_append('清空全部任务: 成功')
      except Exception as e:
        self.task_view_append(e)

  def task_delete(self, button, *data):
    '''
    @get("/task/<taskid>/delete") 删除指定任务
    '''
    _host = self.m._page4_api_server_entry.get_text().strip()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    if _host:
      try:
        _resp = requests.get('http://%s/task/%s/delete' % (_host, data[1]),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          self.w._api_admin_list_rows.remove(data[0])
          self.task_view_append('%s: 删除成功' % data[1])
      except Exception as e:
        self.task_view_append(e)

  def scan_start(self, button, taskid):
    '''
    @post("/scan/<taskid>/start") 指定任务 开始扫描
    要求发送json, 会执行/option/<taskid>/set
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    if _host:
      _mesg = '%s: ' % taskid
      try:
        _headers = {'Content-Type': 'application/json'}
        _resp = requests.post('http://%s/scan/%s/start' % (_host, taskid),
                              json = {},
                              headers = _headers,
                              auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          _mesg = '%sengineid: %s' % (_mesg, _resp['engineid'])
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)

      self.task_view_append(_mesg)

  def scan_stop(self, button, taskid):
    '''
    @get("/scan/<taskid>/stop") 指定任务 停止扫描
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    if _host:
      _mesg = '%s: ' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/stop' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          _mesg += 'ok, stoped.'
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)
      self.task_view_append(_mesg)

  def scan_kill(self, button, taskid):
    '''
    @get("/scan/<taskid>/kill") kill -9 指定任务
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    if _host:
      _mesg = '%s: ' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/kill' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          _mesg += 'ok, killed.'
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)
      self.task_view_append(_mesg)

  def scan_data(self, button, taskid):
    '''
    @get("/scan/<taskid>/data") 查看指定任务的扫描数据,
                                data若有内容说明存在注入
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    if _host:
      _mesg = '%s:\n' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/data' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        # print(_resp)    # _resp['data'], _resp['error'] are list
        if _resp['success']:
          del[_resp['success']]
          _mesg = '%s%s' % (_mesg, _resp)
      except Exception as e:
        _mesg += str(e)
      self.task_view_append(_mesg)

  def scan_log(self, button, taskid):
    '''
    @get("/scan/<taskid>/log") 查看指定任务的扫描日志
    '''
    _host = self.m._page4_api_server_entry.get_text()
    _username = self.m._page4_username_entry.get_text().strip()
    _password = self.m._page4_password_entry.get_text().strip()
    if _host:
      _mesg = '%s:\n' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/log' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

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
      self.task_view_append(_mesg)

  def _get_buffer_text(self, textview):
    _buffer = textview.get_buffer()
    _start = _buffer.get_start_iter()
    _end = _buffer.get_end_iter()
    return _buffer.get_text(_start, _end, False).strip()

  def task_view_append(self, output):
    _task_view_textbuffer = self.m._page4_task_view.get_buffer()

    _mark = _task_view_textbuffer.get_mark('end')
    _end = _task_view_textbuffer.get_iter_at_mark(_mark)

    _task_view_textbuffer.insert(_end, '%s\n' % output)

    self.m._page4_task_view.grab_focus()
    # https://stackoverflow.com/questions/48934458/gtk-sourceview-scroll-to-mark-not-working
    GLib.idle_add(self.m._page4_task_view.scroll_mark_onscreen, _mark)

