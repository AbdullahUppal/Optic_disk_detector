from constants import RESULT_CSV_PATH
import math
import pandas as pd


def calculate_eclidean_error(image_name,cx,cy):
    print("CSV Path: ", RESULT_CSV_PATH)
    df = pd.read_csv(RESULT_CSV_PATH)
    record_mask = df["image"] == image_name
    record = df[record_mask]

    if record.empty:
        raise ValueError(f"Image not found in CSV: {image_name}")

    x, y = record[["x", "y"]].iloc[0]
    print(x, y)
    eclidean_error = math.sqrt(math.pow((cx-x), 2) + math.pow((cy-y),2))

    df.loc[record_mask, "new_x"] = cx
    df.loc[record_mask, "new_y"] = cy
    df.loc[record_mask, "euclidean_error"] = eclidean_error
    df.to_csv(RESULT_CSV_PATH, index=False)

    return eclidean_error



    