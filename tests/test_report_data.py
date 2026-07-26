from src.reports.data import Data, ManipulateData
from tests.conf_log_test import BaseTestCase
import numpy as np
import pandas as pd


class TestReportData(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_shouldNormalizeData(self):
        data = Data()

        raw_data = np.array(
            [
                ["2026-07-15", "", "DESC", "AA:BB", "$", "10.0", "", ""],
                ["2026-07-15", "", "DESC", "CC:DD", "$", "-10.0", "", ""],
            ]
        )
        expected = np.array(
            [["2026", "07", "15", "10.0", "AA", "BB"], ["2026", "07", "15", "-10.0", "CC", "DD"]]
        )

        normalized = data._normalizeData(raw_data)

        self.assertEqual(normalized.shape, expected.shape)
        np.testing.assert_equal(normalized, expected)

    def test_shouldNormalizeLongAccountData(self):
        data = Data()

        raw_data = np.array(
            [
                ["2026-07-15", "", "DESC", "AA:BB:CC", "$", "10.0", "", ""],
                ["2026-07-15", "", "DESC", "DD:EEEEE", "$", "-10.0", "", ""],
            ]
        )
        expected = np.array(
            [
                ["2026", "07", "15", "10.0", "AA", "BB", "CC"],
                ["2026", "07", "15", "-10.0", "DD", "EEEEE", None],
            ]
        )

        normalized = data._normalizeData(raw_data)

        self.assertEqual(normalized.shape, expected.shape)
        np.testing.assert_equal(normalized, expected)


class TestReportManipulateData(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_shouldManipulateDataForOverviewReport(self):
        normalized_data = np.array(
            [
                ["2026", "07", "15", "10.0", "Expenses", "AA", ""],
                ["2026", "07", "15", "-10.0", "Bank", "Checking", ""],
                ["2026", "07", "15", "10.0", "Expenses", "BB", "CC"],
                ["2026", "07", "15", "-10.0", "Bank", "CreditCard", ""],
                ["2026", "07", "16", "10.0", "Expenses", "AA", ""],
                ["2026", "07", "16", "-10.0", "Bank", "Checking", ""],
                ["2026", "08", "21", "10.0", "Expenses", "AA", ""],
                ["2026", "08", "21", "-10.0", "Bank", "Checking", ""],
                ["2026", "08", "29", "10.0", "Liability", "DD", ""],
                ["2026", "08", "29", "-10.0", "Bank", "Checking", ""],
            ]
        )
        expected = pd.DataFrame(
            [
                ["2026/07/15", -10.0, "Bank:Checking"],
                ["2026/07/15", -10.0, "Bank:CreditCard"],
                ["2026/07/15", 20.0, "Expenses"],
                ["2026/07/16", -10.0, "Bank:Checking"],
                ["2026/07/16", 10.0, "Expenses"],
                ["2026/08/21", -10.0, "Bank:Checking"],
                ["2026/08/21", 10.0, "Expenses"],
                ["2026/08/29", -10.0, "Bank:Checking"],
                ["2026/08/29", 10.0, "Liability"],
            ]
        )

        result = ManipulateData.forOverviewReport(normalized_data)

        pd.testing.assert_frame_equal(result, expected)

    def test_shouldManipulateDataForTrendExpensesReport(self):
        normalized_data = np.array(
            [
                ["2026", "07", "15", "10.0", "Expenses", "AA", ""],
                ["2026", "07", "15", "-10.0", "Bank", "Checking", ""],
                ["2026", "07", "15", "10.0", "Expenses", "BB", "CC"],
                ["2026", "07", "15", "-10.0", "Bank", "CreditCard", ""],
                ["2026", "07", "16", "10.0", "Expenses", "AA", ""],
                ["2026", "07", "16", "-10.0", "Bank", "Checking", ""],
                ["2026", "08", "21", "10.0", "Expenses", "AA", ""],
                ["2026", "08", "21", "-10.0", "Bank", "Checking", ""],
                ["2026", "08", "29", "10.0", "Liability", "DD", ""],
                ["2026", "08", "29", "-10.0", "Bank", "Checking", ""],
            ]
        )
        expected = pd.DataFrame(
            [
                ["2026/07/15", -20.0, "Bank"],
                ["2026/07/15", 10.0, "Expenses:AA"],
                ["2026/07/15", 10.0, "Expenses:BB"],
                ["2026/07/16", -10.0, "Bank"],
                ["2026/07/16", 10.0, "Expenses:AA"],
                ["2026/08/21", -10.0, "Bank"],
                ["2026/08/21", 10.0, "Expenses:AA"],
                ["2026/08/29", -10.0, "Bank"],
                ["2026/08/29", 10.0, "Liability"],
            ]
        )

        result = ManipulateData.forTrendExpensesReport(normalized_data)

        pd.testing.assert_frame_equal(result, expected)
