import streamlit as st


class SourceCard:

    def render(
        self,
        source,
    ):

        with st.expander(
            f"📄 Page {source.metadata.get('page_number', '?')}",
            expanded=False,
        ):

            st.caption(
                f"Similarity: {source.distance:.3f}"
            )

            st.write(source.text)