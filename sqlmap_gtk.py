#!/usr/bin/env python3
#
# 2018-08-26 16:54:41
# required: python3.6+, python3-gi, sqlmap

from pathlib import Path
from subprocess import (Popen, PIPE, STDOUT)
from threading import Thread

from widgets import (GLib, Vte, d, g, Box, Frame, btn, label)
from widgets import VERTICAL

from opts_gtk import Notebook
from model import Model
from handlers import Handler
from session import Session, load_settings

SETTINGS = load_settings()
if 'zh' == SETTINGS[1]:
  from tooltips_zh import Widget_Mesg as INIT_MESG
else:
  from tooltips import Widget_Mesg as INIT_MESG

# from basis_and_tool.logging_needle import get_console_logger
# logger = get_console_logger()

# Model()与对象有关, 按照OOP原则, 理应是实例属性
# 但只有一个实例, 所以就这么写吧
m = Model(SETTINGS[0])
del SETTINGS


class Window(g.Window):
  # @profile
  def __init__(self):
    super().__init__(title='sqlmap-gtk')
    self.connect('key_press_event', self.on_quit_by_key)
    self.set_icon_from_file("static/title.ico")
    self.clipboard = g.Clipboard.get(d.SELECTION_CLIPBOARD)

    self._handlers = Handler(self, m)

    _main_box = Box(orientation=VERTICAL)

    self._target_notebook = g.Notebook()
    self._build_target_notebook(self._target_notebook)

    _main_box.pack_start(self._target_notebook, False, True, 0)

    self.main_notebook = g.Notebook()
    self.main_notebook.add_events(d.EventMask.SCROLL_MASK
                                  | d.EventMask.SMOOTH_SCROLL_MASK)
    self.main_notebook.connect('scroll-event', self.scroll_page)
    page1 = self._build_page1()
    page2 = self._build_page2()
    page3 = self._build_page3()
    page4 = self._build_page4()
    page5 = self._build_page5()
    page6 = self._build_page6()

    _ = m._
    self.main_notebook.append_page(page1, label.new_with_mnemonic(_('OPTIONS(_1)')))
    self.main_notebook.append_page(page2, label.new_with_mnemonic(_('EXECUTION(_2)')))
    self.main_notebook.append_page(page3, label.new_with_mnemonic(_('LOG(_3)')))
    self.main_notebook.append_page(page4, label.new_with_mnemonic(_('SQLMAPAPI(_4)')))
    self.main_notebook.append_page(page5, label.new_with_mnemonic(_('HELP(_H)')))
    self.main_notebook.append_page(page6, label.new(_('ABOUT')))

    _main_box.pack_start(self.main_notebook, True, True, 0)
    self.add(_main_box)
    # 初始化完后, 必须要有焦点, 不然按任何键都会报错, 直到操作一次UI:
    # gtk_widget_event: assertion 'WIDGET_REALIZED_FOR_EVENT (widget, event)' failed`
    # 获取焦点
    # m._url_combobox.get_child().grab_focus()
    self.set_focus(m._url_combobox.get_child())

    # add tooltips, placeholders
    INIT_MESG(m)

    self.session = Session(m)
    self.session.load_from_tmp()

  def on_quit(self):
    try:
      self.session.save_to_tmp()
    except Exception as e:
      raise e
    finally:
      g.main_quit()

  # 如果是实现do_key_press_event, 那事件就传不出去了, why?
  def on_quit_by_key(self, widget, event: d.EventKey):
    keysym = event.keyval  # see: gdk/gdkkeysyms.h
    # key_name = d.keyval_name(keysym)
    # print('(keysym %s, %s)' % (keysym, key_name))

    state = event.state
    _ctrl = (state & d.ModifierType.CONTROL_MASK)

    if _ctrl and (keysym == d.KEY_q or keysym == d.KEY_w):
      self.on_quit()
      return True

  def scroll_page(self, notebook, event):
    '''
    https://stackoverflow.com/questions/11773132/gtk-notebook-change-page-with-scrolling-and-alt1-like-firefox-chrome-epipha
    '''
    if event.get_scroll_deltas()[2] < 0:
      notebook.prev_page()
    else:
      notebook.next_page()
    # returns True, so it would stop the emission.
    # 返回True, 会停止向上(父容器)传递信号,
    # 不然page1的_notebook处理完信号后, 会传递给父容器的main_notebook
    return True

  def set_file_entry_text(self, button, data):
    '''
    data: [file_entry, 'title of chooser']
    '''
    if len(data) > 1:   # choose folder
      dialog = g.FileChooserDialog(data[1], self,
                                   g.FileChooserAction.SELECT_FOLDER,
                                   ('_Cancel', g.ResponseType.CANCEL,
                                    '_Select', g.ResponseType.OK))
    else:
      # 点击左侧的 最近使用 可选择目录, 小问题, 不用管.
      dialog = g.FileChooserDialog("choose file", self,
                                   g.FileChooserAction.OPEN,
                                   ('_Cancel', g.ResponseType.CANCEL,
                                    '_OK', g.ResponseType.OK))
    try:
      if dialog.run() == g.ResponseType.OK:
        data[0].set_text(dialog.get_filename())
        data[0].grab_focus()
    finally:
      dialog.destroy()

  def clear_all_entry(self, button):
    for _i in dir(m):
      if _i.endswith('entry'):
        _tmp_entry = getattr(m, _i)
        if isinstance(_tmp_entry, g.Entry) and _tmp_entry is not m._sqlmap_path_entry:
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

  def _show_warn(self, button, mesg):
    if button.get_active():
      # Dialog windows should be set transient for the main application window!
      _ = g.MessageDialog(transient_for = self,
                          flags = 0,
                          message_type = g.MessageType.WARNING,
                          buttons = g.ButtonsType.OK_CANCEL,
                          text = mesg)
      _response = _.run()
      if _response in (g.ResponseType.CANCEL, g.ResponseType.DELETE_EVENT):
        button.set_active(False)

      _.destroy()

  def _build_target_notebook(self, target_nb):
    target_nb.add_events(d.EventMask.SCROLL_MASK
                         | d.EventMask.SMOOTH_SCROLL_MASK)
    target_nb.connect('scroll-event', self.scroll_page)
    # --url
    name_store = g.ListStore(int, str)
    name_store.append([1, "http://www.site.com/vuln.php?id=1"])

    _url_area = Box()
    m._url_combobox.set_model(name_store)
    m._url_combobox.set_entry_text_column(1)

    _url_area.pack_start(m._url_combobox, True, True, 0)

    _burp_area = Box()
    m._burp_logfile_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._burp_logfile]
    )

    _burp_area.pack_start(m._burp_logfile, True, True, 0)
    _burp_area.pack_start(m._burp_logfile_chooser, False, True, 0)

    _request_area = Box()

    m._request_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._request_file]
    )

    _request_area.pack_start(m._request_file, True, True, 0)
    _request_area.pack_start(m._request_file_chooser, False, True, 0)

    _bulkfile_area = Box()
    m._bulkfile_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._bulkfile]
    )

    _bulkfile_area.pack_start(m._bulkfile, True, True, 0)
    _bulkfile_area.pack_start(m._bulkfile_chooser, False, True, 0)

    _configfile_area = Box()
    m._configfile_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._configfile]
    )

    _configfile_area.pack_start(m._configfile, True, True, 0)
    _configfile_area.pack_start(m._configfile_chooser, False, True, 0)

    _google_dork_area = Box()
    _google_dork_area.pack_start(m._google_dork, True, True, 0)

    _direct_connect_area = Box()
    m._direct_connect.set_text('mysql://USER:PASSWORD@DBMS_IP:DBMS_PORT/DATABASE_NAME or '
                               'access://DATABASE_FILEPATH')
    _direct_connect_area.pack_start(m._direct_connect, True, True, 0)

    _ = m._
    target_nb.append_page(_url_area, label.new(_('-u URL')))
    target_nb.append_page(_burp_area, label.new(_('-l LOGFILE')))
    target_nb.append_page(_request_area, label.new(_('-r REQUESTFILE')))
    target_nb.append_page(_bulkfile_area, label.new(_('-m BULKFILE')))
    target_nb.append_page(_configfile_area, label.new(_('-c CONFIGFILE')))
    target_nb.append_page(_google_dork_area, label.new(_('-g GOOGLEDORK')))
    target_nb.append_page(_direct_connect_area, label.new(_('-d DIRECT')))

  def _build_page1(self):
    box = Box(orientation=VERTICAL, spacing=6)
    box.set_border_width(10)
    _ = m._

    # sqlmap命令语句
    _cmd_area = Frame.new(_('A.Options are collected here:'))
    _cmd_area.add(m._cmd_entry)

    # 主构造区
    _notebook = Notebook(m, self._handlers)

    m._general_area_flush_session_ckbtn.connect('toggled',
                                                self._show_warn,
                                                'check --flush-session:\n\n'
                                                'Flush session files for current target?')
    m._misc_area_purge_ckbtn.connect('toggled',
                                     self._show_warn,
                                     'check --purge:\n\n'
                                     'Safely remove all content from sqlmap data directory?')

    _notebook.add_events(d.EventMask.SCROLL_MASK
                         | d.EventMask.SMOOTH_SCROLL_MASK)
    _notebook.connect('scroll-event', self.scroll_page)

    # 构造与执行
    _exec_area = Box()

    _build_button = btn.new_with_mnemonic(_('A.collect(_A)'))
    _build_button.connect('clicked', self._handlers.build_all)

    _unselect_all_btn = btn.new_with_mnemonic(_('unselect(_S)'))
    _unselect_all_btn.connect('clicked', self.unselect_all_ckbtn)
    _clear_all_entry = btn.new_with_mnemonic(_('clear all inputs(_D)'))
    _clear_all_entry.connect('clicked', self.clear_all_entry)

    _run_button = btn.new_with_mnemonic(_('B.run(_F)'))
    _run_button.connect('clicked', self._handlers.run_cmdline)

    _exec_area.pack_start(_build_button, False, True, 0)
    _exec_area.pack_start(_unselect_all_btn, True, False, 0)
    _exec_area.pack_start(_clear_all_entry, True, False, 0)
    _exec_area.pack_end(_run_button, False, True, 0)

    box.pack_start(_cmd_area, False, True, 0)
    box.pack_start(_notebook, True, True, 0)
    box.pack_end(_exec_area, False, True, 0)
    return box

  def _build_page2(self):
    '''
    用subprocess不可实现与sqlmap的交互!
    不管是多线程, 同步还是异步, 都不行, 只能使用pty
    '''
    box = Box(orientation=VERTICAL, spacing=6)
    box.set_border_width(10)

    _row1 = Box(spacing = 6)
    m._page2_respwan_btn.connect('clicked', self._handlers.respawn_terminal)
    m._page2_right_btn.connect("button-press-event", self.on_right_click)
    # can not disable
    # m._page2_right_btn.set_sensitive(False)
    self._build_page2_context()

    _row1.pack_start(m._page2_respwan_btn, False, True, 0)
    _row1.pack_start(m._page2_right_btn, False, True, 0)

    _row2 = Frame()
    # equals: _pty = m._page2_terminal.pty_new_sync(Vte.PtyFlags.DEFAULT)
    _pty = Vte.Pty.new_sync(Vte.PtyFlags.DEFAULT)
    m._page2_terminal.set_pty(_pty)
    m._page2_terminal.connect('key_press_event', self.on_clipboard_by_key)
    m._page2_terminal.connect("button-press-event", self.on_right_click, m._page2_right_btn)

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

    box.pack_start(_row1, False, True, 5)
    box.pack_end(_row2, True, True, 0)
    return box

  def _build_page2_context(self):
    self.popover = g.Popover()
    self.popover.connect('key_press_event', self.on_right_click_by_accel)

    _vbox = g.Box(orientation=VERTICAL, spacing=6)

    copy = btn.new_with_label(m._('Copy(C)'))
    paste = btn.new_with_label(m._('Paste(V)'))
    copy.connect("clicked", self.on_right_click_copy)
    paste.connect("clicked", self.on_right_click_paste)

    _vbox.pack_start(copy, False, True, 5)
    _vbox.pack_start(paste, False, True, 5)

    self.popover.add(_vbox)
    self.popover.set_position(g.PositionType.BOTTOM)

  def on_right_click(self, button, event, widget = None):
    if widget:
      button = widget
    # right button
    if event.button == d.BUTTON_SECONDARY:
      self.popover.set_relative_to(button)
      self.popover.show_all()
      # self.popover.popup()

  def on_right_click_copy(self, widget):
    self._copy()
    self.popover.hide()

  def on_right_click_paste(self, widget):
    self._paste()
    self.popover.hide()

  def on_right_click_by_accel(self, widget, event):
    keysym = event.keyval

    if keysym == d.KEY_c:
      self.on_right_click_copy(widget)
    if keysym == d.KEY_v:
      self.on_right_click_paste(widget)
    if keysym == d.KEY_Escape:
      self.popover.hide()
    return True

  def on_clipboard_by_key(self, widget, event):
    _ctrl = event.state & d.ModifierType.CONTROL_MASK
    keysym = event.keyval

    if _ctrl and keysym == d.KEY_C:
      return self._copy()
    if _ctrl and keysym == d.KEY_V:
      return self._paste()

  def _copy(self):
    if m._page2_terminal.get_has_selection():
      m._page2_terminal.copy_clipboard_format(Vte.Format(1))
      return True

  def _paste(self):
    _text = self.clipboard.wait_for_text()
    if _text is not None and '\n' in _text:
      _ = g.MessageDialog(transient_for = self,
                          flags = 0,
                          message_type = g.MessageType.WARNING,
                          buttons = g.ButtonsType.OK_CANCEL,
                          text = f'Warning: insecure paste:\n\n{_text}')
      _response = _.run()
      _.destroy()
      if _response != g.ResponseType.OK:
        return True

    m._page2_terminal.paste_clipboard()
    return True

  def _build_page3(self):
    box = Box(orientation=VERTICAL, spacing=6)
    box.set_border_width(10)

    _row1 = Frame()

    _log_view_textbuffer = m._page3_log_view.get_buffer()
    self._handlers.clear_log_view_buffer(None)

    _end = _log_view_textbuffer.get_end_iter()
    _log_view_textbuffer.create_mark('end', _end, False)

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(m._page3_log_view)
    _row1.add(_scrolled)

    _row2 = Box()
    m._page3_read_target_btn.connect('clicked', self._handlers.read_target_file)
    m._page3_clear_btn.connect('clicked', self._handlers.clear_log_view_buffer)
    m._page3_read_log_btn.connect('clicked', self._handlers.read_log_file)

    _row2.pack_start(m._page3_read_target_btn, True, False, 0)
    _row2.pack_start(m._page3_clear_btn, True, False, 0)
    _row2.pack_start(m._page3_read_log_btn, True, False, 0)

    box.pack_start(_row1, True, True, 5)
    box.pack_end(_row2, False, True, 0)
    return box

  def _build_page4(self):
    box = Box(orientation=VERTICAL)
    box.set_border_width(10)

    _row1 = Box(spacing = 6)
    _row1.pack_start(m._page4_api_server_label, False, True, 0)
    _row1.pack_start(m._page4_api_server_entry, True, True, 0)
    _row1.pack_start(m._page4_admin_token_label, False, True, 0)
    _row1.pack_start(m._page4_admin_token_entry, True, True, 0)

    _row2 = Box(spacing = 6)
    _arrow_down = g.Image.new_from_icon_name('pan-down-symbolic', 1)
    m._page4_admin_list_btn.set_image(_arrow_down)
    m._page4_admin_list_btn.set_image_position(g.PositionType.RIGHT)
    m._page4_admin_list_btn.set_always_show_image(True)

    m._page4_task_new_btn.connect('clicked', self._handlers.api.task_new)
    m._page4_admin_list_btn.connect('clicked', self._handlers.api.admin_list)
    m._page4_admin_flush_btn.connect('clicked', self._handlers.api.admin_flush)
    m._page4_clear_task_view_btn.connect('clicked', self._handlers.clear_task_view_buffer)

    _row2.pack_start(m._page4_task_new_btn, False, True, 0)
    _row2.pack_start(m._page4_admin_list_btn, False, True, 0)
    _row2.pack_start(m._page4_admin_flush_btn, False, True, 0)
    _row2.pack_start(m._page4_clear_task_view_btn, False, True, 0)
    _row2.pack_end(m._page4_password_entry, False, True, 0)
    _row2.pack_end(m._page4_password_label, False, True, 0)
    _row2.pack_end(m._page4_username_entry, False, True, 0)
    _row2.pack_end(m._page4_username_label, False, True, 0)

    _row3 = Frame()
    _paned = g.Paned()

    self._api_admin_list_rows = g.ListBox.new()
    self._api_admin_list_rows.set_selection_mode(g.SelectionMode.NONE)

    _lscrolled = g.ScrolledWindow()
    _lscrolled.set_size_request(400, -1)
    _lscrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _lscrolled.add(self._api_admin_list_rows)

    _rbox = Box(orientation=VERTICAL)
    _page4_option_set_view_tip = label(label = 'check optiondict.py of sqlmap about options.',
                                       halign = g.Align.START)
    _option_set_view_textbuffer = m._page4_option_set_view.get_buffer()
    _options_example = ("{\n"
                        "  'url': 'http://www.site.com/vuln.php?id=1',\n"
                        "  'level': 1, 'risk': 1,\n\n"
                        "}\n")
    _option_set_view_textbuffer.set_text(_options_example, len(_options_example.encode('utf8')))
    # 貌似scrollwindow要直接包含textview,
    # 不然一直回车后, 页面不会向上滚
    _option_set_scrolled = g.ScrolledWindow()
    _option_set_scrolled.set_size_request(400, -1)
    _option_set_scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _option_set_scrolled.add(m._page4_option_set_view)

    _rbox.pack_start(m._page4_option_get_entry, False, True, 2)
    _rbox.pack_start(_page4_option_set_view_tip, False, True, 2)
    _rbox.pack_start(_option_set_scrolled, True, True, 2)

    # Warning: don't edit pack1(), pack2() again, otherwise it becomes strange.
    _paned.pack1(_lscrolled, False, False)
    _paned.pack2(_rbox, False, True)
    _row3.add(_paned)

    _row4 = Frame()

    _task_view_textbuffer = m._page4_task_view.get_buffer()
    _end = _task_view_textbuffer.get_end_iter()
    _task_view_textbuffer.create_mark('end', _end, False)
    self._handlers.api.task_view_append('response result:')

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(m._page4_task_view)

    _row4.add(_scrolled)

    box.pack_start(_row1, False, True, 5)
    box.pack_start(_row2, False, True, 5)
    box.pack_start(_row3, True, True, 5)
    box.pack_start(_row4, True, True, 5)
    return box

  def _build_page5(self):
    box = Box(orientation=VERTICAL)
    box.set_border_width(10)

    _row1 = Box()
    self._get_sqlmap_path_btn = btn.new_with_label('sqlmap -hh')
    self._get_sqlmap_path_btn.set_sensitive(False)
    self._get_sqlmap_path_btn.connect('clicked', self._make_help_thread)

    _row1.pack_start(self._get_sqlmap_path_btn, False, True, 5)

    _row2 = Frame()

    self._make_help_thread(None)

    _scrolled = g.ScrolledWindow()
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(m._page5_manual_view)

    _row2.add(_scrolled)

    box.pack_start(_row1, False, True, 5)
    box.pack_start(_row2, True, True, 5)
    return box

  def _make_help_thread(self, button):
    isClick = True if button else False
    # 使用线程 填充 帮助标签, 加快启动速度
    t = Thread(target = self._set_manual_view,
               args = (m._page5_manual_view.get_buffer(), isClick))
    t.daemon = True  # 主线程退出了, 当然守护进程也要退出
    t.start()

  def _set_manual_view(self, textbuffer, isClick):
    '''
    不用多线程能行嘛? 想要获得输出结果就一定会有阻塞的可能!
    https://www.jianshu.com/p/11090e197648
    https://wiki.gnome.org/Projects/PyGObject/Threading
    needle注: 操作的共享对象有两个: _get_sqlmap_path_btn, textbuffer
              原则一样, 所有对共用对象的操作都要用GLib.idle_add
              这样写是不是很丑?
              另外, 如果没运行完, 主线程就退出了, 会卡住哦, 属于正常
    '''
    if isClick:
      GLib.idle_add(self._get_sqlmap_path_btn.set_sensitive, False)
      GLib.idle_add(textbuffer.set_text, '')

    # _manual_hh = '/home/needle/bin/output_interval.sh'
    _manual_hh = [self._handlers.get_sqlmap_path(), '-hh']
    try:
      _subprocess = Popen(_manual_hh, stdout=PIPE, stderr=STDOUT)

      for _an_bytes_line_tmp in iter(_subprocess.stdout.readline, b''):
        GLib.idle_add(self.textbuffer_insert,
                      textbuffer,
                      _an_bytes_line_tmp.decode('utf8'))

      _subprocess.wait()
    except FileNotFoundError as e:
      GLib.idle_add(self.textbuffer_insert, textbuffer, str(e))
    except Exception as e:
      print(e)
    finally:
      GLib.idle_add(self._get_sqlmap_path_btn.set_sensitive, True)

    if isClick:
      GLib.idle_add(self._get_sqlmap_path_btn.grab_focus)

  def textbuffer_insert(self, textbuffer, line):
    # get_end_iter也要加锁, py有没有变量锁? 锁btn和textbuffer就行了嘛
    textbuffer.insert(textbuffer.get_end_iter(), line)

  def _build_page6(self):
    box = Box(orientation=VERTICAL, spacing=6)
    box.set_border_width(10)

    _boxes = [Box() for _ in range(3)]

    _lang = label.new('language:')
    _tooltip = label.new('tooltips:')
    _boxes[0].pack_start(_lang, False, True, 10)
    _boxes[0].pack_start(m._page6_lang_en_radio, False, True, 10)
    _boxes[0].pack_start(m._page6_lang_zh_radio, False, True, 10)
    _boxes[0].pack_start(label.new(m._('Take effects after restarting GUI.')), False, True, 10)
    _boxes[1].pack_start(_tooltip, False, True, 10)
    _boxes[1].pack_start(m._page6_tooltips_en_radio, False, True, 10)
    _boxes[1].pack_start(m._page6_tooltips_zh_radio, False, True, 10)

    _url_self = 'https://github.com/needle-wang/sqlmap-gtk'
    _url_tutorial = 'https://python-gtk-3-tutorial.readthedocs.io/en/latest'
    _url_api = 'https://lazka.github.io/pgi-docs/Gtk-3.0/'
    _url_idea = 'https://github.com/kxcode'
    _about_str = f'''
    1. <a href="{_url_self}" title = "{_url_self}">Website</a> VERSION: 0.3.5.1
       2021-01-05 13:33:04
       required: python3.6+, gtk+3.20 above,
                 python3-gi, requests, sqlmap\n
    2. use PyGObject(python3-gi + Gtk+3) to recode sqm.py
    3. thanks to the idea from sqm, author: <a href="{_url_idea}" title="{_url_idea}">KINGX</a>. sqm UI with python2 + tkinter\n
    4. Python GTK+3 Tutorial: <a href="{_url_tutorial}">{_url_tutorial}</a>
    5. PyGObject-GTK 3.0 API: <a href="{_url_api}">{_url_api}</a>
    '''
    _ = label.new(_about_str)
    _.set_use_markup(True)
    # _.set_selectable(True)
    _boxes[2].pack_start(_, False, True, 0)

    box.pack_start(_boxes[0], False, True, 0)
    box.pack_start(_boxes[1], False, True, 0)
    box.pack_start(_boxes[2], False, True, 80)
    return box


def main():
  import time

  start = time.process_time()
  # --------
  win = Window()

  css_provider = g.CssProvider.new()
  css_provider.load_from_path('static/css.css')
  g.StyleContext.add_provider_for_screen(
    d.Screen.get_default(),
    css_provider,
    g.STYLE_PROVIDER_PRIORITY_APPLICATION
  )

  win.connect('destroy', lambda x: win.on_quit())
  # win.maximize()
  win.show_all()
  # --------
  end = time.process_time()
  print('loading cost: %.3f Seconds' % (end - start))
  g.main()


if __name__ == '__main__':
  main()
