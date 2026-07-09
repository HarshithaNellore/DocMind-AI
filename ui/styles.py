"""
Custom styles for DocMind AI.
"""

import streamlit as st


def load_styles() -> None:
    st.markdown(
        """
<style>

.block-container{
    padding-top:1.2rem;
    padding-bottom:1rem;
}

[data-testid="stSidebar"]{
    border-right:1px solid rgba(120,120,120,.15);
}

div[data-testid="stMetric"]{
    border-radius:12px;
    padding:.5rem;
}

</style>
""",
        unsafe_allow_html=True,
    )