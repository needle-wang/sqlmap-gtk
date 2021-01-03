#!/usr/bin/env python3
#
# 2021-01-01 16:40:04


class Widget_Mesg(object):
  def __init__(self, m):
    '''
    m: model.Model
    '''
    self.set_all_tooltips(m)
    self.set_all_placeholders(m)

  def set_all_placeholders(self, m):
    # 0.Target
    self._set_placeholder('-u: Target URL (e.g. "http://www.site.com/vuln.php?id=1")',
                          m._url_combobox.get_child())
    self._set_placeholder('-l: Parse target(s) from Burp or WebScarab proxy log file',
                          m._burp_logfile)
    self._set_placeholder('-r: Load HTTP request from a file(such as fiddler)',
                          m._request_file)
    self._set_placeholder('-m: Scan multiple targets given in a textual file',
                          m._bulkfile)
    self._set_placeholder('-c: Load options from a configuration INI file',
                          m._configfile)
    self._set_placeholder('-g: Process Google dork results as target URLs',
                          m._google_dork)
    # OPTIONS(page1)
    # 1.Inject(Q)
    self._set_placeholder('id,user-agent',
                          m._inject_area_param_entry)
    self._set_placeholder('user-agent, referer',
                          m._inject_area_skip_entry)
    self._set_placeholder('token|session',
                          m._inject_area_param_exclude_entry)
    self._set_placeholder('payload prefix str',
                          m._inject_area_prefix_entry)
    self._set_placeholder('user:password',
                          m._inject_area_dbms_cred_entry)
    self._set_placeholder('String to match when query is evaluated to True',
                          m._detection_area_str_entry)
    self._set_placeholder('String to match when query is evaluated to False',
                          m._detection_area_not_str_entry)
    self._set_placeholder('Regexp to match when query is evaluated to True',
                          m._detection_area_re_entry)
    self._set_placeholder('HTTP code(True)',
                          m._detection_area_code_entry)
    self._set_placeholder('BEUSTQ',
                          m._tech_area_tech_entry)
    self._set_placeholder('5',
                          m._tech_area_time_sec_entry)
    self._set_placeholder('10',
                          m._tech_area_union_col_entry)
    self._set_placeholder('NULL',
                          m._tech_area_union_char_entry)
    self._set_placeholder('valid table',
                          m._tech_area_union_from_entry)
    self._set_placeholder('DNS exfiltration',
                          m._tech_area_dns_entry)
    # 2.Request(W)
    self._set_placeholder('e.g. X-Forwarded-For: 127.0.0.1',
                          m._request_area_header_entry)
    self._set_placeholder('e.g. Accept-Language: fr\\nETag: 123',
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
    self._set_placeholder('post',
                          m._request_area_csrf_method_entry)
    self._set_placeholder('anti-CSRF token',
                          m._request_area_csrf_token_entry)
    self._set_placeholder('import hashlib;id2=hashlib.md5(id).hexdigest()',
                          m._request_area_eval_entry)
    # 3.Enumerate(E)
    self._set_placeholder('>',
                          m._limit_area_start_entry)
    self._set_placeholder('<=',
                          m._limit_area_stop_entry)
    self._set_placeholder('id<3',
                          m._meta_area_where_entry)
    # 4.File(R)
    self._set_placeholder('Local path where Metasploit Framework is installed',
                          m._file_os_access_msf_path_entry)
    self._set_placeholder('Remote absolute path of temporary files directory',
                          m._file_os_access_tmp_path_entry)
    # 5.Other(T)
    self._set_placeholder('sqlmap',
                          m._page1_general_table_prefix_entry)
    self._set_placeholder('Use given script(s) for preprocessing (request)',
                          m._page1_general_preprocess_entry)
    self._set_placeholder('Web server document root directory (e.g. "/var/www")',
                          m._page1_general_web_root_entry)
    self._set_placeholder(r'Regexp for filtering targets. e.g. (www)?\.target\.(com|net|org)',
                          m._page1_general_scope_entry)
    self._set_placeholder('ROW',
                          m._page1_general_test_filter_entry)
    self._set_placeholder('BENCHMARK',
                          m._page1_general_test_skip_entry)
    self._set_placeholder('depth',
                          m._page1_general_crawl_entry)
    self._set_placeholder('Regexp to exclude pages from crawling (e.g. "logout")',
                          m._page1_general_crawl_exclude_entry)
    self._set_placeholder('Log all HTTP traffic into a textual file',
                          m._page1_general_traffic_file_entry)
    self._set_placeholder('Log all HTTP traffic into a HAR file',
                          m._page1_general_har_entry)
    self._set_placeholder('CSV',
                          m._page1_general_dump_format_entry)
    self._set_placeholder('Save options to a configuration INI file',
                          m._page1_general_save_entry)
    self._set_placeholder('Load session from a stored (.sqlite) file',
                          m._page1_general_session_file_entry)
    self._set_placeholder('Custom output directory path',
                          m._page1_general_output_dir_entry)
    self._set_placeholder('Run local OS command(s) when injection found',
                          m._page1_misc_alert_entry)
    self._set_placeholder('Local folder for storing temporary files',
                          m._page1_misc_tmp_dir_entry)
    self._set_placeholder('Location of CSV results file in multiple targets mode',
                          m._page1_misc_results_file_entry)

    self._set_placeholder('no http://',
                          m._page4_api_server_entry)
    self._set_placeholder('32 digit token',
                          m._page4_admin_token_entry)

  def set_all_tooltips(self, m):
    '''
    m: model.Model
    gtk3.24: tooltip of row which contained scale causes flicker.(GTK3's bug?)
    '''
    # OPTIONS(page1)
    # 0._cmd_entry
    self._set_tooltip('1.check, input\n2.click A.collect\n3.click B.run',
                      m._cmd_entry)
    # 1.Inject(Q)
    self._set_tooltip('-p TESTPARAMETER\ncomma-separated, confict with --level',
                      m._inject_area_param_ckbtn,
                      m._inject_area_param_entry)
    self._set_tooltip('--param-filter=P..  Select testable parameter(s) by place (e.g. "POST")',
                      m._inject_area_param_filter_ckbtn,
                      m._inject_area_param_filter_combobox)
    self._set_tooltip('--skip-static Skip testing parameters that not appear to be dynamic\n'
        'Note: sqlmap would not test static style page(such as /param1/value1/),\n'
        'except using * behind parameter at any request method(get/post/header...)',
                      m._inject_area_skip_static_ckbtn)
    self._set_tooltip('--skip=...,...  Skip testing for given parameter(s)',
                      m._inject_area_skip_ckbtn,
                      m._inject_area_skip_entry)
    self._set_tooltip('--param-exclude=.. Regexp to exclude parameters from testing',
                      m._inject_area_param_exclude_ckbtn,
                      m._inject_area_param_exclude_entry)
    self._set_tooltip('--prefix=PREFIX\n'
        'build it by hand in some complex situation\n(vulnerable param at nested JOIN query)',
                      m._inject_area_prefix_ckbtn,
                      m._inject_area_prefix_entry)
    self._set_tooltip('--dbms=DBMS\nForce back-end DBMS to provided value only if definitly',
                      m._inject_area_dbms_ckbtn,
                      m._inject_area_dbms_combobox)
    self._set_tooltip('--dbms-cred=DBMS..  DBMS authentication credentials (user:password)',
                      m._inject_area_dbms_cred_ckbtn,
                      m._inject_area_dbms_cred_entry)
    self._set_tooltip('--os=OS\nonly if definitly',
                      m._inject_area_os_ckbtn,
                      m._inject_area_os_entry)
    self._set_tooltip('--no-cast Turn off payload casting mechanism\n'
        'When retrieving results, all entries would be casted to string type\n'
        'and replaced with a whitespace character in case of NULL values.\n'
        'if in trouble(e.g. older versions of MySQL), check it.',
                      m._inject_area_no_cast_ckbtn)
    self._set_tooltip('--no-escape\n'
        'unchecked: select \'foobar\' become select char(102)+char(111)...\n'
        'checked:  original palyload become longer.',
                      m._inject_area_no_escape_ckbtn)
    self._set_tooltip('--invalid-logical\n'
        'True: id=13, False: id=13 AND 18=19',
                      m._inject_area_invalid_logical_ckbtn)
    self._set_tooltip('--invalid-bignum\n'
        'True: id=13, False: id=99999999',
                      m._inject_area_invalid_bignum_ckbtn)
    self._set_tooltip('--invalid-string\n'
        'True: id=13, False: id=akewmc',
                      m._inject_area_invalid_string_ckbtn)
    self._set_tooltip('--text-only\n'
        'In cases with lot of resource(e.g. js, embeds) in some HTTP responses\' body'
        'check it so that sqlmap focus on textual content\n'
        'to know the distinction of a True query from a False one',
                      m._detection_area_text_only_ckbtn)
    self._set_tooltip('--titles focus on HTML title.',
                      m._detection_area_titles_ckbtn)
    self._set_tooltip('--smart\n'
        'find out a vulnerable target as fast as possible when -m used.'
        'only parameters with which DBMS error(s) can be provoked will be filtered out'
        'Otherwise they are skipped.',
                      m._detection_area_smart_ckbtn)
    self._set_tooltip('--technique=B: Boolean-based blind\n'
                      '            E: Error-based\n'
                      '            U: Union query-based\n'
                      '            S: Stacked queries\n'
                      '            T: Time-based blind\n'
                      '            Q: Inline queries',
                      m._tech_area_tech_ckbtn,
                      m._tech_area_tech_entry)
    self._set_tooltip('--time-sec=default 5\nwhen time-based blind SQL injection',
                      m._tech_area_time_sec_ckbtn,
                      m._tech_area_time_sec_entry)
    self._set_tooltip('--union-cols=default 10\nunion query:\n'
        '12-16 means tests for UNION query SQL injection by using 12 up to 16 columns\n'
        'the range can be increased up to 50 columns by providing an higher --level value.',
                      m._tech_area_union_col_ckbtn,
                      m._tech_area_union_col_entry)
    self._set_tooltip('--union-char=default NULL\nunion query:\n'
        'e.g. --union-char=001\n'
        'higher --level will performs tests with a random number',
                      m._tech_area_union_char_ckbtn,
                      m._tech_area_union_char_entry)
    self._set_tooltip('--union-from=\nunion query',
                      m._tech_area_union_from_ckbtn,
                      m._tech_area_union_from_entry)
    self._set_tooltip('--dns-domain=\nin best case time-based blind:\n'
        'if you controlled a DNS server, check it to speed up the process of data retrieval',
                      m._tech_area_dns_ckbtn,
                      m._tech_area_dns_entry)
    self._set_tooltip('sqlmap itself does no obfuscation of the payload sent,\n'
        'except for strings between single quotes replaced by their CHAR()-alike representation.\n'
        'so input tamper script\'s name here. comma/enter separator\n'
        'see also: sqlmap --list-tampers',
                      m._tamper_area_tamper_view)
    self._set_tooltip('-o, checked means:\n'
        '  --keep-alive\n  --null-connection\n  --threads=3',
                      m._optimize_area_turn_all_ckbtn)
    self._set_tooltip('--threads=\ndefault 1, max to 10',
                      m._optimize_area_thread_num_ckbtn)
    self._set_tooltip('--predict-output\n'
        'confict with --threads',
                      m._optimize_area_predict_ckbtn)
    self._set_tooltip('--keep-alive\n'
        'confict with --proxy',
                      m._optimize_area_keep_alive_ckbtn)
    self._set_tooltip('--null-connection when blind injection'
        'confict with --text-only\n'
        'some HTTP request types can be used to retrieve HTTP response\'s size without getting the HTTP body.\n'
        'two NULL connection techniques: Range and HEAD',
                      m._optimize_area_null_connect_ckbtn)
    # -v:
    # 0: Show only Python tracebacks, error and critical messages.
    # 1: Show also information and warning messages.
    # 2: Show also debug messages.
    # 3: Show also payloads injected.
    # 4: Show also HTTP requests.
    # 5: Show also HTTP responses' headers.
    # 6: Show also HTTP responses' page content.
    # self._set_tooltip('-v default 1',
    #                   m._general_area_verbose_ckbtn)
    self._set_tooltip('--fingerprint\n'
        'fingerprint the exact DBMS version and, where possible, operating system, architecture and patch level\n'
        'together with --dbms, only perform the extensive fingerprint for the specified DBMSonly\n'
        'combining with -b would be more accurate.',
                      m._general_area_finger_ckbtn)
    self._set_tooltip('--hex\n'
        'In lost of cases retrieval of non-ASCII data requires special needs.'
        'checked: data is encoded to hexadecimal form before being retrieved and afterwards unencoded.\n',
                      m._general_area_hex_ckbtn)
    self._set_tooltip('--wizard vector mode for beginner.',
                      m._page1_misc_wizard_ckbtn)
    # 2.Request(W)
    self._set_tooltip('--random-agent\n'
        'by default, User-Agent: sqlmap/1.0-dev\n'
        'so just check it!',
                      m._request_area_random_agent_ckbtn)
    self._set_tooltip('--referer=\n'
        'by default no HTTP Referer header is sent',
                      m._request_area_referer_ckbtn,
                      m._request_area_referer_entry)
    self._set_tooltip('--data=\n'
        'unchecked: the HTTP method is GET\n'
        'checked: change it to POST by providing the data',
                      m._request_area_post_ckbtn,
                      m._request_area_post_entry)
    self._set_tooltip('--auth-file=\n'
        'PEM formatted key_file, that contains your certificate and a private key',
                      m._request_area_auth_file_ckbtn,
                      m._request_area_auth_file_entry)
    self._set_tooltip('--csrf-token=\n'
        'some formes contain anti-CSRF randomized token',
                      m._request_area_csrf_token_ckbtn,
                      m._request_area_csrf_token_entry)
    self._set_tooltip('--csrf-url=\n'
        'if the vulnerable target URL doesn\'t contain the necessary token,\n'
        'use this option.',
                      m._request_area_csrf_url_ckbtn,
                      m._request_area_csrf_url_entry)
    self._set_tooltip('--skip-urlencode\n'
        'In some cases, web server accepts only their raw non-encoded form',
                      m._request_area_skip_urlencode_ckbtn)
    self._set_tooltip('--hpp\n'
        'bypassing WAF/IPS protection mechanisms.\n'
        'it is particularly effective against ASP/IIS and ASP.NET/IIS platforms.',
                      m._request_area_hpp_ckbtn)
    self._set_tooltip('--delay= specify a number of seconds to hold between each HTTP(S) request',
                      m._request_area_delay_ckbtn,
                      m._request_area_delay_entry)
    self._set_tooltip('--retries=\n'
        'specify the maximum number of retries when the HTTP(S) connection timeouts.\n'
        'By default it retries up to three times.',
                      m._request_area_retries_ckbtn,
                      m._request_area_retries_entry)
    self._set_tooltip('--randomize=\n'
        'specify parameter names whose values you want to be randomly changed during each request.\n'
        'length and type are being kept according to provided original values.',
                      m._request_area_randomize_ckbtn,
                      m._request_area_randomize_entry)
    self._set_tooltip('--eval= eval some python code before each request',
                      m._request_area_eval_ckbtn,
                      m._request_area_eval_entry)
    self._set_tooltip('--safe-url=\n'
        'URL address to visit frequently during testing to bypass some kind of limitation.',
                      m._request_area_safe_url_ckbtn,
                      m._request_area_safe_url_entry)
    self._set_tooltip('--safe-post=\n'
        'HTTP POST data to send to a given safe URL address.',
                      m._request_area_safe_post_ckbtn,
                      m._request_area_safe_post_entry)
    self._set_tooltip('--safe-req=\n'
        'Load and use safe HTTP request from a file.',
                      m._request_area_safe_req_ckbtn,
                      m._request_area_safe_req_entry)
    self._set_tooltip('--safe-freq=SAFE..  Test requests between two visits to a given safe URL',
                      m._request_area_safe_freq_ckbtn,
                      m._request_area_safe_freq_entry)
    # 3.Enumerate(E)
    self._set_tooltip('-b get DB banner: version()/@@version',
                      m._enum_area_opts_ckbtns[0][0])
    self._set_tooltip('--privileges\n'
        'on sql server, it would display you whether or not each user is a database administrator,\n'
        'rather than the list of privileges for all users.',
                      m._enum_area_opts_ckbtns[1][2])
    self._set_tooltip('--roles only for oracle',
                      m._enum_area_opts_ckbtns[1][3])
    self._set_tooltip('--tables\n'
        'if no -D, sqlmap will enumerate the tables for all DBMS databases.',
                      m._enum_area_opts_ckbtns[2][0])
    self._set_tooltip('--columns enumerate the all columns\'s name and type\n'
        'combine with -D, -T, -C\n'
        'if no -D, use the current database name\n'
        'PostgreSQL: requires public or the name of a system database.',
                      m._enum_area_opts_ckbtns[2][1])
    self._set_tooltip('--schema\n'
        'contain all databases, tables and columns, together with their respective types.\n'
        'better to combine with --exclude-sysdbs.',
                      m._enum_area_opts_ckbtns[2][2])
    self._set_tooltip('--count get the number of entries in table(s)',
                      m._enum_area_opts_ckbtns[2][3])
    self._set_tooltip('Redump entries having unknown character marker (?)',
                      m._dump_area_repair_ckbtn)
    self._set_tooltip('Retrieve SQL statements being run on DBMS',
                      m._dump_area_statements_ckbtn)
    self._set_tooltip('--search together with:\n'
        '  -C=comma-separated column name\n'
        '  -T=comma-separated table name\n'
        '  -D=comma-separated DB name',
                      m._dump_area_search_ckbtn)
    self._set_tooltip('--exclude-sysdb\n'
        'Note: on sql server, master is not considered a system database.',
                      m._dump_area_no_sys_db_ckbtn)
    self._set_tooltip('-D DB\n'
        'on Oracle you have to provide the TABLESPACE_NAME instead of the database name.',
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
    self._set_tooltip('--pivot-column=P\n'
        'for Microsoft SQL Server, Sybase and SAP MaxDB\n'
        'use it when the automatically chosen one is not suitable.',
                      m._meta_area_pivot_ckbtn,
                      m._meta_area_pivot_entry)
    self._set_tooltip('--sql-query=QUERY\n'
        'If the query is a SELECT statement, sqlmap retrieve its output.\n'
        'If the web supports multiple statements, use stacked query.',
                      m._runsql_area_sql_query_ckbtn,
                      m._runsql_area_sql_query_entry)
    self._set_tooltip('--sql-shell\nit provides TAB completion and history support.',
                      m._runsql_area_sql_shell_ckbtn)
    self._set_tooltip('--common-tables\n'
        'if --tables can not retrieve, usually because:\n'
        '  1.MySQL<5.0: information_schema is not available.\n'
        '  2.Access:    MSysObjects is not readable - default setting.\n'
        '  3.--current-user no read privileges of the system table.\n'
        '  if 1 or 2, check it.(see also, txt/common-tables.txt - sqlmap)',
                      m._brute_force_area_common_tables_ckbtn)
    self._set_tooltip('--common-columns see --common-tables',
                      m._brute_force_area_common_columns_ckbtn)
    # 4.File(R)
    self._set_tooltip('remote file path from the underlying file system\n'
        'only if: 1.MySQL, PostgreSQL or Microsoft SQL Server\n'
        '         2.the session user has the needed privileges',
                      m._file_read_area_file_read_ckbtn,
                      m._file_read_area_file_read_entry)
    self._set_tooltip('just view the file that has downloaded.',
                      m._file_read_area_file_read_btn)
    self._set_tooltip('--udf-inject\n'
        'UDF: user-defined function, only for MySQL or PostgreSQL.\n',
                      m._file_write_area_udf_ckbtn)
    self._set_tooltip('optional, together with --udf-inject',
                      m._file_write_area_shared_lib_ckbtn,
                      m._file_write_area_shared_lib_entry)
    self._set_tooltip('the local file path. if checked, --file-dest required.\n'
        'only if: 1.MySQL, PostgreSQL or Microsoft SQL Server\n'
        '         2.the session user has the needed privileges',
                      m._file_write_area_file_write_ckbtn,
                      m._file_write_area_file_write_entry)
    self._set_tooltip('the remote absolute path to upload\n'
        'only combine with  --file-write\n'
        'Note: single quote will show up in payload!',
                      m._file_write_area_file_dest_ckbtn,
                      m._file_write_area_file_dest_entry)
    self._set_tooltip('--os-cmd=\n'
        'only if: 1.MySQL, PostgreSQL or Microsoft SQL Server\n'
        '         2.the session user has the needed privileges\n\n'
        'MySQL/PostgreSQL: by uploading a shared library containing sys_exec() and sys_eval()\n\n'
        'SQL Server: by abusing xp_cmdshell stored procedure.\n'
        '            if disabled(SQL Server>=2005), sqlmap re-enables it;\n'
        '            if not exist, sqlmap creates it from scratch.',
                      m._file_os_access_os_cmd_ckbtn,
                      m._file_os_access_os_cmd_entry)
    self._set_tooltip('--os-shell  it provides TAB completion and history support.\n'
        'if no stacked queries(e.g. php/asp + MySQL) and the DBMS is MySQL;\n'
        '   the DBMS and the web server are hosted on the same server:\n\n'
        '  sqlmap abuses the SELECT clause\'s INTO OUTFILE to create a web backdoor'
        ' in a writable folder within the web server document root.\n\n'
        'mysql built-in web backdoor: ASP, ASP.NET, JSP, PHP',
                      m._file_os_access_os_shell_ckbtn)
    self._set_tooltip('MySQL和PostgreSQL:\n'
        '  1.Database in-memory execution of the Metasploit\'s shellcode via sqlmap own user-defined function sys_bineval()\n'
        '  2.Upload and execution of a Metasploit\'s stand-alone payload stager via sqlmap own user-defined function sys_exec()\n'
        '  or via xp_cmdshell() on Microsoft SQL Server',
                      m._file_os_access_os_pwn_ckbtn)
    self._set_tooltip('only when:\n'
        '  1.running sqlmap with high privileges(uid=0, windows: Administrator);\n'
        '  2.the target DBMS runs as Administrator on Windows,\n'
        'performing a SMB reflection attack (MS08-068).',
                      m._file_os_access_os_smbrelay_ckbtn)
    self._set_tooltip('Microsoft SQL Server 2000, 2005:\n'
        '  exploiting sp_replwritetovarbin(MS09-004)',
                      m._file_os_access_os_bof_ckbtn)
    self._set_tooltip('perform a privilege escalation via Metasploit\'s getsystem command\n'
        'Tips, on Windows:\n'
        '  MySQL: by default runs as SYSTEM\n'
        '  Server 2000: by default runs as SYSTEM\n'
        '  Server 2005/2008: runs most of the times as NETWORK SERVICE, sometimes as LOCAL SERVICE\n'
        '  PostgreSQL: runs as a low-privileged user postgres\n'
        '    linux:\n'
        '  PostgreSQL: runs as a low-privileged user postgres',
                      m._file_os_access_priv_esc_ckbtn)
    # 5.Other(T)
    self._set_tooltip('--check-internet',
                      m._page1_general_check_internet_ckbtn)
    self._set_tooltip('--fresh-queries',
                      m._page1_general_fresh_queries_ckbtn)
    self._set_tooltip('--forms\n'
        'if you want to test some kind of forms:\n'
        '  1.get the request file or form\'s fields by yourself,\n'
        '  2.use -r request_file or --data.\n'
        'now use --forms: sqlmap parse the forms it has\n'
        'Note: all forms and all fields in forms.',
                      m._page1_general_forms_ckbtn)
    self._set_tooltip('--cleanup\n'
        'Clean up the DBMS from sqlmap specific UDF and tables',
                      m._page1_misc_cleanup_ckbtn)
    self._set_tooltip('--table-prefix=\n'
        'Prefix used for temporary tables (default: "sqlmap")',
                      m._page1_general_table_prefix_ckbtn,
                      m._page1_general_table_prefix_entry)
    self._set_tooltip('--binary-fields=\n'
        'Result fields having binary values (e.g. "digest")\n',
                      m._page1_general_binary_fields_ckbtn,
                      m._page1_general_binary_fields_entry)
    self._set_tooltip('--charset=\n'
        'to speed-up the data retrieval for Blind SQL injection.',
                      m._page1_general_charset_ckbtn,
                      m._page1_general_charset_entry)
    self._set_tooltip('--encoding= Force character encoding used for data retrieval.',
                      m._page1_general_encoding_ckbtn,
                      m._page1_general_encoding_entry)
    self._set_tooltip('--test-filter=TE.. Select tests by payloads and/or titles (e.g. ROW)',
                      m._page1_general_test_filter_ckbtn,
                      m._page1_general_test_filter_entry)
    self._set_tooltip('--test-skip=TEST.. Skip tests by payloads and/or titles (e.g. BENCHMARK)',
                      m._page1_general_test_skip_ckbtn,
                      m._page1_general_test_skip_entry)
    self._set_tooltip('--crawl= collect vulnerable links crawling from the target location',
                      m._page1_general_crawl_ckbtn,
                      m._page1_general_crawl_entry)
    self._set_tooltip('--dump-format=\nCSV(default), HTML or SQLITE',
                      m._page1_general_dump_format_ckbtn,
                      m._page1_general_dump_format_entry)
    self._set_tooltip('--skip-waf\n'
        'uncheck: sends a dummy parameter containing a suspicious payload\n'
        'In case of any problems, check it.',
                      m._page1_misc_skip_waf_ckbtn)
    self._set_tooltip('--unstable  Adjust options for unstable connections',
                      m._page1_misc_unstable_ckbtn)
    self._set_tooltip('--gpage=\n'
        'by default -g use the first 100 resulting URLs\n'
        'combine with --gpage',
                      m._page1_misc_gpage_ckbtn)
    self._set_tooltip('--answers=ANSWERS Set predefined answers(e.g. "quit=N,follow=N")',
                      m._page1_misc_answers_ckbtn,
                      m._page1_misc_answers_entry)
    self._set_tooltip('-z MNEMONICS Use short mnemonics (e.g. "flu,bat,ban,tec=EU")',
                      m._page1_misc_z_ckbtn,
                      m._page1_misc_z_entry)
    # API区(page4)
    self._set_tooltip('sqlmapapi.py -s --username="admin" --password="secret"',
                      m._page4_api_server_label,
                      m._page4_api_server_entry)
    self._set_tooltip('options to view(space-separated). click "option:"',
                      m._page4_option_get_entry)
    _api_usage = '''sqlampapi HOW-TO:
    - server: sqlmapapi.py -s
    - client:
      1. input API server and Admin token
      2. click "create task"
      3. click "view tasks", tasks show up below
      4. input python dict type options to set here:
      {
        'url': 'http://www.site.com/vuln.php?id=1',
        'level': 1, 'risk': 1,
      }
      5. click "set:" to send the dict
      6. click start after sending the dict
      Note: 1. click "view tasks" to recheck tasks' status.
            2. sqlmapapi's options are not the same with sqlmap;
               sqlmapapi accept options, but won't verify it!
               delete the task whose option is invalid!
    '''
    self._set_tooltip(_api_usage,
                      m._page4_option_set_view)

  def _set_placeholder(self, placeholder, *widgets):
    '''
    widgets: mostly entry
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
