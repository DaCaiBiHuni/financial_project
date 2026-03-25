from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PriceChartWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(5, 3))
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        self.axes.set_title('Last 12 Months Trend')
        self.axes.set_xlabel('Month')
        self.axes.set_ylabel('Price')

    def plot_prices(self, history):
        self.axes.clear()
        self.axes.set_title('Last 12 Months Trend')
        self.axes.set_xlabel('Month')
        self.axes.set_ylabel('Price')
        if not history:
            self.axes.text(0.5, 0.5, 'No price history', ha='center', va='center', transform=self.axes.transAxes)
        else:
            prices = [price for price, _ts in history]
            labels = [ts[:7] for _price, ts in history]
            x = list(range(len(prices)))
            self.axes.plot(x, prices, marker='o')
            self.axes.set_xticks(x)
            self.axes.set_xticklabels(labels, rotation=45, ha='right')
        self.figure.tight_layout()
        self.draw()
