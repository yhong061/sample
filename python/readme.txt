
=============================
=============================
whttps://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
tar -xvf Python-3.7.0.tar.xz
./configure && make && sudo make altinstall

python3.7 -V

如果报这个错误：
ModuleNotFoundError: No module named '_ctypes'
可通过安装libffi(-dev[el])
https://bugs.python.org/issue31652
来解决（安装完重新运行sudo make altinstall），
Ubuntu用这个命令：
sudo apt install libffi-dev

=============================
=============================
=============================
=============================
=============================
=============================
=============================
