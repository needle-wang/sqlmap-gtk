# sqlmap-ui
sqlmap 简易 ui, using PyGObject(gtk+3) 


### screenshort
![screenshot](https://github.com/needle-wang/sqlmap-ui/blob/master/screenshots/sqlmap-ui1.png)
### Installation

#### required:
python3.5+  
pygobject: `pip3 install PyGObject` or `apt-get install python3-gi`  
[sqlmap](https://github.com/sqlmapproject/sqlmap): `pip2 install sqlmap`
#### get:
`git clone https://github.com/needle-wang/sqlmap-ui.git`
#### run:
`./sqlmap_ui.py`

#### about
1. VERSION: 0.1  
   2018年 09月 03日 星期一 03:34:31 CST  
   作者: needle wang ( needlewang2011@gmail.com )
2. 使用PyGObject(Gtk+3: python3-gi)重写sqm.py
3. 感谢sqm( https://github.com/kxcode/gui-for-sqlmap )的作者: [KINGX](https://github.com/kxcode)  
   (sqm UI 使用的是python2 + tkinter)

#### Reference:
1. Gtk+3教程: https://python-gtk-3-tutorial.readthedocs.io/en/latest/
2. Gtk+3 API: https://lazka.github.io/pgi-docs/Gtk-3.0/
