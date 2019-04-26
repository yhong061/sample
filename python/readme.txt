
=============================
=============================
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
tar -xvf Python-3.7.0.tar.xz
#./configure --with-ssl
./configure
&& make && sudo make install

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
module help:
>>> import ConfigParser
>>> help(ConfigParser)



=============================
=============================
CURDIR = dirname(abspath(__file__))
sys.path.append(join(CURDIR, '..'))

print("++++call : ", sys._getframe().f_code.co_name)  //print function name

sys.stdout.flush()

rc = atests(*sys.argv[1:])
def atests(interpreter, *arguments):

=============================
=============================
=============================
