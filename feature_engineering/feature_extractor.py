from pathlib import Path

import pandas as pd


DEFAULT_FEATURE_OUTPUT_PATH = Path("data/features/features.csv")
REQUIRED_CLEAN_COLUMNS = [
    "datetime",
    "log_level",
    "component",
    "event_type",
    "block_id",
    "source_ip",
    "destination_ip",
    "block_size",
]
FEATURE_COLUMNS = [
    "hour_of_day",
    "is_error",
    "component_encoded",
    "event_type_encoded",
    "block_size",
    "event_frequency",
    "source_ip_encoded",
    "destination_ip_encoded",
]


class HDFSFeatureExtractor:
    """
    Converts cleaned HDFS logs into ML-ready numerical features.
    """

    def extract(
        self,
        logs: pd.DataFrame | str | Path,
        output_path: str | Path = DEFAULT_FEATURE_OUTPUT_PATH,
    ) -> pd.DataFrame:
        frame = self._load_frame(logs)
        self.validate_schema(frame)

        prepared = frame.copy()
        prepared["datetime"] = pd.to_datetime(prepared["datetime"], errors="coerce")
        prepared["block_size"] = pd.to_numeric(prepared["block_size"], errors="coerce").fillna(0)
        prepared = prepared.dropna(subset=["datetime"]).copy()

        for column in ["component", "event_type", "source_ip", "destination_ip", "block_id"]:
            prepared[column] = prepared[column].astype("string").str.strip().fillna("UNKNOWN")
            prepared[column] = prepared[column].replace({"": "UNKNOWN", "<NA>": "UNKNOWN"})

        features = pd.DataFrame(index=prepared.index)
        features["hour_of_day"] = prepared["datetime"].dt.hour.astype("int64")
        features["is_error"] = (
            prepared["log_level"].astype("string").str.upper().eq("ERROR").astype("int64")
        )
        features["component_encoded"] = self._encode_categories(prepared["component"])
        features["event_type_encoded"] = self._encode_categories(prepared["event_type"])
        features["block_size"] = prepared["block_size"].astype("float64")
        features["event_frequency"] = prepared.groupby("block_id")["block_id"].transform("count").astype("int64")
        features["source_ip_encoded"] = self._encode_categories(prepared["source_ip"])
        features["destination_ip_encoded"] = self._encode_categories(prepared["destination_ip"])

        features = features[FEATURE_COLUMNS].reset_index(drop=True)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        features.to_csv(output, index=False)
        return features

    def validate_schema(self, frame: pd.DataFrame) -> None:
        missing_columns = [
            column for column in REQUIRED_CLEAN_COLUMNS if column not in frame.columns
        ]
        if missing_columns:
            raise ValueError(f"Missing required cleaned columns: {missing_columns}")

    def _load_frame(self, logs: pd.DataFrame | str | Path) -> pd.DataFrame:
        if isinstance(logs, pd.DataFrame):
            return logs
        return pd.read_csv(logs)

    @staticmethod
    def _encode_categories(series: pd.Series) -> pd.Series:
        values = series.astype("string").fillna("UNKNOWN")
        categories = {value: index for index, value in enumerate(sorted(values.unique()))}
        return values.map(categories).astype("int64")


def extract_hdfs_features(
    input_path: str | Path = "data/processed/hdfs_cleaned.csv",
    output_path: str | Path = DEFAULT_FEATURE_OUTPUT_PATH,
) -> pd.DataFrame:
    return HDFSFeatureExtractor().extract(input_path, output_path)


if __name__ == "__main__":
    extract_hdfs_features()
