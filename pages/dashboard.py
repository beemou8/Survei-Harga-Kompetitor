import streamlit as st

def show_dashboard():
    user = st.session_state['user_data']

    # Custom Header
    col_info, col_logout = st.columns([3, 1])
    with col_info:
        st.subheader(f"Halo, {user['nama_lengkap']} 👋")
        st.caption(f"{user['cabang']} | {user['role']}")
    with col_logout:
        st.write("") 
        if st.button("Logout", use_container_width=True):
            del st.session_state['user_data']
            if 'menu' in st.session_state:
                del st.session_state['menu']
            st.rerun()

    st.divider()

    # Main Menu
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Input Data", use_container_width=True, type="primary"):
            st.session_state['menu'] = 'input'
    with col2:
        if st.button("📜 History", use_container_width=True):
            st.session_state['menu'] = 'history'

    # Admin Section
    if user['role'] == 'admin':
        st.write("")
        st.markdown("#### Admin Panel")
        col3, col4 = st.columns(2)
        with col3:
            if st.button("👤 Tambah User", use_container_width=True):
                st.session_state['menu'] = 'add_user'
        with col4:
            if st.button("✏️ Edit User", use_container_width=True):
                st.session_state['menu'] = 'edit_user'

    st.divider()

    # Routing
    if 'menu' in st.session_state and st.session_state['menu']:
        if st.button("⬅️ Kembali"):
            st.session_state['menu'] = None
            st.rerun()
        st.write("")

    current_menu = st.session_state.get('menu')
    
    if current_menu == 'input':
        from pages.input_data import show_input
        show_input()
    elif current_menu == 'history':
        from pages.history_data import show_history
        show_history()
    elif current_menu == 'add_user':
        from pages.add_user import show_add_user
        show_add_user()
    elif current_menu == 'edit_user':
        from pages.edit_user import show_edit_user
        show_edit_user()