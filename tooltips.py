#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 10月 23日 星期二 05:24:32 CST


class Widget_Mesg(object):
  def __init__(self, m):
    '''
    m: model.Model
    '''
    self.set_all_tooltips(m)
    self.set_all_placeholders(m)

  def set_all_placeholders(self, m):
    '''
    m: model.Model
    '''
    # 0.target区
    self._set_placeholder('通常是从 目标url/burp日志/HTTP请求... 中任选一项',
                          m._url_combobox.get_child())
    self._set_placeholder('-l: Burp或WebScarab代理的日志文件路径(用来解析目标)',
                          m._burp_logfile)
    self._set_placeholder('-r: 包含HTTP请求的的文件路径(如从fiddler中得来的)',
                          m._request_file)
    self._set_placeholder('-m: 给定一个包含多个目标的文本路径',
                          m._bulkfile)
    self._set_placeholder('-c: 从一个本地ini配置文件载入选项',
                          m._configfile)
    self._set_placeholder('-x: 远程sitemap(.xml)文件的url(用来解析目标)',
                          m._sitemap_url)
    self._set_placeholder('-g: 将google dork的结果作为目标url',
                          m._google_dork)
    # 一、选项区(page1)
    # 1.测试页面
    self._set_placeholder('id',
                          m._inject_area_param_entry)
    self._set_placeholder('用于闭合',
                          m._inject_area_prefix_entry)
    self._set_placeholder('user:password',
                          m._inject_area_dbms_cred_entry)
    self._set_placeholder('查询为真时页面出现的字串',
                          m._detection_area_str_entry)
    self._set_placeholder('查询为假时的',
                          m._detection_area_not_str_entry)
    self._set_placeholder('正则匹配查询为真时的字串',
                          m._detection_area_re_entry)
    self._set_placeholder('查询为真时的',
                          m._detection_area_code_entry)
    self._set_placeholder('BEUSTQ',
                          m._tech_area_tech_entry)
    self._set_placeholder('时间盲注时',
                          m._tech_area_time_sec_entry)
    self._set_placeholder('union查询时',
                          m._tech_area_union_col_entry,
                          m._tech_area_union_chr_entry,
                          m._tech_area_union_from_entry)
    self._set_placeholder('DNS exfiltration',
                          m._tech_area_dns_entry)
    # 2.请求页面
    self._set_placeholder('X-Forwarded-For: 127.0.0.1',
                          m._request_area_header_entry)
    self._set_placeholder('Accept-Language: fr\\nETag: 123',
                          m._request_area_headers_entry)
    self._set_placeholder('post',
                          m._request_area_method_entry)
    self._set_placeholder('Basic, Digest, NTLM or PKI',
                          m._request_area_auth_type_entry)
    self._set_placeholder('name:password',
                          m._request_area_auth_cred_entry)
    self._set_placeholder('PEM cert/private key file',
                          m._request_area_auth_file_entry)
    self._set_placeholder('import hashlib;id2=hashlib.md5(id).hexdigest()',
                          m._request_area_eval_entry)
    # 3.枚举页面
    # 4.文件页面
    # 5.其他页面
    self._set_placeholder('CSV (default), HTML or SQLITE',
                          m._page1_general_dump_format_entry)
    self._set_placeholder('ROW',
                          m._page1_general_test_filter_entry)
    self._set_placeholder('BENCHMARK',
                          m._page1_general_test_skip_entry)
    self._set_placeholder('/var/www',
                          m._page1_misc_web_root_entry)

  def set_all_tooltips(self, m):
    '''
    m: model.Model
    使用gtk3.24时, 有scale组件的行内的tooltip会flicker(闪烁)(GTK3的bug!)
    只能禁用了
    '''
    # 0.target区
    self._set_tooltip('必填项, 从 目标url/burp日志/HTTP请求... 任选一项',
                      m._url_combobox)
    self._set_tooltip('-l: Burp或WebScarab代理的日志文件路径(用来解析目标)',
                      m._burp_logfile)
    self._set_tooltip('-r: 包含HTTP请求的的文件路径(如从fiddler中得来的)',
                      m._request_file)
    self._set_tooltip('-m: 给定一个包含多个目标的文本路径',
                      m._bulkfile)
    self._set_tooltip('-c: 从一个本地ini配置文件载入选项',
                      m._configfile)
    self._set_tooltip('-x: 远程sitemap(.xml)文件的url(用来解析目标)',
                      m._sitemap_url)
    self._set_tooltip('-g: 将google dork的结果作为目标url',
                      m._google_dork)
    # 一、选项区(page1)
    # 0._cmd_entry
    self._set_tooltip('1.勾选, 填写所需的 选项\n2.点击 收集选项\n3.点击 开始',
                      m._cmd_entry)
    # 1.测试页面
    self._set_tooltip('-p TESTPARAMETER\tTestable parameter(s)',
                      m._inject_area_param_ckbtn,
                      m._inject_area_param_entry)
    self._set_tooltip('--skip-static\tSkip testing parameters that not appear to be dynamic',
                      m._inject_area_skip_static_ckbtn)
    self._set_tooltip('--prefix=PREFIX\tInjection payload prefix string',
                      m._inject_area_prefix_ckbtn,
                      m._inject_area_prefix_entry)
    self._set_tooltip('--suffix=SUFFIX\tInjection payload suffix string',
                      m._inject_area_suffix_ckbtn,
                      m._inject_area_suffix_entry)
    self._set_tooltip('--skip=...,...\tSkip testing for given parameter(s)',
                      m._inject_area_skip_ckbtn,
                      m._inject_area_skip_entry)
    self._set_tooltip('--param-exclude=.. Regexp to exclude parameters from testing',
                      m._inject_area_param_exclude_ckbtn,
                      m._inject_area_param_exclude_entry)
    self._set_tooltip('--dbms=DBMS\tForce back-end DBMS to provided value',
                      m._inject_area_dbms_ckbtn,
                      m._inject_area_dbms_combobox)
    self._set_tooltip('--dbms-cred=DBMS..  DBMS authentication credentials (user:password)',
                      m._inject_area_dbms_cred_ckbtn,
                      m._inject_area_dbms_cred_entry)
    self._set_tooltip('--os=OS\tForce back-end DBMS operating system to provided value',
                      m._inject_area_os_ckbtn,
                      m._inject_area_os_entry)
    self._set_tooltip('--no-cast\tTurn off payload casting mechanism',
                      m._inject_area_no_cast_ckbtn)
    self._set_tooltip('--no-escape\tTurn off string escaping mechanism',
                      m._inject_area_no_escape_ckbtn)
    self._set_tooltip('--invalid-logical\tUse logical operations for invalidating values',
                      m._inject_area_invalid_logic_ckbtn)
    self._set_tooltip('--invalid-bignum    Use big numbers for invalidating values',
                      m._inject_area_invalid_bignum_ckbtn)
    self._set_tooltip('--invalid-string    Use random strings for invalidating values',
                      m._inject_area_invalid_str_ckbtn)
    # self._set_tooltip('--level=默认为1',
                      # m._detection_area_level_ckbtn,)
    self._set_tooltip('--text-only',
                      m._detection_area_text_only_ckbtn)
    # self._set_tooltip('--risk=默认为1',
                      # m._detection_area_risk_ckbtn,)
    self._set_tooltip('--titles',
                      m._detection_area_titles_ckbtn)
    self._set_tooltip('--string=STRING\tString to match when query is evaluated to True',
                      m._detection_area_str_ckbtn,
                      m._detection_area_str_entry)
    self._set_tooltip('--not-string=NOT..  String to match when query is evaluated to False',
                      m._detection_area_not_str_ckbtn,
                      m._detection_area_not_str_entry)
    self._set_tooltip('--regexp=',
                      m._detection_area_re_ckbtn,
                      m._detection_area_re_entry)
    self._set_tooltip('--code=',
                      m._detection_area_code_ckbtn,
                      m._detection_area_code_entry)
    self._set_tooltip('--technique=B: Boolean-based blind\n'
                      '            E: Error-based\n'
                      '            U: Union query-based\n'
                      '            S: Stacked queries\n'
                      '            T: Time-based blind\n'
                      '            Q: Inline queries',
                      m._tech_area_tech_ckbtn,
                      m._tech_area_tech_entry)
    self._set_tooltip('--time-sec=默认为5',
                      m._tech_area_time_sec_ckbtn,
                      m._tech_area_time_sec_entry)
    self._set_tooltip('--union-cols=',
                      m._tech_area_union_col_ckbtn,
                      m._tech_area_union_col_entry)
    self._set_tooltip('--union-char=',
                      m._tech_area_union_chr_ckbtn,
                      m._tech_area_union_chr_entry)
    self._set_tooltip('--union-from=',
                      m._tech_area_union_from_ckbtn,
                      m._tech_area_union_from_entry)
    self._set_tooltip('--dns-domain=',
                      m._tech_area_dns_ckbtn,
                      m._tech_area_dns_entry)
    self._set_tooltip('--second-url=',
                      m._tech_area_second_url_ckbtn,
                      m._tech_area_second_url_entry)
    self._set_tooltip('--second-req=',
                      m._tech_area_second_req_ckbtn,
                      m._tech_area_second_req_entry)
    self._set_tooltip('此处填写要使用的tamper脚本名\n详见: sqlmap --list-tamper\n回车或逗号拼接',
                      m._tamper_area_tamper_view)
    self._set_tooltip('-o',
                      m._optimize_area_turn_all_ckbtn)
    self._set_tooltip('--threads=默认为1',
                      m._optimize_area_thread_num_ckbtn)
    self._set_tooltip('--predict-output',
                      m._optimize_area_predict_ckbtn)
    self._set_tooltip('--keep-alive',
                      m._optimize_area_keep_alive_ckbtn)
    self._set_tooltip('--null-connection',
                      m._optimize_area_null_connect_ckbtn)
    # self._set_tooltip('-v 默认为1',
                      # m._general_area_verbose_ckbtn)
    self._set_tooltip('--fingerprint',
                      m._general_area_finger_ckbtn)
    self._set_tooltip('--hex',
                      m._general_area_hex_ckbtn)
    self._set_tooltip('--batch',
                      m._general_area_batch_ckbtn)
    self._set_tooltip('--wizard(其他选项可不选)',
                      m._page1_misc_wizard_ckbtn)
    # 2.请求页面
    self._set_tooltip('--random-agent',
                      m._request_area_random_agent_ckbtn)
    self._set_tooltip('--user-agent=',
                      m._request_area_user_agent_ckbtn,
                      m._request_area_user_agent_entry)
    self._set_tooltip('--host=',
                      m._request_area_host_ckbtn,
                      m._request_area_host_entry)
    self._set_tooltip('--referer=',
                      m._request_area_referer_ckbtn,
                      m._request_area_referer_entry)
    self._set_tooltip('--header=',
                      m._request_area_header_ckbtn,
                      m._request_area_header_entry)
    self._set_tooltip('--headers=',
                      m._request_area_headers_ckbtn,
                      m._request_area_headers_entry)
    self._set_tooltip('--method=',
                      m._request_area_method_ckbtn,
                      m._request_area_method_entry)
    self._set_tooltip('--param-del=',
                      m._request_area_param_del_ckbtn,
                      m._request_area_param_del_entry)
    self._set_tooltip('--data=(填数据, 不是填文件路径哈)',
                      m._request_area_post_ckbtn,
                      m._request_area_post_entry)
    self._set_tooltip('--cookie=填数据, 不是填文件名哈',
                      m._request_area_cookie_ckbtn,
                      m._request_area_cookie_entry)
    self._set_tooltip('--cookie-del=',
                      m._request_area_cookie_del_ckbtn,
                      m._request_area_cookie_del_entry)
    self._set_tooltip('--load-cookies=',
                      m._request_area_load_cookies_ckbtn,
                      m._request_area_load_cookies_entry)
    self._set_tooltip('--drop-set-cookie=',
                      m._request_area_drop_set_cookie_ckbtn)
    self._set_tooltip('--auth-type=Basic, Digest, NTLM or PKI',
                      m._request_area_auth_type_ckbtn,
                      m._request_area_auth_type_entry)
    self._set_tooltip('--auth-cred=',
                      m._request_area_auth_cred_ckbtn,
                      m._request_area_auth_cred_entry)
    self._set_tooltip('--auth-file=',
                      m._request_area_auth_file_ckbtn,
                      m._request_area_auth_file_entry)
    self._set_tooltip('--csrf-token=',
                      m._request_area_csrf_token_ckbtn,
                      m._request_area_csrf_token_entry)
    self._set_tooltip('--csrf-url=',
                      m._request_area_csrf_url_ckbtn,
                      m._request_area_csrf_url_entry)
    self._set_tooltip('--ignore-redirects',
                      m._request_area_ignore_redirects_ckbtn)
    self._set_tooltip('--ignore-timeouts',
                      m._request_area_ignore_timeouts_ckbtn)
    self._set_tooltip('--ignore-code=',
                      m._request_area_ignore_code_ckbtn,
                      m._request_area_ignore_code_entry)
    self._set_tooltip('--skip-urlencode',
                      m._request_area_skip_urlencode_ckbtn)
    self._set_tooltip('--force-ssl',
                      m._request_area_force_ssl_ckbtn)
    self._set_tooltip('--chunked',
                      m._request_area_chunked_ckbtn)
    self._set_tooltip('--hpp',
                      m._request_area_hpp_ckbtn)
    self._set_tooltip('--delay=隔几秒发送一个HTTP请求',
                      m._request_area_delay_ckbtn,
                      m._request_area_delay_entry)
    self._set_tooltip('--timeout=',
                      m._request_area_timeout_ckbtn,
                      m._request_area_timeout_entry)
    self._set_tooltip('--retries=连接超时后的重连次数',
                      m._request_area_retries_ckbtn,
                      m._request_area_retries_entry)
    self._set_tooltip('--randomize=',
                      m._request_area_randomize_ckbtn,
                      m._request_area_randomize_entry)
    self._set_tooltip('--eval=发送请求前先进行额外的处理(python code), 如:\n'
                      'import hashlib;id2=hashlib.md5(id).hexdigest()',
                      m._request_area_eval_ckbtn,
                      m._request_area_eval_entry)
    self._set_tooltip('--safe-url=',
                      m._request_area_safe_url_ckbtn,
                      m._request_area_safe_url_entry)
    self._set_tooltip('--safe-post=',
                      m._request_area_safe_post_ckbtn,
                      m._request_area_safe_post_entry)
    self._set_tooltip('--safe-req=',
                      m._request_area_safe_req_ckbtn,
                      m._request_area_safe_req_entry)
    self._set_tooltip('--safe-freq=SAFE.. Test requests between two visits to a given safe URL',
                      m._request_area_safe_freq_ckbtn,
                      m._request_area_safe_freq_entry)
    self._set_tooltip('--ignore-proxy',
                      m._request_area_ignore_proxy_ckbtn)
    self._set_tooltip('--proxy=',
                      m._request_area_proxy_ckbtn,
                      m._request_area_proxy_ip_label,
                      m._request_area_proxy_ip_entry,
                      m._request_area_proxy_port_label,
                      m._request_area_proxy_port_entry)
    self._set_tooltip('--proxy-file=',
                      m._request_area_proxy_file_ckbtn,
                      m._request_area_proxy_file_entry)
    self._set_tooltip('--proxy-cred=',
                      m._request_area_proxy_username_label,
                      m._request_area_proxy_username_entry,
                      m._request_area_proxy_password_label,
                      m._request_area_proxy_password_entry)
    self._set_tooltip('--tor',
                      m._request_area_tor_ckbtn)
    self._set_tooltip('--tor-port=',
                      m._request_area_tor_port_ckbtn,
                      m._request_area_tor_port_entry)
    self._set_tooltip('--tor-type=',
                      m._request_area_tor_type_ckbtn,
                      m._request_area_tor_type_entry)
    self._set_tooltip('--check-tor',
                      m._request_area_check_tor_ckbtn)
    # 3.枚举页面
    self._set_tooltip('-b',
                      m._enum_area_opts_ckbtns[0][0])
    self._set_tooltip('--current-user',
                      m._enum_area_opts_ckbtns[0][1])
    self._set_tooltip('--current-db',
                      m._enum_area_opts_ckbtns[0][2])
    self._set_tooltip('--hostname',
                      m._enum_area_opts_ckbtns[0][3])
    self._set_tooltip('--is-dba',
                      m._enum_area_opts_ckbtns[0][4])
    self._set_tooltip('--users',
                      m._enum_area_opts_ckbtns[1][0])
    self._set_tooltip('--passwords',
                      m._enum_area_opts_ckbtns[1][1])
    self._set_tooltip('--privileges',
                      m._enum_area_opts_ckbtns[1][2])
    self._set_tooltip('--roles',
                      m._enum_area_opts_ckbtns[1][3])
    self._set_tooltip('--dbs',
                      m._enum_area_opts_ckbtns[1][4])
    self._set_tooltip('--tables',
                      m._enum_area_opts_ckbtns[2][0])
    self._set_tooltip('--columns',
                      m._enum_area_opts_ckbtns[2][1])
    self._set_tooltip('--schema',
                      m._enum_area_opts_ckbtns[2][2])
    self._set_tooltip('--count',
                      m._enum_area_opts_ckbtns[2][3])
    self._set_tooltip('--comments',
                      m._enum_area_opts_ckbtns[2][4])
    self._set_tooltip('--dump',
                      m._dump_area_dump_ckbtn)
    self._set_tooltip('--dump-all',
                      m._dump_area_dump_all_ckbtn)
    self._set_tooltip('--search',
                      m._dump_area_search_ckbtn)
    self._set_tooltip('--exclude-sysdb',
                      m._dump_area_no_sys_db_ckbtn)
    self._set_tooltip('--repair',
                      m._dump_area_repair_ckbtn)
    self._set_tooltip('--start=',
                      m._limit_area_start_ckbtn,
                      m._limit_area_start_entry)
    self._set_tooltip('--stop=',
                      m._limit_area_stop_ckbtn,
                      m._limit_area_stop_entry)
    self._set_tooltip('--first=',
                      m._blind_area_first_ckbtn,
                      m._blind_area_first_entry)
    self._set_tooltip('--last=',
                      m._blind_area_last_ckbtn,
                      m._blind_area_last_entry)
    self._set_tooltip('-D DB',
                      m._meta_area_D_ckbtn,
                      m._meta_area_D_entry)
    self._set_tooltip('-T TBL',
                      m._meta_area_T_ckbtn,
                      m._meta_area_T_entry)
    self._set_tooltip('-C COL',
                      m._meta_area_C_ckbtn,
                      m._meta_area_C_entry)
    self._set_tooltip('-U USER',
                      m._meta_area_U_ckbtn,
                      m._meta_area_U_entry)
    self._set_tooltip('-X EXCLUDE',
                      m._meta_area_X_ckbtn,
                      m._meta_area_X_entry)
    self._set_tooltip('--pivot-column=P..',
                      m._meta_area_pivot_ckbtn,
                      m._meta_area_pivot_entry)
    self._set_tooltip('--where=',
                      m._meta_area_where_ckbtn,
                      m._meta_area_where_entry)
    self._set_tooltip('--sql-query=QUERY',
                      m._runsql_area_sql_query_ckbtn,
                      m._runsql_area_sql_query_entry)
    self._set_tooltip('--sql-shell',
                      m._runsql_area_sql_shell_ckbtn)
    self._set_tooltip('--sql-file=SQLFILE',
                      m._runsql_area_sql_file_ckbtn,
                      m._runsql_area_sql_file_entry)
    self._set_tooltip('--common-tables',
                      m._brute_force_area_common_tables_ckbtn)
    self._set_tooltip('--common-columns',
                      m._brute_force_area_common_columns_ckbtn)
    # 4.文件页面
    self._set_tooltip('远程DB所在服务器上的文件路径',
                      m._file_read_area_file_read_ckbtn,
                      m._file_read_area_file_read_entry)
    self._set_tooltip('只能查看已下载到本地的文件',
                      m._file_read_area_file_read_btn)
    self._set_tooltip('--udf-inject',
                      m._file_write_area_udf_ckbtn)
    self._set_tooltip('与--udf-inject配套使用, 可选',
                      m._file_write_area_shared_lib_ckbtn,
                      m._file_write_area_shared_lib_entry)
    self._set_tooltip('若使用此选项, 则--file-dest为必选项',
                      m._file_write_area_file_write_ckbtn,
                      m._file_write_area_file_write_entry)
    self._set_tooltip('上传到DB服务器中的文件名, 要求是绝对路径, 构造后会有引号!\n'
                      '与本地文件路径配套使用, 单独勾选无意义',
                      m._file_write_area_file_dest_ckbtn,
                      m._file_write_area_file_dest_entry)
    self._set_tooltip('--os-cmd=',
                      m._file_os_access_os_cmd_ckbtn,
                      m._file_os_access_os_cmd_entry)
    self._set_tooltip('--os-shell',
                      m._file_os_access_os_shell_ckbtn)
    self._set_tooltip('Prompt for an OOB shell, Meterpreter or VNC',
                      m._file_os_access_os_pwn_ckbtn)
    self._set_tooltip('--os-smbrelay',
                      m._file_os_access_os_smbrelay_ckbtn)
    self._set_tooltip('--os-bof',
                      m._file_os_access_os_bof_ckbtn)
    self._set_tooltip('--priv-esc',
                      m._file_os_access_priv_esc_ckbtn)
    self._set_tooltip('--msf-path=MSFPATH Local path where Metasploit Framework is installed',
                      m._file_os_access_msf_path_ckbtn,
                      m._file_os_access_msf_path_entry)
    self._set_tooltip('--tmp-path=TMPPATH Remote absolute path of temporary files directory',
                      m._file_os_access_tmp_path_ckbtn,
                      m._file_os_access_tmp_path_entry)
    self._set_tooltip('--reg-key=',
                      m._file_os_registry_reg_key_label,
                      m._file_os_registry_reg_key_entry)
    self._set_tooltip('--reg-value=',
                      m._file_os_registry_reg_value_label,
                      m._file_os_registry_reg_value_entry)
    self._set_tooltip('--reg-data=',
                      m._file_os_registry_reg_data_label,
                      m._file_os_registry_reg_data_entry)
    self._set_tooltip('--reg-type=',
                      m._file_os_registry_reg_type_label,
                      m._file_os_registry_reg_type_entry)
    # 5.其他页面
    self._set_tooltip('--check-internet',
                      m._page1_general_check_internet_ckbtn)
    self._set_tooltip('--fresh-queries',
                      m._page1_general_fresh_queries_ckbtn)
    self._set_tooltip('--flush-session',
                      m._page1_general_flush_session_ckbtn)
    self._set_tooltip('--eta',
                      m._page1_general_eta_ckbtn)
    self._set_tooltip('--binary-fields=',
                      m._page1_general_binary_fields_ckbtn,
                      m._page1_general_binary_fields_entry)
    self._set_tooltip('--forms',
                      m._page1_general_forms_ckbtn)
    self._set_tooltip('--parse-errors',
                      m._page1_general_parse_errors_ckbtn)
    self._set_tooltip('--cleanup',
                      m._page1_misc_cleanup_ckbtn)
    self._set_tooltip('--preprocess=',
                      m._page1_general_preprocess_ckbtn,
                      m._page1_general_preprocess_entry)
    self._set_tooltip('--crawl=',
                      m._page1_general_crawl_ckbtn,
                      m._page1_general_crawl_entry)
    self._set_tooltip('--crawl-exclude=',
                      m._page1_general_crawl_exclude_ckbtn,
                      m._page1_general_crawl_exclude_entry)
    self._set_tooltip('--charset=',
                      m._page1_general_charset_ckbtn,
                      m._page1_general_charset_entry)
    self._set_tooltip('--encoding=',
                      m._page1_general_encoding_ckbtn,
                      m._page1_general_encoding_entry)
    self._set_tooltip('-s SESSIONFILE      Load session from a stored (.sqlite) file',
                      m._page1_general_session_file_ckbtn,
                      m._page1_general_session_file_entry)
    self._set_tooltip('--output-dir=',
                      m._page1_general_output_dir_ckbtn,
                      m._page1_general_output_dir_entry)
    self._set_tooltip('--dump-format=',
                      m._page1_general_dump_format_ckbtn,
                      m._page1_general_dump_format_entry)
    self._set_tooltip('--csv-del=',
                      m._page1_general_csv_del_ckbtn,
                      m._page1_general_csv_del_entry)
    self._set_tooltip('-t TRAFFICFILE      Log all HTTP traffic into a textual file',
                      m._page1_general_traffic_file_ckbtn,
                      m._page1_general_traffic_file_entry)
    self._set_tooltip('--har=HARFILE       Log all HTTP traffic into a HAR file',
                      m._page1_general_har_ckbtn,
                      m._page1_general_har_entry)
    self._set_tooltip('--save=SAVECONFIG Save options to a configuration INI file',
                      m._page1_general_save_ckbtn,
                      m._page1_general_save_entry)
    self._set_tooltip('--scope=SCOPE Regexp to filter targets from provided proxy log',
                      m._page1_general_scope_ckbtn,
                      m._page1_general_scope_entry)
    self._set_tooltip('--test-filter=TE.. Select tests by payloads and/or titles (e.g. ROW)',
                      m._page1_general_test_filter_ckbtn,
                      m._page1_general_test_filter_entry)
    self._set_tooltip('--test-skip=TEST.. Skip tests by payloads and/or titles (e.g. BENCHMARK)',
                      m._page1_general_test_skip_ckbtn,
                      m._page1_general_test_skip_entry)
    self._set_tooltip('--web-root=WEBROOT Web server document root directory (e.g. "/var/www")',
                      m._page1_misc_web_root_ckbtn,
                      m._page1_misc_web_root_entry)
    self._set_tooltip('--tmp-dir=TMPDIR Local directory for storing temporary files',
                      m._page1_misc_tmp_dir_ckbtn,
                      m._page1_misc_tmp_dir_entry)
    self._set_tooltip('--identify-waf',
                      m._page1_misc_identify_waf_ckbtn)
    self._set_tooltip('--skip-waf',
                      m._page1_misc_skip_waf_ckbtn)
    self._set_tooltip('--smart',
                      m._page1_misc_smart_ckbtn)
    self._set_tooltip('--list-tampers',
                      m._page1_misc_list_tampers_ckbtn)
    self._set_tooltip('--sqlmap-shell',
                      m._page1_misc_sqlmap_shell_ckbtn)
    self._set_tooltip('--disable-coloring',
                      m._page1_misc_disable_color_ckbtn)
    self._set_tooltip('--offline',
                      m._page1_misc_offline_ckbtn)
    self._set_tooltip('--mobile',
                      m._page1_misc_mobile_ckbtn)
    self._set_tooltip('--beep',
                      m._page1_misc_beep_ckbtn)
    self._set_tooltip('--purge',
                      m._page1_misc_purge_ckbtn)
    self._set_tooltip('--dependencies',
                      m._page1_misc_dependencies_ckbtn)
    self._set_tooltip('--update',
                      m._page1_general_update_ckbtn)
    self._set_tooltip('--answers=ANSWERS Set question answers(e.g. "quit=N,follow=N")',
                      m._page1_misc_answers_ckbtn,
                      m._page1_misc_answers_entry)
    self._set_tooltip('--alert=ALERT Run host OS command(s) when SQL injection is found',
                      m._page1_misc_alert_ckbtn,
                      m._page1_misc_alert_entry)
    self._set_tooltip('--gpage=GOOGLEPAGE Use Google dork results from specified page number',
                      m._page1_misc_gpage_ckbtn)
    self._set_tooltip('-z MNEMONICS Use short mnemonics (e.g. "flu,bat,ban,tec=EU")',
                      m._page1_misc_z_ckbtn,
                      m._page1_misc_z_entry)
    # 二、日志区(page3)
    self._set_tooltip('不会修改文件',
                      m._page3_clear_btn)
    # 三、API区(page4)
    self._set_tooltip('必填项, 不要加http://',
                      m._page4_api_server_label,
                      m._page4_api_server_entry)
    self._set_tooltip('必填项, 32位的token',
                      m._page4_admin_token_label,
                      m._page4_admin_token_entry)
    self._set_tooltip('此处填写要查看的选项(空格分隔), 如: url risk level',
                      m._page4_option_get_entry)
    _api_usage = '''sqlampapi使用步骤:
    1. 在本地或远程运行: ./sqlmapapi.py -s
    2. 填写API区第一行的server和token
    3. 点击 创建任务
    4. 点击 显示任务 后, 下方窗格中会显示任务列表
    5. 在本窗格中填写 python dict类型的选项如:
    {
      'url': 'http://www.site.com/vuln.php?id=1',
      'level': 1, 'risk': 1,
    }
    6. 点击 设置:(会发送 本窗格的选项dict)
    7. 点击 启动 (设置了选项才有意义)
    注: 1.要查看任务的状态, 点击 显示任务 进行刷新
        2.sqlmapapi支持的选项与sqlmap不兼容,
          且其进行选项设置时, 没有检查选项!
          如果设置了无效的选项, 只能删除任务!
    '''
    self._set_tooltip(_api_usage,
                      m._page4_option_set_view)

  def _set_placeholder(self, placeholder, *widgets):
    '''
    widgets: 应该都是entry吧?
    只有entry才有set_placeholder_text方法
    '''
    for _widget in widgets:
      _widget.set_placeholder_text(placeholder)

  def _set_tooltip(self, tooltip, *widgets):
    for _widget in widgets:
      _widget.set_tooltip_text(tooltip)


def main():
  from widgets import g
  from sqlmap import Window

  win = Window()
  win.connect('destroy', g.main_quit)
  win.show_all()
  g.main()


if __name__ == '__main__':
  main()
