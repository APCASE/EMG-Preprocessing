# Essa classe será utilizada para criar um widget para plotagem dos dados
# utilizando o qt desginer.

from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import style
style.use('fivethirtyeight')
class PlotWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())
        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.canvas)
        self.canvas.figure.clear()
        self.setLayout(verticalLayout)