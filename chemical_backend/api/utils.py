import pandas as pd

def compute_summary(file_obj):
    df = pd.read_csv(file_obj)

    total_count = len(df)

    averages = {
        "flowrate_avg": float(df["Flowrate"].mean()),
        "pressure_avg": float(df["Pressure"].mean()),
        "temperature_avg": float(df["Temperature"].mean()),
    }

    type_distribution = df["Type"].value_counts().to_dict()

    summary = {
        "total_count": total_count,
        "averages": averages,
        "type_distribution": type_distribution,
    }

    return summary
