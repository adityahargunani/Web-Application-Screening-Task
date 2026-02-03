REQUIRED_COLUMNS = {"Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"}

def validate_columns(df):
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def validate_numeric(df):
    for col in ["Flowrate", "Pressure", "Temperature"]:
        if not df[col].dtype.kind in "fi":
            raise ValueError(f"Column '{col}' must be numeric")
