"""
Workspace component.
"""

from __future__ import annotations

import streamlit as st

from ui.components import Uploader


class Workspace:
    """
    Workspace management panel.
    """

    def __init__(
        self,
        container,
    ) -> None:

        self.container = container

    def render(self):

        st.subheader("📂 Workspace")

        uploaded_files = Uploader().render()

        return uploaded_files