#!/usr/bin/env python3
#
# 2018年 11月 09日 星期五 14:48:40 CST

from os import sep as OS_SEP
# python3.5+
from pathlib import Path
from urllib import request

from gtk3_header import g, Gdk as d

drag_targets = [g.TargetEntry.new("text/uri-list", 0, 80)]


class FileEntry(g.Entry):
  def __init__(self):
    super().__init__()

    self.completion = g.EntryCompletion()
    # self.completion.set_match_func(self.match_partly, None)

    self.completion.set_model(g.ListStore(str))
    # 行内选择, 选择上框, 会触发changed和insert-text, 不能一起使用
    # self.completion.set_inline_selection(True)
    # 行内补全, 匹配成功的条目自动上框(选中状态)
    self.completion.set_inline_completion(True)

    self.completion.set_minimum_key_length(1)
    self.completion.set_text_column(0)

    self.set_completion(self.completion)
    # 一用insert-text信号, 就报错~:
    # Warning: g_value_get_int: assertion 'G_VALUE_HOLDS_INT (value)' failed
    self.connect('changed', self.on_changed)

    # 拖放文件功能
    self.drag_dest_set(g.DestDefaults.ALL, drag_targets, d.DragAction.COPY)
    self.connect('drag-data-received', self.set_path_by_drag)

  def set_path_by_drag(self, entry, context, x, y, data, info, time):
    '''
    https://stackoverflow.com/questions/24094186/drag-and-drop-file-example-in-pygobject
    为什么会调用两次?? 单独写例子却只运行一次, 继承的原因嘛?
    '''
    uris = data.get_data().split()
    print(uris)
    if uris:
      path = self.get_file_path_from_dnd_dropped_uri(uris[0].decode('utf8'))
      # print('path: ', path)
      entry.set_text(path)
    # context.finish(True, False, time)

    return True

  def get_file_path_from_dnd_dropped_uri(self, uri):
    path = ""
    if uri.startswith('file:\\\\\\'):  # windows
        path = uri[8:]  # 8 is len('file:///')
    elif uri.startswith('file://'):  # nautilus, rox
        path = uri[7:]  # 7 is len('file://')
    elif uri.startswith('file:'):  # xffm
        path = uri[5:]  # 5 is len('file:')

    path = request.url2pathname(path)  # escape special chars
    # path = path.strip('\r\n\x00')  # remove \r\n and NULL
    return path

  def on_changed(self, *args):
    '''
    不管是用户输入, 还是set_text都会触发此方法!
    竟然不存在 判断是否为用户打字触发的 信号~
    修复这两个类竟然花了一晚上时间, 唉...
    '''
    if not self.has_focus():
      return
    _file_store = self.completion.get_model()
    _file_store.clear()

    _file = Path(self.get_text().strip())
    # 如果写c::,  会抛异常, 暂时不管
    if not _file.is_dir():
      _file = _file.parent

    if _file.is_dir():
      try:  # for iterdir()
        for _i in _file.iterdir():
          if _i.is_dir():
            # _file_store.append([_i.name + OS_SEP])
            _file_store.append([str(_i) + OS_SEP])
          else:
            # _file_store.append([_i.name])
            _file_store.append([str(_i)])
      except PermissionError as e:
        print(e)

  def match_partly(self, completion, entrystr, iter, data):
    '''
    set_inline_completion不生效呢?
    '''
    modelstr = completion.get_model()[iter][0]
    _entrystr_name = Path(entrystr).name
    return modelstr.startswith(_entrystr_name)


class NumberEntry(g.Entry, g.Editable):
  '''
  Entry是Editable的子类, 如果单继承Entry的话, 由于python的动态特性,
  本类任何重载的方法, 会反应到g.Editable上(啥?? # 自答, 然后自问)
  1. https://stackoverflow.com/questions/2726839/creating-a-pygtk-text-field-that-only-accepts-number
  2. https://stackoverflow.com/questions/38815694/gtk-3-position-attribute-on-insert-text-signal-from-gtk-entry-is-always-0
  **Important Note: You have to inherit from Gtk.Editable in addition to Gtk.Entry.**
  If you do not do so,
  you will start seeing (the validation or whatever you do inside do_insert_text) applying to every other Gtk.Entry in your application.
  If you do not inherit,
  you are overriding the base implementation provided by Gtk.Editable(which is called by all other Gtk.Entry widgets in your application).
  By inheriting from Gtk.Editable, you override only the 'local' copy of the base implementation which only applies to your custom class.
  3. https://stackoverflow.com/questions/40074977/how-to-format-the-entries-in-gtk-entry/40163816
  关于: Warning: g_value_get_int: assertion 'G_VALUE_HOLDS_INT (value)' failed
  '''
  def __init__(self):
    super().__init__()

  def do_insert_text(self, new_text, length, position):
    filtered_text = ''.join([i for i in new_text if i in '0123456789'])

    if filtered_text:
      self.get_buffer().insert_text(position, filtered_text, length)
      return position + length

    return position


def main():
  pass


if __name__ == '__main__':
  main()
