## SQLMAP-UI
sqlmap ui, using PyGObject(gtk+3) 


#### SCREENSHORT
![screenshot](https://github.com/needle-wang/sqlmap-ui/blob/master/screenshots/sqlmap-ui1.png)

#### INSTALLATION

1. **REQUIRED**  
  - GTK+3.20(which is hard to install at win), python3.5+  
  - pygobject: `pip3 install PyGObject` or `apt-get install python3-gi`  
  - requests: `pip3 install requests`
  - [sqlmap](https://github.com/sqlmapproject/sqlmap): `pip2 install sqlmap` #hope sqlmap ports to python3 in future...
2. **GET**
  - `git clone https://github.com/needle-wang/sqlmap-ui.git`
3. **RUN**  
  - `./sqlmap_ui.py`

#### TODO
- ~~UI重新排版~~
- ~~分离并完善tooltip等提示信息~~
- ~~细节优化(margin, padding啥的)~~
- 打从加了filechooserbutton起, 启动就慢了一倍:  
   根据line_profiler输出: gtk.FileChooserButton()有性能问题!  
- ~~重构~~
- ~~添加session功能(v0.2.2)~~
- ~~重构成MVC模式(结构重构改动很大, v0.3)~~
- ~~将管道流集成到UI里(无法实现, 改用pty实现成功)~~
- ~~添加API区(实现sqlmapapi client)~~  
- 继续重构, 优化

#### ABOUT
1. V0.3.2  
   2019年 04月 29日 星期一 21:20:07 CST
   V0.3.1  
   2019年 04月 25日 星期四 17:36:44 CST  
   作者: needle wang ( needlewang2011@gmail.com )
2. 使用PyGObject(Gtk+3: python3-gi)重写sqm.py
3. 感谢[sqm](https://github.com/kxcode/gui-for-sqlmap)带来的灵感, 其作者: [KINGX](https://github.com/kxcode) (sqm UI 使用的是python2 + tkinter)

#### REFERENCE
1. Gtk+3教程: https://python-gtk-3-tutorial.readthedocs.io/en/latest/
2. Gtk+3 API: https://lazka.github.io/pgi-docs/Gtk-3.0/
