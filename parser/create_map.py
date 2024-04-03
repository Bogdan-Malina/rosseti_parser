import pandas as pd
import folium
from database import engine


def create_map(connection):
    map_data = pd.read_sql_table('build_ids', con=connection)
    _map = folium.Map(location=(59.938784, 30.314997), zoom_start=12)
    for each in map_data.iterrows():
        _map.add_child(
            folium.Marker(
                location=[each[1]["latitude"], each[1]["longitude"]],
                clustered_marker=True
            )
        )
    _map.save("data/map.html")


if __name__ == "__main__":
    with engine.connect() as conn:
        create_map(conn)
