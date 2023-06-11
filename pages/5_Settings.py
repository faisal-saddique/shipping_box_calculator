import streamlit as st
import pandas as pd

df = pd.DataFrame(
    [
       {"PADDING ON SIDES (in)": 2, "PADDING ON TOP": 2, "PADDING ON BOTTOM": 0, "MAX BOX WEIGHT (lbs)":45},
   ]
)

st.header("SETTINGS")

st.write("APPLIES TO ALL SHIPMENTS")

edited_df = st.data_editor(df)

# st.write("---")

# st.dataframe(edited_df["padd"])