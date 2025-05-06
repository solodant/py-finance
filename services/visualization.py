import pandas as pd
import matplotlib.pyplot as plt

class VisualizationService:
    """Service for data visualization."""
    
    @staticmethod
    def show(prices: pd.Series, analysis: dict, title: str):
        """Display financial charts."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        prices.plot(ax=ax1, title=f"{title} - Price", grid=True)
        
        analysis['returns'].plot(ax=ax2, color='green', label='Returns')
        ax2_vol = ax2.twinx()
        analysis['volatility'].plot(ax=ax2_vol, color='red', label='Volatility')
        
        lines = ax2.get_legend_handles_labels()[0]
        lines += ax2_vol.get_legend_handles_labels()[0]
        ax2.legend(lines, ['Returns', 'Volatility'], loc='upper left')
        
        plt.tight_layout()
        plt.show()