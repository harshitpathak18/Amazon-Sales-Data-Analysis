def layout_modifications(st):
    # Set the wide layout for the app
    st.set_page_config(layout="wide")

    # Remove the Streamlit watermark
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Remove margin and padding from the top of the page
    st.markdown("""
    <style>
    #root > div:nth-child(1) > div > div > div > div > section > div {
    padding-top: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Remove padding and margin from the top of the sidebar
    st.markdown("""
    <style>
    .sidebar-content {
    padding-top: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)