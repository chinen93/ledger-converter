import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, MultipleLocator


from config.logging import get_logger
from config.settings import get_settings
from src.reports.data import (
    ACCOUNT_BANK_CHECKING,
    ACCOUNT_BANK_CREDIT_CARD,
    ACCOUNT_BANK_SAVING,
    ACCOUNT_BANKS,
    ACCOUNT_EXPENSES,
    ACCOUNT_LIABILITY,
    ManipulateData,
)
import matplotlib.pyplot as plt


class Report:

    def __init__(self, data: np.ndarray):
        self.initial_data = data

        self.log = get_logger(__name__)

        self.settings = get_settings()
        assert self.settings.OUTPUT_FOLDER is not None
        self.output_folder = self.settings.OUTPUT_FOLDER

    def report_overview(self):
        reportData = ManipulateData.forOverviewReport(self.initial_data)

        assert reportData.shape[1] == 3
        reportData.columns = ["date", "amount", "account"]
        reportData["date"] = pd.to_datetime(reportData["date"], format="%Y/%m/%d")

        filteredReportData = reportData.loc[
            ~reportData["account"].isin([ACCOUNT_EXPENSES, ACCOUNT_LIABILITY])
        ]
        pivot = filteredReportData.pivot_table(
            index="date",
            columns="account",
            values="amount",
            aggfunc="sum",
            fill_value=0,
        )
        running = pivot.cumsum()

        fig, (ax1, ax2) = plt.subplots(
            2, 1, sharex=True, figsize=(15, 9), gridspec_kw={"height_ratios": [1, 2]}
        )

        # Savings
        running[ACCOUNT_BANK_SAVING].plot(ax=ax1)

        # Checking and Credit Card
        running[[ACCOUNT_BANK_CHECKING, ACCOUNT_BANK_CREDIT_CARD]].plot(ax=ax2)

        def thousands(x, pos):
            if abs(x) >= 1_000_000:
                return f"{x / 1_000_000:.2f}M"
            elif abs(x) >= 1_000:
                return f"{x / 1_000:.2f}k"
            return f"{x:.2f}"

        ax1.set_ylabel("Balance")
        ax1.grid(True)
        ax1.yaxis.set_major_locator(MultipleLocator(10000))
        ax1.yaxis.set_major_formatter(FuncFormatter(thousands))
        ax1.legend(title="Account")

        ax2.set_ylabel("Balance")
        ax2.grid(True)
        ax2.axhline(y=0, color="black", linewidth=1.2, linestyle="-")
        ax2.yaxis.set_major_locator(MultipleLocator(1000))
        ax2.yaxis.set_major_formatter(FuncFormatter(thousands))
        ax2.legend(title="Account")
        ax2.set_xlabel("Date")
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

        fig.suptitle("Running Balance by Account")
        plt.tight_layout()

        filename = self.output_folder + "running_balance.png"
        self.log.info(f"Save Report: '{filename}'")

        fig.savefig(filename, dpi=300, bbox_inches="tight")

        
        # plt.show()

    def report_trend_expenses(self):

        expense_groups = {
            "Housing": ["Apt"],
            "Main": ["Comida", "Compras", "Mercado", "Viagem"],
            "Other": []
        }

        reportData = ManipulateData.forTrendExpensesReport(self.initial_data)

        assert reportData.shape[1] == 3
        reportData.columns = ["date", "amount", "account"]
        reportData["date"] = pd.to_datetime(reportData["date"], format="%Y/%m/%d")

        # print(reportData)

        # Only expenses
        expenses = reportData[reportData["account"].str.startswith("Expenses:")].copy()

        # Extract category
        expenses["category"] = expenses["account"].str.replace("Expenses:", "", regex=False)

        # Convert date and extract month
        expenses["date"] = pd.to_datetime(expenses["date"])
        expenses["month"] = expenses["date"].dt.to_period("M")

        # Group by month and category
        monthly_expenses = (
            expenses
            .groupby(["month", "category"])["amount"]
            .sum()
            .reset_index()
        )

        # print(monthly_expenses)

        def thousands(x, pos):
            if abs(x) >= 1_000_000:
                return f"{x / 1_000_000:.2f}M"
            elif abs(x) >= 1_000:
                return f"{x / 1_000:.2f}k"
            return f"{x:.0f}"
        
        plot_data = monthly_expenses.pivot(
            index="month",
            columns="category",
            values="amount"
        ).fillna(0)

        # Create top 8 + Other dataframe
        all_categories = plot_data.columns.tolist()
        expense_groups["Other"] = [
            c for c in all_categories
            if c not in expense_groups["Housing"] + expense_groups["Main"]
        ]

        other_totals = plot_data[expense_groups["Other"] ].sum().sort_values(ascending=False)

        top_other_categories = other_totals.head(10).index

        other_plot = plot_data[top_other_categories].copy()
        # print(other_plot)
        other_plot["Other"] = (
            plot_data[expense_groups["Other"] ]
            .drop(columns=top_other_categories)
            .sum(axis=1)
        )
                
        fig, (ax1, ax2, ax3) = plt.subplots(
            3,
            1,
            figsize=(15, 9),
            sharex=True,
            gridspec_kw={"height_ratios": [1, 2, 4]}
        )

        # Apartment
        plot_data[expense_groups["Housing"]].plot(
            ax=ax1
        )
        ax1.yaxis.set_major_locator(MultipleLocator(2000))
        ax1.yaxis.set_major_formatter(FuncFormatter(thousands))
        ax1.set_title("Apartment Expenses")
        ax1.set_ylabel("Amount ($)")
        ax1.grid(axis="y")
        ax1.legend(
            title="Category",
            fontsize=8,
            title_fontsize=10,
            bbox_to_anchor=(1.02, 1),
            loc="upper left"
        )


        # Main
        plot_data[expense_groups["Main"]].plot(
            kind="bar",
            ax=ax2
        )
        ax2.yaxis.set_major_locator(MultipleLocator(250))
        ax2.yaxis.set_major_formatter(FuncFormatter(thousands))
        ax2.set_title("Main Expenses")
        ax2.set_ylabel("Amount ($)")
        ax2.grid(axis="y")
        ax2.legend(
            title="Category",
            fontsize=8,
            title_fontsize=10,
            bbox_to_anchor=(1.02, 1),
            loc="upper left"
        )


        # Other expenses
        other_plot.plot(
            kind="bar",
            stacked=True,
            colormap="tab20",
            ax=ax3
        )
        ax3.yaxis.set_major_locator(MultipleLocator(1000))
        ax3.yaxis.set_major_formatter(FuncFormatter(thousands))
        ax3.set_title("Other Expenses (Top Categories)")
        ax3.set_ylabel("Amount ($)")
        ax3.grid(axis="y")
        ax3.legend(
            title="Category",
            fontsize=8,
            title_fontsize=10,
            bbox_to_anchor=(1.02, 1),
            loc="upper left"
        )

        plt.xticks(rotation=45)
        plt.tight_layout(rect=(0, 0, 1, 0.96))

        fig.suptitle("Monthly Expenses Breakdown")

        filename = self.output_folder + "trend_expenses.png"
        self.log.info(f"Save Report: '{filename}'")

        fig.savefig(filename, dpi=300, bbox_inches="tight")

        # plt.show()