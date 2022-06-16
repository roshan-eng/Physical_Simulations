from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys


class Planet:
    def __init__(self, mass, position, *args):
        self.mass = mass
        self.acc = 0
        self.vel = 0
        self.position = np.array(position)
        self.others = args

    def force(self, other):
        G = 10 ** -3
        r = other.position - self.position
        f = G * self.mass * other.mass * r / np.linalg.norm(r) ** 2
        return f

    def move(self, dt=0.1):
        f = np.zeros(3)
        for other in self.others:
            f += self.force(other)

        self.acc = f / self.mass
        self.vel += self.acc * dt
        self.position += self.vel * dt


class Visualizer(object):
    def __init__(self):
        self.traces = dict()
        self.points = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 40
        self.w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
        self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()

        # create the background grids
        # gx = gl.GLGridItem()
        # gx.rotate(90, 0, 1, 0)
        # gx.translate(-10, 0, 0)
        # self.w.addItem(gx)
        # gy = gl.GLGridItem()
        # gy.rotate(90, 1, 0, 0)
        # gy.translate(0, -10, 0)
        # self.w.addItem(gy)
        # gz = gl.GLGridItem()
        # gz.translate(0, 0, -10)
        # self.w.addItem(gz)

        self.n = 17
        self.planets = []
        for i in range(self.n):
            self.planets.append(Planet(np.random.randint(500, 1000), np.random.uniform(-30, 30, 3)))

        for obj in self.planets:
            obj.others = [x for x in self.planets if x != obj]

        self.pts = dict()
        for i in range(self.n):
            self.pts[i] = np.array([self.planets[i].position])
            self.traces[i] = gl.GLLinePlotItem(pos=self.pts[i], color=pg.glColor(
                (i, self.n * 1.3)), width=(i + 1) / 10, antialias=True)
            self.points[i] = gl.GLScatterPlotItem(pos=self.pts[i][-1], color=pg.glColor(
                (i, self.n * 1.3)), size=30)
            self.w.addItem(self.traces[i])
            self.w.addItem(self.points[i])

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec()

    def set_plot_data(self, name, points, color, width):
        self.traces[name].setData(pos=points, color=color, width=width)
        self.points[name].setData(pos=points[-1], color=color, size=30)

    def update(self):
        for i in range(self.n):
            self.planets[i].move()
            self.pts[i] = np.vstack([self.pts[i], [self.planets[i].position]])

            if len(self.pts[i]) > 800:
                self.pts[i] = self.pts[i][1:]

            self.set_plot_data(
                name=i, points=self.pts[i],
                color=pg.glColor((i, self.n * 1.3)),
                width=(i + 1) / 10
            )

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()


# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    v = Visualizer()
    v.animation()
