#!/usr/bin/env python3
#
# 2021-01-02 14:35:19


class Text(object):
  def __init__(self, language = 'en'):
    self._locale = language

    self.text_dict = {}

    self.text_dict['open1'] = ''
    self.text_dict['open2'] = None

    self.text_dict['open'] = '打开'
    self.text_dict['language'] = '语言'

    self.text_dict['OPTIONS(_1)'] = '选项区(_1)'
    self.text_dict['EXECUTION(_2)'] = '输出区(_2)'
    self.text_dict['LOG(_3)'] = '日志区(_3)'
    self.text_dict['SQLMAPAPI(_4)'] = 'API区(_4)'
    self.text_dict['HELP(_H)'] = '帮助(_H)'
    self.text_dict['ABOUT'] = '关于'

    self.text_dict['reopen'] = '重开'
    self.text_dict['context menu'] = '右键菜单'
    self.text_dict['Copy(C)'] = '复制(C)'
    self.text_dict['Paste(V)'] = '粘贴(V)'
    self.text_dict['view target file'] = '查看target文件'
    self.text_dict['view log file'] = '查看log文件'
    self.text_dict['create task'] = '创建任务'
    self.text_dict['view tasks'] = '显示任务'
    self.text_dict['delete all tasks'] = '删除所有任务'
    self.text_dict['clear view'] = '清空反馈的结果'
    self.text_dict['username:'] = '用户名:'
    self.text_dict['passwd:'] = '密码:'
    self.text_dict['stop'] = '停止'
    self.text_dict['start'] = '启动'
    self.text_dict['list'] = '所有选项'
    self.text_dict['option:'] = '选项:'
    self.text_dict['set:'] = '设置:'
    self.text_dict['view:('] = '查看:('
    self.text_dict['flush all tasks: Done.'] = '清空全部任务: 成功.'

    self.text_dict['Take effects after restarting GUI.'] = '重启GUI后生效.'

    self.text_dict['A.Options are collected here:'] = 'A.收集选项 的结果显示在这:'

    self.text_dict['Inject(_Q)'] = '测试(_Q)'
    self.text_dict['Request(_W)'] = '请求(_W)'
    self.text_dict['Enumerate(_E)'] = '枚举(_E)'
    self.text_dict['File(_R)'] = '文件(_R)'
    self.text_dict['Other(_T)'] = '其他(_T)'

    self.text_dict['sqlmap path:'] = '指定sqlmap路径:'
    self.text_dict['Injection'] = '注入选项'
    self.text_dict['Detection'] = '探测选项'
    self.text_dict['Technique'] = '各注入技术的选项'
    self.text_dict['Optimize'] = '性能优化'
    self.text_dict['Offen'] = '常用选项'
    self.text_dict['Hidden'] = '隐藏选项'
    self.text_dict['Request custom'] = 'request定制'
    self.text_dict['Anonymous/Proxy'] = '隐匿/代理'
    self.text_dict['Enumeration'] = '枚举'
    self.text_dict['Dump'] = 'Dump(转储)'
    self.text_dict['Limit'] = 'Limit(dump时的限制)'
    self.text_dict['Blind inject options'] = '盲注选项'
    self.text_dict['DB, Table, Column name...'] = '数据库名, 表名, 列名...'
    self.text_dict['Execute SQL'] = '执行SQL语句'
    self.text_dict['Brute force'] = '暴破表名/列名'
    self.text_dict['Read remote file'] = '读取远程文件'
    self.text_dict['Upload local file'] = '上传本地文件'
    self.text_dict['Access to the OS behind the DBMS'] = '访问后端OS'
    self.text_dict['Access to register in remote WIN'] = '访问WIN下注册表'
    self.text_dict['General'] = '通用项'
    self.text_dict['Misc'] = '杂项'

    self.text_dict['check if exists:'] = '检查是否存在:'
    self.text_dict['cat'] = '查看'
    self.text_dict['with Meterpreter(TCP connect):'] = 'Meterpreter相关(TCP连接):'
    self.text_dict['operate:'] = '操作:'
    self.text_dict['read'] = '读取'
    self.text_dict['add'] = '新增'
    self.text_dict['delete'] = '删除'

    self.text_dict['A.collect(_A)'] = 'A.收集选项(_A)'
    self.text_dict['unselect(_S)'] = '反选(_S)'
    self.text_dict['clear all inputs(_D)'] = '清空所有输入框(_D)'
    self.text_dict['B.run(_F)'] = 'B.开始(_F)'

    # sqlmap -hh | awk '/^ *-/{print($1)}' | sed -e 's;[,=].*;;' -e 's;\(.*\);self.text_dict["\1"] = None;'
    self.text_dict["-hh"] = None
    self.text_dict["--version"] = None
    self.text_dict["-v"] = '输出详细程度'

    self.text_dict["-u"] = '目标url'
    self.text_dict["-u URL"] = self.text_dict["-u"]
    self.text_dict["-d"] = None
    self.text_dict["-l"] = 'burp日志'
    self.text_dict["-l LOGFILE"] = self.text_dict["-l"]
    self.text_dict["-m"] = 'BULKFILE'
    self.text_dict["-m BULKFILE"] = self.text_dict["-m"]
    self.text_dict["-r"] = 'HTTP请求'
    self.text_dict["-r REQUESTFILE"] = self.text_dict["-r"]
    self.text_dict["-g"] = 'GOOGLEDORK'
    self.text_dict["-g GOOGLEDORK"] = self.text_dict["-g"]
    self.text_dict["-c"] = 'ini文件'
    self.text_dict["-c CONFIGFILE"] = self.text_dict["-c"]

    self.text_dict["-A"] = '指定User-Agent头'
    self.text_dict["--user-agent"] = self.text_dict["-A"]
    self.text_dict["-H"] = '额外的header(-H)'
    self.text_dict["-header"] = self.text_dict["-H"]
    self.text_dict["--method"] = '指定HTTP请求方式'
    self.text_dict["--data"] = '通过POST提交data:'
    self.text_dict["--param-del"] = '指定--data=中的参数分隔符'
    self.text_dict["--cookie"] = '请求中要包含的Cookie:'
    self.text_dict["--cookie-del"] = '指定cookie分隔符'
    self.text_dict["--live-cookies"] = 'live_cookies'
    self.text_dict["--load-cookies"] = '本地Cookie文件'
    self.text_dict["--drop-set-cookie"] = '丢弃Set-Cookie头'
    self.text_dict["--mobile"] = '模拟手机请求'
    self.text_dict["--random-agent"] = '随机User-Agent头'
    self.text_dict["--host"] = 'Host头'
    self.text_dict["--referer"] = 'referer头'
    self.text_dict["--headers"] = '额外的headers'
    self.text_dict["--auth-type"] = 'http认证类型'
    self.text_dict["--auth-cred"] = 'http认证账密'
    self.text_dict["--auth-file"] = 'http认证文件'
    self.text_dict["--ignore-code"] = '忽略错误型状态码:'
    self.text_dict["--ignore-proxy"] = '忽略系统默认代理'
    self.text_dict["--ignore-redirects"] = '忽略重定向'
    self.text_dict["--ignore-timeouts"] = '忽略连接超时'
    self.text_dict["--proxy"] = '使用代理'
    self.text_dict["--proxy-cred"] = None
    self.text_dict["--proxy-file"] = '代理列表文件'
    self.text_dict["--proxy-freq"] = None
    self.text_dict["--tor"] = '使用Tor匿名网络'
    self.text_dict["--tor-port"] = 'Tor端口'
    self.text_dict["--tor-type"] = 'Tor代理类型'
    self.text_dict["--check-tor"] = '检查Tor连接'
    self.text_dict["--delay"] = '请求间隔(秒)'
    self.text_dict["--timeout"] = '超时前等几秒'
    self.text_dict["--retries"] = '超时重试次数'
    self.text_dict["--randomize"] = '指定要随机改变值的参数'
    self.text_dict["--safe-url"] = '顺便掺杂地访问一个安全url'
    self.text_dict["--safe-post"] = '提交到安全url的post数据'
    self.text_dict["--safe-req"] = '从文件载入safe HTTP请求'
    self.text_dict["--safe-freq"] = '访问安全url的频率'
    self.text_dict["--skip-urlencode"] = 'payload不使用url编码'
    self.text_dict["--csrf-token"] = 'csrf_token'
    self.text_dict["--csrf-url"] = '获取csrf_token的url'
    self.text_dict["--csrf-method"] = 'csrf_method'
    self.text_dict["--csrf-retries"] = 'csrf_retries'
    self.text_dict["--force-ssl"] = '强制使用HTTPS'
    self.text_dict["--chunked"] = '"分块传输"发送POST请求'
    self.text_dict["--hpp"] = 'HTTP参数污染'
    self.text_dict["--eval"] = None
    self.text_dict["-o"] = '启用所有优化选项'
    self.text_dict["--predict-output"] = '预测通常的查询结果'
    self.text_dict["--keep-alive"] = 'http连接使用keep-alive'
    self.text_dict["--null-connection"] = '只比较响应大小报头, 不获取响应主体'
    self.text_dict["--threads"] = '使用线程数:'
    self.text_dict["-p"] = '仅测参数'
    self.text_dict["--skip"] = '忽略参数'
    self.text_dict["--skip-static"] = '跳过不像是动态的参数'
    self.text_dict["--param-exclude"] = '忽略参数(正则)'
    self.text_dict["--param-filter"] = '仅测范围'
    self.text_dict["--dbms"] = '固定DBMS为'
    self.text_dict["--dbms-cred"] = 'DB认证'
    self.text_dict["--os"] = '固定OS为'
    self.text_dict["--invalid-bignum"] = '使用大数'
    self.text_dict["--invalid-logical"] = '使用布尔运算'
    self.text_dict["--invalid-string"] = '使用随机字串'
    self.text_dict["--no-cast"] = '关闭数据类型转换'
    self.text_dict["--no-escape"] = '关掉string转义'
    self.text_dict["--prefix"] = 'payload前缀'
    self.text_dict["--suffix"] = 'payload后缀'
    self.text_dict["--tamper"] = 'tamper脚本'
    self.text_dict["--level"] = '探测等级(范围)'
    self.text_dict["--risk"] = 'payload危险等级'
    self.text_dict["--string"] = '指定True时的字符串'
    self.text_dict["--not-string"] = '指定False时的字符串'
    self.text_dict["--regexp"] = '指定正则'
    self.text_dict["--code"] = '指定http状态码'
    self.text_dict["--smart"] = '寻找明显目标并测试'
    self.text_dict["--text-only"] = '仅对比文本'
    self.text_dict["--titles"] = '仅对比title'
    self.text_dict["--technique"] = '注入技术'
    self.text_dict["--time-sec"] = '指定DB延迟几秒响应'
    self.text_dict["--union-cols"] = '指定最大union列数'
    self.text_dict["--union-char"] = '指定枚举列数时所用字符'
    self.text_dict["--union-from"] = '指定枚举列数时from的表名'
    self.text_dict["--dns-domain"] = '指定DNS'
    self.text_dict["--second-url"] = '指定二阶响应的url'
    self.text_dict["--second-req"] = '使用含二阶HTTP请求的文件:'
    self.text_dict["-f"] = '精确检测DB等版本信息'
    self.text_dict["--fingerprint"] = self.text_dict["-f"]
    self.text_dict["-a"] = None
    self.text_dict["-b"] = 'DB banner'
    self.text_dict["--banner"] = self.text_dict["-b"]
    self.text_dict["--current-user"] = '当前用户'
    self.text_dict["--current-db"] = '当前数据库'
    self.text_dict["--hostname"] = '主机名'
    self.text_dict["--is-dba"] = '是否为DBA'
    self.text_dict["--users"] = '用户'
    self.text_dict["--passwords"] = "密码"
    self.text_dict["--privileges"] = "权限"
    self.text_dict["--roles"] = "角色"
    self.text_dict["--dbs"] = "库名"
    self.text_dict["--tables"] = "表名"
    self.text_dict["--columns"] = "列名"
    self.text_dict["--schema"] = "架构"
    self.text_dict["--count"] = "行数"
    self.text_dict["--dump"] = 'dump(某库某表的条目)'
    self.text_dict["--dump-all"] = '全部dump(拖库)'
    self.text_dict["--search"] = '搜索'
    self.text_dict["--comments"] = "备注"
    self.text_dict["--statements"] = '获取正在运行的sql语句'
    self.text_dict["-D"] = '指定库名'
    self.text_dict["-T"] = '指定表名'
    self.text_dict["-C"] = '指定列名'
    self.text_dict["-X"] = '排除标志符'
    self.text_dict["-U"] = '指定用户'
    self.text_dict["--exclude-sysdbs"] = '排除系统库'
    self.text_dict["--pivot-column"] = '指定Pivot列名'
    self.text_dict["--where"] = 'where子句'
    self.text_dict["--start"] = '始于第'
    self.text_dict["--stop"] = '止于第'
    self.text_dict["--first"] = '从第'
    self.text_dict["--last"] = '到第'
    self.text_dict["--sql-query"] = 'SQL语句:'
    self.text_dict["--sql-shell"] = '打开一个SQL交互shell'
    self.text_dict["--sql-file"] = '本地SQL文件:'
    self.text_dict["--common-tables"] = '常用表名'
    self.text_dict["--common-columns"] = '常用列名'
    self.text_dict["--common-files"] = '常用文件'
    self.text_dict["--udf-inject"] = '注入UDF(仅限MySQL和PostgreSQL)'
    self.text_dict["--shared-lib"] = '本地共享库路径(--shared-lib=)'
    self.text_dict["--file-read"] = '远程文件路径(--file-read=)'
    self.text_dict["--file-write"] = '本地文件路径(--file-write=)'
    self.text_dict["--file-dest"] = '远程文件路径(--file-dest=)'
    self.text_dict["--os-cmd"] = '执行CLI命令'
    self.text_dict["--os-shell"] = '获取交互shell'
    self.text_dict["--os-pwn"] = None
    self.text_dict["--os-smbrelay"] = None
    self.text_dict["--os-bof"] = None
    self.text_dict["--priv-esc"] = None
    self.text_dict["--msf-path"] = '本地Metasploit安装路径'
    self.text_dict["--tmp-path"] = '远程临时目录(绝对路径)'
    self.text_dict["--reg-read"] = None
    self.text_dict["--reg-add"] = None
    self.text_dict["--reg-del"] = None
    self.text_dict["--reg-key"] = '键路径'
    self.text_dict["--reg-value"] = '键名'
    self.text_dict["--reg-data"] = '键值'
    self.text_dict["--reg-type"] = '键值类型'
    self.text_dict["-s"] = '载入会话文件'
    self.text_dict["-t"] = '转存所有http流量到文本'
    self.text_dict["--answers"] = '设置交互时的问题答案:'
    self.text_dict["--base64"] = None
    self.text_dict["--base64-safe"] = None
    self.text_dict["--batch"] = '非交互模式, 一切皆默认'
    self.text_dict["--binary-fields"] = '有二进制值的字段'
    self.text_dict["--check-internet"] = '检查与目标的网络连接'
    self.text_dict["--cleanup"] = '清理DBMS中的入侵痕迹!'
    self.text_dict["--crawl"] = '爬网站(的层级/深度)'
    self.text_dict["--crawl-exclude"] = '爬站时排除(正则)页面'
    self.text_dict["--csv-del"] = '(csv文件的)分隔符'
    self.text_dict["--charset"] = '盲注所用的字符集合'
    self.text_dict["--dump-format"] = 'dump结果的文件格式'
    self.text_dict["--encoding"] = '字符编码(用于数据获取)'
    self.text_dict["--eta"] = '显示剩余时间'
    self.text_dict["--flush-session"] = '清空本地的目标session>'
    self.text_dict["--forms"] = '获取form表单参数并测试'
    self.text_dict["--fresh-queries"] = '刷新此次查询'
    self.text_dict["--gpage"] = 'GOOGLEDORK时的页码'
    self.text_dict["--har"] = '转存至HAR文件'
    self.text_dict["--hex"] = '响应使用hex转换'
    self.text_dict["--output-dir"] = '指定output目录'
    self.text_dict["--parse-errors"] = '解析并显示响应中的错误信息'
    self.text_dict["--preprocess"] = '处理请求的脚本'
    self.text_dict["--postprocess"] = '处理响应的脚本'
    self.text_dict["--repair"] = '重新获取有未知符号(?)的条目'
    self.text_dict["--save"] = '保存选项至INI文件'
    self.text_dict["--scope"] = '从代理日志过滤出目标(正则)'
    self.text_dict["--skip-heuristics"] = '跳过SQLi/XSS侦测'
    self.text_dict["--skip-waf"] = '跳过WAF/IPS侦测'
    self.text_dict["--table-prefix"] = '临时表前缀'
    self.text_dict["--test-filter"] = '测试过滤器(从payload/title选择)'
    self.text_dict["--test-skip"] = '测试跳过(从payload/title选择)'
    self.text_dict["--web-root"] = '远程web的根目录'
    self.text_dict["-z"] = '使用短的助记符'
    self.text_dict["--alert"] = '发现注入时运行本地命令:'
    self.text_dict["--beep"] = '响铃'
    self.text_dict["--dependencies"] = '检查丢失的(非核心的)sqlmap依赖'
    self.text_dict["--disable-coloring"] = '禁用终端输出的颜色'
    self.text_dict["--list-tampers"] = '列出可用的tamper脚本'
    self.text_dict["--offline"] = '离线模式(仅使用本地会话数据)'
    self.text_dict["--purge"] = '抹除所有本地记录!'
    self.text_dict["--results-file"] = '指定CSV文件位置:'
    self.text_dict["--sqlmap-shell"] = '打开sqlmap交互shell'
    self.text_dict["--tmp-dir"] = '本地临时目录'
    self.text_dict["--unstable"] = '为不稳定的连接调整选项'
    self.text_dict["--update"] = '更新sqlmap'
    self.text_dict["--wizard"] = '新手向导'

  def gettext(self, string: str) -> str:
    if self._locale == 'zh':
      _ = self.text_dict.get(string, string)
      if _:
        return _
    return string

  def get_level_note(self):
    if self._locale == 'zh':
      _ = ('Level 1(默认): 所有GET, POST参数\n'
           'Level 2  追加: Cookie\n'
           'Level 3  追加: User-Agent/Referer\n'
           'Level 4  追加: ?\n'
           'Level 5  追加: Host报头')
    else:
      _ = ('Level 1(default): all GET, POST fields\n'
           'Level 2   append: Cookie\n'
           'Level 3   append: User-Agent/Referer\n'
           'Level 4   append: ?\n'
           'Level 5   append: Host header')
    return _

  def get_risk_note(self):
    if self._locale == 'zh':
      _ = ('Risk 1(默认): 基本无风险\n'
           'Risk 2  追加: 大量时间型盲注\n'
           'Risk 3  追加: OR型布尔盲注')
    else:
      _ = ('Risk 1(default): no risk\n'
           'Risk 2   append: Time-Based Blind\n'
           'Risk 3   append: "OR" Blind')
    return _


def main():
  _ = Text()
  print(_.gettext('open'))
  print(_.gettext('open1'))
  print(_.gettext('open2'))
  print(_.gettext('open3'))


if __name__ == '__main__':
  main()
