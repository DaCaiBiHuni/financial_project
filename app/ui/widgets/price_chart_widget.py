from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PriceChartWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(5, 3))
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        self.axes.set_title('Price Trend')
        self.axes.set_xlabel('Point')
        self.axes.set_ylabel('Price')

    def plot_prices(self, history):
        self.axes.clear()
        self.axes.set_title('Price Trend')
        self.axes.set_xlabel('Point')
        self.axes.set_ylabel('Price')
        if not history:
            self.axes.text(0.5, 0.5, 'No price history', ha='center', va='center', transform=self.axes.transAxes)
        else:
            prices = [price for price, _ts in history]
            x = list(range(1, len(prices) + 1))
            self.axes.plot(x, prices, marker='o')
        self.figure.tight_layout()
        self.draw()
