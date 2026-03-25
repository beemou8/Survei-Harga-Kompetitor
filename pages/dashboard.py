import streamlit as st

def show_dashboard():
    user = st.session_state['user_data']

    # =========================
    # SIDEBAR
    # =========================
    with st.sidebar:
        st.markdown("### 👤 Profil")
        st.write(user['nama_lengkap'])
        st.caption(user['cabang'])
        st.caption(f"Role: {user['role']}")

        st.divider()

        # tombol logout
        if st.button("Logout"):
            del st.session_state['user_data']
            st.rerun()

    # =========================
    # HEADER
    # =========================
    st.title(f"Halo, {user['nama_lengkap']} 👋")
    st.caption("Silakan pilih menu di bawah")

    st.divider()

    # =========================
    # MENU UTAMA
    # =========================
    col1, col2 = st.columns(2)

    # tombol input data
    with col1:
        if st.button("➕ Input Data", use_container_width=True):
            st.session_state['menu'] = 'input'

    # tombol history
    with col2:
        if st.button("📜 History", use_container_width=True):
            st.session_state['menu'] = 'history'

    # =========================
    # MENU ADMIN
    # =========================
    if user['role'] == 'admin':
        st.divider()
        st.markdown("### ⚙️ Admin Panel")

        col3, col4 = st.columns(2)

        with col3:
            if st.button("👤 Tambah User", use_container_width=True):
                st.session_state['menu'] = 'add_user'

        with col4:
            if st.button("✏️ Edit User", use_container_width=True):
                st.session_state['menu'] = 'edit_user'

    st.divider()

    # =========================
    # ROUTING MENU
    # =========================
    if 'menu' not in st.session_state:
        st.info("Pilih menu untuk mulai")

    elif st.session_state['menu'] == 'input':
        from pages.input_data import show_input
        show_input()

    elif st.session_state['menu'] == 'history':
        from pages.history_data import show_history
        show_history()

    elif st.session_state['menu'] == 'add_user':
        from pages.add_user import show_add_user
        show_add_user()

    elif st.session_state['menu'] == 'edit_user':
        from pages.edit_user import show_edit_user
        show_edit_user()