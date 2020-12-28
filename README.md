## sqlmap-gtk
sqlmap GUI, using PyGObject(gtk+3)  

此GUI只能在linux下运行, 已在kali, debian系中测试通过.  
如果想在win下使用, 可以使用[sqlmap-wx](https://github.com/needle-wang/sqlmap-wx)(维护慢, 还有很大的改善空间).  
欢迎使用, 反馈!  

sqlmap已经移植到了python3!  
来自sqlmap's FAQ:  
"Both Python 2 and 3 are supported from May of 2019"  

#### 截图
![screenshot](https://github.com/needle-wang/sqlmap-gtk/blob/master/screenshots/sqlmap-ui1.png)

#### 为什么需要GUI?
    选项太多了, 没有GUI, 总会忘了选项, 含义及使用.
    于是不时地: sqlmap -hh和sqlmap wiki和google. 翻找半天, 阅读又要琢磨半天. 
    我学使用sqlmap断续好些年了, 存了看了好些资料, 等过段时间, 又模糊了, 没用.
    光一个中文手册就看了好多遍, 总感觉缺点什么, 后来想明白了, 缺少视觉上的位置记忆.
    滚动+链接跳转的文献, 缺少纸张的阅读痕迹, 也就是位置记忆.
    当然, 还有个使用时长的原因.

    另外, 光会选项也没有用, wiki上的介绍过于零碎, 选项背后的技术细节很多,
    工具描述不够详细, 很多选项有前提要求, 这就要求使用者要有相应的知识储备了
    可记性就是不好, 怎么办? 边用边学? 过段时间又忘了, 毕竟只在特定场景才有效.
    计算机是个大类, 要记的东西太多了.

    这里, 我将选项进行了分类, wiki集成进了GUI, 增加了使用前提, 使用时会有提示,
    也许会方便些吧. 熟练后可以注释掉tooltip.

#### 安装与使用
1. **要求**  
  - python3.6+, GTK+3.20  
  - pygobject: `pip3 install PyGObject` or `apt-get install python3-gi`  
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
- V0.3.4.2  
   2019年10月10日 08:06:05  
   作者: needle wang
- 使用PyGObject(Gtk+3 + python3-gi)重写sqm.py  
- 感谢[sqm](https://github.com/kxcode/gui-for-sqlmap)带来的灵感, 其作者: [KINGX](https://github.com/kxcode) (sqm UI 使用的是python2 + tkinter)  

#### 参考文献
- Python GTK+3教程: https://python-gtk-3-tutorial.readthedocs.io/en/latest/  
- PyGObject API: https://lazka.github.io/pgi-docs/Gtk-3.0/  
