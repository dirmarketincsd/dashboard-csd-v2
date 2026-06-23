def conectar_sheet():
    import streamlit as st
    from google.oauth2.service_account import Credentials
    
    # En producción usa secrets de Streamlit, en local usa credentials.json
    try:
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
    except:
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID)