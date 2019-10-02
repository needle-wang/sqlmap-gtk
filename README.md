## sqlmap-gtk
sqlmap GUI, using PyGObject(gtk+3)  

包含sqlmap所有选项(除了-d, 不定时更新sqlmap选项)  
支持sqlmapapi客户端(API区)  
内置终端  
会话功能, 自动保存和载入上一次的选项  

此GUI只能在linux下运行, 已在kali, debian系中测试通过.  
如果想在win下使用, 建议使用[sqlmap-wx](https://github.com/needle-wang/sqlmap-wx/).  
欢迎使用, 反馈!!  

sqlmap已经移植到了python3!  
来自sqlmap's FAQ:  
"Both Python 2 and 3 are supported from May of 2019"  

#### 截图
![screenshot](https://github.com/needle-wang/sqlmap-gtk/blob/master/screenshots/sqlmap-ui1.png)

#### 安装
1. **要求**  
  - python3.5+, GTK+3.20  
  - pygobject: `pip3 install PyGObject` or `apt-get install python3-gi`  
  - requests: `pip3 install requests`  
  - 最新的[sqlmap](https://github.com/sqlmapproject/sqlmap): `git clone` it.  
2. **获取本GUI**  
  - `git clone https://github.com/needle-wang/sqlmap-gtk.git`  
  或 从这下载: [releases](https://github.com/needle-wang/sqlmap-gtk/releases/)(不一定最新)  
3. **运行**  
  - `./sqlmap_gtk.py`

#### TODO
- ~~UI重新排版~~
- ~~分离并完善tooltip等提示信息~~
- ~~细节优化(margin, padding啥的)~~
- ~~打从加了filechooserbutton起, 启动就慢了一倍:  
   根据line_profiler输出: gtk.FileChooserButton()有性能问题!~~
- ~~重构~~
- ~~添加session功能(v0.2.2)~~
- ~~重构成MVC模式(结构重构改动很大, v0.3)~~
- ~~将管道流集成到UI里(无法实现, 改用pty实现成功)~~
- ~~添加API区(实现sqlmapapi client)~~
- ~~修复: 修改filechooserbutton(常有什么network path超时警告, 启动加快),  
  输出滚动不准确, file entry补全, G_VALUE_HOLDS_INT警告~~
- ~~更新选项, 添加隐藏选项~~
- 继续重构, 优化

#### 关于
1. V0.3.4.1  
   2019年10月02日 23:39:57  
   作者: needle wang ( needlewang2011@gmail.com )  
2. 使用PyGObject(Gtk+3: python3-gi)重写sqm.py  
3. 感谢[sqm](https://github.com/kxcode/gui-for-sqlmap)带来的灵感, 其作者: [KINGX](https://github.com/kxcode) (sqm UI 使用的是python2 + tkinter)  

#### 参考文献
1. Gtk+3教程: https://python-gtk-3-tutorial.readthedocs.io/en/latest/  
2. Gtk+3 API: https://lazka.github.io/pgi-docs/Gtk-3.0/  
