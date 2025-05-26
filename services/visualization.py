import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sns.set(style="darkgrid")


class VisualizationService:
    """Service for single asset data visualization (e.g., one stock)."""

    @staticmethod
    def show(prices: pd.Series, analysis: dict, title: str):
        """Display price, returns and volatility for one asset."""

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        fig.suptitle(f"{title}", fontsize=16)

        ax1.plot(prices.index, prices.values, label="Price", color="blue")
        ax1.set_ylabel("Price")
        ax1.legend()
        ax1.grid(True)

        ax2.plot(analysis["returns"].index, analysis["returns"].values, label="Returns", color="green")

        ax2_vol = ax2.twinx()
        ax2_vol.plot(analysis["volatility"].index, analysis["volatility"].values, label="Volatility", color="red")

        ax2.set_ylabel("Returns")
        ax2_vol.set_ylabel("Volatility")

        lines = ax2.get_legend_handles_labels()[0] + ax2_vol.get_legend_handles_labels()[0]
        labels = ["Returns", "Volatility"]
        ax2.legend(lines, labels, loc="upper left")

        ax2.grid(True)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()


class CurrencyVisualizationService:
    """Service to visualize currency price dynamics and correlation."""

    @staticmethod
    def show(currency_data: dict[str, pd.Series], title: str):
        """Display price charts and correlation matrix for currencies."""
        df = pd.DataFrame(currency_data)
        corr = df.pct_change(fill_method=None).corr()

        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle(f"{title}", fontsize=16)

        palette = sns.color_palette("tab10", n_colors=len(df.columns))
        for i, col in enumerate(df.columns):
            axes[0].plot(df.index, df[col], label=col, color=palette[i])

        axes[0].set_title("Currency Prices", fontsize=14)
        axes[0].set_xlabel("Date")
        axes[0].set_ylabel("Price")
        axes[0].legend()
        axes[0].grid(True)

        sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=axes[1])
        axes[1].set_title("Correlation Matrix of Returns", fontsize=14)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()


class StockVisualizationService:
    """Service for visualizing multiple stocks."""

    @staticmethod
    def show(price_data_dict: dict[str, pd.Series], analysis_dict: dict[str, dict[str, pd.Series]]):
        """Display prices, returns, and volatility for multiple stocks."""
        tickers = list(price_data_dict.keys())

        fig, axes = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
        fig.suptitle("Stocks", fontsize=16)

        palette = sns.color_palette("tab10", n_colors=len(tickers))
        color_map = dict(zip(tickers, palette))

        for ticker in tickers:
            axes[0].plot(price_data_dict[ticker].index, price_data_dict[ticker].values,
                         label=ticker, color=color_map[ticker])
        axes[0].set_ylabel("Price")
        axes[0].legend(title="Ticker")
        axes[0].grid(True)

        for ticker in tickers:
            ret_series = analysis_dict[ticker]["returns"]
            axes[1].plot(ret_series.index, ret_series.values,
                         label=ticker, color=color_map[ticker])
        axes[1].set_ylabel("Returns")
        axes[1].legend(title="Ticker")
        axes[1].grid(True)

        for ticker in tickers:
            vol_series = analysis_dict[ticker]["volatility"]
            axes[2].plot(vol_series.index, vol_series.values,
                         label=ticker, color=color_map[ticker])
        axes[2].set_ylabel("Volatility")
        axes[2].legend(title="Ticker")
        axes[2].grid(True)

        axes[2].set_xlabel("Date")
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
