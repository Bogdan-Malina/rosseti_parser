import pandas as pd
import folium


def create_map():
    map_data = pd.read_csv("data/build_ids.csv")
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
    create_map()