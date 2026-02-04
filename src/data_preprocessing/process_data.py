import pandas as pd
from loguru import logger


def clean_and_process_data(
    data_input_path: str = "data/dpt2022_csv/dpt2022.csv",
    data_output_path: str = "data/output/prenom_clean.csv",
):
    # Input
    logger.info("Load input dataset")
    data = pd.read_csv(data_input_path, sep=";", encoding="utf-8")

    # Rename
    data = data.rename(
        columns={
            "sexe": "sex",
            "preusuel": "name",
            "annais": "year",
            "dpt": "dept",
            "nombre": "count",
        }
    )
    data["sex"] = data["sex"].astype(str)
    # DROP NA
    logger.info("Drop NA")
    data = data.dropna(subset=["name", "dept", "year", "count", "sex"])

    # Name with only one letter
    logger.info("Drop name with only one letter:")
    data["len_name"] = data["name"].apply(lambda x: len(x))
    logger.info(data[data["len_name"] == 1]["name"].unique())
    data = data[data["len_name"] > 1]
    data = data.drop(columns="len_name")

    # Lines with year XXXX or dep XX
    data = data[(data["year"] != "XXXX") & (data["dept"] != "XX")]
    logger.info("Types columns:")
    print(data.dtypes)
    logger.info("Export dataset")
    data.to_csv(data_output_path, index=False)


if __name__ == "__main__":
    clean_and_process_data()
