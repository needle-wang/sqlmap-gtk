#!/usr/bin/env python3
#
# 2021-01-05 01:43:57

'''
# https://blog.51cto.com/underthehood/1663604
# http://blog.timd.cn/python-gettext/
# https://docs.python.org/3.8/library/gettext.html#gettext.translation

edit my_app.py:
import gettext

_ = gettext.gettext

if __name__ == "__main__":
  print _("hello world")

cd static
# 1.生成1个pot文件(翻译模板), -k与_之间不能有空格
xgettext -k_ -o sqlmap_gtk.pot --from-code='UTF-8' ../sqlmap_gtk.py
# 2.首次生成po文件(翻译文件)
msginit -l en -i sqlmap_gtk.pot
msginit -l zh_CN -i sqlmap_gtk.pot
# 3.修改po文件, 翻译字符串, 并把里面的charset改成UTF-8
vim en.po; vim zh_CN.po
# 4.新建目录结构, 用msgfmt生成mo文件(用-o把mo文件放到相应目录中)
mkdir -p locale/zh_CN/LC_MESSAGES
mkdir -p locale/en/LC_MESSAGES
msgfmt -o locale/zh_CN/LC_MESSAGES/sqlmap_gtk.mo zh_CN.po
msgfmt -o locale/en/LC_MESSAGES/sqlmap_gtk.mo en.po
# 以上完成所有准备工作.
# 之后py文件中要翻译的字串发生变化(修改/增删), 要重新生成po文件,
用msgmerge替代msginit:
msgmerge -U zh_CN.po my_app.pot
再重复3和4.

# 国际化, 两种方式:
# 一、根据OS的环境变量自动选择语言: 略
#     向 python解释器 的全局变量里添加 _ = gettext.gettext
# 二、在程序中实时切换:
#     向 当前模块 的全局变量里添加 _ = gettext.gettext
edit my_app.py:
import os
import gettext
# 这其实是mo文件的文件名!
APP_NAME = "my_app"
# mo文件的base目录
LOCALE_DIR = os.path.abspath("locale")
# 这条语句会将_()函数自动放到python的内置命名空间中
gettext.install(APP_NAME, LOCALE_DIR)  # 如果不想, 也可不加, 用下面的install就行
# 获取中文翻译类的实例
lang_zh_CN = gettext.translation(APP_NAME, LOCALE_DIR, ["zh_CN"])
# 获取英文翻译类的实例
lang_en = gettext.translation(APP_NAME, LOCALE_DIR, ["en"])

if __name__ == "__main__":
  # 安装中文, _()在当前模块的命名空间
  lang_zh_CN.install()
  print _("hello world")
  # 安装英文(程序中实时切换回英文)
  lang_en.install()
  print _("hello world")
'''
