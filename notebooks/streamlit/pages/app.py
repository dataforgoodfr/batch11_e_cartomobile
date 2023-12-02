import streamlit as st
from page1_functions import get_datas, get_isochrones, make_map
from streamlit_folium import folium_static

DATA_PATH = "datas"


def choose_town(df):
    col1, col2, col3 = st.columns(3)
    with col1:
        region_choices = df.region_name.sort_values(ascending=True).unique()
        region = st.selectbox("Choose a region", region_choices, index=0)
        with col2:
            dep_choices = (
                df.query(f"region_name == {region}")
                .dep_name.sort_values(ascending=True)
                .unique()
            )
            dep = st.selectbox("Choose a department", dep_choices, index=0)
            with col3:
                town_choices = (
                    df.query(f"region_name == {region} and dep_name == {dep}")
                    .nom.sort_values(ascending=True)
                    .unique()
                )
                town = st.selectbox("Choose a town", town_choices, index=0)
    return town


def choose_isos():
    """dirty fix for type mismatch in slide"""
    # iso = np.array([0, 0, 0, 0], dtype=int)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        iso_0 = st.slider(
            "Isochrone range:  first ", min_value=1, max_value=97, value=5
        )
        with col2:
            iso_1 = st.slider(
                "second", min_value=iso_0 + 1, max_value=98, value=iso_0 + 1
            )  #
            with col3:
                iso_2 = st.slider(
                    "third", min_value=iso_1 + 1, max_value=99, value=iso_1 + 1
                )  #
                with col4:
                    iso_3 = st.slider(
                        "fourth", min_value=iso_2 + 1, max_value=100, value=iso_2 + 1
                    )  #
    iso = [iso_0 * 1e3, iso_1 * 1e3, iso_2 * 1e3, iso_3 * 1e3]
    return iso


# STREAMLIT APP LAYOUT
def main():
    st.title("E-motion")

    bornes, communes = get_datas(
        DATA_PATH, "dataset_charge_points.feather", "2022-12-31"
    )

    town = choose_town(communes)
    # st.write(town)

    iso = choose_isos()
    # st.write(iso)

    token = "pk.eyJ1IjoibWlrYWxlcm95IiwiYSI6ImNsZzZvcDN4dDBmbXMzZHFmYmd1ajJ6bGIifQ.-GfBZA2ZGXHpkELd0eLBAw"

    centre_df = get_isochrones(communes, town, iso, token)
    # st.write(centre_df)

    # title_html = f"""
    #          <h3 align="center" style="font-size:12px"><b>{town} | {iso[0]} / {iso[1]} / {iso[2]} / {iso[3]} m</b></h3>
    #          """
    # title = st.markdown(title_html, unsafe_allow_html=True)

    m = make_map(centre_df, communes, bornes)

    # st_map = st_folium(m, width="100%", height="80%")
    _map = folium_static(m)
    st.map(_map)


if __name__ == "__main__":
    main()
