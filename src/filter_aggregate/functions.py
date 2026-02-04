# Many functions for filtering and aggregating dataframes

import pandas as pd

YEARS = list(str(i) for i in range(1900, 2023))

ALL_DEPTS = [
    "971",
    "972",
    "973",
    "974",
    "976",
    "77",
    "78",
    "91",
    "75",
    "93",
    "94",
    "92",
    "95",
    "36",
    "28",
    "37",
    "41",
    "18",
    "45",
    "39",
    "25",
    "90",
    "21",
    "70",
    "71",
    "89",
    "58",
    "76",
    "61",
    "50",
    "14",
    "27",
    "02",
    "80",
    "62",
    "60",
    "59",
    "68",
    "67",
    "57",
    "55",
    "54",
    "52",
    "51",
    "08",
    "10",
    "88",
    "44",
    "85",
    "49",
    "72",
    "53",
    "35",
    "29",
    "56",
    "22",
    "87",
    "16",
    "17",
    "24",
    "33",
    "79",
    "40",
    "64",
    "47",
    "19",
    "23",
    "86",
    "09",
    "82",
    "12",
    "11",
    "81",
    "30",
    "65",
    "31",
    "66",
    "32",
    "34",
    "48",
    "46",
    "15",
    "03",
    "07",
    "38",
    "26",
    "74",
    "42",
    "63",
    "69",
    "73",
    "43",
    "01",
    "84",
    "83",
    "06",
    "05",
    "04",
    "13",
    "20",
]


def filter_data_by_name(df, name):
    """Filter the dataframe by name."""
    filtered = df[(df["name"] == name)]
    return filtered


def complete_year_dept_panel(df_name, all_depts, years):
    """
    df_name : DataFrame filtré sur un prénom
    all_depts : liste de tous les départements possibles
    years : range ou liste des années à couvrir
    """
    # Index complet year × dept
    full_index = pd.MultiIndex.from_product([years, all_depts], names=["year", "dept"])

    df_full = full_index.to_frame(index=False)

    # Merge avec les vraies données
    df_completed = df_full.merge(df_name, on=["year", "dept"], how="left").fillna(
        {"count": 0}
    )

    return df_completed


def filter_and_complete_data(df, name):
    df_filtered = filter_data_by_name(df, name)
    df_filtered = complete_year_dept_panel(df_filtered, ALL_DEPTS, YEARS)
    return df_filtered


def aggregate_df_by_sexe(df_filtered):
    return df_filtered.groupby("sex").agg(occ=("sex", "count"))


def aggregate_df_name_by_year(df_filtered_name):
    """Aggregation the dataframe by year."""
    return df_filtered_name.groupby(["year"], as_index=False).agg({"count": "sum"})


def merge_df_code_reg_dep(filtered_name_data, reg_dep):
    merged_data = filtered_name_data.merge(
        reg_dep, how="left", left_on="dept", right_on="code_dep"
    )
    return merged_data


def aggregate_over_regions(merged_data):
    agg_reg = merged_data.groupby(
        ["nom_reg", "code_reg", "geometry_region", "year"], as_index=False
    ).agg({"count": "sum"})
    return agg_reg


def aggregate_over_departements(merged_data):
    agg_dep = merged_data.groupby(
        ["dept", "code_dep", "nom_dep", "geometry_departement", "year"], as_index=False
    ).agg({"count": "sum"})
    return agg_dep


def filter_data_over_year(df, year):
    filtered = df[df["year"] == year]
    return filtered
