import streamlit as st


class StatusBadge:

    COLORS = {
        "ready": "🟢 Ready",
        "processing": "🟡 Processing",
        "failed": "🔴 Failed",
        "pending": "⚪ Pending",
    }

    def render(
        self,
        status,
    ):

        st.caption(
            self.COLORS.get(
                status.value.lower(),
                status.value,
            )
        )