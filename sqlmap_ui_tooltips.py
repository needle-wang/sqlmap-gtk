#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 10月 23日 星期二 05:24:32 CST


class Widget_Mesg(object):
  def __init__(self, w):
    '''
    w: sqlmap_ui.UI_Window
    '''
    self._w = w

  def set_all_tooltips(self):
    ui = self._w

    # 一、选项区(page1)
    # 0.target区
    self._set_tooltip('必填项, 从 目标url/burp日志/HTTP请求... 任选一项',
                      ui._url_combobox)
    self._set_tooltip('-l: Burp或WebScarab代理的日志文件路径(用来解析目标)',
                      ui._burp_logfile)
    self._set_tooltip('-r: 包含HTTP请求的的文件路径(如从fiddler中得来的)',
                      ui._request_file)
    self._set_tooltip('-m: 给定一个包含多个目标的文本路径',
                      ui._bulkfile)
    self._set_tooltip('-c: 从一个本地ini配置文件载入选项',
                      ui._configfile)
    self._set_tooltip('-x: 远程sitemap(.xml)文件的url(用来解析目标)',
                      ui._sitemap_url)
    self._set_tooltip('-g: 将google dork的结果作为目标url',
                      ui._google_dork)
    # 1.测试页面
    self._set_tooltip('-p TESTPARAMETER\tTestable parameter(s)',
                      ui._inject_area_param_ckbtn,
                      ui._inject_area_param_entry)
    self._set_tooltip('--skip-static\tSkip testing parameters that not appear to be dynamic',
                      ui._inject_area_skip_static_ckbtn)
    self._set_tooltip('--skip=...,...\tSkip testing for given parameter(s)',
                      ui._inject_area_skip_ckbtn,
                      ui._inject_area_skip_entry)
    self._set_tooltip('--param-exclude=.. Regexp to exclude parameters from testing',
                      ui._inject_area_param_exclude_ckbtn,
                      ui._inject_area_param_exclude_entry)
    self._set_tooltip('--dbms=DBMS\tForce back-end DBMS to provided value',
                      ui._inject_area_dbms_ckbtn,
                      ui._inject_area_dbms_combobox)
    self._set_tooltip('--dbms-cred=DBMS..  DBMS authentication credentials (user:password)',
                      ui._inject_area_dbms_cred_ckbtn,
                      ui._inject_area_dbms_cred_entry)
    self._set_tooltip('--os=OS\tForce back-end DBMS operating system to provided value',
                      ui._inject_area_os_ckbtn,
                      ui._inject_area_os_entry)
    self._set_tooltip('--invalid-bignum    Use big numbers for invalidating values',
                      ui._inject_area_invalid_bignum_ckbtn)
    self._set_tooltip('--invalid-logical\tUse logical operations for invalidating values',
                      ui._inject_area_invalid_logic_ckbtn)
    self._set_tooltip('--invalid-string    Use random strings for invalidating values',
                      ui._inject_area_invalid_str_ckbtn)
    self._set_tooltip('--no-cast\tTurn off payload casting mechanism',
                      ui._inject_area_no_cast_ckbtn)
    self._set_tooltip('--no-escape\tTurn off string escaping mechanism',
                      ui._inject_area_no_escape_ckbtn)
    self._set_tooltip('--prefix=PREFIX\tInjection payload prefix string',
                      ui._inject_area_prefix_ckbtn,
                      ui._inject_area_prefix_entry)
    self._set_tooltip('--suffix=SUFFIX\tInjection payload suffix string',
                      ui._inject_area_suffix_ckbtn,
                      ui._inject_area_suffix_entry)
    self._set_tooltip('--level=默认为1',
                      ui._detection_area_level_ckbtn,
                      ui._detection_area_level_combobox)
    self._set_tooltip('--text-only',
                      ui._detection_area_text_only_ckbtn)
    self._set_tooltip('--risk=默认为1',
                      ui._detection_area_risk_ckbtn,
                      ui._detection_area_risk_combobox)
    self._set_tooltip('--titles',
                      ui._detection_area_titles_ckbtn)
    self._set_tooltip('--string=STRING\tString to match when query is evaluated to True',
                      ui._detection_area_str_ckbtn,
                      ui._detection_area_str_entry)
    self._set_tooltip('--not-string=NOT..  String to match when query is evaluated to False',
                      ui._detection_area_not_str_ckbtn,
                      ui._detection_area_not_str_entry)
    self._set_tooltip('--regexp=',
                      ui._detection_area_re_ckbtn,
                      ui._detection_area_re_entry)
    self._set_tooltip('--code=',
                      ui._detection_area_code_ckbtn,
                      ui._detection_area_code_entry)
    self._set_tooltip('--technique=',
                      ui._tech_area_tech_ckbtn,
                      ui._tech_area_tech_entry)
    self._set_tooltip('--time-sec=默认为5',
                      ui._tech_area_time_sec_ckbtn,
                      ui._tech_area_time_sec_entry)
    self._set_tooltip('--union-cols=',
                      ui._tech_area_union_col_ckbtn,
                      ui._tech_area_union_col_entry)
    self._set_tooltip('--union-char=',
                      ui._tech_area_union_chr_ckbtn,
                      ui._tech_area_union_chr_entry)
    self._set_tooltip('--union-from=',
                      ui._tech_area_union_from_ckbtn,
                      ui._tech_area_union_from_entry)
    self._set_tooltip('--dns-domain=',
                      ui._tech_area_dns_ckbtn,
                      ui._tech_area_dns_entry)
    self._set_tooltip('--second-url=',
                      ui._tech_area_second_url_ckbtn,
                      ui._tech_area_second_url_entry)
    self._set_tooltip('--second-req=',
                      ui._tech_area_second_req_ckbtn,
                      ui._tech_area_second_req_entry)
    self._set_tooltip('此处填写要使用的tamper脚本名\n详见: sqlmap --list-tamper\n回车或逗号拼接',
                      ui._tamper_area)
    self._set_tooltip('-o',
                      ui._optimize_area_turn_all_ckbtn)
    self._set_tooltip('--threads=默认为1',
                      ui._optimize_area_thread_num_ckbtn,
                      ui._optimize_area_thread_num_combobox)
    self._set_tooltip('--predict-output',
                      ui._optimize_area_predict_ckbtn)
    self._set_tooltip('--keep-alive',
                      ui._optimize_area_keep_alive_ckbtn)
    self._set_tooltip('--null-connection',
                      ui._optimize_area_null_connect_ckbtn)
    self._set_tooltip('-v 默认为1',
                      ui._general_area_verbose_ckbtn,
                      ui._general_area_verbose_entry)
    self._set_tooltip('--fingerprint',
                      ui._general_area_finger_ckbtn)
    self._set_tooltip('--hex',
                      ui._general_area_hex_ckbtn)
    self._set_tooltip('--batch',
                      ui._general_area_batch_ckbtn)
    # 2.请求页面
    self._set_tooltip('--random-agent',
                      ui._request_area_random_agent_ckbtn)
    self._set_tooltip('--user-agent=',
                      ui._request_area_user_agent_ckbtn,
                      ui._request_area_user_agent_entry)
    self._set_tooltip('--host=',
                      ui._request_area_host_ckbtn,
                      ui._request_area_host_entry)
    self._set_tooltip('--referer=',
                      ui._request_area_referer_ckbtn,
                      ui._request_area_referer_entry)
    self._set_tooltip('--header=',
                      ui._request_area_header_ckbtn,
                      ui._request_area_header_entry)
    self._set_tooltip('--headers=',
                      ui._request_area_headers_ckbtn,
                      ui._request_area_headers_entry)
    self._set_tooltip('--method=',
                      ui._request_area_method_ckbtn,
                      ui._request_area_method_entry)
    self._set_tooltip('--param-del=',
                      ui._request_area_param_del_ckbtn,
                      ui._request_area_param_del_entry)
    self._set_tooltip('--data=(填数据, 不是填文件路径哈)',
                      ui._request_area_post_ckbtn,
                      ui._request_area_post_entry)
    self._set_tooltip('--cookie=填数据, 不是填文件名哈',
                      ui._request_area_cookie_ckbtn,
                      ui._request_area_cookie_entry)
    self._set_tooltip('--cookie-del=',
                      ui._request_area_cookie_ckbtn,
                      ui._request_area_cookie_entry)
    self._set_tooltip('--load-cookies=',
                      ui._request_area_load_cookies_ckbtn,
                      ui._request_area_load_cookies_entry)
    self._set_tooltip('--drop-set-cookie=',
                      ui._request_area_drop_set_cookie_ckbtn)
    self._set_tooltip('--auth-type=Basic, Digest, NTLM or PKI',
                      ui._request_area_auth_type_ckbtn,
                      ui._request_area_auth_type_entry)
    self._set_tooltip('--auth-cred=',
                      ui._request_area_auth_cred_ckbtn,
                      ui._request_area_auth_cred_entry)
    self._set_tooltip('--auth-file=',
                      ui._request_area_auth_file_ckbtn,
                      ui._request_area_auth_file_entry)
    self._set_tooltip('--csrf-token=',
                      ui._request_area_csrf_token_ckbtn,
                      ui._request_area_csrf_token_entry)
    self._set_tooltip('--csrf-url=',
                      ui._request_area_csrf_url_ckbtn,
                      ui._request_area_csrf_url_entry)
    self._set_tooltip('--ignore-redirects',
                      ui._request_area_ignore_redirects_ckbtn)
    self._set_tooltip('--ignore-timeouts',
                      ui._request_area_ignore_timeouts_ckbtn)
    self._set_tooltip('--ignore-code=',
                      ui._request_area_ignore_code_ckbtn,
                      ui._request_area_ignore_code_entry)
    self._set_tooltip('--skip-urlencode',
                      ui._request_area_skip_urlencode_ckbtn)
    self._set_tooltip('--force-ssl',
                      ui._request_area_force_ssl_ckbtn)
    self._set_tooltip('--hpp',
                      ui._request_area_hpp_ckbtn)
    self._set_tooltip('隔几秒发送一个HTTP请求',
                      ui._request_area_delay_ckbtn,
                      ui._request_area_delay_entry)
    self._set_tooltip('--timeout=',
                      ui._request_area_timeout_ckbtn,
                      ui._request_area_timeout_entry)
    self._set_tooltip('--retries=连接超时后的重连次数',
                      ui._request_area_retries_ckbtn,
                      ui._request_area_retries_entry)
    self._set_tooltip('--randomize=',
                      ui._request_area_randomize_ckbtn,
                      ui._request_area_randomize_entry)
    self._set_tooltip('--eval=发送请求前先进行额外的处理(python code), 如:\n'
                      'import hashlib;id2=hashlib.md5(id).hexdigest()',
                      ui._request_area_eval_ckbtn,
                      ui._request_area_eval_entry)
    self._set_tooltip('--safe-url=',
                      ui._request_area_safe_url_ckbtn,
                      ui._request_area_safe_url_entry)
    self._set_tooltip('--safe-post=',
                      ui._request_area_safe_post_ckbtn,
                      ui._request_area_safe_post_entry)
    self._set_tooltip('--safe-req=',
                      ui._request_area_safe_req_ckbtn,
                      ui._request_area_safe_req_entry)
    self._set_tooltip('--safe-freq=',
                      ui._request_area_safe_freq_ckbtn,
                      ui._request_area_safe_freq_entry)
    self._set_tooltip('--ignore-proxy',
                      ui._request_area_ignore_proxy_ckbtn)
    self._set_tooltip('--proxy=',
                      ui._request_area_proxy_ckbtn,
                      ui._request_area_proxy_ip_label,
                      ui._request_area_proxy_ip_entry,
                      ui._request_area_proxy_port_label,
                      ui._request_area_proxy_port_entry)
    self._set_tooltip('--proxy-file=',
                      ui._request_area_proxy_file_ckbtn,
                      ui._request_area_proxy_file_entry)
    self._set_tooltip('--proxy-cred=',
                      ui._request_area_proxy_username_label,
                      ui._request_area_proxy_username_entry,
                      ui._request_area_proxy_password_label,
                      ui._request_area_proxy_password_entry)
    self._set_tooltip('--tor',
                      ui._request_area_tor_ckbtn)
    self._set_tooltip('--tor-port=',
                      ui._request_area_tor_port_ckbtn,
                      ui._request_area_tor_port_entry)
    self._set_tooltip('--tor-type=',
                      ui._request_area_tor_type_ckbtn,
                      ui._request_area_tor_type_entry)
    self._set_tooltip('--check-tor',
                      ui._request_area_check_tor_ckbtn)
    # 3.枚举页面
    self._set_tooltip('-b',
                      ui._enum_area_opts_ckbtns[0][0])
    self._set_tooltip('--current-user',
                      ui._enum_area_opts_ckbtns[0][1])
    self._set_tooltip('--current-db',
                      ui._enum_area_opts_ckbtns[0][2])
    self._set_tooltip('--hostname',
                      ui._enum_area_opts_ckbtns[0][3])
    self._set_tooltip('--is-dba',
                      ui._enum_area_opts_ckbtns[0][4])
    self._set_tooltip('--users',
                      ui._enum_area_opts_ckbtns[1][0])
    self._set_tooltip('--passwords',
                      ui._enum_area_opts_ckbtns[1][1])
    self._set_tooltip('--privileges',
                      ui._enum_area_opts_ckbtns[1][2])
    self._set_tooltip('--roles',
                      ui._enum_area_opts_ckbtns[1][3])
    self._set_tooltip('--dbs',
                      ui._enum_area_opts_ckbtns[1][4])
    self._set_tooltip('--tables',
                      ui._enum_area_opts_ckbtns[2][0])
    self._set_tooltip('--columns',
                      ui._enum_area_opts_ckbtns[2][1])
    self._set_tooltip('--schema',
                      ui._enum_area_opts_ckbtns[2][2])
    self._set_tooltip('--count',
                      ui._enum_area_opts_ckbtns[2][3])
    self._set_tooltip('--comments',
                      ui._enum_area_opts_ckbtns[2][4])
    self._set_tooltip('--dump',
                      ui._dump_area_dump_ckbtn)
    self._set_tooltip('--dump-all',
                      ui._dump_area_dump_all_ckbtn)
    self._set_tooltip('--search',
                      ui._dump_area_search_ckbtn)
    self._set_tooltip('--exclude-sysdb',
                      ui._dump_area_no_sys_db_ckbtn)
    self._set_tooltip('--start=',
                      ui._limit_area_start_ckbtn,
                      ui._limit_area_start_entry)
    self._set_tooltip('--stop=',
                      ui._limit_area_stop_ckbtn,
                      ui._limit_area_stop_entry)
    self._set_tooltip('--first=',
                      ui._blind_area_first_ckbtn,
                      ui._blind_area_first_entry)
    self._set_tooltip('--last=',
                      ui._blind_area_last_ckbtn,
                      ui._blind_area_last_entry)
    self._set_tooltip('-D DB',
                      ui._meta_area_D_ckbtn,
                      ui._meta_area_D_entry)
    self._set_tooltip('-T TBL',
                      ui._meta_area_T_ckbtn,
                      ui._meta_area_T_entry)
    self._set_tooltip('-C COL',
                      ui._meta_area_C_ckbtn,
                      ui._meta_area_C_entry)
    self._set_tooltip('-U USER',
                      ui._meta_area_U_ckbtn,
                      ui._meta_area_U_entry)
    self._set_tooltip('-X EXCLUDE',
                      ui._meta_area_X_ckbtn,
                      ui._meta_area_X_entry)
    self._set_tooltip('--pivot-column=P..',
                      ui._meta_area_pivot_ckbtn,
                      ui._meta_area_pivot_entry)
    self._set_tooltip('--where=',
                      ui._meta_area_where_ckbtn,
                      ui._meta_area_where_entry)
    self._set_tooltip('--sql-query=QUERY',
                      ui._runsql_area_sql_query_ckbtn,
                      ui._runsql_area_sql_query_entry)
    self._set_tooltip('--sql-file=SQLFILE',
                      ui._runsql_area_sql_file_ckbtn,
                      ui._runsql_area_sql_file_entry)
    self._set_tooltip('--common-tables',
                      ui._brute_force_area_common_tables_ckbtn)
    self._set_tooltip('--common-columns',
                      ui._brute_force_area_common_columns_ckbtn)
    # 4.文件页面
    self._set_tooltip('远程DB所在服务器上的文件路径',
                      ui._file_read_area_file_read_ckbtn,
                      ui._file_read_area_file_read_entry)
    self._set_tooltip('只能查看已下载到本地的文件',
                      ui._file_read_area_file_btn)
    self._set_tooltip('--udf-inject',
                      ui._file_write_area_udf_ckbtn)
    self._set_tooltip('与--udf-inject配套使用, 可选',
                      ui._file_write_area_shared_lib_ckbtn,
                      ui._file_write_area_shared_lib_entry)
    self._set_tooltip('若使用此选项, 则--file-dest为必选项',
                      ui._file_write_area_file_write_ckbtn,
                      ui._file_write_area_file_write_entry)
    self._set_tooltip('上传到DB服务器中的文件名, 要求是绝对路径, 构造后会有引号!\n'
                      '与本地文件路径配套使用, 单独勾选无意义',
                      ui._file_write_area_file_dest_ckbtn,
                      ui._file_write_area_file_dest_entry)
    self._set_tooltip('--os-cmd=',
                      ui._file_os_access_os_cmd_ckbtn,
                      ui._file_os_access_os_cmd_entry)
    self._set_tooltip('--os-shell',
                      ui._file_os_access_os_shell_ckbtn)
    self._set_tooltip('Prompt for an OOB shell, Meterpreter or VNC',
                      ui._file_os_access_os_pwn_ckbtn)
    self._set_tooltip('--os-smbrelay',
                      ui._file_os_access_os_smbrelay_ckbtn)
    self._set_tooltip('--os-bof',
                      ui._file_os_access_os_bof_ckbtn)
    self._set_tooltip('--priv-esc',
                      ui._file_os_access_priv_esc_ckbtn)
    self._set_tooltip('--msf-path=MSFPATH Local path where Metasploit Framework is installed',
                      ui._file_os_access_msf_path_ckbtn,
                      ui._file_os_access_msf_path_entry)
    self._set_tooltip('--tmp-path=TMPPATH Remote absolute path of temporary files directory',
                      ui._file_os_access_tmp_path_ckbtn,
                      ui._file_os_access_tmp_path_entry)
    self._set_tooltip('--reg-read',
                      ui._file_os_registry_reg_read_ckbtn)
    self._set_tooltip('--reg-add',
                      ui._file_os_registry_reg_add_ckbtn)
    self._set_tooltip('--reg-del',
                      ui._file_os_registry_reg_del_ckbtn)
    self._set_tooltip('--reg-key=',
                      ui._file_os_registry_reg_key_ckbtn,
                      ui._file_os_registry_reg_key_entry)
    self._set_tooltip('--reg-value=',
                      ui._file_os_registry_reg_value_ckbtn,
                      ui._file_os_registry_reg_value_entry)
    self._set_tooltip('--reg-data=',
                      ui._file_os_registry_reg_data_ckbtn,
                      ui._file_os_registry_reg_data_entry)
    self._set_tooltip('--reg-type=',
                      ui._file_os_registry_reg_type_ckbtn,
                      ui._file_os_registry_reg_type_entry)
    # 5.其他页面
    self._set_tooltip('--check-internet',
                      ui._page1_general_check_internet_ckbtn)
    self._set_tooltip('--fresh-queries',
                      ui._page1_general_fresh_queries_ckbtn)
    self._set_tooltip('--flush-session',
                      ui._page1_general_flush_session_ckbtn)
    self._set_tooltip('--eta',
                      ui._page1_general_eta_ckbtn)
    self._set_tooltip('--binary-fields=',
                      ui._page1_general_binary_fields_ckbtn,
                      ui._page1_general_binary_fields_entry)
    self._set_tooltip('--forms',
                      ui._page1_general_forms_ckbtn)
    self._set_tooltip('--parse-errors',
                      ui._page1_general_parse_errors_ckbtn)
    self._set_tooltip('--cleanup',
                      ui._page1_misc_cleanup_ckbtn)
    self._set_tooltip('--crawl=',
                      ui._page1_general_crawl_ckbtn,
                      ui._page1_general_crawl_entry)
    self._set_tooltip('--crawl-exclude=',
                      ui._page1_general_crawl_exclude_ckbtn,
                      ui._page1_general_crawl_exclude_entry)
    self._set_tooltip('--charset=',
                      ui._page1_general_charset_ckbtn,
                      ui._page1_general_charset_entry)
    self._set_tooltip('--encoding=',
                      ui._page1_general_encoding_ckbtn,
                      ui._page1_general_encoding_entry)
    self._set_tooltip('-s SESSIONFILE      Load session from a stored (.sqlite) file',
                      ui._page1_general_session_file_ckbtn,
                      ui._page1_general_session_file_entry)
    self._set_tooltip('--output-dir=',
                      ui._page1_general_output_dir_ckbtn,
                      ui._page1_general_output_dir_entry)
    self._set_tooltip('--dump-format=',
                      ui._page1_general_dump_format_ckbtn,
                      ui._page1_general_dump_format_entry)
    self._set_tooltip('--csv-del=',
                      ui._page1_general_csv_del_ckbtn,
                      ui._page1_general_csv_del_entry)
    self._set_tooltip('-t TRAFFICFILE      Log all HTTP traffic into a textual file',
                      ui._page1_general_traffic_file_ckbtn,
                      ui._page1_general_traffic_file_entry)
    self._set_tooltip('--har=HARFILE       Log all HTTP traffic into a HAR file',
                      ui._page1_general_har_ckbtn,
                      ui._page1_general_har_entry)
    self._set_tooltip('--save=SAVECONFIG Save options to a configuration INI file',
                      ui._page1_general_save_ckbtn,
                      ui._page1_general_save_entry)
    self._set_tooltip('--scope=SCOPE Regexp to filter targets from provided proxy log',
                      ui._page1_general_scope_ckbtn,
                      ui._page1_general_scope_entry)
    self._set_tooltip('--test-filter=TE.. Select tests by payloads and/or titles (e.g. ROW)',
                      ui._page1_general_test_filter_ckbtn,
                      ui._page1_general_test_filter_entry)
    self._set_tooltip('--test-skip=TEST.. Skip tests by payloads and/or titles (e.g. BENCHMARK)',
                      ui._page1_general_test_skip_ckbtn,
                      ui._page1_general_test_skip_entry)
    self._set_tooltip('--web-root=WEBROOT Web server document root directory (e.g. "/var/www")',
                      ui._page1_misc_web_root_ckbtn,
                      ui._page1_misc_web_root_entry)
    self._set_tooltip('--tmp-dir=TMPDIR Local directory for storing temporary files',
                      ui._page1_misc_tmp_dir_ckbtn,
                      ui._page1_misc_tmp_dir_entry)
    self._set_tooltip('--identify-waf',
                      ui._page1_misc_identify_waf_ckbtn)
    self._set_tooltip('--skip-waf',
                      ui._page1_misc_skip_waf_ckbtn)
    self._set_tooltip('--smart',
                      ui._page1_misc_smart_ckbtn)
    self._set_tooltip('--list-tampers',
                      ui._page1_misc_list_tampers_ckbtn)
    self._set_tooltip('--disable-coloring',
                      ui._page1_misc_disable_color_ckbtn)
    self._set_tooltip('--offline',
                      ui._page1_misc_offline_ckbtn)
    self._set_tooltip('--mobile',
                      ui._page1_misc_mobile_ckbtn)
    self._set_tooltip('--beep',
                      ui._page1_misc_beep_ckbtn)
    self._set_tooltip('--purge',
                      ui._page1_misc_purge_ckbtn)
    self._set_tooltip('--dependencies',
                      ui._page1_misc_dependencies_ckbtn)
    self._set_tooltip('--update',
                      ui._page1_general_update_ckbtn)
    self._set_tooltip('--answers=ANSWERS Set question answers(e.g. "quit=N,follow=N")',
                      ui._page1_misc_answers_ckbtn,
                      ui._page1_misc_answers_entry)
    self._set_tooltip('--alert=ALERT Run host OS command(s) when SQL injection is found',
                      ui._page1_misc_alert_ckbtn,
                      ui._page1_misc_alert_entry)
    self._set_tooltip('--gpage=GOOGLEPAGE Use Google dork results from specified page number',
                      ui._page1_misc_gpage_ckbtn,
                      ui._page1_misc_gpage_entry)
    self._set_tooltip('-z MNEMONICS Use short mnemonics (e.g. "flu,bat,ban,tec=EU")',
                      ui._page1_misc_z_ckbtn,
                      ui._page1_misc_z_entry)
    # 二、显示区(page2)
    self._set_tooltip('不会动实际的文件',
                      ui._page2_clear_btn)

  def _set_tooltip(self, tooltip, *widgets):
    for _widget in widgets:
      _widget.set_tooltip_text(tooltip)


def main():
  from gtk3_header import Gtk as g
  from sqlmap_ui import UI_Window

  win = UI_Window()
  win.connect('destroy', g.main_quit)
  win.show_all()
  g.main()


if __name__ == '__main__':
  main()
