# first problem
报错：AttributeError: module 'pkgutil' has no attribute 'ImpImporter'，因为pip的版本与Python版本不匹配，解决方法是升级pip。
solutions:
1. python -m ensurepip --upgrade
2. C:\Program Files\Python312\python.exe -m pip install --upgrade pip
 在 C:\Program Files\Python312文件的路径下执行python.exe -m pip install --upgrade pip

# second problem
报错：ModuleNotFoundError: No module named 'distutils',Python环境缺少distutils模块，这是Python标准库的一部分，但某些情况下可能没有被正确安装。
solution: 
首先尝试安装distutils
python -m ensurepip --upgrade
python -m pip install --upgrade setuptools
升级pip版本
python.exe -m pip install --upgrade pip