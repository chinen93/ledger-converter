import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter


from config.settings import get_settings
from src.reports.data import ManipulateData
import matplotlib.pyplot as plt


class Report:

    def __init__(self, data: np.ndarray):
        self.initial_data = data
        self.settings = get_settings()

    def report_overview(self):
        reportData = ManipulateData.forOverviewReport(self.initial_data)

        assert reportData.shape[1] == 3
        reportData.columns = ["date", "amount", "account"]
        reportData["date"] = pd.to_datetime(reportData["date"], format="%Y/%m/%d")

        filteredReportData = reportData.loc[~reportData["account"].isin(["Expenses", "Liability"])]
        pivot = filteredReportData.pivot_table(
            index="date",
            columns="account",
            values="amount",
            aggfunc="sum",
            fill_value=0,
        )
        running = pivot.cumsum()

        fig, (ax1, ax2) = plt.subplots(
            2, 1, sharex=True, figsize=(12, 8), gridspec_kw={"height_ratios": [1, 1]}
        )

        # Savings
        running["Bank:Saving"].plot(ax=ax1)

        # Checking and Credit Card
        running[["Bank:Checking", "Bank:CreditCard"]].plot(ax=ax2)

        def thousands(x, pos):
            if abs(x) >= 1_000_000:
                return f"{x / 1_000_000:.2f}M"
            elif abs(x) >= 1_000:
                return f"{x / 1_000:.2f}k"
            return f"{x:.2f}"

        ax1.set_ylabel("Balance")
        ax1.grid(True)
        ax1.yaxis.set_major_formatter(FuncFormatter(thousands))
        ax1.legend(title="Account")

        ax2.set_ylabel("Balance")
        ax2.grid(True)
        ax2.yaxis.set_major_formatter(FuncFormatter(thousands))
        ax2.legend(title="Account")
        ax2.set_xlabel("Date")
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

        fig.suptitle("Running Balance by Account")

        # fig.savefig("running_balance.png", dpi=300, bbox_inches="tight")
        plt.show()
