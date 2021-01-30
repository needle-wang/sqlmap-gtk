## sqlmap-gtk
sqlmap GUI, using PyGObject(gtk+3)

supports linux, test on Mint 20, kali 2020.4  
[sqlmap-wx](https://github.com/needle-wang/sqlmap-wx) on win, which needs to improve.  
sqlmap has port to python3.  
don't use python2 any more please.

#### SCREENSHOT
![screenshot](https://github.com/needle-wang/sqlmap-gtk/blob/master/screenshots/sqlmap-ui1.png)

#### HOW-TO
1. **Prerequisites**
  - *python3.6+, GTK+3.20 above*(linux has contained)
  - [sqlmap](https://github.com/sqlmapproject/sqlmap): (choose one)
    - `pip3 install sqlmap`(suggestion)
    - `git clone https://github.com/sqlmapproject/sqlmap.git`
  - pygobject: (choose one)
    - `apt-get install python3-gi`(suggestion)
    - `pip3 install PyGObject`
  - requests: `pip3 install requests`
2. **Download**
  - `git clone https://github.com/needle-wang/sqlmap-gtk.git`
3. **Run**
  - `./sqlmap_gtk.py`

#### FUNCTION
- all sqlmap(1.4.12.45#dev) options(except --all)
- built-in terminal
- sqlmapapi client
- built-in mini wiki(tooltip and placeholder)
- session: autosave current options before quit, autoload last used options
- language switch(see `ABOUT` page): English, Chinese  
  *if you don't need zh lang at all:*  
    `rm -r static/{zh_CN.po,locale}`  
    it works fine.

#### ABOUT
- v0.3.5.2  
  2021-01-29 04:04:35
- use PyGObject(python3-gi + Gtk+3) to recode sqm.py
- thanks to the idea from sqm <https://github.com/kxcode/gui-for-sqlmap>  
  author: [KINGX](https://github.com/kxcode)(sqm UI using python2 + tkinter)  

#### REFERENCE
- Python GTK+3 Tutorial: <https://python-gtk-3-tutorial.readthedocs.io/en/latest/>
- PyGObject-GTK 3.0 API: <https://lazka.github.io/pgi-docs/Gtk-3.0/>
