#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 08月 29日 星期三 15:34:10 CST

import os
import time

# python3.5+
from pathlib import Path
from subprocess import Popen
from urllib.parse import urlparse

# from basis_and_too.logging_needle import get_console_logger
# logger = get_console_logger()


class Singal_Handlers(object):
  def __init__(self, w):
    '''
    w: sqlmap_ui.UI_Window
    还不能用注解, 会相互import
    '''
    self._w = w

  def build_all(self, button):
    _target = self._get_target()
    self._collect_opts()

    _opts_list = (
      self._setting_opts + self._request_opts +
      self._enumeration_opts + self._file_opts + self._other_opts
    )

    _final_line = _target + ''.join(_opts_list)

    if _final_line:
      self._w._cmd_entry.set_text(_final_line)

  def run_cmdline(self, button):
    _sqlmap_opts = self._w._cmd_entry.get_text().strip()

    # TODO, 还是加个输入框, 指定sqlmap的路径吧
    if _sqlmap_opts:
      if os.name == 'posix':
        _cmdline_str = ''.join(('/usr/bin/env xterm -hold -e sqlmap ', _sqlmap_opts))
      else:
        _cmdline_str = ''.join(('start cmd /k python sqlmap.py ', _sqlmap_opts))

      # print(_cmdline_str)
      Popen(_cmdline_str, shell = True)

  def set_file_entry_text(self, button, entry):
    entry.set_text(button.get_filename())

  def clear_buffer(self, button):
    self._w._log_view_textbuffer.set_text('')

  def optimize_area_controller(self, button):
    ui = self._w
    if ui._optimize_area_turn_all_ckbtn.get_active():
      ui._optimize_area_predict_ckbtn.set_active(False)
      ui._optimize_area_keep_alive_ckbtn.set_active(False)
      ui._optimize_area_null_connect_ckbtn.set_active(False)

      ui._optimize_area_predict_ckbtn.set_sensitive(False)
      ui._optimize_area_keep_alive_ckbtn.set_sensitive(False)
      ui._optimize_area_null_connect_ckbtn.set_sensitive(False)
    else:
      ui._optimize_area_predict_ckbtn.set_sensitive(True)
      ui._optimize_area_keep_alive_ckbtn.set_sensitive(True)
      ui._optimize_area_null_connect_ckbtn.set_sensitive(True)

  def _get_url_dir(self):
    '''
    return: pathlib.PosixPath
    '''
    _load_url = self._w._url_combobox.get_child().get_text()

    if _load_url:
      if not _load_url.startswith('http'):
        _load_url = 'http://' + _load_url

      _load_host = urlparse(_load_url).netloc

      return Path.home() / '.sqlmap/output' / _load_host

  def _log_view_insert(self, file_path):
    '''
    file_path: pathlib.PosixPath
    '''
    ui = self._w
    _end_iter = ui._log_view_textbuffer.get_end_iter()
    try:
      with file_path.open() as _f:
        _line_list_tmp = _f.readlines()
        if _line_list_tmp:
          for _line_tmp in _line_list_tmp:
            ui._log_view_textbuffer.insert(_end_iter, _line_tmp)
        else:
          ui._log_view_textbuffer.insert(_end_iter, str(file_path) + ': 空文件')
    except EnvironmentError as e:
      ui._log_view_textbuffer.insert(_end_iter, str(e))
    finally:
      ui._log_view_textbuffer.insert(
        _end_iter,
        time.strftime('\n%Y-%m-%d %R:%S: ----------我是分割线----------\n',
                      time.localtime()))

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
    ui = self._w
    ui.main_notebook.next_page()

    _base_dir = self._get_url_dir()
    _load_file = ui._file_read_area_file_read_entry.get_text()

    if _base_dir and _load_file:
      # 不能用os.sep, 因为是依据远程OS的sep而定
      # 沿用sqlmap库中的filePathToSafeString函数
      _load_file = (_load_file.replace("/", "_").replace("\\", "_")
                              .replace(" ", "_").replace(":", "_"))

      _dumped_file_path = _base_dir / 'files' / _load_file
      self._log_view_insert(_dumped_file_path)

  def _get_target(self):
    ui = self._w
    current_page_num = ui._target_notbook.get_current_page()
    if current_page_num is 0:
      return " -u '" + ui._url_combobox.get_child().get_text().strip() + "'"
    elif current_page_num is 1:
      return " -l '" + ui._burp_logfile.get_text().strip() + "'"
    elif current_page_num is 2:
      return " -r '" + ui._request_file.get_text().strip() + "'"
    elif current_page_num is 3:
      return " -x '" + ui._sitemap_url.get_text().strip() + "'"
    elif current_page_num is 4:
      return " -m '" + ui._bulkfile.get_text().strip() + "'"
    elif current_page_num is 5:
      return " -g '" + ui._google_dork.get_text().strip() + "'"
    elif current_page_num is 6:
      return " -c '" + ui._configfile.get_text().strip() + "'"

  def _collect_opts(self):
    ui = self._w

    self._other_opts = [
      self._get_text_only_ckbtn("--check-internet",
                                ui._page1_general_check_internet_ckbtn),
      self._get_text_only_ckbtn("--fresh-queries",
                                ui._page1_general_fresh_queries_ckbtn),
      self._get_text_only_ckbtn("--flush-session",
                                ui._page1_general_flush_session_ckbtn),
      self._get_text_only_ckbtn("--eta",
                                ui._page1_general_eta_ckbtn),
      self._get_text_from_entry("--binary-fields=",
                                ui._page1_general_binary_fields_ckbtn,
                                ui._page1_general_binary_fields_entry),
      self._get_text_only_ckbtn("--forms",
                                ui._page1_general_forms_ckbtn),
      self._get_text_only_ckbtn("--parse-errors",
                                ui._page1_general_parse_errors_ckbtn),
      self._get_text_only_ckbtn("--cleanup",
                                ui._page1_misc_cleanup_ckbtn),
      self._get_text_from_entry("--crawl=",
                                ui._page1_general_crawl_ckbtn,
                                ui._page1_general_crawl_entry),
      self._get_text_from_entry("--crawl-exclude=",
                                ui._page1_general_crawl_exclude_ckbtn,
                                ui._page1_general_crawl_exclude_entry),
      self._get_text_from_entry("--charset=",
                                ui._page1_general_charset_ckbtn,
                                ui._page1_general_charset_entry),
      self._get_text_from_entry("--encoding=",
                                ui._page1_general_encoding_ckbtn,
                                ui._page1_general_encoding_entry),
      self._get_text_from_entry("-s ",
                                ui._page1_general_session_file_ckbtn,
                                ui._page1_general_session_file_entry),
      self._get_text_from_entry("--output-dir=",
                                ui._page1_general_output_dir_ckbtn,
                                ui._page1_general_output_dir_entry),
      self._get_text_from_entry("--dump-format=",
                                ui._page1_general_dump_format_ckbtn,
                                ui._page1_general_dump_format_entry),
      self._get_text_from_entry("--csv-del=",
                                ui._page1_general_csv_del_ckbtn,
                                ui._page1_general_csv_del_entry),
      self._get_text_from_entry("-t ",
                                ui._page1_general_traffic_file_ckbtn,
                                ui._page1_general_traffic_file_entry),
      self._get_text_from_entry("--har=",
                                ui._page1_general_har_ckbtn,
                                ui._page1_general_har_entry),
      self._get_text_from_entry("--save=",
                                ui._page1_general_save_ckbtn,
                                ui._page1_general_save_entry),
      self._get_text_from_entry("--scope=",
                                ui._page1_general_scope_ckbtn,
                                ui._page1_general_scope_entry),
      self._get_text_from_entry("--test-filter=",
                                ui._page1_general_test_filter_ckbtn,
                                ui._page1_general_test_filter_entry),
      self._get_text_from_entry("--test-skip=",
                                ui._page1_general_test_skip_ckbtn,
                                ui._page1_general_test_skip_entry),
      self._get_text_from_entry("--web-root=",
                                ui._page1_misc_web_root_ckbtn,
                                ui._page1_misc_web_root_entry),
      self._get_text_from_entry("--tmp-dir=",
                                ui._page1_misc_tmp_dir_ckbtn,
                                ui._page1_misc_tmp_dir_entry),
      self._get_text_only_ckbtn("--identify-waf",
                                ui._page1_misc_identify_waf_ckbtn),
      self._get_text_only_ckbtn("--skip-waf",
                                ui._page1_misc_skip_waf_ckbtn),
      self._get_text_only_ckbtn("--smart",
                                ui._page1_misc_smart_ckbtn),
      self._get_text_only_ckbtn("--list-tampers",
                                ui._page1_misc_list_tampers_ckbtn),
      self._get_text_only_ckbtn("--disable-coloring",
                                ui._page1_misc_disable_color_ckbtn),
      self._get_text_only_ckbtn("--offline",
                                ui._page1_misc_offline_ckbtn),
      self._get_text_only_ckbtn("--mobile",
                                ui._page1_misc_mobile_ckbtn),
      self._get_text_only_ckbtn("--beep",
                                ui._page1_misc_beep_ckbtn),
      self._get_text_only_ckbtn("--purge",
                                ui._page1_misc_purge_ckbtn),
      self._get_text_only_ckbtn("--dependencies",
                                ui._page1_misc_dependencies_ckbtn),
      self._get_text_only_ckbtn("--update",
                                ui._page1_general_update_ckbtn),
      self._get_text_from_entry("--answers=",
                                ui._page1_misc_answers_ckbtn,
                                ui._page1_misc_answers_entry),
      self._get_text_from_entry("--alert=",
                                ui._page1_misc_alert_ckbtn,
                                ui._page1_misc_alert_entry),
      self._get_text_from_entry("--gpage=",
                                ui._page1_misc_gpage_ckbtn,
                                ui._page1_misc_gpage_spinbtn, None),
      self._get_text_from_entry("-z ",
                                ui._page1_misc_z_ckbtn,
                                ui._page1_misc_z_entry),
    ]

    self._file_opts = [
      self._get_text_from_entry("--file-read=",
                                ui._file_read_area_file_read_ckbtn,
                                ui._file_read_area_file_read_entry),
      self._get_text_only_ckbtn("--udf-inject",
                                ui._file_write_area_udf_ckbtn),
      self._get_text_from_entry("--shared-lib=",
                                ui._file_write_area_shared_lib_ckbtn,
                                ui._file_write_area_shared_lib_entry),
      self._get_text_from_entry("--file-write=",
                                ui._file_write_area_file_write_ckbtn,
                                ui._file_write_area_file_write_entry),
      self._get_text_from_entry("--file-dest=",
                                ui._file_write_area_file_dest_ckbtn,
                                ui._file_write_area_file_dest_entry),
      self._get_text_from_entry("--os-cmd=",
                                ui._file_os_access_os_cmd_ckbtn,
                                ui._file_os_access_os_cmd_entry),
      self._get_text_only_ckbtn("--os-shell",
                                ui._file_os_access_os_shell_ckbtn),
      self._get_text_only_ckbtn("--os-pwn",
                                ui._file_os_access_os_pwn_ckbtn),
      self._get_text_only_ckbtn("--os-smbrelay",
                                ui._file_os_access_os_smbrelay_ckbtn),
      self._get_text_only_ckbtn("--os-bof",
                                ui._file_os_access_os_bof_ckbtn),
      self._get_text_only_ckbtn("--priv-esc",
                                ui._file_os_access_priv_esc_ckbtn),
      self._get_text_from_entry("--msf-path=",
                                ui._file_os_access_msf_path_ckbtn,
                                ui._file_os_access_msf_path_entry),
      self._get_text_from_entry("--tmp-path=",
                                ui._file_os_access_tmp_path_ckbtn,
                                ui._file_os_access_tmp_path_entry),
      self._get_text_only_ckbtn(ui._file_os_registry_reg_combobox.get_active_id(),
                                ui._file_os_registry_reg_ckbtn),
      self._get_text_from_entry("--reg-key=",
                                ui._file_os_registry_reg_ckbtn,
                                ui._file_os_registry_reg_key_entry),
      self._get_text_from_entry("--reg-value=",
                                ui._file_os_registry_reg_ckbtn,
                                ui._file_os_registry_reg_value_entry),
      self._get_text_from_entry("--reg-data=",
                                ui._file_os_registry_reg_ckbtn,
                                ui._file_os_registry_reg_data_entry),
      self._get_text_from_entry("--reg-type=",
                                ui._file_os_registry_reg_ckbtn,
                                ui._file_os_registry_reg_type_entry),
    ]

    self._enumeration_opts = [
      self._get_text_only_ckbtn("-b",
                                ui._enum_area_opts_ckbtns[0][0]),
      self._get_text_only_ckbtn("--current-user",
                                ui._enum_area_opts_ckbtns[0][1]),
      self._get_text_only_ckbtn("--current-db",
                                ui._enum_area_opts_ckbtns[0][2]),
      self._get_text_only_ckbtn("--hostname",
                                ui._enum_area_opts_ckbtns[0][3]),
      self._get_text_only_ckbtn("--is-dba",
                                ui._enum_area_opts_ckbtns[0][4]),
      self._get_text_only_ckbtn("--users",
                                ui._enum_area_opts_ckbtns[1][0]),
      self._get_text_only_ckbtn("--passwords",
                                ui._enum_area_opts_ckbtns[1][1]),
      self._get_text_only_ckbtn("--privileges",
                                ui._enum_area_opts_ckbtns[1][2]),
      self._get_text_only_ckbtn("--roles",
                                ui._enum_area_opts_ckbtns[1][3]),
      self._get_text_only_ckbtn("--dbs",
                                ui._enum_area_opts_ckbtns[1][4]),
      self._get_text_only_ckbtn("--tables",
                                ui._enum_area_opts_ckbtns[2][0]),
      self._get_text_only_ckbtn("--columns",
                                ui._enum_area_opts_ckbtns[2][1]),
      self._get_text_only_ckbtn("--schema",
                                ui._enum_area_opts_ckbtns[2][2]),
      self._get_text_only_ckbtn("--count",
                                ui._enum_area_opts_ckbtns[2][3]),
      self._get_text_only_ckbtn("--comments",
                                ui._enum_area_opts_ckbtns[2][4]),
      self._get_text_only_ckbtn("--dump",
                                ui._dump_area_dump_ckbtn),
      self._get_text_only_ckbtn("--dump-all",
                                ui._dump_area_dump_all_ckbtn),
      self._get_text_only_ckbtn("--search",
                                ui._dump_area_search_ckbtn),
      self._get_text_only_ckbtn("--exclude-sysdb",
                                ui._dump_area_no_sys_db_ckbtn),
      self._get_text_from_entry("--start=",
                                ui._limit_area_start_ckbtn,
                                ui._limit_area_start_entry),
      self._get_text_from_entry("--stop=",
                                ui._limit_area_stop_ckbtn,
                                ui._limit_area_stop_entry),
      self._get_text_from_entry("--first=",
                                ui._blind_area_first_ckbtn,
                                ui._blind_area_first_entry),
      self._get_text_from_entry("--last=",
                                ui._blind_area_last_ckbtn,
                                ui._blind_area_last_ckbtn),
      self._get_text_from_entry("-D ",
                                ui._meta_area_D_ckbtn,
                                ui._meta_area_D_entry),
      self._get_text_from_entry("-T ",
                                ui._meta_area_T_ckbtn,
                                ui._meta_area_T_entry),
      self._get_text_from_entry("-C ",
                                ui._meta_area_C_ckbtn,
                                ui._meta_area_C_entry),
      self._get_text_from_entry("-U ",
                                ui._meta_area_U_ckbtn,
                                ui._meta_area_U_entry),
      self._get_text_from_entry("-X ",
                                ui._meta_area_X_ckbtn,
                                ui._meta_area_X_entry),
      self._get_text_from_entry("--pivot-column=",
                                ui._meta_area_pivot_ckbtn,
                                ui._meta_area_pivot_entry),
      self._get_text_from_entry("--where=",
                                ui._meta_area_where_ckbtn,
                                ui._meta_area_where_entry),
      self._get_text_from_entry("--sql-query=",
                                ui._runsql_area_sql_query_ckbtn,
                                ui._runsql_area_sql_query_entry),
      self._get_text_from_entry("--sql-file=",
                                ui._runsql_area_sql_file_ckbtn,
                                ui._runsql_area_sql_file_entry),
      self._get_text_only_ckbtn("--common-tables",
                                ui._brute_force_area_common_tables_ckbtn),
      self._get_text_only_ckbtn("--common-columns",
                                ui._brute_force_area_common_columns_ckbtn),
    ]

    self._request_opts = [
      self._get_text_only_ckbtn("--random-agent",
                                ui._request_area_random_agent_ckbtn),
      self._get_text_from_entry("--user-agent=",
                                ui._request_area_user_agent_ckbtn,
                                ui._request_area_user_agent_entry),
      self._get_text_from_entry("--host=",
                                ui._request_area_host_ckbtn,
                                ui._request_area_host_entry),
      self._get_text_from_entry("--referer=",
                                ui._request_area_referer_ckbtn,
                                ui._request_area_referer_entry),
      self._get_text_from_entry("--header=",
                                ui._request_area_header_ckbtn,
                                ui._request_area_header_entry),
      self._get_text_from_entry("--headers=",
                                ui._request_area_headers_ckbtn,
                                ui._request_area_headers_entry),
      self._get_text_from_entry("--method=",
                                ui._request_area_method_ckbtn,
                                ui._request_area_method_entry),
      self._get_text_from_entry("--param-del=",
                                ui._request_area_param_del_ckbtn,
                                ui._request_area_param_del_entry),
      self._get_text_from_entry("--data=",
                                ui._request_area_post_ckbtn,
                                ui._request_area_post_entry),
      self._get_text_from_entry("--cookie=",
                                ui._request_area_cookie_ckbtn,
                                ui._request_area_cookie_entry),
      self._get_text_from_entry("--cookie-del=",
                                ui._request_area_cookie_del_ckbtn,
                                ui._request_area_cookie_del_entry),
      self._get_text_from_entry("--load-cookies=",
                                ui._request_area_load_cookies_ckbtn,
                                ui._request_area_load_cookies_entry),
      self._get_text_only_ckbtn("--drop-set-cookie",
                                ui._request_area_drop_set_cookie_ckbtn),
      self._get_text_from_entry("--auth-type=",
                                ui._request_area_auth_type_ckbtn,
                                ui._request_area_auth_type_entry),
      self._get_text_from_entry("--auth-cred=",
                                ui._request_area_auth_cred_ckbtn,
                                ui._request_area_auth_cred_entry),
      self._get_text_from_entry("--auth-file=",
                                ui._request_area_auth_file_ckbtn,
                                ui._request_area_auth_file_entry),
      self._get_text_from_entry("--csrf-token=",
                                ui._request_area_csrf_token_ckbtn,
                                ui._request_area_csrf_token_entry),
      self._get_text_from_entry("--csrf-url=",
                                ui._request_area_csrf_url_ckbtn,
                                ui._request_area_csrf_url_entry),
      self._get_text_only_ckbtn("--ignore-redirects",
                                ui._request_area_ignore_redirects_ckbtn),
      self._get_text_only_ckbtn("--ignore-timeouts",
                                ui._request_area_ignore_timeouts_ckbtn),
      self._get_text_from_entry("--ignore-code=",
                                ui._request_area_ignore_code_ckbtn,
                                ui._request_area_ignore_code_entry),
      self._get_text_only_ckbtn("--skip-urlencode",
                                ui._request_area_skip_urlencode_ckbtn),
      self._get_text_only_ckbtn("--force-ssl",
                                ui._request_area_force_ssl_ckbtn),
      self._get_text_only_ckbtn("--hpp",
                                ui._request_area_hpp_ckbtn),
      self._get_text_from_entry("--delay=",
                                ui._request_area_delay_ckbtn,
                                ui._request_area_delay_entry),
      self._get_text_from_entry("--timeout=",
                                ui._request_area_timeout_ckbtn,
                                ui._request_area_timeout_entry),
      self._get_text_from_entry("--retries=",
                                ui._request_area_retries_ckbtn,
                                ui._request_area_retries_entry),
      self._get_text_from_entry("--randomize=",
                                ui._request_area_randomize_ckbtn,
                                ui._request_area_randomize_entry),
      self._get_text_from_entry("--eval=",
                                ui._request_area_eval_ckbtn,
                                ui._request_area_eval_entry),
      self._get_text_from_entry("--safe-url=",
                                ui._request_area_safe_url_ckbtn,
                                ui._request_area_safe_url_entry),
      self._get_text_from_entry("--safe-post=",
                                ui._request_area_safe_post_ckbtn,
                                ui._request_area_safe_post_entry),
      self._get_text_from_entry("--safe-req=",
                                ui._request_area_safe_req_ckbtn,
                                ui._request_area_safe_req_entry),
      self._get_text_from_entry("--safe-freq=",
                                ui._request_area_safe_freq_ckbtn,
                                ui._request_area_safe_freq_entry),
      self._get_text_only_ckbtn("--ignore-proxy",
                                ui._request_area_ignore_proxy_ckbtn),
      self._get_http_proxy(),
      self._get_http_proxy_cred(),
      self._get_text_from_entry("--proxy-file=",
                                ui._request_area_proxy_file_ckbtn,
                                ui._request_area_proxy_file_entry),
      self._get_text_only_ckbtn("--tor",
                                ui._request_area_tor_ckbtn),
      self._get_text_from_entry("--tor-port=",
                                ui._request_area_tor_port_ckbtn,
                                ui._request_area_tor_port_entry),
      self._get_text_from_entry("--tor-type=",
                                ui._request_area_tor_type_ckbtn,
                                ui._request_area_tor_type_entry),
      self._get_text_only_ckbtn("--check-tor",
                                ui._request_area_check_tor_ckbtn),
    ]

    self._setting_opts = [
      self._get_text_from_entry("-p ",
                                ui._inject_area_param_ckbtn,
                                ui._inject_area_param_entry),
      self._get_text_only_ckbtn("--skip-static",
                                ui._inject_area_skip_static_ckbtn),
      self._get_text_from_entry("--prefix=",
                                ui._inject_area_prefix_ckbtn,
                                ui._inject_area_prefix_entry),
      self._get_text_from_entry("--suffix=",
                                ui._inject_area_suffix_ckbtn,
                                ui._inject_area_suffix_entry),
      self._get_text_from_entry("--skip=",
                                ui._inject_area_skip_ckbtn,
                                ui._inject_area_skip_entry),
      self._get_text_from_entry("--para-exclude=",
                                ui._inject_area_param_exclude_ckbtn,
                                ui._inject_area_param_exclude_entry),
      self._get_text_from_entry("--dbms=",
                                ui._inject_area_dbms_ckbtn,
                                ui._inject_area_dbms_combobox.get_child()),
      self._get_text_from_entry("--dbms-cred=",
                                ui._inject_area_dbms_cred_ckbtn,
                                ui._inject_area_dbms_cred_entry),
      self._get_text_from_entry("--os=",
                                ui._inject_area_os_ckbtn,
                                ui._inject_area_os_entry),
      self._get_text_only_ckbtn("--no-cast",
                                ui._inject_area_no_cast_ckbtn),
      self._get_text_only_ckbtn("--no-escape",
                                ui._inject_area_no_escape_ckbtn),
      self._get_text_only_ckbtn("--invalid-logic",
                                ui._inject_area_invalid_logic_ckbtn),
      self._get_text_only_ckbtn("--invalid-bignum",
                                ui._inject_area_invalid_bignum_ckbtn),
      self._get_text_only_ckbtn("--invalid-str",
                                ui._inject_area_invalid_str_ckbtn),
      self._get_text_from_scale("--level=",
                                ui._detection_area_level_ckbtn,
                                ui._detection_area_level_scale),
      self._get_text_only_ckbtn("--text-only",
                                ui._detection_area_text_only_ckbtn),
      self._get_text_from_scale("--risk=",
                                ui._detection_area_risk_ckbtn,
                                ui._detection_area_risk_scale),
      self._get_text_only_ckbtn("--titles",
                                ui._detection_area_titles_ckbtn),
      self._get_text_from_entry("--string=",
                                ui._detection_area_str_ckbtn,
                                ui._detection_area_str_entry),
      self._get_text_from_entry("--not-string=",
                                ui._detection_area_not_str_ckbtn,
                                ui._detection_area_not_str_entry),
      self._get_text_from_entry("--regexp=",
                                ui._detection_area_re_ckbtn,
                                ui._detection_area_re_entry),
      self._get_text_from_entry("--code=",
                                ui._detection_area_code_ckbtn,
                                ui._detection_area_code_entry),
      self._get_text_from_entry("--technique=",
                                ui._tech_area_tech_ckbtn,
                                ui._tech_area_tech_entry),
      self._get_text_from_entry("--time-sec=",
                                ui._tech_area_time_sec_ckbtn,
                                ui._tech_area_time_sec_entry),
      self._get_text_from_entry("--union-cols=",
                                ui._tech_area_union_col_ckbtn,
                                ui._tech_area_union_col_entry),
      self._get_text_from_entry("--union-char=",
                                ui._tech_area_union_chr_ckbtn,
                                ui._tech_area_union_chr_entry),
      self._get_text_from_entry("--union-from=",
                                ui._tech_area_union_from_ckbtn,
                                ui._tech_area_union_from_entry),
      self._get_text_from_entry("--dns-domain=",
                                ui._tech_area_dns_ckbtn,
                                ui._tech_area_dns_entry),
      self._get_text_from_entry("--second-url=",
                                ui._tech_area_second_url_ckbtn,
                                ui._tech_area_second_url_entry),
      self._get_text_from_entry("--second-req=",
                                ui._tech_area_second_req_ckbtn,
                                ui._tech_area_second_req_entry),
      self._get_text_only_ckbtn("-o",
                                ui._optimize_area_turn_all_ckbtn),
      self._get_text_from_entry("--threads=",
                                ui._optimize_area_thread_num_ckbtn,
                                ui._optimize_area_thread_num_spinbtn, None),
      self._get_text_only_ckbtn("--predict-output",
                                ui._optimize_area_predict_ckbtn),
      self._get_text_only_ckbtn("--keep-alive",
                                ui._optimize_area_keep_alive_ckbtn),
      self._get_text_only_ckbtn("--null-connection",
                                ui._optimize_area_null_connect_ckbtn),
      self._get_text_from_scale("-v ",
                                ui._general_area_verbose_ckbtn,
                                ui._general_area_verbose_scale),
      self._get_text_only_ckbtn("--fingerprint",
                                ui._general_area_finger_ckbtn),
      self._get_text_only_ckbtn("--hex",
                                ui._general_area_hex_ckbtn),
      self._get_text_only_ckbtn("--batch",
                                ui._general_area_batch_ckbtn),
      self._get_tampers(),
    ]

  def _get_http_proxy_cred(self):
    ui = self._w

    _use_proxy = ui._request_area_proxy_ckbtn.get_active()
    _username = ui._request_area_proxy_username_entry.get_text()
    _pass = ui._request_area_proxy_password_entry.get_text()

    if all((_use_proxy, _username, _pass)) :
      return "".join((" --proxy-cred='", _username, ":", _pass, "'"))
    return ''

  def _get_http_proxy(self):
    ui = self._w

    _use_proxy = ui._request_area_proxy_ckbtn.get_active()
    _ip = ui._request_area_proxy_ip_entry.get_text()
    _port = ui._request_area_proxy_port_entry.get_text()

    if _use_proxy and _ip:
      if _port:
        return "".join((" --proxy='", _ip, ":", _port, "'"))
      else:
        return "".join((" --proxy='", _ip, "'"))
    return ''

  def _get_tampers(self):
    ''' --tamper=TAMPER     Use given script(s) for tampering injection data '''

    _tamper_textbuffer = self._w._tamper_area_tamper_textbuffer
    _tampers = ''

    _start_iter = _tamper_textbuffer.get_start_iter()
    _end_iter = _tamper_textbuffer.get_end_iter()
    for _tamper_tmp in _tamper_textbuffer.get_text(_start_iter, _end_iter, False).splitlines():
      if _tamper_tmp.strip():
        _tampers = _tampers + _tamper_tmp.strip() + ','

    if _tampers:
      return " --tamper='" + _tampers.rstrip(',') + "'"
    return ''

  def _get_text_from_scale(self, opt_str, ckbtn, scale):
    if ckbtn.get_active():
      return ''.join((' ', opt_str, str(int(scale.get_value()))))
    return ''

  def _get_text_only_ckbtn(self, opt_str, ckbtn):
    if ckbtn.get_active():
      return ''.join((' ', opt_str))
    return ''

  def _get_text_from_entry(self, opt_str, ckbtn, entry, quote = "'"):
    if ckbtn.get_active() and entry.get_text():
      if quote:
        return ''.join((' ', opt_str, quote, entry.get_text(), quote))
      else:
        return ''.join((' ', opt_str, entry.get_text()))
    return ''


def main():
  from gtk3_header import Gtk as g
  from sqlmap_ui import UI_Window

  win = UI_Window()
  win.connect('destroy', g.main_quit)
  win.show_all()
  g.main()


if __name__ == '__main__':
  main()
