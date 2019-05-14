#!/usr/bin/env python3
# encoding: utf-8
#
# 2019年 05月 14日 星期二 19:44:19 CST

from widgets import g, Box, Frame, label, tv
from widgets import HORIZONTAL, VERTICAL


class Notebook(g.Notebook):
  '''
  m: model.Model
  '''
  def __init__(self, m, handlers):
    super().__init__()

    self.m = m
    self._handlers = handlers
    # 选项区 - 设置, 请求, 枚举, 文件, 其他
    page1_setting = self._build_page1_setting(m)
    page1_request = self._build_page1_request()
    page1_enumeration = self._build_page1_enumeration()
    page1_file = self._build_page1_file()
    page1_other = self._build_page1_other()

    self.append_page(page1_setting, label.new_with_mnemonic('测试(_Q)'))
    self.append_page(page1_request, label.new_with_mnemonic('请求(_W)'))
    self.append_page(page1_enumeration, label.new_with_mnemonic('枚举(_E)'))
    self.append_page(page1_file, label.new_with_mnemonic('文件(_R)'))
    self.append_page(page1_other, label.new_with_mnemonic('其他(_T)'))

  def cb_single(self, widget, ckbtn):
    if widget.get_active():
      ckbtn.set_active(False)

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

  def _build_page1_setting(self, m):
    box = Box(orientation=VERTICAL)

    _row0 = Box()
    _sqlmap_path_label = label(label = '指定sqlmap路径:')
    m._sqlmap_path_entry.set_text('sqlmap')
    m._sqlmap_path_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._sqlmap_path_entry]
    )

    _row0.pack_start(_sqlmap_path_label, False, True, 5)
    _row0.pack_start(m._sqlmap_path_entry, True, True, 5)
    _row0.pack_start(m._sqlmap_path_chooser, False, True, 5)

    _row1 = Box()
    _inject_area = self._build_page1_setting_inject(self.m)
    _detection_area = self._build_page1_setting_detection(self.m)
    _tech_area = self._build_page1_setting_tech(self.m)

    _row1.pack_start(_inject_area, False, True, 5)
    _row1.pack_start(_detection_area, True, True, 5)
    _row1.pack_start(_tech_area, False, True, 5)

    _row2 = Box()
    _tamper_area = self._build_page1_setting_tamper(self.m)
    _optimize_area = self._build_page1_setting_optimize(self.m)
    _general_area = self._build_page1_setting_general(self.m)

    _row2.pack_start(_tamper_area, False, True, 5)
    _row2.pack_start(_optimize_area, False, True, 5)
    _row2.pack_start(_general_area, False, True, 5)

    box.pack_start(_row0, False, True, 5)
    box.pack_start(_row1, False, True, 0)
    box.pack_start(_row2, False, True, 5)

    scrolled = g.ScrolledWindow()
    scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    scrolled.add(box)
    return scrolled

  def _build_page1_setting_tech(self, m):
    f = Frame.new('各注入技术的选项')

    _tech_area_opts = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    _row1.pack_start(m._tech_area_tech_ckbtn, False, True, 5)
    _row1.pack_end(m._tech_area_tech_entry, False, True, 5)

    _row2 = Box()
    _row2.pack_start(m._tech_area_time_sec_ckbtn, False, True, 5)
    _row2.pack_end(m._tech_area_time_sec_entry, False, True, 5)

    _row3 = Box()
    _row3.pack_start(m._tech_area_union_col_ckbtn, False, True, 5)
    _row3.pack_end(m._tech_area_union_col_entry, False, True, 5)

    _row4 = Box()
    _row4.pack_start(m._tech_area_union_chr_ckbtn, False, True, 5)
    _row4.pack_end(m._tech_area_union_chr_entry, False, True, 5)

    _row5 = Box()
    _row5.pack_start(m._tech_area_union_from_ckbtn, False, True, 5)
    _row5.pack_end(m._tech_area_union_from_entry, False, True, 5)

    _row6 = Box()
    _row6.pack_start(m._tech_area_dns_ckbtn, True, True, 5)
    _row6.pack_end(m._tech_area_dns_entry, True, True, 5)

    _row7 = Box()
    _row7.pack_start(m._tech_area_second_url_ckbtn, True, True, 5)
    _row7.pack_end(m._tech_area_second_url_entry, True, True, 5)

    _row8 = Box()
    _row8.pack_start(m._tech_area_second_req_ckbtn, True, True, 5)

    _row9 = Box()
    m._tech_area_second_req_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._tech_area_second_req_entry]
    )

    _row9.pack_end(m._tech_area_second_req_chooser, False, True, 5)
    _row9.pack_end(m._tech_area_second_req_entry, True, True, 5)

    # 添加行: _row1 - _row9
    for _i in range(1, 10):
      _tech_area_opts.add(locals()[''.join(('_row', str(_i)))])

    f.add(_tech_area_opts)
    return f

  def _build_page1_setting_detection(self, m):
    f = Frame.new('探测选项')

    _detection_area_opts = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    _row1.pack_start(m._detection_area_level_ckbtn, False, True, 5)
    _row1.pack_start(m._detection_area_level_scale, True, True, 5)

    _row2 = Box()
    _row2.pack_start(m._detection_area_risk_ckbtn, False, True, 5)
    _row2.pack_start(m._detection_area_risk_scale, True, True, 10)

    _row3 = Box()
    _row3.pack_start(m._detection_area_str_ckbtn, False, True, 5)
    _row3.pack_end(m._detection_area_str_entry, True, True, 5)

    _row4 = Box()
    _row4.pack_start(m._detection_area_not_str_ckbtn, False, True, 5)
    _row4.pack_end(m._detection_area_not_str_entry, True, True, 5)

    _row5 = Box()
    _row5.pack_start(m._detection_area_re_ckbtn, False, True, 5)
    _row5.pack_end(m._detection_area_re_entry, True, True, 5)

    _row6 = Box()
    _row6.pack_start(m._detection_area_code_ckbtn, False, True, 5)
    _row6.pack_start(m._detection_area_code_entry, False, True, 5)

    _row7 = Box()
    m._detection_area_text_only_ckbtn.connect(
      'clicked',
      self.cb_single, m._detection_area_titles_ckbtn)
    m._detection_area_titles_ckbtn.connect(
      'clicked',
      self.cb_single, m._detection_area_text_only_ckbtn)

    _row7.pack_start(m._detection_area_text_only_ckbtn, True, True, 5)
    _row7.pack_start(m._detection_area_titles_ckbtn, True, True, 5)

    # 添加行: _row1 - _row7
    for _i in range(1, 8):
      _detection_area_opts.add(locals()[''.join(('_row', str(_i)))])

    f.add(_detection_area_opts)
    return f

  def _build_page1_setting_general(self, m):
    f = Frame.new('常用选项')
    _general_area_opts = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    m._general_area_verbose_scale.set_value(1.0)

    _row1.pack_start(m._general_area_verbose_ckbtn, False, True, 5)
    _row1.pack_start(m._general_area_verbose_scale, True, True, 5)

    _row2 = Box()
    _row2.pack_start(m._general_area_finger_ckbtn, False, True, 5)

    _row3 = Box()
    _row3.pack_start(m._general_area_hex_ckbtn, False, True, 5)

    _row4 = Box()
    _row4.pack_start(m._general_area_batch_ckbtn, False, True, 5)

    _row5 = Box()
    _row5.pack_start(m._page1_misc_wizard_ckbtn, False, True, 5)

    _general_area_opts.add(_row1)
    _general_area_opts.add(_row2)
    _general_area_opts.add(_row3)
    _general_area_opts.add(_row4)
    _general_area_opts.add(_row5)

    f.add(_general_area_opts)
    return f

  def _build_page1_setting_optimize(self, m):
    f = Frame.new('性能优化')

    _optimize_area_opts = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    m._optimize_area_turn_all_ckbtn.connect('clicked', self.optimize_area_controller)

    _row1.pack_start(m._optimize_area_turn_all_ckbtn, False, True, 5)

    _row2 = Box()
    _row2.pack_start(m._optimize_area_thread_num_ckbtn, False, True, 5)
    _row2.pack_start(m._optimize_area_thread_num_spinbtn, True, True, 5)

    _row3 = Box()
    _row3.pack_start(m._optimize_area_predict_ckbtn, False, True, 5)

    _row4 = Box()
    _row4.pack_start(m._optimize_area_keep_alive_ckbtn, False, True, 5)

    _row5 = Box()
    _row5.pack_start(m._optimize_area_null_connect_ckbtn, False, True, 5)

    # 添加行: _row1 - _row5
    for _i in range(1, 6):
      _optimize_area_opts.add(locals()[''.join(('_row', str(_i)))])

    f.add(_optimize_area_opts)
    return f

  def _build_page1_setting_tamper(self, m):
    '''
    frame套box, box再套scroll会出现:
    一直按回车出现滚动条后, 光标会下移 直到移出可见区, 原内容不会上移
    即内容的显示没有 下滑 滚轮的效果.
    '''
    f = Frame.new('tamper脚本')

    m._tamper_area_tamper_view = tv()
    m._tamper_area_tamper_view.set_wrap_mode(g.WrapMode.CHAR)

    _scrolled = g.ScrolledWindow()
    _scrolled.set_size_request(300, -1)
    _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    _scrolled.add(m._tamper_area_tamper_view)

    f.add(_scrolled)
    return f

  def _build_page1_setting_inject(self, m):
    f = Frame.new('注入选项')

    _row1 = Box()
    _row1.pack_start(m._inject_area_param_ckbtn, False, True, 5)
    _row1.pack_start(m._inject_area_param_entry, True, True, 5)

    _row2 = Box()
    # set_active(True)为选中状态
    m._inject_area_skip_static_ckbtn.set_active(True)

    _row2.pack_start(m._inject_area_skip_static_ckbtn, True, True, 5)

    _row3 = Box()
    _row3.pack_start(m._inject_area_prefix_ckbtn, False, True, 5)
    _row3.pack_start(m._inject_area_prefix_entry, True, True, 5)

    _row4 = Box()
    _row4.pack_start(m._inject_area_suffix_ckbtn, False, True, 5)
    _row4.pack_start(m._inject_area_suffix_entry, True, True, 5)

    _row5 = Box()
    _row5.pack_start(m._inject_area_skip_ckbtn, False, True, 5)
    _row5.pack_start(m._inject_area_skip_entry, True, True, 5)

    _row6 = Box()
    _row6.pack_start(m._inject_area_param_exclude_ckbtn, False, True, 5)
    _row6.pack_start(m._inject_area_param_exclude_entry, True, True, 5)

    _row7 = Box()
    _db_store = g.ListStore(str)
    _db_store.append(["mysql"])
    _db_store.append(["sqlite"])
    _db_store.append(["sqlserver"])

    m._inject_area_dbms_combobox.set_model(_db_store)
    m._inject_area_dbms_combobox.set_entry_text_column(0)

    _row7.pack_start(m._inject_area_dbms_ckbtn, False, True, 5)
    _row7.pack_start(m._inject_area_dbms_combobox, True, True, 5)

    _row8 = Box()
    _row8.pack_start(m._inject_area_dbms_cred_ckbtn, False, True, 5)
    _row8.pack_start(m._inject_area_dbms_cred_entry, True, True, 5)

    _row9 = Box()
    _row9.pack_start(m._inject_area_os_ckbtn, False, True, 5)
    _row9.pack_start(m._inject_area_os_entry, True, True, 5)

    _row10 = Box()
    _row10.pack_start(m._inject_area_no_cast_ckbtn, False, True, 5)
    _row10.pack_start(m._inject_area_no_escape_ckbtn, False, True, 5)

    _row11 = Box()
    _invalid_label = label.new('对payload中的废值:')

    _row11.pack_start(_invalid_label, False, True, 5)
    _row11.pack_end(m._inject_area_invalid_logic_ckbtn, False, True, 5)

    _row12 = Box()
    _row12.pack_end(m._inject_area_invalid_str_ckbtn, False, True, 5)
    _row12.pack_end(m._inject_area_invalid_bignum_ckbtn, False, True, 5)

    _inject_area_opts = Box(orientation=VERTICAL, spacing=6)
    # 添加行: _row1 - _row12
    for _i in range(1, 13):
      _inject_area_opts.add(locals()[''.join(('_row', str(_i)))])

    f.add(_inject_area_opts)
    return f

  def _build_page1_request(self):
    box = Box(orientation=VERTICAL)

    _row1 = Box()
    _request_header_area = self._build_page1_request_header(self.m)

    _row1.pack_start(_request_header_area, True, True, 5)

    _row2 = Box()
    _request_data_area = self._build_page1_request_data(self.m)

    _row2.pack_start(_request_data_area, True, True, 5)

    _row3 = Box()
    _request_custom_area = self._build_page1_request_custom(self.m)

    _row3.pack_start(_request_custom_area, True, True, 5)

    _row4 = Box()
    _request_proxy_area = self._build_page1_request_proxy(self.m)

    _row4.pack_start(_request_proxy_area, True, True, 5)

    box.pack_start(_row1, False, True, 5)
    box.pack_start(_row2, False, True, 5)
    box.pack_start(_row3, False, True, 5)
    box.pack_start(_row4, False, True, 5)

    scrolled = g.ScrolledWindow()
    scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    scrolled.add(box)
    return scrolled

  def _build_page1_request_proxy(self, m):
    f = Frame.new('隐匿/代理')
    _request_proxy_opts = Box(orientation=VERTICAL, spacing = 5)

    _row1 = Box()
    _row1.pack_start(m._request_area_safe_url_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_safe_url_entry, True, True, 5)
    _row1.pack_start(m._request_area_safe_post_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_safe_post_entry, True, True, 5)

    _row2 = Box()
    m._request_area_safe_req_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._request_area_safe_req_entry]
    )

    _row2.pack_start(m._request_area_safe_req_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_safe_req_entry, True, True, 0)
    _row2.pack_start(m._request_area_safe_req_chooser, False, True, 5)
    _row2.pack_start(m._request_area_safe_freq_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_safe_freq_entry, False, True, 5)

    _row3 = g.Separator.new(HORIZONTAL)

    _row4 = Box()
    m._request_area_proxy_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._request_area_proxy_file_entry]
    )

    _row4.pack_start(m._request_area_ignore_proxy_ckbtn, False, True, 5)
    _row4.pack_start(m._request_area_proxy_ckbtn, False, True, 5)
    _row4.pack_start(m._request_area_proxy_file_ckbtn, False, True, 5)
    _row4.pack_start(m._request_area_proxy_file_entry, True, True, 0)
    _row4.pack_start(m._request_area_proxy_file_chooser, False, True, 5)

    _row5 = Box()
    _row5.pack_start(m._request_area_proxy_ip_label, False, True, 5)
    _row5.pack_start(m._request_area_proxy_ip_entry, True, True, 5)
    _row5.pack_start(m._request_area_proxy_port_label, False, True, 5)
    _row5.pack_start(m._request_area_proxy_port_entry, False, True, 5)
    _row5.pack_start(m._request_area_proxy_username_label, False, True, 5)
    _row5.pack_start(m._request_area_proxy_username_entry, True, True, 5)
    _row5.pack_start(m._request_area_proxy_password_label, False, True, 5)
    _row5.pack_start(m._request_area_proxy_password_entry, True, True, 5)

    _row6 = Box()
    _row6.pack_start(m._request_area_tor_ckbtn, False, True, 5)
    _row6.pack_start(m._request_area_tor_port_ckbtn, False, True, 5)
    _row6.pack_start(m._request_area_tor_port_entry, False, True, 5)
    _row6.pack_start(m._request_area_tor_type_ckbtn, False, True, 5)
    _row6.pack_start(m._request_area_tor_type_entry, False, True, 5)
    _row6.pack_start(m._request_area_check_tor_ckbtn, False, True, 5)

    # 添加行: _row1 - _row6
    for _i in range(1, 7):
      _request_proxy_opts.add(locals()[''.join(('_row', str(_i)))])

    f.add(_request_proxy_opts)
    return f

  def _build_page1_request_custom(self, m):
    f = Frame.new('request定制')
    _request_custom_opts = Box(orientation=VERTICAL, spacing = 5)

    _row1 = Box()
    m._request_area_ignore_code_entry.set_text('401')

    _row1.pack_start(m._request_area_ignore_redirects_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_ignore_timeouts_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_ignore_code_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_ignore_code_entry, True, True, 5)
    _row1.pack_start(m._request_area_skip_urlencode_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_force_ssl_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_chunked_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_hpp_ckbtn, False, True, 5)

    _row2 = Box()
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

    _row3 = Box()
    _row3.pack_start(m._request_area_eval_ckbtn, False, True, 5)
    _row3.pack_start(m._request_area_eval_entry, True, True, 5)

    _request_custom_opts.add(_row1)
    _request_custom_opts.add(_row2)
    _request_custom_opts.add(_row3)

    f.add(_request_custom_opts)
    return f

  def _build_page1_request_data(self, m):
    f = Frame.new('HTTP data')
    _request_data_opts = Box(orientation=VERTICAL, spacing = 5)

    _row1 = Box()
    m._request_area_param_del_entry.set_max_length(1)

    _row1.pack_start(m._request_area_method_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_method_entry, False, True, 5)
    _row1.pack_start(m._request_area_param_del_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_param_del_entry, False, True, 5)

    _row2 = Box()
    _row2.pack_start(m._request_area_post_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_post_entry, True, True, 5)

    _row3 = g.Separator.new(HORIZONTAL)

    _row4 = Box()
    _row4.pack_start(m._request_area_cookie_ckbtn, False, True, 5)
    _row4.pack_start(m._request_area_cookie_entry, True, True, 5)
    _row4.pack_start(m._request_area_cookie_del_ckbtn, False, True, 5)
    _row4.pack_start(m._request_area_cookie_del_entry, False, True, 5)

    _row5 = Box()
    m._request_area_load_cookies_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._request_area_load_cookies_entry]
    )

    _row5.pack_start(m._request_area_load_cookies_ckbtn, False, True, 5)
    _row5.pack_start(m._request_area_load_cookies_entry, True, True, 0)
    _row5.pack_start(m._request_area_load_cookies_chooser, False, True, 5)
    _row5.pack_start(m._request_area_drop_set_cookie_ckbtn, False, True, 5)

    _row6 = g.Separator.new(HORIZONTAL)

    _row7 = Box()
    m._request_area_auth_type_entry.set_max_width_chars(25)
    m._request_area_auth_file_entry.set_max_width_chars(25)

    m._request_area_auth_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._request_area_auth_file_entry]
    )

    _row7.pack_start(m._request_area_auth_type_ckbtn, False, True, 5)
    _row7.pack_start(m._request_area_auth_type_entry, True, True, 5)
    _row7.pack_start(m._request_area_auth_cred_ckbtn, False, True, 5)
    _row7.pack_start(m._request_area_auth_cred_entry, True, True, 5)
    _row7.pack_start(m._request_area_auth_file_ckbtn, False, True, 5)
    _row7.pack_start(m._request_area_auth_file_entry, True, True, 0)
    _row7.pack_start(m._request_area_auth_file_chooser, False, True, 5)

    _row8 = Box()
    _row8.pack_start(m._request_area_csrf_token_ckbtn, False, True, 5)
    _row8.pack_start(m._request_area_csrf_token_entry, True, True, 5)
    _row8.pack_start(m._request_area_csrf_url_ckbtn, False, True, 5)
    _row8.pack_start(m._request_area_csrf_url_entry, True, True, 5)

    # 添加行: _row1 - _row8
    for _i in range(1, 9):
      _request_data_opts.add(locals()[''.join(('_row', str(_i)))])

    f.add(_request_data_opts)
    return f

  def _build_page1_request_header(self, m):
    f = Frame.new('HTTP header')
    _request_header_opts = Box(orientation=VERTICAL, spacing = 5)

    _row1 = Box()
    m._request_area_random_agent_ckbtn.set_active(True)

    _row1.pack_start(m._request_area_random_agent_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_user_agent_ckbtn, False, True, 5)
    _row1.pack_start(m._request_area_user_agent_entry, True, True, 5)

    _row2 = Box()
    _row2.pack_start(m._request_area_host_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_host_entry, True, True, 5)
    _row2.pack_start(m._request_area_referer_ckbtn, False, True, 5)
    _row2.pack_start(m._request_area_referer_entry, True, True, 5)

    _row3 = Box()
    _row3.pack_start(m._request_area_header_ckbtn, False, True, 5)
    _row3.pack_start(m._request_area_header_entry, True, True, 5)
    _row3.pack_start(m._request_area_headers_ckbtn, False, True, 5)
    _row3.pack_start(m._request_area_headers_entry, True, True, 5)

    _request_header_opts.add(_row1)
    _request_header_opts.add(_row2)
    _request_header_opts.add(_row3)

    f.add(_request_header_opts)
    return f

  def _build_page1_enumeration(self):
    box = Box(orientation=VERTICAL)

    _row1 = Box()
    _row1.props.margin = 10

    _enum_area = self._build_page1_enumeration_enum(self.m)
    _dump_area = self._build_page1_enumeration_dump(self.m)
    _limit_area = self._build_page1_enumeration_limit(self.m)
    _blind_area = self._build_page1_enumeration_blind(self.m)

    _row1.pack_start(_enum_area, False, True, 10)
    _row1.pack_start(_dump_area, False, True, 10)
    _row1.pack_start(_limit_area, False, True, 10)
    _row1.pack_start(_blind_area, False, True, 10)

    _row2 = Box()
    _row2.props.margin = 10

    _meta_area = self._build_page1_enumeration_meta(self.m)

    _row2.pack_start(_meta_area, True, True, 10)

    _row3 = Box()
    _row3.props.margin = 10

    _runsql_area = self._build_page1_enumeration_runsql(self.m)

    _row3.pack_start(_runsql_area, True, True, 10)

    _row4 = Box()
    _row4.props.margin = 10
    _brute_force_area = self._build_page1_enumeration_brute_force(self.m)

    _row4.pack_start(_brute_force_area, False, True, 10)

    box.add(_row1)
    box.add(_row2)
    box.add(_row3)
    box.add(_row4)
    return box

  def _build_page1_enumeration_brute_force(self, m):
    f = Frame.new('暴破表名/列名')

    _brute_force_area_opts = Box(orientation=VERTICAL)

    _row1 = Box()

    _row1.pack_start(label.new('检查是否存在:'), False, True, 10)
    _row1.pack_start(m._brute_force_area_common_tables_ckbtn, False, True, 0)
    _row1.pack_start(m._brute_force_area_common_columns_ckbtn, False, True, 10)

    _brute_force_area_opts.pack_start(_row1, False, True, 5)

    f.add(_brute_force_area_opts)
    return f

  def _build_page1_enumeration_runsql(self, m):
    f = Frame.new('执行SQL语句')

    _runsql_area_opts = Box(orientation=VERTICAL)

    _row1 = Box()
    _row1.pack_start(m._runsql_area_sql_query_ckbtn, False, True, 10)
    _row1.pack_start(m._runsql_area_sql_query_entry, True, True, 10)

    _row2 = Box()
    m._runsql_area_sql_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._runsql_area_sql_file_entry]
    )

    _row2.pack_start(m._runsql_area_sql_shell_ckbtn, False, True, 10)
    _row2.pack_start(m._runsql_area_sql_file_ckbtn, False, True, 10)
    _row2.pack_start(m._runsql_area_sql_file_entry, True, True, 0)
    _row2.pack_start(m._runsql_area_sql_file_chooser, False, True, 10)

    _runsql_area_opts.pack_start(_row1, False, True, 5)
    _runsql_area_opts.pack_start(_row2, False, True, 5)

    f.add(_runsql_area_opts)
    return f

  def _build_page1_enumeration_meta(self, m):
    f = Frame.new('数据库名, 表名, 列名...')

    _meta_area_opts = Box(orientation=VERTICAL)

    _row1 = Box()

    _col1 = Box()     # It's row actually.
    _col1.pack_start(m._meta_area_D_ckbtn, False, True, 10)
    _col1.pack_start(m._meta_area_D_entry, True, True, 10)

    _col2 = Box()
    _col2.pack_start(m._meta_area_T_ckbtn, False, True, 10)
    _col2.pack_start(m._meta_area_T_entry, True, True, 10)

    _col3 = Box()
    _col3.pack_start(m._meta_area_C_ckbtn, False, True, 10)
    _col3.pack_start(m._meta_area_C_entry, True, True, 10)

    _col4 = Box()
    _col4.pack_start(m._meta_area_U_ckbtn, False, True, 10)
    _col4.pack_start(m._meta_area_U_entry, True, True, 10)

    _row1.pack_start(_col1, False, True, 5)
    _row1.pack_start(_col2, False, True, 5)
    _row1.pack_start(_col3, False, True, 5)
    _row1.pack_start(_col4, False, True, 5)

    _row2 = Box()

    _col1 = Box()
    _col1.pack_start(m._meta_area_X_ckbtn, False, True, 10)
    _col1.pack_start(m._meta_area_X_entry, True, True, 10)

    _col2 = Box()
    _col2.pack_start(m._meta_area_pivot_ckbtn, False, True, 10)
    _col2.pack_start(m._meta_area_pivot_entry, True, True, 10)

    _row2.pack_start(_col1, False, True, 5)
    _row2.pack_start(_col2, False, True, 5)

    _row3 = Box()
    _row3.pack_start(m._meta_area_where_ckbtn, False, True, 10)
    _row3.pack_start(m._meta_area_where_entry, True, True, 10)

    _meta_area_opts.pack_start(_row1, False, True, 5)
    _meta_area_opts.pack_start(_row2, False, True, 5)
    _meta_area_opts.pack_start(_row3, False, True, 5)

    f.add(_meta_area_opts)
    return f

  def _build_page1_enumeration_blind(self, m):
    f = Frame.new('盲注选项')

    _blind_area_opts = Box(orientation=VERTICAL)

    _row1 = Box()
    _row1.pack_start(m._blind_area_first_ckbtn, False, True, 5)
    _row1.pack_start(m._blind_area_first_entry, False, True, 10)

    _blind_area_opts.pack_start(_row1, False, True, 10)

    _row2 = Box()
    _row2.pack_start(m._blind_area_last_ckbtn, False, True, 5)
    _row2.pack_start(m._blind_area_last_entry, False, True, 10)

    _blind_area_opts.pack_start(_row2, False, True, 10)

    f.add(_blind_area_opts)
    return f

  def _build_page1_enumeration_limit(self, m):
    f = Frame.new('limit(dump时的限制)')

    _limit_area_opts = Box(orientation=VERTICAL)

    _row1 = Box()
    _row1.pack_start(m._limit_area_start_ckbtn, False, True, 5)
    _row1.pack_start(m._limit_area_start_entry, False, True, 0)
    _row1.pack_start(label.new('条'), False, True, 5)

    _row2 = Box()
    _row2.pack_start(m._limit_area_stop_ckbtn, False, True, 5)
    _row2.pack_start(m._limit_area_stop_entry, False, True, 0)
    _row2.pack_start(label.new('条'), False, True, 5)

    _limit_area_opts.pack_start(_row1, False, True, 10)
    _limit_area_opts.pack_start(_row2, False, True, 10)

    f.add(_limit_area_opts)
    return f

  def _build_page1_enumeration_dump(self, m):
    f = Frame.new('Dump(转储)')

    _dump_area_opts = Box(spacing=6)

    # 加这一层, 只是为了横向上有padding
    _dump_area_opts_cols = Box(orientation=VERTICAL)

    _dump_area_opts_cols.add(m._dump_area_dump_ckbtn)
    _dump_area_opts_cols.add(m._dump_area_dump_all_ckbtn)
    _dump_area_opts_cols.add(m._dump_area_search_ckbtn)
    _dump_area_opts_cols.add(m._dump_area_no_sys_db_ckbtn)
    _dump_area_opts_cols.add(m._dump_area_repair_ckbtn)

    _dump_area_opts.pack_start(_dump_area_opts_cols, False, True, 10)

    f.add(_dump_area_opts)
    return f

  def _build_page1_enumeration_enum(self, m):
    f = Frame.new('枚举')

    _enum_area_opts = Box(spacing=6)

    # Do not use: [g.Box()] * 3, 会有闭包现象
    _enu_area_opts_cols = [Box(orientation=VERTICAL),
                           Box(orientation=VERTICAL),
                           Box(orientation=VERTICAL)]

    for _x in range(len(m._enum_area_opts_ckbtns)):
      for _y in m._enum_area_opts_ckbtns[_x]:
        # 每列, 至上往下add
        _enu_area_opts_cols[_x].add(_y)
      # 添加三列, 方便对齐...
      _enum_area_opts.pack_start(_enu_area_opts_cols[_x], False, True, 10)

    f.add(_enum_area_opts)
    return f

  def _build_page1_file(self):
    box = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    _row1.props.margin = 10
    _file_read_area = self._build_page1_file_read(self.m)

    _row1.pack_start(_file_read_area, True, True, 10)

    _row2 = Box()
    _row2.props.margin = 10
    _file_write_area = self._build_page1_file_write(self.m)

    _row2.pack_start(_file_write_area, True, True, 10)

    _row3 = Box()
    _row3.props.margin = 10
    _file_os_access_area = self._build_page1_file_os_access(self.m)
    _row3.pack_start(_file_os_access_area, True, True, 10)

    _row4 = Box()
    _row4.props.margin = 10
    _file_os_registry_area = self._build_page1_file_os_registry(self.m)

    _row4.pack_start(_file_os_registry_area, True, True, 10)

    box.add(_row1)
    box.add(_row2)
    box.add(_row3)
    box.add(_row4)
    return box

  def _build_page1_file_os_registry(self, m):
    f = Frame.new('访问WIN下注册表')

    _file_os_registry_opts = Box(orientation=VERTICAL)

    _row1 = Box()
    m._file_os_registry_reg_combobox.append('--reg-read', '读取')
    m._file_os_registry_reg_combobox.append('--reg-add', '新增')
    m._file_os_registry_reg_combobox.append('--reg-del', '删除')
    m._file_os_registry_reg_combobox.set_active(0)

    _row1.pack_start(m._file_os_registry_reg_ckbtn, False, True, 5)
    _row1.pack_start(m._file_os_registry_reg_combobox, False, True, 5)

    _row2 = Box()
    _row2.pack_start(m._file_os_registry_reg_key_label, False, True, 5)
    _row2.pack_start(m._file_os_registry_reg_key_entry, True, True, 5)
    _row2.pack_start(m._file_os_registry_reg_value_label, False, True, 5)
    _row2.pack_start(m._file_os_registry_reg_value_entry, True, True, 5)

    _row3 = Box()
    _row3.pack_start(m._file_os_registry_reg_data_label, False, True, 5)
    _row3.pack_start(m._file_os_registry_reg_data_entry, True, True, 5)
    _row3.pack_start(m._file_os_registry_reg_type_label, False, True, 5)
    _row3.pack_start(m._file_os_registry_reg_type_entry, True, True, 5)

    _file_os_registry_opts.add(_row1)
    _file_os_registry_opts.add(_row2)
    _file_os_registry_opts.add(_row3)

    f.add(_file_os_registry_opts)
    return f

  def _build_page1_file_os_access(self, m):
    f = Frame.new('访问后端OS')

    _file_os_access_opts = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    _row1.pack_start(m._file_os_access_os_cmd_ckbtn, False, True, 5)
    _row1.pack_start(m._file_os_access_os_cmd_entry, True, True, 5)

    _row2 = Box()
    _row2.pack_start(m._file_os_access_os_shell_ckbtn, False, True, 5)
    _row2.pack_start(m._file_os_access_os_pwn_ckbtn, False, True, 5)
    _row2.pack_start(m._file_os_access_os_smbrelay_ckbtn, False, True, 5)
    _row2.pack_start(m._file_os_access_os_bof_ckbtn, False, True, 5)
    _row2.pack_start(m._file_os_access_priv_esc_ckbtn, False, True, 5)

    _row3 = Box()
    m._file_os_access_msf_path_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
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

    f.add(_file_os_access_opts)
    return f

  def _build_page1_file_write(self, m):
    f = Frame.new('文件上传')

    _file_write_area_opts = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    m._file_write_area_shared_lib_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._file_write_area_shared_lib_entry]
    )

    _row1.pack_start(m._file_write_area_udf_ckbtn, False, True, 5)
    _row1.pack_start(m._file_write_area_shared_lib_ckbtn, False, True, 5)
    _row1.pack_start(m._file_write_area_shared_lib_entry, True, True, 0)
    _row1.pack_start(m._file_write_area_shared_lib_chooser, False, True, 5)

    _row2 = Box()
    m._file_write_area_file_write_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._file_write_area_file_write_entry]
    )

    _row2.pack_start(m._file_write_area_file_write_ckbtn, False, True, 5)
    _row2.pack_start(m._file_write_area_file_write_entry, True, True, 0)
    _row2.pack_start(m._file_write_area_file_write_chooser, False, True, 5)

    _row3 = Box()
    _row3.pack_start(m._file_write_area_file_dest_ckbtn, False, True, 5)
    _row3.pack_start(m._file_write_area_file_dest_entry, True, True, 5)

    _file_write_area_opts.pack_start(_row1, False, True, 5)
    _file_write_area_opts.pack_start(_row2, False, True, 5)
    _file_write_area_opts.pack_start(_row3, False, True, 5)

    f.add(_file_write_area_opts)
    return f

  def _build_page1_file_read(self, m):
    f = Frame.new('读取远程文件')

    _file_read_area_opts = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    m._file_read_area_file_read_entry.set_text('/etc/passwd')
    m._file_read_area_file_read_btn.connect('clicked', self._handlers.read_dumped_file)

    _row1.pack_start(m._file_read_area_file_read_ckbtn, False, True, 5)
    _row1.pack_start(m._file_read_area_file_read_entry, True, True, 0)
    _row1.pack_start(m._file_read_area_file_read_btn, False, True, 5)

    _file_read_area_opts.pack_start(_row1, False, True, 5)

    f.add(_file_read_area_opts)
    return f

  def _build_page1_other(self):
    '''
    最大的宽应该是由最长的 request定制的第一行 决定

    如果所有标签页全用ScrolledWindow的话, UI的尺寸(size)会变得很小
    以"其他"标签的height作为标准高,
    高于此height的标签页使用ScrolledWindow, 显示滚动条
    '''
    box = Box(orientation=VERTICAL)

    _row1 = Box()
    _page1_other_general_area = self._build_page1_other_general(self.m)

    _row1.pack_start(_page1_other_general_area, True, True, 5)

    _row2 = Box()
    _page1_other_misc_area = self._build_page1_other_misc(self.m)

    _row2.pack_start(_page1_other_misc_area, True, True, 5)

    box.add(_row1)
    box.add(_row2)
    return box

  def _build_page1_other_misc(self, m):
    f = Frame.new('杂项')
    _page1_other_misc_opts = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    m._page1_misc_tmp_dir_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._page1_misc_tmp_dir_entry, '选择 本地临时目录']
    )

    _row1.pack_start(m._page1_misc_web_root_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_misc_web_root_entry, True, True, 5)
    _row1.pack_start(m._page1_misc_tmp_dir_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_misc_tmp_dir_entry, True, True, 0)
    _row1.pack_start(m._page1_misc_tmp_dir_chooser, False, True, 5)

    _row2 = Box()
    _row2.pack_start(m._page1_misc_identify_waf_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_skip_waf_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_smart_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_list_tampers_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_sqlmap_shell_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_disable_color_ckbtn, False, True, 5)

    _row3 = Box()
    m._page1_misc_purge_ckbtn.connect('toggled', self._show_warn)

    _row3.pack_start(m._page1_misc_offline_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_misc_mobile_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_misc_beep_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_misc_purge_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_misc_dependencies_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_general_update_ckbtn, False, True, 5)

    _row4 = Box()
    m._page1_misc_answers_entry.set_text('quit=N,follow=N')

    _row4.pack_start(m._page1_misc_answers_ckbtn, False, True, 5)
    _row4.pack_start(m._page1_misc_answers_entry, True, True, 5)
    _row4.pack_start(m._page1_misc_alert_ckbtn, False, True, 5)
    _row4.pack_start(m._page1_misc_alert_entry, True, True, 5)
    _row4.pack_start(m._page1_misc_gpage_ckbtn, False, True, 5)
    _row4.pack_start(m._page1_misc_gpage_spinbtn, False, True, 5)

    _row5 = Box()
    m._page1_misc_z_entry.set_text('flu,bat,ban,tec=EU...')

    _row5.pack_start(m._page1_misc_z_ckbtn, False, True, 5)
    _row5.pack_start(m._page1_misc_z_entry, True, True, 5)

    _page1_other_misc_opts.add(_row1)
    _page1_other_misc_opts.add(_row2)
    _page1_other_misc_opts.add(_row3)
    _page1_other_misc_opts.add(_row4)
    _page1_other_misc_opts.add(_row5)
    # _page1_other_misc_opts.add(g.Separator.new(HORIZONTAL))
    f.add(_page1_other_misc_opts)
    return f

  def _build_page1_other_general(self, m):
    f = Frame.new('通用项')
    _page1_other_general_opts = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    _row1.pack_start(m._page1_general_check_internet_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_general_fresh_queries_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_general_flush_session_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_general_eta_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_general_binary_fields_ckbtn, False, True, 5)
    _row1.pack_start(m._page1_general_binary_fields_entry, False, True, 5)

    _row2 = Box()
    m._page1_general_preprocess_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._page1_general_preprocess_entry]
    )

    _row2.pack_start(m._page1_general_forms_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_general_parse_errors_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_misc_cleanup_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_general_preprocess_ckbtn, False, True, 5)
    _row2.pack_start(m._page1_general_preprocess_entry, True, True, 0)
    _row2.pack_start(m._page1_general_preprocess_chooser, False, True, 5)

    _row3 = Box()
    _row3.pack_start(m._page1_general_crawl_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_general_crawl_entry, True, True, 5)
    _row3.pack_start(m._page1_general_crawl_exclude_ckbtn, False, True, 5)
    _row3.pack_start(m._page1_general_crawl_exclude_entry, True, True, 5)

    _row4 = Box()
    m._page1_general_charset_entry.set_text('0123456789abcdef')
    m._page1_general_encoding_entry.set_text('GBK')

    _row4.pack_start(m._page1_general_charset_ckbtn, False, True, 5)
    _row4.pack_start(m._page1_general_charset_entry, True, True, 5)
    _row4.pack_start(m._page1_general_encoding_ckbtn, False, True, 5)
    _row4.pack_start(m._page1_general_encoding_entry, False, True, 5)

    _row5 = Box()
    m._page1_general_session_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._page1_general_session_file_entry]
    )

    m._page1_general_output_dir_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._page1_general_output_dir_entry, '选择 结果保存在哪']
    )

    _row5.pack_start(m._page1_general_session_file_ckbtn, False, True, 5)
    _row5.pack_start(m._page1_general_session_file_entry, True, True, 0)
    _row5.pack_start(m._page1_general_session_file_chooser, False, True, 5)
    _row5.pack_start(m._page1_general_output_dir_ckbtn, False, True, 5)
    _row5.pack_start(m._page1_general_output_dir_entry, True, True, 0)
    _row5.pack_start(m._page1_general_output_dir_chooser, False, True, 5)

    _row6 = Box()
    m._page1_general_dump_format_entry.set_max_width_chars(40)
    m._page1_general_csv_del_entry.set_max_length(1)
    m._page1_general_csv_del_entry.set_text(',')

    _row6.pack_start(m._page1_general_dump_format_ckbtn, False, True, 5)
    _row6.pack_start(m._page1_general_dump_format_entry, False, True, 5)
    _row6.pack_start(m._page1_general_csv_del_ckbtn, False, True, 5)
    _row6.pack_start(m._page1_general_csv_del_entry, False, True, 5)

    _row7 = Box()
    m._page1_general_traffic_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._page1_general_traffic_file_entry]
    )

    m._page1_general_har_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._page1_general_har_entry]
    )

    _row7.pack_start(m._page1_general_traffic_file_ckbtn, False, True, 5)
    _row7.pack_start(m._page1_general_traffic_file_entry, True, True, 0)
    _row7.pack_start(m._page1_general_traffic_file_chooser, False, True, 5)
    _row7.pack_start(m._page1_general_har_ckbtn, False, True, 5)
    _row7.pack_start(m._page1_general_har_entry, True, True, 0)
    _row7.pack_start(m._page1_general_har_chooser, False, True, 5)

    _row8 = Box()
    m._page1_general_save_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._page1_general_save_entry]
    )

    m._page1_general_scope_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._page1_general_scope_entry]
    )

    _row8.pack_start(m._page1_general_save_ckbtn, False, True, 5)
    _row8.pack_start(m._page1_general_save_entry, True, True, 0)
    _row8.pack_start(m._page1_general_save_chooser, False, True, 5)
    _row8.pack_start(m._page1_general_scope_ckbtn, False, True, 5)
    _row8.pack_start(m._page1_general_scope_entry, True, True, 0)
    _row8.pack_start(m._page1_general_scope_chooser, False, True, 5)

    _row9 = Box()
    _row9.pack_start(m._page1_general_test_filter_ckbtn, False, True, 5)
    _row9.pack_start(m._page1_general_test_filter_entry, True, True, 5)
    _row9.pack_start(m._page1_general_test_skip_ckbtn, False, True, 5)
    _row9.pack_start(m._page1_general_test_skip_entry, True, True, 5)

    # 添加行: _row1 - _row9
    for _i in range(1, 10):
      _page1_other_general_opts.add(locals()[''.join(('_row', str(_i)))])

    f.add(_page1_other_general_opts)
    return f


def main():
  from model import Model
  from handlers import Handler

  win = g.Window(title = 'sqlmap-options')
  m = Model()

  n = Notebook(m, Handler(win, m))
  win.add(n)

  win.connect('destroy', g.main_quit)
  win.show_all()

  g.main()


if __name__ == '__main__':
  main()
