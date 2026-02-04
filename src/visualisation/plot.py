# Principal functions for plots

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import json
import geopandas as gpd
from src.filter_aggregate.functions import (
    aggregate_over_regions,
    aggregate_over_departements,
    filter_data_over_year,
)


def plot_ts_name_over_year(aggregate_df, name, figsize: tuple = (20, 10)):
    plt.figure(figsize=figsize)
    plt.plot(
        aggregate_df["year"],
        aggregate_df["count"],
        marker="o",
        color="dodgerblue",
        linewidth=2,
        label="Nb de naissance",
    )

    plt.title(f"Évolution du prénom {name}", fontsize=20, fontweight="bold")
    plt.xlabel("Année", fontsize=14)
    plt.ylabel("Nombre de naissances", fontsize=14)

    plt.xticks(aggregate_df["year"][::2], rotation=45)
    plt.legend(fontsize=12)
    plt.tight_layout()

    plt.show()


def plot_map_static_matplotlib(df_merged: pd.DataFrame, year: str, mode: str = "reg"):
    cfg = _get_geo_config(mode)

    agg = cfg["agg_func"](df_merged)
    df_year = filter_data_over_year(agg, year)

    gdf = gpd.GeoDataFrame(df_year, geometry=cfg["geometry_col"])

    fig, ax = plt.subplots(figsize=(6, 6))
    gdf.plot(
        column="count",
        cmap="Blues",
        linewidth=0.6,
        edgecolor="0.5",
        legend=True,
        ax=ax,
        legend_kwds={"shrink": 0.5, "aspect": 20, "pad": 0.01},
    )

    ax.set_title(f"Répartition par {cfg['label']} en {year}", fontsize=14)
    ax.set_axis_off()
    return fig


def _get_geo_config(mode: str):
    if mode == "dep":
        return {
            "geojson_path": "data/geojson/input/ref-departements-domcom-rapproches.geojson",
            "code_col": "code_dep",
            "name_col": "nom_dep",
            "featureidkey": "properties.DDEP_C_COD",
            "label": "département",
            "geometry_col": "geometry_departement",
            "agg_func": aggregate_over_departements,
        }
    elif mode == "reg":
        return {
            "geojson_path": "data/geojson/input/ref-regions-domcom-rapproches.geojson",
            "code_col": "code_reg",
            "name_col": "nom_reg",
            "featureidkey": "properties.DREG_C_COD",
            "label": "région",
            "geometry_col": "geometry_region",
            "agg_func": aggregate_over_regions,
        }
    else:
        raise ValueError("mode doit être 'reg' ou 'dep'")


def plot_map_interactive_plotly(df_year, geojson, cfg, global_max):
    fig = px.choropleth_map(
        df_year,
        geojson=geojson,
        locations=cfg["code_col"],
        color="count",
        featureidkey=cfg["featureidkey"],
        map_style="carto-positron",
        zoom=3.5,
        center={"lat": 46.6, "lon": 2.5},
        opacity=0.7,
        color_continuous_scale=px.colors.sequential.Oranges,
        range_color=(0, df_year["count"].max()),
        hover_name=cfg["name_col"] if cfg["name_col"] in df_year.columns else None,
    )
    fig.update_layout(margin=dict(r=0, t=0, l=0, b=0), height=700)
    return fig


def plot_map_france(df_agg_year, year, mode: str = "reg"):
    if mode == "reg":
        geometry = "geometry_region"
        mode_label = "région"
    elif mode == "dep":
        geometry = "geometry_departement"
        mode_label = "departement"
    else:
        raise ValueError("Le paramètre 'mode' doit être 'reg' ou 'dep'.")
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))

    gdf_valid = gpd.GeoDataFrame(df_agg_year, geometry=geometry)
    gdf_valid.plot(
        column="count",
        cmap="Blues",
        linewidth=0.8,
        edgecolor="0.5",
        legend=True,
        ax=ax,
        legend_kwds={"shrink": 0.5, "aspect": 20, "pad": 0.01},
    )

    ax.set_title(
        f"Répartition par {mode_label} sur l'année {year}",
        fontsize=14,
        # fontweight="bold",
    )
    ax.set_axis_off()
    return fig
