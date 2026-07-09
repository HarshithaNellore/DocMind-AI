"""
Main UI controller.
"""

from __future__ import annotations

import streamlit as st

from services import ServiceContainer

from ui.components.sidebar import Sidebar
from ui.pages.upload_page import UploadPage


class UIController:

    def __init__(
        self,
        container: ServiceContainer,
    ) -> None:

        self.container = container

    def run(self) -> None:

        Sidebar(self.container.document_manager,).render()

        UploadPage(
            self.container,
        ).render()