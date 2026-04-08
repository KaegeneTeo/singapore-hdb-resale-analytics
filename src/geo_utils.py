import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from pathlib import Path

GEOJSON_PATH = Path("data/geo/singapore_planning_areas.geojson")

# Hardcoded centroids for all 26 HDB towns
TOWN_CENTROIDS = {
    "ANG MO KIO": (1.3691, 103.8454),
    "BEDOK": (1.3236, 103.9305),
    "BISHAN": (1.3508, 103.8485),
    "BUKIT BATOK": (1.3496, 103.7496),
    "BUKIT MERAH": (1.2846, 103.8196),
    "BUKIT PANJANG": (1.3784, 103.7611),
    "BUKIT TIMAH": (1.3294, 103.8021),
    "CENTRAL AREA": (1.2897, 103.85),
    "CHOA CHU KANG": (1.3854, 103.7441),
    "CLEMENTI": (1.3151, 103.7657),
    "GEYLANG": (1.3186, 103.8872),
    "HOUGANG": (1.3714, 103.8922),
    "JURONG EAST": (1.3331, 103.7421),
    "JURONG WEST": (1.3397, 103.7036),
    "KALLANG/WHAMPOA": (1.3201, 103.8627),
    "MARINE PARADE": (1.3039, 103.9057),
    "PASIR RIS": (1.3736, 103.9493),
    "PUNGGOL": (1.4051, 103.9022),
    "QUEENSTOWN": (1.2946, 103.8037),
    "SEMBAWANG": (1.4491, 103.8198),
    "SENGKANG": (1.3911, 103.8952),
    "SERANGOON": (1.3501, 103.8727),
    "TAMPINES": (1.3496, 103.9568),
    "TOA PAYOH": (1.3346, 103.8492),
    "WOODLANDS": (1.4360, 103.7865),
    "YISHUN": (1.4293, 103.8352)
}


def load_sg_geojson():
    """Load Singapore planning area GeoJSON as GeoDataFrame."""
    return gpd.read_file(GEOJSON_PATH)


def town_to_latlon(town):
    """Map HDB town name to (lat, lon)."""
    return TOWN_CENTROIDS.get(town.upper(), (None, None))


def aggregate_by_town(df):
    """Aggregate transactions by town and return GeoDataFrame for mapping."""
    df = df.copy()
    df["lat"], df["lon"] = zip(*df["town"].map(town_to_latlon))
    agg = df.groupby("town").agg({
        "resale_price": "median",
        "lat": "first",
        "lon": "first"
    }).reset_index()
    gdf = gpd.GeoDataFrame(agg, geometry=[Point(xy) for xy in zip(agg["lon"], agg["lat"])], crs="EPSG:4326")
    return gdf
