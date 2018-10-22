## SQLMAP-UI
sqlmap ui, using PyGObject(gtk+3) 


#### SCREENSHORT
![screenshot](https://github.com/needle-wang/sqlmap-ui/blob/master/screenshots/sqlmap-ui1.png)

#### INSTALLATION

1. **REQUIRED**  
  - python3.5+  
  - pygobject: `pip3 install PyGObject` or `apt-get install python3-gi`  
  - [sqlmap](https://github.com/sqlmapproject/sqlmap): `pip2 install sqlmap`
2. **GET**
  - `git clone https://github.com/needle-wang/sqlmap-ui.git`
3. **RUN**  
  - `./sqlmap_ui.py`

#### TODO
1. UI重新排版(ok)
2. 完善tooltip, 将tooltip与条目合并成一个字典!
3. 细节优化(margin, padding啥的)
4. 代码重构, 划分为多模块形式?
5. 将管道流集成到UI里?

#### ABOUT
1. VERSION: 0.2  
   2018年 10月 22日 星期一 16:24:05 CST  
   VERSION: 0.1  
   2018年 09月 03日 星期一 03:34:31 CST  
   作者: needle wang ( needlewang2011@gmail.com )
2. 使用PyGObject(Gtk+3: python3-gi)重写sqm.py
3. 感谢[sqm](https://github.com/kxcode/gui-for-sqlmap)的作者: [KINGX](https://github.com/kxcode) (sqm UI 使用的是python2 + tkinter)

#### REFERENCE
1. Gtk+3教程: https://python-gtk-3-tutorial.readthedocs.io/en/latest/
2. Gtk+3 API: https://lazka.github.io/pgi-docs/Gtk-3.0/
