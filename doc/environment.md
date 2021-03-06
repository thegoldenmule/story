## Setting up a development environment
---

### Windows
* Remove any existing Python installations.
* Download and install PyCharm community edition [here](http://www.jetbrains.com/pycharm/download/).
* Download portable Kivy distribution [here](http://kivy.org/docs/installation/installation-windows.html).
* Follow instructions [here](https://groups.google.com/d/msg/kivy-users/xTpib2C8r_A/n6kPu-gAfD8J) to set environmental variables and symlinks for PyCharm.
* Download and run register-python.py script [here](https://code.google.com/p/maphew/source/browse/register-python/register-python.py) to register Kivy Python with Windows registry.
* Download and install SciPy binary [here](http://sourceforge.net/projects/scipy/files/scipy/).
* Install pip by downloading `get-pip.py` [here](https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py). Install with `python get-pip.py`.
* Download NumPy whl file [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy). Install with `pip install numpy.whl`.
* Install the Natural Language Toolkit [here](https://pypi.python.org/pypi/nltk).
* Open a terminal and type:
    * python
    * import nltk
    * nltk.download()
    * When prompted, download 'all'
* You're done!