import random
import numpy as np

class PlotLive:
    
    def __init__(self, canvas, interval, nSubplots):
        self._canvas = canvas
        self._interval = interval
        self._nSubplots = nSubplots
        self._yData = [random.random() for _ in range(int(interval[1]-interval[0]))]
        
        self.__colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
        self.buidPlot()

    def buidPlot(self):
        self._canvas.figure.clear()
        self._axes = []
        self._lines = []
        nColor = len(self.__colors)
        for i in range(self._nSubplots):
            color = self.__colors[i%nColor]

            self._axes.append(self._canvas.figure.add_subplot(self._nSubplots, 1, i+1))
            self._lines.append(self._axes[i].plot([], [], color=color))
            self._axes[i].set_xlim(self._interval[0], self._interval[1])
        
        self._canvas.figure.tight_layout()
        self._canvas.draw()

    def updateGraph(self, xData, yData):
        for i in range(self._nSubplots):
            l = self._lines[i][0]
            l.set_xdata(xData[str(i)])
            l.set_ydata(yData[str(i)])

        self._canvas.draw()
        self._canvas.flush_events()


class AnalysisPreprocessingPlot:

    def __init__(self, canvas, interval):

        self.__canvas = canvas
        self.__interval = interval
        self.__canvas.figure.clear()
        self.__axes = self.__canvas.figure.add_subplot(111)
        self.__preprocessingFunctionLine = self.__axes.plot([], [])
        self.__targetLine = self.__axes.plot([], [])
        self.__axes.set_xlim(self.__interval[0], self.__interval[1])

        self.__canvas.figure.tight_layout()
        self.__canvas.draw()
    
    def updatePlot(self, y):
        self.__axes.set_ylim(0.9*np.min(y), np.max(y)*1.1)
        x = np.arange(0, np.shape(y)[0], 1)
        
        self.__preprocessingFunctionLine[0].set_xdata(x)
        self.__preprocessingFunctionLine[0].set_ydata(y)

        #self.__targetLine[0].set_xdata(x)
        #self.__targetLine[0].set_ydata(y_target)

        self.__canvas.draw()
        self.__canvas.flush_events()
    
    def updateBiasPlot(self, y_target):
        x = np.arange(0, np.shape(y_target)[0], 1)
        self.__targetLine[0].set_xdata(x)
        self.__targetLine[0].set_ydata(y_target)

        self.__canvas.draw()
        self.__canvas.flush_events()
