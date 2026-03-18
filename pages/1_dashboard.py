import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
from src.filter_aggregate.functions import (
    aggregate_over_departements,
    filter_and_complete_data,
    aggregate_df_name_by_year,
    merge_df_code_reg_dep,
    aggregate_over_regions,
    aggregate_df_by_sexe,
)
from src.visualisation.plot import plot_map_interactive_plotly, _get_geo_config
import json

st.set_page_config(page_title="Dashboard - Prénoms", layout="wide")


# ========================
# 📥 Load data (cached)
# ========================
@st.cache_data
def load_data():
    return pd.read_csv(
        "data/output/prenom_clean.csv",
        dtype={"dept": str, "year": str, "sex": str},
    )


@st.cache_data
def load_geo():
    return gpd.read_parquet("data/geojson/output/region_departement.parquet")


@st.cache_data
def load_geojson(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_all_geojson():
    return {
        "reg": load_geojson("data/geojson/input/ref-regions-domcom-rapproches.geojson"),
        "dep": load_geojson(
            "data/geojson/input/ref-departements-domcom-rapproches.geojson"
        ),
    }


@st.cache_data
def prepare_name_data(data, name):
    filter_name = filter_and_complete_data(data, name)

    # Agrégations lourdes
    agg_sex = aggregate_df_by_sexe(filter_name)
    agg_year = aggregate_df_name_by_year(filter_name)
    return filter_name, agg_sex, agg_year


@st.cache_data
def prepare_geo_data(filter_name, _reg_dep):
    # merge lourd une seule fois
    merged = merge_df_code_reg_dep(filter_name, _reg_dep)
    # agrégations lourdes une seule fois
    agg_reg = aggregate_over_regions(merged)
    agg_dep = aggregate_over_departements(merged)
    return merged, agg_reg, agg_dep


@st.cache_data
def load_names(data):
    return sorted(data["name"].dropna().unique())


@st.cache_data
def load_global_stats(data):
    # Top 20
    top_names = (
        data[data["name"] != "_PRENOMS_RARES"]
        .groupby("name", as_index=False)
        .agg(count=("count", "sum"))
        .sort_values("count", ascending=False)
    )
    # Global Sex distribution
    agg_sex = data.groupby("sex", as_index=False).agg(count=("count", "sum"))
    sex_counts = agg_sex.set_index("sex")["count"].to_dict()

    return top_names.head(20), sex_counts


data = load_data()
reg_dep = load_geo()
geojsons = load_all_geojson()

NAMES = load_names(data)

# ========================
# 🏷️ Main title
# ========================
st.title("📊 Dashboard des prénoms")

tab_search, tab_global = st.tabs(["🔎 Recherche par prénom", "🏆 Palmarès & Global"])

with tab_search:
    default_index = NAMES.index("CHANTAL") if "CHANTAL" in NAMES else 0
    #### Select NAME
    name = st.selectbox("Choisi un prénom :", NAMES, index=default_index)

    filter_name, agg_sex, agg_year = prepare_name_data(data, name)
    merged, agg_reg, agg_dep = prepare_geo_data(filter_name, reg_dep)

    years_available = sorted(filter_name["year"].unique())

    st.markdown(
        f"Statistiques pour le prénom **{name}**",
        unsafe_allow_html=True,
    )

    # ========================
    # 🗺️ Statistique par sexe
    # ========================
    st.subheader("🗺️ Répartition par sexe")
    sex_counts = agg_sex["occ"].to_dict()

    nb_boy = int(sex_counts.get("1", 0))
    nb_girl = int(sex_counts.get("2", 0))

    col1, col2 = st.columns(2)
    with col1:
        st.metric("👦 Garçons", nb_boy)
    with col2:
        st.metric("👧 Filles", nb_girl)

    # ========================
    # 📈 Courbe par année
    # ========================
    st.subheader(f"📈 Évolution du prénom **{name}** dans le temps")
    fig_line = px.line(
        agg_year,
        x="year",
        y="count",
        markers=True,
        title=f"Nombre de naissances pour {name}",
    )

    st.plotly_chart(fig_line, width="stretch")

    # ========================
    # 🗺️ Carte par année
    # ========================
    st.subheader(f"🗺️ Répartition géographique")

    year_selected = st.select_slider(
        "##### 🗓️ Année",
        options=years_available,
        # value=years_available,  # dernière année par défaut
    )
    cfg_reg = _get_geo_config("reg")
    cfg_dep = _get_geo_config("dep")

    agg_reg_year = agg_reg[agg_reg["year"] == year_selected]
    agg_dep_year = agg_dep[agg_dep["year"] == year_selected]
    global_max = max(
        agg_reg_year["count"].max(),
        agg_dep_year["count"].max(),
    )
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🗺️ Naissances par région")
        fig_reg = plot_map_interactive_plotly(
            agg_reg_year, geojsons["reg"], cfg_reg, global_max
        )
        st.plotly_chart(fig_reg, width="stretch")

    with col2:
        st.markdown("### 🗺️ Naissances par département")
        fig_dep = plot_map_interactive_plotly(
            agg_dep_year, geojsons["dep"], cfg_dep, global_max
        )
        st.plotly_chart(fig_dep, width="stretch")


with tab_global:
    # ========================
    # Popularité
    # ========================
    st.subheader(f"📌 Informations générales")

    top_20, sex_counts = load_global_stats(data)

    fig_bar = px.bar(
        top_20,
        x="name",
        y="count",
        title="Top 20 des prénoms les plus donnés en France",
    )

    st.plotly_chart(fig_bar, width="stretch")

    st.markdown("Occurrence des prénoms par sexe (Total) :")

    nb_boy = int(sex_counts.get("1", 0))  # 1 = garçons
    nb_girl = int(sex_counts.get("2", 0))  # 2 = filles

    col1, col2 = st.columns(2)
    with col1:
        st.metric("👦 Garçons", f"{nb_boy:,}".replace(",", " "))

    with col2:
        st.metric("👧 Filles", f"{nb_girl:,}".replace(",", " "))
