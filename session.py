#!/usr/bin/env python3
#
# 2018-11-09 15:06:50

from configparser import ConfigParser
from widgets import (g, et)


LAST_TMP = 'static/last.tmp'


def load_settings():
  _cfg = ConfigParser()
  _cfg.optionxform = str
  _cfg.read(LAST_TMP, 'utf8')

  if not _cfg.has_section('Setting'):
    _cfg.add_section('Setting')

  _ = ['en', 'en']
  try:
    if _cfg['Setting']['language'] == 'zh':
      _[0] = 'zh'
  except KeyError:
    pass
  try:
    if _cfg['Setting']['tooltips'] == 'zh':
      _[1] = 'zh'
  except KeyError:
    pass

  return _


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
    self._save_to_tmp_radio()

    with open(LAST_TMP, 'w') as f:
      self._cfg.write(f)

  def load_from_tmp(self):
    self._cfg.read(LAST_TMP, 'utf8')

    self._load_from_tmp_target()
    self._load_from_tmp_ckbtn()
    self._load_from_tmp_entry()
    self._load_from_tmp_radio()

  def _save_to_tmp_target(self):
    if self._cfg.has_section('Target'):
      self._cfg.remove_section('Target')

    self._cfg.add_section('Target')

    _tmp_url = self.m._url_combobox.get_child().get_text().strip()

    if _tmp_url:
      self._cfg['Target']['_url_combobox'] = _tmp_url

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

      if _i == 'tampers':
        tampers = getattr(self.m, _i)

        for _tamper, index in zip(tampers, range(len(tampers))):
          if _tamper.get_active():
            _checked.append('tamper_{}'.format(index))

    # print(_checked)
    self._cfg['CheckButton']['checked'] = ','.join(_checked)

  def _save_to_tmp_entry(self):
    if self._cfg.has_section('Entry'):
      self._cfg.remove_section('Entry')

    self._cfg.add_section('Entry')

    for _i in dir(self.m):
      if _i.endswith('entry'):
        _tmp_entry = getattr(self.m, _i)

        if isinstance(_tmp_entry, et) and _tmp_entry.get_text().strip():
          self._cfg['Entry'][_i] = _tmp_entry.get_text()

  def _save_to_tmp_radio(self):
    if self._cfg.has_section('Setting'):
      self._cfg.remove_section('Setting')

    self._cfg.add_section('Setting')

    self._cfg['Setting']['language'] = 'en'
    self._cfg['Setting']['tooltips'] = 'en'
    if self.m._page6_lang_zh_radio.get_active():
      self._cfg['Setting']['language'] = 'zh'
    if self.m._page6_tooltips_zh_radio.get_active():
      self._cfg['Setting']['tooltips'] = 'zh'

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

  def _load_from_tmp_ckbtn(self):
    if not self._cfg.has_section('CheckButton'):
      self._cfg.add_section('CheckButton')

    try:
      _checked = self._cfg['CheckButton']['checked'].split(',')
      _tampers = list(self.m.tampers.keys())
      for _i in _checked:
        if _i:  # _i could be ''
          if _i.endswith('_ckbtn'):
            _tmp_ckbtn = getattr(self.m, _i)
            _tmp_ckbtn.set_active(True)
          if _i.startswith('tamper_'):
            _tampers[int(_i[len('tamper_'):])].set_active(True)
        else:  # if _checked = [''], then use default
          pass
    except KeyError as e:
      # if no checked button, then pass
      pass

  def _load_from_tmp_entry(self):
    if not self._cfg.has_section('Entry'):
      self._cfg.add_section('Entry')

    for _i in self._cfg.options('Entry'):
      try:
        _tmp_entry = getattr(self.m, _i)
        if isinstance(_tmp_entry, et) and self._cfg['Entry'][_i]:
          # print(type(self._cfg['Entry'][_i]))
          _tmp_entry.set_text(self._cfg['Entry'][_i])
      except AttributeError as e:
        pass

  def _load_from_tmp_radio(self):
    if not self._cfg.has_section('Setting'):
      self._cfg.add_section('Setting')

    try:
      if self._cfg['Setting']['language'] == 'zh':
        self.m._page6_lang_zh_radio.set_active(True)
    except KeyError:
      pass
    try:
      if self._cfg['Setting']['tooltips'] == 'zh':
        self.m._page6_tooltips_zh_radio.set_active(True)
    except KeyError:
      pass


def main():
  pass


if __name__ == '__main__':
  main()
