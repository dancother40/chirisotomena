import streamlit as st
import pandas as pd
import os

def obtener_resultado(goles_a, goles_b):

    if goles_a > goles_b:
        return "A"

    elif goles_b > goles_a:
        return "B"

    else:
        return "EMPATE"


def calcular_puntos(pred_a, pred_b, real_a, real_b):

    puntos = 0

    resultado_pred = obtener_resultado(pred_a, pred_b)
    resultado_real = obtener_resultado(real_a, real_b)

    if resultado_pred == resultado_real:
        puntos += 1

    if pred_a == real_a and pred_b == real_b:
        puntos += 1

    return puntos


st.title("Mundialito CHIRISOTOMENA")
st.write("Ranking de participantes")

st.divider()

ARCHIVO_PRONOSTICOS = "pronosticos.csv"
ARCHIVO_RESULTADOS = "resultados.csv"

st.subheader("Pronósticos registrados")

if os.path.exists(ARCHIVO_PRONOSTICOS):

    df_pronosticos = pd.read_csv(
    ARCHIVO_PRONOSTICOS,
    encoding="utf-8-sig",
    sep=","
)

    st.dataframe(df_pronosticos)

    csv = df_pronosticos.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Descargar pronósticos",
        data=csv,
        file_name="pronosticos.csv",
        mime="text/csv"
    )

else:
    st.warning("Todavía no existe pronosticos.csv.")
    st.stop()


st.divider()

st.header("Tabla de posiciones")

if os.path.exists(ARCHIVO_RESULTADOS):

    df_resultados = pd.read_csv(
        ARCHIVO_RESULTADOS,
        encoding="utf-8-sig",
        sep=","
    )

    df = df_pronosticos.merge(
        df_resultados,
        on="id_partido",
        how="inner"
    )

    ranking = []

    for _, fila in df.iterrows():

        puntos = calcular_puntos(
            fila["goles_a"],
            fila["goles_b"],
            fila["goles_real_a"],
            fila["goles_real_b"]
        )

        ranking.append({
            "nombre": fila["nombre"],
            "puntos": puntos
        })

    if len(ranking) > 0:

        df_ranking = pd.DataFrame(ranking)

        tabla = df_ranking.groupby(
            "nombre"
        )["puntos"].sum().reset_index()

        tabla = tabla.sort_values(
            by="puntos",
            ascending=False
        )

        st.dataframe(tabla)

        csv_ranking = tabla.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Descargar ranking",
            data=csv_ranking,
            file_name="ranking.csv",
            mime="text/csv"
        )

    else:
        st.info("No hay coincidencias entre pronósticos y resultados.")

else:
    st.info("Todavía no existe resultados.csv. Cuando lo subas, se calculará el ranking.")