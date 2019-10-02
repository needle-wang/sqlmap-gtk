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
    self._set_placeholder('id,user-agent',
                          m._inject_area_param_entry)
    self._set_placeholder('用于闭合',
                          m._inject_area_prefix_entry)
    self._set_placeholder('user-agent,referer',
                          m._inject_area_skip_entry)
    self._set_placeholder('token|session',
                          m._inject_area_param_exclude_entry)
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
    self._set_placeholder('5',
                          m._tech_area_time_sec_entry)
    self._set_placeholder('10',
                          m._tech_area_union_col_entry)
    self._set_placeholder('NULL',
                          m._tech_area_union_char_entry)
    self._set_placeholder('有效表名',
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
    self._set_placeholder('&',
                          m._request_area_param_del_entry)
    self._set_placeholder('query=foobar&id=1',
                          m._request_area_post_entry)
    self._set_placeholder('AU=233;SESSIONID=AABBCCDDEEFF;',
                          m._request_area_cookie_entry)
    self._set_placeholder(';',
                          m._request_area_cookie_del_entry)
    self._set_placeholder('Basic, Digest, NTLM or PKI',
                          m._request_area_auth_type_entry)
    self._set_placeholder('name:password',
                          m._request_area_auth_cred_entry)
    self._set_placeholder('PEM cert/private key file',
                          m._request_area_auth_file_entry)
    self._set_placeholder('token字段名',
                          m._request_area_csrf_token_entry)
    self._set_placeholder('import hashlib;id2=hashlib.md5(id).hexdigest()',
                          m._request_area_eval_entry)
    # 3.枚举页面
    self._set_placeholder('不包含该行',
                          m._limit_area_start_entry)
    self._set_placeholder('包含该行',
                          m._limit_area_stop_entry)
    # 4.文件页面
    self._set_placeholder('配合 Meterpreter相关 使用',
                          m._file_os_access_msf_path_entry)
    # 5.其他页面
    self._set_placeholder('CSV(默认), HTML or SQLITE',
                          m._page1_general_dump_format_entry)
    self._set_placeholder(r'(www)?\.target\.(com|net|org)',
                          m._page1_general_scope_entry)
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
    self._set_tooltip('-p\n逗号分隔, 与--level不兼容',
                      m._inject_area_param_ckbtn,
                      m._inject_area_param_entry)
    self._set_tooltip('--skip-static\n'
        '另外: sqlmap不会针对(伪)静态网页(/param1/value1/),\n'
        '在任意(get/post/header等)可能的注入参数后加*即可',
                      m._inject_area_skip_static_ckbtn)
    self._set_tooltip('--prefix=PREFIX\n'
        '当情况复杂(如注入点位于嵌套JOIN查询中)时, 需要手动处理',
                      m._inject_area_prefix_ckbtn,
                      m._inject_area_prefix_entry)
    self._set_tooltip('--suffix=SUFFIX\n',
                      m._inject_area_suffix_ckbtn,
                      m._inject_area_suffix_entry)
    self._set_tooltip('--skip=...,...\tSkip testing for given parameter(s)',
                      m._inject_area_skip_ckbtn,
                      m._inject_area_skip_entry)
    self._set_tooltip('--param-exclude=.. Regexp to exclude parameters from testing',
                      m._inject_area_param_exclude_ckbtn,
                      m._inject_area_param_exclude_entry)
    self._set_tooltip('--dbms=DBMS\n很确定是哪种DBMS时使用',
                      m._inject_area_dbms_ckbtn,
                      m._inject_area_dbms_combobox)
    self._set_tooltip('--dbms-cred=DBMS..  DBMS authentication credentials (user:password)',
                      m._inject_area_dbms_cred_ckbtn,
                      m._inject_area_dbms_cred_entry)
    self._set_tooltip('--os=OS\n仅在确定知道DBMS所在OS名称时使用',
                      m._inject_area_os_ckbtn,
                      m._inject_area_os_entry)
    self._set_tooltip('--no-cast\n'
        '检索结果时, 默认会将条目cast为字符串类型(优化检索),\n'
        '若数据检索有问题(如某些老版本mysql)时, 勾选',
                      m._inject_area_no_cast_ckbtn)
    self._set_tooltip('--no-escape\n'
        '注: 默认 select \'foobar\'会变成 select char(102)+char(111)...\n'
        '    优点: 转义引号, 绕过; 缺点: 长度变长',
                      m._inject_area_no_escape_ckbtn)
    self._set_tooltip('--invalid-logical',
                      m._inject_area_invalid_logic_ckbtn)
    self._set_tooltip('--invalid-bignum',
                      m._inject_area_invalid_bignum_ckbtn)
    self._set_tooltip('--invalid-string',
                      m._inject_area_invalid_str_ckbtn)
    self._set_tooltip('--text-only\n'
        '有的响应正文包含大量其他内容(如js脚本)\n'
        '勾选, 可以让sqlmap只关注text文件',
                      m._detection_area_text_only_ckbtn)
    self._set_tooltip('--titles',
                      m._detection_area_titles_ckbtn)
    self._set_tooltip('--string=STRING',
                      m._detection_area_str_ckbtn,
                      m._detection_area_str_entry)
    self._set_tooltip('--not-string=NOT..',
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
    self._set_tooltip('--time-sec=默认5秒\n时间盲注时',
                      m._tech_area_time_sec_ckbtn,
                      m._tech_area_time_sec_entry)
    self._set_tooltip('--union-cols=默认10列\nunion查询时\n'
        '提高level, 可增加至50列;\n'
        '填12-16表示使用12到16列',
                      m._tech_area_union_col_ckbtn,
                      m._tech_area_union_col_entry)
    self._set_tooltip('--union-char=默认使用NULL\nunion查询时\n'
        '提高level, 会使用随机数\n'
        '如--union-char=001',
                      m._tech_area_union_char_ckbtn,
                      m._tech_area_union_char_entry)
    self._set_tooltip('--union-from=\nunion查询时',
                      m._tech_area_union_from_ckbtn,
                      m._tech_area_union_from_entry)
    self._set_tooltip('--dns-domain=\n'
        '如果控制了目标url的DNS服务器, 才可使用此选项\n'
        '这样做只是用来加快数据检索',
                      m._tech_area_dns_ckbtn,
                      m._tech_area_dns_entry)
    self._set_tooltip('--second-url=',
                      m._tech_area_second_url_ckbtn,
                      m._tech_area_second_url_entry)
    self._set_tooltip('--second-req=',
                      m._tech_area_second_req_ckbtn,
                      m._tech_area_second_req_entry)
    self._set_tooltip('sqlmap只会对CHAR()字符串进行混淆,\n'
        '不会对其他的payload进行任何混淆.\n'
        '要绕过IPS设备或Web应用防火墙(WAF)时, 使用此选项\n'
        '此处填写要使用的tamper脚本名\n'
        '详见: sqlmap --list-tamper\n回车或逗号拼接',
                      m._tamper_area_tamper_view)
    self._set_tooltip('-o, 开启后会默认:\n'
        '  --keep-alive\n  --null-connection\n  --threads=3',
                      m._optimize_area_turn_all_ckbtn)
    self._set_tooltip('--threads=\n默认为1, 最大为10',
                      m._optimize_area_thread_num_ckbtn)
    self._set_tooltip('--predict-output\n'
        '此开关与--threads不兼容',
                      m._optimize_area_predict_ckbtn)
    self._set_tooltip('--keep-alive\n'
        '此开关与--proxy不兼容',
                      m._optimize_area_keep_alive_ckbtn)
    self._set_tooltip('--null-connection\n'
        '有的请求类型可用来获取响应大小而不用获取响应主体\n'
        '两种NULL连接技术: Range和HEAD\n'
        '此开关与--text-only不兼容',
                      m._optimize_area_null_connect_ckbtn)
    # -v:
    # 0: 只显示Python回源(tracebacks), 错误(error)和关键(criticle)信息。
    # 1: 同时显示信息(info)和警告信息（warning)（默认为1）
    # 2: 同时显示调试信息(debug)
    # 3: 同时显示注入的有效载荷(payloads)
    # 4: 同时显示http请求
    # 5: 同时显示http响应头
    # 6: 同时显示http响应内容
    # self._set_tooltip('-v 默认为1',
                      # m._general_area_verbose_ckbtn)
    self._set_tooltip('--fingerprint\n'
        '默认就会自动指纹DB,\n'
        '开启此开关后, 会发送更多请求, 以确定更精确的DB/OS等版本信息',
                      m._general_area_finger_ckbtn)
    self._set_tooltip('--hex\n'
        '响应中的非ASCII数据不准确(如乱码)时, 会将其先编码成16进制格式',
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
    self._set_tooltip('--referer=\n'
        '默认情况下(即不加此参数)不会发送Referer报头',
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
    self._set_tooltip('--data=\n'
        '默认情况下sqlmap发送的是GET请求, 若使用此参数, 会将数据post到目标\n'
        '比如搜索框, 表单等会通过post方式发送数据',
                      m._request_area_post_ckbtn,
                      m._request_area_post_entry)
    self._set_tooltip('--cookie=',
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
    self._set_tooltip('--auth-file=\n'
        'PEM格式的key_file, 包含你的证书和私钥',
                      m._request_area_auth_file_ckbtn,
                      m._request_area_auth_file_entry)
    self._set_tooltip('--csrf-token=\n'
        '有的表单中含有隐藏的随机token字段, 来防止csrf攻击',
                      m._request_area_csrf_token_ckbtn,
                      m._request_area_csrf_token_entry)
    self._set_tooltip('--csrf-url=\n'
        '若目标url没有token字段, 则指定有token字段的url',
                      m._request_area_csrf_url_ckbtn,
                      m._request_area_csrf_url_entry)
    self._set_tooltip('--ignore-redirects',
                      m._request_area_ignore_redirects_ckbtn)
    self._set_tooltip('--ignore-timeouts',
                      m._request_area_ignore_timeouts_ckbtn)
    self._set_tooltip('--ignore-code=',
                      m._request_area_ignore_code_ckbtn,
                      m._request_area_ignore_code_entry)
    self._set_tooltip('--skip-urlencode\n'
        '有的server只接受未编码的参数',
                      m._request_area_skip_urlencode_ckbtn)
    self._set_tooltip('--force-ssl',
                      m._request_area_force_ssl_ckbtn)
    self._set_tooltip('--chunked',
                      m._request_area_chunked_ckbtn)
    self._set_tooltip('--hpp\n'
        '绕过WAF/IP/IDS的一种方法, 对ASP/IIS, ASP.NET/IIS特别有效',
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
    self._set_tooltip('--safe-url=\n'
        '避免错误请求过多而被屏蔽',
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
    self._set_tooltip('-b\t获取version()/@@version',
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
    self._set_tooltip('--privileges\n'
        'sql server会显示每个用户是否为dba, 而不是所有用户的权限列表',
                      m._enum_area_opts_ckbtns[1][2])
    self._set_tooltip('--roles 仅限oracle可用',
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
    self._set_tooltip('--repair',
                      m._dump_area_repair_ckbtn)
    self._set_tooltip('--statements',
                      m._dump_area_statements_ckbtn)
    self._set_tooltip('--search 需配合以下选项使用:\n'
        '  -C=逗号分隔的列名: 将在所有DB中的所有表中 搜索指定列名\n'
        '  -T=逗号分隔的表名: 将在所有DB中 搜索指定表名\n'
        '  -D=逗号分隔的数据库名: 将 搜索指定库名\n',
                      m._dump_area_search_ckbtn)
    self._set_tooltip('--exclude-sysdb\n注: sql server上master库不视为系统库',
                      m._dump_area_no_sys_db_ckbtn)
    self._set_tooltip('--dump-all',
                      m._dump_area_dump_all_ckbtn)
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
    self._set_tooltip('--pivot-column=P\n当自动选择的privot列不正确时使用此项',
                      m._meta_area_pivot_ckbtn,
                      m._meta_area_pivot_entry)
    self._set_tooltip('--where=',
                      m._meta_area_where_ckbtn,
                      m._meta_area_where_entry)
    self._set_tooltip('--sql-query=QUERY\n'
        '如果是select语句, 会返回输出;\n'
        '如果目标支持多语句查询, 会使用堆查询技术',
                      m._runsql_area_sql_query_ckbtn,
                      m._runsql_area_sql_query_entry)
    self._set_tooltip('--sql-shell\n支持TAB补全, 历史记录',
                      m._runsql_area_sql_shell_ckbtn)
    self._set_tooltip('--sql-file=SQLFILE',
                      m._runsql_area_sql_file_ckbtn,
                      m._runsql_area_sql_file_entry)
    self._set_tooltip('--common-tables\n'
        '有时--tables会失败, 通常原因如下:\n'
        '  1.MySQL<5.0: information_schema不可用\n'
        '  2.Access:    默认系统表(MSysObjects)不可读\n'
        '  --current-user没有 读取系统表的 权限',
                      m._brute_force_area_common_tables_ckbtn)
    self._set_tooltip('--common-columns',
                      m._brute_force_area_common_columns_ckbtn)
    # 4.文件页面
    self._set_tooltip('远程DB所在主机上的文件路径\n'
        '前提: 1.MySQL, PostgreSQL或Microsoft SQL Server\n'
        '      2.当前用户有 读取文件的 相关权限',
                      m._file_read_area_file_read_ckbtn,
                      m._file_read_area_file_read_entry)
    self._set_tooltip('只能查看已下载到本地的文件',
                      m._file_read_area_file_read_btn)
    self._set_tooltip('--udf-inject\tUDF即user-defined function\n'
        '将共享库上传到DB所在文件系统上, 来创建用户自定义的函数以供使用',
                      m._file_write_area_udf_ckbtn)
    self._set_tooltip('与--udf-inject配套使用, 可选',
                      m._file_write_area_shared_lib_ckbtn,
                      m._file_write_area_shared_lib_entry)
    self._set_tooltip('若使用此选项, 则--file-dest为必选项\n'
        '前提: 1.MySQL, PostgreSQL或Microsoft SQL Server\n'
        '      2.当前用户有 使用特定函数上传文件的 相关权限',
                      m._file_write_area_file_write_ckbtn,
                      m._file_write_area_file_write_entry)
    self._set_tooltip('上传到DB服务器中的文件名, 要求是绝对路径, 构造后会有引号!\n'
                      '与本地文件路径配套使用, 单独勾选无意义',
                      m._file_write_area_file_dest_ckbtn,
                      m._file_write_area_file_dest_entry)
    self._set_tooltip('--os-cmd=\n'
        '前提: 1.MySQL, PostgreSQL或Microsoft SQL Server\n'
        '      2.当前用户有相关权限\n'
        'MySQL或者PostgreSQL: 上传包含sys_exec和sys_eval函数的共享库\n'
        'SQL Server: 使用xp_cmdshell存储过程, 若被禁用(>=2005), 就启用它;\n'
        '                                     若不存在, 就从新创建它',
                      m._file_os_access_os_cmd_ckbtn,
                      m._file_os_access_os_cmd_entry)
    self._set_tooltip('--os-shell\n支持TAB补全, 历史记录\n'
        '若不支持堆查询(如asp/php + MySQL), 且是MySQL(库站未分离!):\n'
        '  会使用SELECT子句INTO OUTFILE在可写目录创建一个web后门来执行命令\n'
        '支持的web后门类型有: ASP, ASP.NET, JSP, PHP',
                      m._file_os_access_os_shell_ckbtn)
    self._set_tooltip('MySQL和PostgreSQL:\n'
        '  1.通过UDF中的sys_bineval函数 执行Metasploit的shellcode\n'
        '  2.通过UDF中的sys_exec函数 上传并执行Metasploit的stand-alone payload stager\n'
        'Microsoft SQL Server:\n'
        '  1.通过xp_cmdshell储存过程 上传并执行Metasploit的stand-alone payload stager\n',
                      m._file_os_access_os_pwn_ckbtn)
    self._set_tooltip('前提: 最高权限(linux: uid=0, windows: Administrator)\n'
        '  通过SMB攻击(MS08-068) 执行Metasploit的shellcode',
                      m._file_os_access_os_smbrelay_ckbtn)
    self._set_tooltip('SQL Server 2000, 2005:\n'
        '  通过sp_replwritetovarbin存储过程(MS09-004)溢出漏洞 执行Metasploit的payload\n'
        '  sqlmap有自己的漏洞利用自动DEP内存保护绕过来触发漏洞, 但它依赖于Metasploit来生成shellcode, 以便在成功利用后执行',
                      m._file_os_access_os_bof_ckbtn)
    self._set_tooltip('运行Metasploit的getsystem command命令来 提升权限\n'
        '注: windows:\n'
        '  MySQL: 默认以SYSTEM身份运行\n'
        '  Server 2000: 默认以SYSTEM身份运行\n'
        '  Server 2005-2008: 多数以NETWORK SERVICE, 少数以LOCAL SERVICE身份运行\n'
        '  PostgreSQL: 默认以低权限的用户postgres运行\n'
        '    linux:\n'
        '  PostgreSQL: 默认以低权限的用户postgres运行',
                      m._file_os_access_priv_esc_ckbtn)
    self._set_tooltip('--msf-path=',
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
    self._set_tooltip('--binary-fields=\n'
        '指定有二进制值的列, 获取该列数据时, 会转成16进制输出',
                      m._page1_general_binary_fields_ckbtn,
                      m._page1_general_binary_fields_entry)
    self._set_tooltip('--forms\n'
        '若想对 form表单参数 测试:\n'
        '  1.通过某些方式得到请求文件或表单参数\n'
        '  2.可用-r读取请求文件或--data指定表单参数\n'
        '但--forms开关: 可让sqlmap自行获取url响应中的表单参数 再做测试\n'
        '注: 是所有的表单, 及所有表单参数',
                      m._page1_general_forms_ckbtn)
    self._set_tooltip('--parse-errors',
                      m._page1_general_parse_errors_ckbtn)
    self._set_tooltip('--cleanup',
                      m._page1_misc_cleanup_ckbtn)
    self._set_tooltip('--preprocess=',
                      m._page1_general_preprocess_ckbtn,
                      m._page1_general_preprocess_entry)
    self._set_tooltip('--crawl=  并且会收集有漏洞url',
                      m._page1_general_crawl_ckbtn,
                      m._page1_general_crawl_entry)
    self._set_tooltip('--crawl-exclude=',
                      m._page1_general_crawl_exclude_ckbtn,
                      m._page1_general_crawl_exclude_entry)
    self._set_tooltip('--charset=  如获取SHA1密文时, 请求数会减小30%',
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
    self._set_tooltip('--smart\n'
        '用于 批量扫描(如-m时), 快速粗略地寻找明显目标,\n'
        '再对 可引发DBMS错误的参数 进一步扫描',
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
    self._set_tooltip('--purge  应该只是抹除output目录吧',
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
  from widgets import d, g
  from sqlmap_gtk import Window

  win = Window()

  css_provider = g.CssProvider.new()
  css_provider.load_from_path('css.css')
  g.StyleContext.add_provider_for_screen(
    d.Screen.get_default(),
    css_provider,
    g.STYLE_PROVIDER_PRIORITY_APPLICATION
  )

  win.connect('destroy', g.main_quit)
  win.show_all()
  g.main()


if __name__ == '__main__':
  main()
