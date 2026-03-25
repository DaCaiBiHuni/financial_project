from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PriceChartWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(6, 3.6), facecolor='white')
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        self._apply_style()

    def _apply_style(self):
        self.axes.set_title('1Y Monthly Trend', fontsize=11)
        self.axes.set_xlabel('Month', fontsize=9)
        self.axes.set_ylabel('Price', fontsize=9)
        self.axes.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)
        for spine in ['top', 'right']:
            self.axes.spines[spine].set_visible(False)

    def plot_prices(self, history):
        self.axes.clear()
        self._apply_style()
        if not history:
            self.axes.text(0.5, 0.5, 'No price history', ha='center', va='center', transform=self.axes.transAxes, fontsize=10)
        else:
            prices = [price for price, _ts in history]
            labels = [ts[:7] for _price, ts in history]
            x = list(range(len(prices)))
            self.axes.plot(x, prices, color='#2563eb', linewidth=2.0, marker='o', markersize=4)
            self.axes.fill_between(x, prices, min(prices), color='#93c5fd', alpha=0.2)
            self.axes.set_xticks(x)
            self.axes.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
            self.axes.tick_params(axis='y', labelsize=8)
        self.figure.tight_layout()
        self.draw()
