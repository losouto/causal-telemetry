import unittest
import tempfile
import os
import pandas as pd
from src.ingestion.reveal import filter_telemetry_columns, load_run_telemetry

class TestIngestion(unittest.TestCase):
    def test_filter_telemetry_columns(self):
        sample_cols = [
            "Perf:Cycles.node0[count]",
            "Turbostat:Busy%.core1[%]",
            "GPU: utilization.gpu.0[%]",
            "IrrelevantMetric.value",
        ]
        filtered = filter_telemetry_columns(sample_cols)
        self.assertEqual(len(filtered), 3)
        self.assertNotIn("IrrelevantMetric.value", filtered)

    def test_load_run_telemetry_downcasting(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_csv = os.path.join(tmpdir, "test_run.csv")
            df_dummy = pd.DataFrame({
                "time": [1, 2, 3],
                "metric_float": [1.123456789, 2.987654321, 3.555555555]
            })
            df_dummy.to_csv(test_csv, index=False)

            df_loaded = load_run_telemetry(test_csv, downcast_float=True)
            self.assertEqual(str(df_loaded["metric_float"].dtype), "float32")

if __name__ == "__main__":
    unittest.main()
