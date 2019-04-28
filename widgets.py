#!/usr/bin/env python3
#
# 2018年 11月 09日 星期五 14:48:40 CST

from os import sep as OS_SEP
# python3.5+
from pathlib import Path

from gtk3_header import g


class FileEntry(g.Entry):
  def __init__(self):
    super().__init__()

    self.completion = g.EntryCompletion()
    # self.completion.set_match_func(self.match_partly, None)

    self.completion.set_model(None)
    # 选择上框, 不行, 会触发changed!
    # self.completion.set_inline_selection(True)
    # 匹配成功的条目上框
    self.completion.set_inline_completion(True)

    self.completion.set_minimum_key_length(1)
    self.completion.set_text_column(0)

    self.set_completion(self.completion)
    self.connect('changed', self.on_changed)

  def on_changed(self, *args):
    _file_store = g.ListStore(str)

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

      self.completion.set_model(_file_store)

  def match_partly(self, completion, entrystr, iter, data):
    '''
    set_inline_completion不生效呢?
    '''
    modelstr = completion.get_model()[iter][0]
    _entrystr_name = Path(entrystr).name
    return modelstr.startswith(_entrystr_name)


class NumberEntry(g.Entry):
  '''
  https://stackoverflow.com/questions/2726839/creating-a-pygtk-text-field-that-only-accepts-number
  '''
  def __init__(self):
    super().__init__()
    self.connect('changed', self.on_changed)

  def on_changed(self, *args):
    # print(args)
    text = self.get_text().strip()
    self.set_text(''.join([i for i in text if i in '0123456789']))


def main():
  pass


if __name__ == '__main__':
  main()
