#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 08月 29日 星期三 15:34:10 CST

import os
import subprocess

from basis_and_tool.logging_needle import get_console_logger

logger = get_console_logger()


class Singal_Handlers(object):
  def __init__(self, w):
    '''
    w: sqlmap_ui.UI_Window
    还不能用注解, 会互相import
    '''
    self._w = w

  def build_all(self, button):
    ui = self._w
    _agent = ' --random-agent'
    _target = " -u '" + ui._url_combobox.get_child().get_text() + "'"

    _final_line = (
      _agent + _target + self._param_builder() +
      self._tamper_builder() + self._read_file_builder() +
      self._sql_query_builder() + self._post_builder() +
      self._level_builder() + self._risk_builder() +
      self._titles_builder() + self._hex_builder() +
      self._text_only_builder() + self._code_builder() +
      self._re_builder() + self._str_builder() +
      self._time_sec_builder() + self._tech_builder() +
      self._opti_turn_all_builder() + self._predict_builder() +
      self._keep_alive_builder() + self._null_connect_builder() +
      self._thread_num_builder() + self._dbms_builder() +
      self._union_col_builder() + self._union_chr_builder() +
      self._cookie_builder() + self._prefix_builder() +
      self._suffix_builder() + self._os_builder() +
      self._skip_builder() + self._batch_builder() +
      self._banner_builder() + self._cur_user_builder() +
      self._cur_db_builder() + self._hostname_builder() +
      self._is_dba_builder() + self._users_builder() +
      self._passwds_builder() + self._priv_builder() +
      self._roles_builder() + self._dbs_builder() +
      self._tables_builder() + self._columns_builder() +
      self._schema_builder() + self._count_builder() +
      self._dump_builder() + self._dump_all_builder() +
      self._search_builder() + self._D_builder() +
      self._T_builder() + self._C_builder() +
      self._no_sys_db_builder() + self._start_builder() +
      self._stop_builder() + self._first_builder() +
      self._last_builder() + self._verbose_builder() +
      self._finger_builder()
    )

    ui._cmd_entry.set_text(_final_line)

  def run_cmd(self, button):
    ui = self._w
    _sqlmap_opts = ui._cmd_entry.get_text()
    if _sqlmap_opts:
      if os.name == 'posix':
        _cmdline_str = '/usr/bin/env sqlmap' + _sqlmap_opts
      else:
        _cmdline_str = "start cmd /k python sqlmap.py " + _sqlmap_opts

      print(_cmdline_str)
      subprocess.Popen(_cmdline_str, shell = True)

  def _finger_builder(self):
    ''' -f, --fingerprint   Perform an extensive DBMS version fingerprint '''
    ui = self._w
    if ui._general_area_finger_chkbtn.get_active():
      return ' --fingerprint'
    return ''

  def _verbose_builder(self):
    ''' -v VERBOSE            Verbosity level: 0-6 (default 1) '''
    ui = self._w
    if ui._general_area_verbose_ckbtn.get_active():
      return ' -v ' + ui._detail_vv_combobox.get_child().get_text()
    return ''

  def _last_builder(self):
    ''' --last=LASTCHAR     Last query output word character to retrieve '''
    ui = self._w
    if ui._blind_area_last_ckbtn.get_active():
      return ' --last=' + ui._blind_area_last_entry.get_text()
    return ''

  def _first_builder(self):
    ''' --first=FIRSTCHAR   First query output word character to retrieve '''
    ui = self._w
    if ui._blind_area_first_ckbtn.get_active():
      return ' --first=' + ui._blind_area_first_entry.get_text()
    return ''

  def _stop_builder(self):
    ''' --stop=LIMITSTOP    Last dump table entry to retrieve '''
    ui = self._w
    if ui._limit_area_stop_ckbtn.get_active():
      return ' --stop=' + ui._limit_area_stop_entry.get_text()
    return ''

  def _start_builder(self):
    ''' --start=LIMITSTART  First dump table entry to retrieve '''
    ui = self._w
    if ui._limit_area_start_ckbtn.get_active():
      return ' --start=' + ui._limit_area_start_entry.get_text()
    return ''

  def _C_builder(self):
    ''' -C COL              DBMS database table column(s) to enumerate '''
    ui = self._w
    if ui._meta_area_C_ckbtn.get_active():
      return " -C '" + ui._meta_area_C_entry.get_text() + "'"
    return ''

  def _T_builder(self):
    '''
    -T TBL              DBMS database table(s) to enumerate
    '''
    ui = self._w
    if ui._meta_area_T_ckbtn.get_active():
      return " -T '" + ui._meta_area_T_entry.get_text() + "'"
    return ''

  def _D_builder(self):
    '''
    -D DB               DBMS database to enumerate
    '''
    ui = self._w
    if ui._meta_area_D_ckbtn.get_active():
      return " -D '" + ui._meta_area_D_entry.get_text() + "'"
    return ''

  def _no_sys_db_builder(self):
    ''' --exclude-sysdbs    Exclude DBMS system databases when enumerating tables '''
    ui = self._w
    if ui._dump_area_no_sys_db_ckbtn.get_active():
      return ' --exclude-sysdb'
    return ''

  def _search_builder(self):
    ''' --search            Search column(s), table(s) and/or database name(s) '''
    ui = self._w
    if ui._dump_area_search_ckbtn.get_active():
      return ' --search'
    return ''

  def _dump_all_builder(self):
    ''' --dump-all          Dump all DBMS databases tables entries '''
    ui = self._w
    if ui._dump_area_dump_all_ckbtn.get_active():
      return ' --dump-all'
    return ''

  def _dump_builder(self):
    ''' --dump              Dump DBMS database table entries '''
    ui = self._w
    if ui._dump_area_dump_ckbtn.get_active():
      return ' --dump'
    return ''

  def _count_builder(self):
    ''' --count             Retrieve number of entries for table(s) '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[2][3].get_active():
      return ' --count'
    return ''

  def _schema_builder(self):
    ''' --schema            Enumerate DBMS schema '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[2][2].get_active():
      return ' --schema'
    return ''

  def _columns_builder(self):
    ''' --columns           Enumerate DBMS database table columns '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[2][1].get_active():
      return ' --columns'
    return ''

  def _tables_builder(self):
    ''' --tables            Enumerate DBMS database tables '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[2][0].get_active():
      return ' --tables'
    return ''

  def _dbs_builder(self):
    ''' --dbs               Enumerate DBMS databases '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[1][4].get_active():
      return ' --dbs'
    return ''

  def _roles_builder(self):
    ''' --roles             Enumerate DBMS users roles '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[1][3].get_active():
      return ' --roles'
    return ''

  def _priv_builder(self):
    ''' --privileges        Enumerate DBMS users privileges '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[1][2].get_active():
      return ' --privileges'
    return ''

  def _passwds_builder(self):
    ''' --passwords         Enumerate DBMS users password hashes '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[1][1].get_active():
      return ' --passwords'
    return ''

  def _users_builder(self):
    ''' --users             Enumerate DBMS users '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[1][0].get_active():
      return ' --users'
    return ''

  def _is_dba_builder(self):
    ''' --is-dba            Detect if the DBMS current user is DBA '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[0][4].get_active():
      return ' --is-dba'
    return ''

  def _hostname_builder(self):
    ''' --hostname          Retrieve DBMS server hostname '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[0][3].get_active():
      return ' --hostname'
    return ''

  def _cur_db_builder(self):
    ''' --current-db        Retrieve DBMS current database '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[0][2].get_active():
      return ' --current-db'
    return ''

  def _cur_user_builder(self):
    ''' --current-user      Retrieve DBMS current user '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[0][1].get_active():
      return ' --current-user'
    return ''

  def _banner_builder(self):
    ''' -b, --banner        Retrieve DBMS banner '''
    ui = self._w
    if ui._enum_area_opts_ckbtns[0][0].get_active():
      return ' --banner'
    return ''

  def _batch_builder(self):
    ''' --batch             Never ask for user input, use the default behavior '''
    ui = self._w
    if ui._general_area_batch_ckbtn.get_active():
      return ' --batch'
    return ''

  def _skip_builder(self):
    ''' --skip=SKIP         Skip testing for given parameter(s) '''
    ui = self._w
    if ui._inject_area_skip_ckbtn.get_active():
      return " --skip='" + ui._inject_area_skip_entry.get_text() + "'"
    return ''

  def _os_builder(self):
    ''' --os=OS             Force back-end DBMS operating system to provided value '''
    ui = self._w
    if ui._inject_area_os_ckbtn.get_active():
      return " --os='" + ui._inject_area_os_entry.get_text() + "'"
    return ''

  def _suffix_builder(self):
    ''' --suffix=SUFFIX     Injection payload suffix string '''
    ui = self._w
    if ui._inject_area_suffix_ckbtn.get_active():
      return " --suffix='" + ui._inject_area_suffix_entry.get_text() + "'"
    return ''

  def _prefix_builder(self):
    ''' --prefix=PREFIX     Injection payload prefix string '''
    ui = self._w
    if ui._inject_area_prefix_ckbtn.get_active():
      return " --prefix='" + ui._inject_area_prefix_entry.get_text() + "'"
    return ''

  def _cookie_builder(self):
    ''' --cookie=COOKIE     HTTP Cookie header value '''
    ui = self._w
    if ui._cookie_ckbtn.get_active():
      return " --cookie='" + ui._cookie_entry.get_text() + "'"
    return ''

  def _union_chr_builder(self):
    ''' --union-char=UCHAR  Character to use for bruteforcing number of columns '''
    ui = self._w
    if ui._tech_area_union_chr_ckbtn.get_active():
      return " --union-cols='" + ui._tech_area_union_chr_entry.get_text() + "'"
    return ''

  def _union_col_builder(self):
    ''' --union-cols=UCOLS  Range of columns to test for UNION query SQL injection '''
    ui = self._w
    if ui._tech_area_union_col_ckbtn.get_active():
      return " --union-cols='" + ui._tech_area_union_col_entry.get_text() + "'"
    return ''

  def _dbms_builder(self):
    ''' --dbms=DBMS         Force back-end DBMS to provided value '''
    ui = self._w
    if ui._inject_area_dbms_ckbtn.get_active():
      return " --dbms='" + ui._inject_area_dbms_combobox.get_child().get_text() + "'"
    return ''

  def _thread_num_builder(self):
    ''' --threads=THREADS   Max number of concurrent HTTP(s) requests (default 1) '''
    ui = self._w
    if ui._optimize_area_thread_num_ckbtn.get_active():
      return " --threads='" + ui._optimize_area_thread_num_combobox.get_child().get_text() + "'"
    return ''

  def _null_connect_builder(self):
    ''' --null-connection   Retrieve page length without actual HTTP response body '''
    ui = self._w
    if ui._optimize_area_null_connect_ckbtn.get_active():
      return ' --null-connection'
    return ''

  def _keep_alive_builder(self):
    ''' --keep-alive        Use persistent HTTP(s) connections '''
    ui = self._w
    if ui._optimize_area_keep_alive_ckbtn.get_active():
      return ' --keep-alive'
    return ''

  def _predict_builder(self):
    ''' --predict-output    Predict common queries output '''
    ui = self._w
    if ui._optimize_area_predict_ckbtn.get_active():
      return ' --predict-output'
    return ''

  def _opti_turn_all_builder(self):
    ''' -o                  Turn on all optimization switches '''
    ui = self._w
    if ui._optimize_area_turn_all_ckbtn.get_active():
      return ' -o'
    return ''

  def _tech_builder(self):
    ''' --technique=TECH    SQL injection techniques to use (default "BEUSTQ") '''
    ui = self._w
    if ui._tech_area_tech_ckbtn.get_active():
      return " --technique='" + ui._tech_area_tech_entry.get_text() + "'"
    return ''

  def _time_sec_builder(self):
    ''' --time-sec=TIMESEC  Seconds to delay the DBMS response (default 5) '''
    ui = self._w
    if ui._tech_area_time_sec_ckbtn.get_active():
      return " --time-sec='" + ui._tech_area_time_sec_entry.get_text() + "'"
    return ''

  def _str_builder(self):
    ''' --string=STRING     String to match when query is evaluated to True '''
    ui = self._w
    if ui._check_area_str_ckbtn.get_active():
      return " --string='" + ui._check_area_str_entry.get_text() + "'"
    return ''

  def _re_builder(self):
    ''' --regexp=REGEXP     Regexp to match when query is evaluated to True '''
    ui = self._w
    if ui._check_area_re_ckbtn.get_active():
      return " --regexp='" + ui._check_area_re_entry.get_text() + "'"
    return ''

  def _code_builder(self):
    ''' --code=CODE         HTTP code to match when query is evaluated to True '''
    ui = self._w
    if ui._check_area_code_ckbtn.get_active():
      return ' --code="' + ui._check_area_code_entry.get_text() + '"'
    return ''

  def _text_only_builder(self):
    ''' --text-only         Compare pages based only on the textual content '''
    ui = self._w
    if ui._check_area_text_only_ckbtn.get_active():
      return ' --text-only'
    return ''

  def _hex_builder(self):
    ''' --hex               Use hex conversion during data retrieval '''
    ui = self._w
    if ui._general_area_hex_ckbtn.get_active():
      return ' --hex'
    return ''

  def _titles_builder(self):
    ''' --titles            Compare pages based only on their titles '''
    ui = self._w
    if ui._check_area_titles_ckbtn.get_active():
      return ' --titles'
    return ''

  def _risk_builder(self):
    ''' --risk=RISK         Risk of tests to perform (1-3, default 1) '''
    ui = self._w
    if ui._check_area_risk_ckbtn.get_active():
      return " --risk='" + ui._check_area_risk_combobox.get_child().get_text() + "'"
    return ''

  def _level_builder(self):
    ''' --level=LEVEL       Level of tests to perform (1-5, default 1) '''
    ui = self._w
    if ui._check_area_level_ckbtn.get_active():
      return " --level='" + ui._check_area_level_combobox.get_child().get_text() + "'"
    return ''

  def _post_builder(self):
    ''' --data=DATA         Data string to be sent through POST '''
    ui = self._w
    if ui.page1_request_post_ckbtn.get_active():
      return " --data='" + ui.page1_request_post_entry.get_text() + "'"
    return ''

  def _sql_query_builder(self):
    ''' --sql-query=QUERY   SQL statement to be executed '''
    ui = self._w
    if ui._runsql_area_runsql_ckbtn.get_active():
      return " --sql-query='" + ui._runsql_area_runsql_entry.get_text() + "'"
    return ''

  def _read_file_builder(self):
    ''' --file-read=RFILE   Read a file from the back-end DBMS file system '''
    ui = self._w
    if ui._file_read_area_file_read_ckbtn.get_active():
      return " --file-read='" + ui._file_read_area_file_read_entry.get_text() + "'"
    return ''

  def _tamper_builder(self):
    '''
    暂时不写
    '''
    return ''

  def _param_builder(self):
    ''' -p TESTPARAMETER    Testable parameter(s) '''
    ui = self._w
    if ui._inject_area_param_ckbtn.get_active():
      return " -p '" + ui._inject_area_param_entry.get_text() + "'"
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
