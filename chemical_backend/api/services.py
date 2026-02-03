import pandas as pd
from .validators import validate_columns, validate_numeric

def analyze_csv(file_obj):
    df = pd.read_csv(file_obj)

    validate_columns(df)
    validate_numeric(df)

    total_count = len(df)

    stats = {
        "flowrate": {
            "avg": float(df["Flowrate"].mean()),
            "min": float(df["Flowrate"].min()),
            "max": float(df["Flowrate"].max()),
            "std": float(df["Flowrate"].std()),
        },
        "pressure": {
            "avg": float(df["Pressure"].mean()),
            "min": float(df["Pressure"].min()),
            "max": float(df["Pressure"].max()),
            "std": float(df["Pressure"].std()),
        },
        "temperature": {
            "avg": float(df["Temperature"].mean()),
            "min": float(df["Temperature"].min()),
            "max": float(df["Temperature"].max()),
            "std": float(df["Temperature"].std()),
        },
    }

    type_distribution = df["Type"].value_counts().to_dict()

    return {
        "total_count": total_count,
        "statistics": stats,
        "type_distribution": type_distribution,
    }
