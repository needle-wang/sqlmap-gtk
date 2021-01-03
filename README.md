## sqlmap-gtk
sqlmap GUI, using PyGObject(gtk+3)  

support linux, test on Mint 20, kali 2020.4  
[sqlmap-wx](https://github.com/needle-wang/sqlmap-wx) on win, which needs to improve.  
sqlmap has port to python3.  
don't use python2 any more please.  

#### SCREENSHOT
![screenshot](https://github.com/needle-wang/sqlmap-gtk/blob/master/screenshots/sqlmap-ui1.png)

#### HOW-TO
1. **pre-request**  
  - *python3.6+, GTK+3.20 above*(linux has contained)  
  - pygobject: (choose one)
    - `apt-get install python3-gi`(suggestion)  
    - `pip3 install PyGObject`
  - requests: `pip3 install requests`  
  - lastest [sqlmap](https://github.com/sqlmapproject/sqlmap): `git clone` it.  
2. **download**  
  - `git clone https://github.com/needle-wang/sqlmap-gtk.git`  
3. **run**  
  - `./sqlmap_gtk.py`

#### FUNCTION
- sqlmap(1.3.12.1#dev) all options(except -d)
- sqlmapapi client
- built-in terminal
- session: autosave current options before quit, autoload last used options
- language switch: english, chinese

#### ABOUT
- v0.3.5  
  2021-01-03 16:56:23
- use PyGObject(python3-gi + Gtk+3) to recode sqm.py
- thanks to the idea from sqm <https://github.com/kxcode/gui-for-sqlmap>  
  author: [KINGX](https://github.com/kxcode)(sqm UI using python2 + tkinter)  

#### REFERENCE
- Python GTK+3 Tutorial: <https://python-gtk-3-tutorial.readthedocs.io/en/latest/>
- PyGObject-GTK 3.0 API: <https://lazka.github.io/pgi-docs/Gtk-3.0/>
