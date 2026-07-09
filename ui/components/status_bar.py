"""
Status bar component.
"""

import streamlit as st


class StatusBar:

    def render(
        self,
        message: str,
    ) -> None:

        st.info(message)