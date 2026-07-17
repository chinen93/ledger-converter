from src.reports.data import Data
from tests.conf_log_test import BaseTestCase
import numpy as np


class TestReportData(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_shouldNormalizeData(self):
        data = Data()

        raw_data = np.array([
            ["2026-07-15","","DESC","A:B","$",10.0,"",""],
            ["2026-07-15","","DESC","C:D","$",-10.0,"",""],
        ])
        expected = np.array([
            ["2026-07-15", 10.0, "A", "B"],
            ["2026-07-15", -10.0, "C", "D"]
        ])

        normalized = data._normalizeData(raw_data)

        self.assertEqual(normalized.shape, (2, 4))
        np.testing.assert_equal(normalized, expected)

    def test_shouldNormalizeLongAccountData(self):
        data = Data()

        raw_data = np.array([
            ["2026-07-15","","DESC","A:B:C","$",10.0,"",""],
            ["2026-07-15","","DESC","D:EEEEE","$",-10.0,"",""],
        ])
        expected = np.array([
            ["2026-07-15", 10.0, "A", "B", "C"],
            ["2026-07-15", -10.0, "D", "EEEEE", ""]
        ])

        normalized = data._normalizeData(raw_data)

        self.assertEqual(normalized.shape, (2, 5))
        np.testing.assert_equal(normalized, expected)
        
    def test_shouldNormalizeDataCombineMonthAndAccount(self):
        data = Data()

        raw_data = np.array([
            ["2026-07-15","","DESC","A:B","$",10.0,"",""],
            ["2026-07-15","","DESC","C:D","$",-10.0,"",""],
            ["2026-07-15","","DESC","A:B","$",10.0,"",""],
            ["2026-07-15","","DESC","C:D","$",-10.0,"",""],
            ["2026-07-16","","DESC","A:B","$",10.0,"",""],
            ["2026-07-16","","DESC","C:D","$",-10.0,"",""],
        ])
        expected = np.array([
            ["2026-07-15", 20.0, "A", "B"],
            ["2026-07-15", -20.0, "C", "D"],
            ["2026-07-16", 10.0, "A", "B"],
            ["2026-07-16", -10.0, "C", "D"]
        ])

        normalized = data._normalizeData(raw_data)

        self.assertEqual(normalized.shape, (4, 4))
        np.testing.assert_equal(normalized, expected)
