import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
import geopandas as gpd

MAPBOX_STYLE = "open-street-map"
SINGAPORE_CENTER = [1.3521, 103.8198]
ZOOM = 10


def make_choropleth_map(df, value_col, title):
    geojson = gpd.read_file("data/geo/singapore_planning_areas.geojson")
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations="town",
        featureidkey="properties.PLN_AREA_N",
        color=value_col,
        center={"lat": SINGAPORE_CENTER[0], "lon": SINGAPORE_CENTER[1]},
        mapbox_style=MAPBOX_STYLE,
        zoom=ZOOM,
        title=title
    )
    return fig

def make_heatmap_folium(df):
    m = folium.Map(location=SINGAPORE_CENTER, zoom_start=ZOOM)
    heat_data = df[["lat", "lon"]].dropna().values.tolist()
    HeatMap(heat_data, radius=10).add_to(m)
    return m

def make_scatter_map(df, color_col):
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color=color_col,
        center={"lat": SINGAPORE_CENTER[0], "lon": SINGAPORE_CENTER[1]},
        mapbox_style=MAPBOX_STYLE,
        zoom=ZOOM
    )
    return fig
