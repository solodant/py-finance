import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class VisualizationService:
    """Service for data visualization."""

    @staticmethod
    def show(prices: pd.Series, analysis: dict, title: str):
        """Display financial charts."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        prices.plot(ax=ax1, title=f"{title} - Price", grid=True)

        analysis["returns"].plot(ax=ax2, color="green", label="Returns")
        ax2_vol = ax2.twinx()
        analysis["volatility"].plot(ax=ax2_vol, color="red", label="Volatility")

        lines = ax2.get_legend_handles_labels()[0]
        lines += ax2_vol.get_legend_handles_labels()[0]
        ax2.legend(lines, ["Returns", "Volatility"], loc="upper left")

        plt.tight_layout()
        plt.show()


class CurrencyVisualizationService:
    """Service to visualize currency price dynamics and correlation."""

    @staticmethod
    def show(currency_data: dict[str, pd.Series], title: str):
        """Display price charts and correlation matrix for currencies in one window."""
        df = pd.DataFrame(currency_data)

        corr = df.pct_change(fill_method=None).corr()

        fig, axes = plt.subplots(2, 1, figsize=(12, 10))

        for col in df.columns:
            df[col].plot(ax=axes[0], label=col)

        axes[0].set_title(f"{title} - Currency Prices")
        axes[0].set_xlabel("Date")
        axes[0].set_ylabel("Price")
        axes[0].legend()
        axes[0].grid(True)

        sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=axes[1])
        axes[1].set_title(f"{title} - Correlation Matrix of Returns")

        plt.tight_layout()
        plt.show()
