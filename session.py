#!/usr/bin/env python3
#
# 2018年 11月 09日 星期五 15:06:50 CST

from configparser import ConfigParser
from widgets import (g, et)


LAST_TMP = 'last.tmp'


class Session(object):
  def __init__(self, m):
    '''
    m: model.Model
    '''
    self.m = m

    self._cfg = ConfigParser()
    # https://stackoverflow.com/questions/19359556/configparser-reads-capital-keys-and-make-them-lower-case
    # 所有选项的key, 都会传给optionxform(), 该方法会将key转成小写!
    # 将optionxform替换成str, 表示不做转换
    self._cfg.optionxform = str

  def save_to_tmp(self):
    self._save_to_tmp_target()
    self._save_to_tmp_ckbtn()
    self._save_to_tmp_entry()

    with open(LAST_TMP, 'w') as f:
      self._cfg.write(f)

  def load_from_tmp(self):
    self._cfg.read(LAST_TMP, 'utf8')

    self._load_from_tmp_target()
    self._load_from_tmp_ckbtn()
    self._load_from_tmp_entry()

  def _save_to_tmp_target(self):
    if self._cfg.has_section('Target'):
      self._cfg.remove_section('Target')

    self._cfg.add_section('Target')

    _tmp_url = self.m._url_combobox.get_child().get_text().strip()

    if _tmp_url:
      self._cfg['Target']['_url_combobox'] = _tmp_url

  def _save_to_tmp_entry(self):
    if self._cfg.has_section('Entry'):
      self._cfg.remove_section('Entry')

    self._cfg.add_section('Entry')

    for _i in dir(self.m):
      if _i.endswith('entry'):
        _tmp_entry = getattr(self.m, _i)

        if isinstance(_tmp_entry, et) and _tmp_entry.get_text().strip():
          self._cfg['Entry'][_i] = _tmp_entry.get_text()

  def _save_to_tmp_ckbtn(self):
    if self._cfg.has_section('CheckButton'):
      self._cfg.remove_section('CheckButton')

    self._cfg.add_section('CheckButton')

    _checked = []
    for _i in dir(self.m):
      if _i.endswith('ckbtn'):
        _tmp_ckbtn = getattr(self.m, _i)

        if isinstance(_tmp_ckbtn, g.CheckButton) and _tmp_ckbtn.get_active():
          _checked.append(_i)

    self._cfg['CheckButton']['checked'] = ','.join(_checked)

  def _load_from_tmp_target(self):
    if not self._cfg.has_section('Target'):
      self._cfg.add_section('Target')

    for _i in self._cfg.options('Target'):
      if _i == '_url_combobox':
        # 不去手动改LAST_TMP, self.m就肯定有_i属性了
        _tmp_url = self.m._url_combobox.get_child()

        if self._cfg['Target'][_i]:
          _tmp_url.set_text(self._cfg['Target'][_i])

      break

  def _load_from_tmp_entry(self):
    if not self._cfg.has_section('Entry'):
      self._cfg.add_section('Entry')

    for _i in self._cfg.options('Entry'):
      # 不去手动改LAST_TMP, self.m就肯定有_i属性了
      _tmp_entry = getattr(self.m, _i)

      if isinstance(_tmp_entry, et) and self._cfg['Entry'][_i]:
        # print(type(self._cfg['Entry'][_i]))
        _tmp_entry.set_text(self._cfg['Entry'][_i])

  def _load_from_tmp_ckbtn(self):
    if not self._cfg.has_section('CheckButton'):
      self._cfg.add_section('CheckButton')

    try:
      _checked = self._cfg['CheckButton']['checked'].split(',')
      for _i in _checked:
        if _i:  # _i可能为''
          # 不去手动改LAST_TMP, self.m就肯定有_i属性了
          _tmp_ckbtn = getattr(self.m, _i)
          _tmp_ckbtn.set_active(True)
        else:  # _checked = [''], 则使用默认值
          pass
    except KeyError as e:
      # if no checked button, then pass
      pass


def main():
  pass


if __name__ == '__main__':
  main()
