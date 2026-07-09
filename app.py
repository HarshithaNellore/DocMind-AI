"""
DocMind AI Version 2
"""

import streamlit as st

from services import ServiceContainer
from ui.styles import load_styles

from ui import UIController
from ui.theme import (
    APP_ICON,
    APP_TITLE,
    LAYOUT,
    SIDEBAR_STATE,
)


st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)
load_styles()
container = ServiceContainer()

controller = UIController(
    container,
)

controller.run()