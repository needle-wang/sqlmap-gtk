## sqlmap-gtk-zh
sqlmap GUI, using PyGObject(gtk+3)  

此GUI只能在linux下运行, 已在Mint 20, kali 2020.4 中通过测试.  
win下可以使用[sqlmap-wx](https://github.com/needle-wang/sqlmap-wx)(维护慢, 还有很大的改善空间).  
sqlmap已经移植到了python3.  
请不要再使用python2.

#### 截图
![screenshot](https://github.com/needle-wang/sqlmap-gtk/blob/master/screenshots/sqlmap-ui1.png)

#### 为什么需要GUI?
    选项太多, 容易忘记选项, 含义及使用.
    需要经常: sqlmap -hh, sqlmap wiki和google.
    视觉上的位置记忆: 滚动+链接跳转的文献, 缺少纸张的阅读痕迹, 也就是位置记忆.

    光会选项也没用, wiki上的介绍过于零碎, 选项背后的技术细节很多,
    工具描述不够详细, 很多选项有前提要求, 只在特定场景才有效.

    这里, 我将选项进行了分类, wiki集成进了GUI, 增加了使用前提, 使用时会有提示,
    也许会方便些. 熟练后可以自行注释掉tooltip.

#### 安装与使用
1. **要求**  
  - python3.6+, GTK+3.20以上(linux已自带)  
  - pygobject: (二选一)
    - `apt-get install python3-gi`(推荐)  
    - `pip3 install PyGObject`
  - requests: `pip3 install requests`  
  - 最新的[sqlmap](https://github.com/sqlmapproject/sqlmap): `git clone` it.  
2. **下载本GUI**  
  - `git clone https://github.com/needle-wang/sqlmap-gtk.git`  
  或 从这下载: [releases](https://github.com/needle-wang/sqlmap-gtk/releases)(不一定最新)  
3. **运行**  
  - `./sqlmap_gtk.py`

#### 功能
- 包含sqlmap(1.3.12.1#dev)所有选项(除了-d, 不定时更新sqlmap选项)  
- 支持sqlmapapi客户端(API区)  
- 内置终端  
- 会话功能, 自动保存和载入上一次的选项  

#### 关于
- V0.3.4.3  
   2021年01月01日 02:18:45
- 使用PyGObject(python3-gi + Gtk+3)重写sqm.py  
- 感谢[sqm]<https://github.com/kxcode/gui-for-sqlmap>带来的灵感,  
  其作者: [KINGX](https://github.com/kxcode)(sqm UI 使用的是python2 + tkinter)  

#### 参考文献
- Python GTK+3教程: <https://python-gtk-3-tutorial.readthedocs.io/en/latest/>
- PyGObject-GTK 3.0 API: <https://lazka.github.io/pgi-docs/Gtk-3.0/>
