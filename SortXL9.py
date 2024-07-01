import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import random
import subprocess
import os
# Ensure wkhtmltopdf is installed
if not os.path.exists('/usr/local/bin/wkhtmltopdf'):
    st.warning("wkhtmltopdf is not installed. Running setup script...")
    subprocess.run(['bash', 'setup.sh'], check=True)
import pdfkit

st.set_page_config(page_title="ProcureTrack", layout="wide")

# Placeholder for the OTP (in a real application, this should be handled more securely)
otp_placeholder = st.empty()

# Initial username and password
initial_username = 'admin'
initial_password = 'default_password'

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'password' not in st.session_state:
    st.session_state.password = initial_password
if 'username' not in st.session_state:
    st.session_state.username = initial_username
if 'otp' not in st.session_state:
    st.session_state.otp = ''
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'track_option' not in st.session_state:
    st.session_state.track_option = 'sensor_procurement'

# Function to send OTP
def send_otp():
    st.session_state.otp = str(random.randint(100000, 999999))
    otp_placeholder.text(f"Your OTP is: {st.session_state.otp}")  # This simulates sending the OTP

# Function to render the login form
def login():
    st.markdown("""
    <style>
    .login-form {
        max-width: 400px;
        margin: auto;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .login-form h2 {
        text-align: center;
        color: #004d99;
    }
    .login-form input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .login-form button {
        width: 100%;
        padding: 10px;
        background-color: #004d99;
        border: none;
        color: white;
        border-radius: 5px;
        cursor: pointer;
    }
    .login-form button:hover {
        background-color: #003366;
    }
    .login-form .links {
        text-align: center;
        margin-top: 10px;
    }
    .login-form .links a {
        color: #004d99;
        text-decoration: none;
        margin: 0 10px;
    }
    .login-form .links a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="login-form">
        <h2>Login</h2>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if username == st.session_state.username and password == st.session_state.password:
            st.session_state.logged_in = True
            st.session_state.page = 'selection'
            st.success("Logged in successfully")
            st.experimental_rerun()  # Ensure the app reruns to reflect the state change
        else:
            st.error("Invalid username or password")

    # Hidden buttons to handle page changes
    if st.button("Change Password", key="change-password-link", on_click=lambda: change_page('change_password')):
        st.experimental_rerun()

    if st.button("Forgot Password", key="forgot-password-link", on_click=lambda: change_page('forgot_password')):
        st.experimental_rerun()

# Function to change the page
def change_page(page):
    st.session_state.page = page

# Function to render the change password form
def change_password():
    st.markdown("""
    <style>
    .change-password-form {
        max-width: 400px;
        margin: auto;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .change-password-form h2 {
        text-align: center;
        color: #004d99;
    }
    .change-password-form input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .change-password-form button {
        width: 100%;
        padding: 10px;
        background-color: #004d99;
        border: none;
        color: white;
        border-radius: 5px;
        cursor: pointer;
    }
    .change-password-form button:hover {
        background-color: #003366;
    }
    </style>
    <div class="change-password-form">
        <h2>Change Password</h2>
    """, unsafe_allow_html=True)

    old_password = st.text_input("Old Password", type="password", key="change_old_password")
    new_password = st.text_input("New Password", type="password", key="change_new_password")
    confirm_password = st.text_input("Confirm New Password", type="password", key="change_confirm_password")
    if st.button("Change Password", key="change_password_button"):
        if old_password == st.session_state.password:
            if new_password == confirm_password:
                st.session_state.password = new_password
                st.success("Password changed successfully")
            else:
                st.error("New passwords do not match")
        else:
            st.error("Old password is incorrect")

    if st.button("Go to Login"):
        st.session_state.page = 'login'
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Function to render the forgot password form
def forgot_password():
    st.markdown("""
    <style>
    .forgot-password-form {
        max-width: 400px;
        margin: auto;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .forgot-password-form h2 {
        text-align: center;
        color: #004d99;
    }
    .forgot-password-form input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .forgot-password-form button {
        width: 100%;
        padding: 10px;
        background-color: #004d99;
        border: none;
        color: white;
        border-radius: 5px;
        cursor: pointer;
    }
    .forgot-password-form button:hover {
        background-color: #003366;
    }
    </style>
    <div class="forgot-password-form">
        <h2>Forgot Password</h2>
    """, unsafe_allow_html=True)

    phone_number = st.text_input("Enter your phone number", key="forgot_phone_number")
    if st.button("Send OTP", key="forgot_send_otp"):
        send_otp()
    otp = st.text_input("Enter OTP", key="forgot_otp")
    new_password = st.text_input("New Password", type="password", key="forgot_new_password")
    confirm_password = st.text_input("Confirm New Password", type="password", key="forgot_confirm_password")
    if st.button("Reset Password", key="forgot_reset_password"):
        if otp == st.session_state.otp:
            if new_password == confirm_password:
                st.session_state.password = new_password
                st.success("Password reset successfully")
            else:
                st.error("New passwords do not match")
        else:
            st.error("Invalid OTP")

    if st.button("Go to Login"):
        st.session_state.page = 'login'
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Function to render the selection page
def selection_page():
    st.markdown("""
    <style>
    .selection-page {
        max-width: 600px;
        margin: 100px auto;
        padding: 30px;
        background-color: #ffffff;
        border-radius: 20px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
        animation: fadeIn 1.5s ease-in-out;
        text-align: center;
    }
    .selection-page h2 {
        color: #004d99;
        margin-bottom: 40px;
        font-size: 28px;
        font-family: 'Arial', sans-serif;
    }
    .selection-button {
        width: 45%;
        padding: 20px;
        background-color: #004d99;
        border: none;
        color: white;
        border-radius: 10px;
        cursor: pointer;
        margin: 10px 5%;
        font-size: 18px;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    .selection-button:hover {
        background-color: #003366;
        transform: scale(1.05);
    }
    .selection-button:active {
        transform: scale(0.95);
    }
    .selection-button:focus {
        outline: none;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    body {
        background: linear-gradient(135deg, #71b7e6, #9b59b6);
    }
    </style>
    <div class="selection-page">
        <h2>Select Tracking Option</h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sensor Procurement", key="sensor_procurement", use_container_width=True):
            st.session_state.track_option = 'sensor_procurement'
            st.session_state.page = 'main'
            st.experimental_rerun()

    with col2:
        if st.button("Sensor Replacement", key="sensor_replacement", use_container_width=True):
            st.session_state.track_option = 'sensor_replacement'
            st.session_state.page = 'main'
            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Main app logic
def main():
    # Custom logo and title
    st.write("""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <img src="https://1000logos.net/wp-content/uploads/2021/08/Reliance-Industries-Limited-RIL-Logo.jpg" width="200" height="125" style="margin-bottom: 10px;">
        </div>
        """, unsafe_allow_html=True)

    # Define the HTML string
    html_string = '<h1>ProcureTrack</h1>'
    # Display the HTML using st.markdown
    st.markdown(html_string, unsafe_allow_html=True)
    st.markdown('<h2 class="subheader"><em>Automating Your Procurement Workflow</em></h2>', unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = 'login'
        st.experimental_rerun()
    # Define local_css function
    def local_css():
        css = """
        <style>
        body {
            font-family: "Arial", sans-serif;
            background-color: #f5f5f5;
        }
        h1, h2, h3 {
            color: #004d99;
        }
        .subheader {
            margin-right: 100px;  /* Adjust this value to shift more or less */
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    # Apply custom CSS
    local_css()

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        # Ensure the dates are correctly converted to datetime
        df['Sensor Expiry Date'] = pd.TimedeltaIndex(df['Sensor Expiry Date'], unit='d') + datetime(1899, 12, 30)
        df['procurement_date'] = pd.TimedeltaIndex(df['procurement_date'], unit='d') + datetime(1899, 12, 30)
        df['sensor replacement'] = pd.to_datetime(df['sensor replacement'], format='%Y-%m-%d', errors='coerce')

        st.write("## Uploaded Data Preview:")
        st.dataframe(df.head())

        st.sidebar.header("Filter Options")
        plant = st.sidebar.selectbox("Select Plant", ['All'] + df['plant'].unique().tolist())
        make = st.sidebar.selectbox("Select Make", ['All'] + df['Make'].unique().tolist())
        model = st.sidebar.selectbox("Select Model", ['All'] + df['model'].unique().tolist())
        gas_type = st.sidebar.selectbox("Select Gas Type", ['All'] + df['gas type'].unique().tolist())

        date_label = "procurement_date" if st.session_state.track_option == 'sensor_procurement' else "sensor replacement"
        date_range = st.sidebar.date_input(f"Select {date_label} Range", [])

        st.sidebar.header("Help")
        st.sidebar.info("""
        **How to Use This App:**
        1. Upload your Excel file.
        2. Use the filters to narrow down your data.
        3. View and download the filtered data.
        """)

        filtered_df = df.copy()
        if plant != 'All':
            filtered_df = filtered_df[filtered_df['plant'] == plant]
        if make != 'All':
            filtered_df = filtered_df[filtered_df['Make'] == make]
        if model != 'All':
            filtered_df = filtered_df[filtered_df['model'] == model]
        if gas_type != 'All':
            filtered_df = filtered_df[filtered_df['gas type'] == gas_type]

        if date_range:
            start_date, end_date = date_range
            if len(date_range) == 2:
                filtered_df = filtered_df[(filtered_df[date_label] >= pd.Timestamp(start_date)) & (filtered_df[date_label] <= pd.Timestamp(end_date))]
                st.write(f"### Total Entries: {filtered_df.shape[0]}")
                if st.checkbox("Show Filtered Data"):
                    st.dataframe(filtered_df)
        else:
            st.write("No entries found for the selected filters.")


        def convert_df_to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')

            # Convert date columns to string with only date part
            date_columns = ['sensor replacement','Sensor Expiry Date', 'procurement_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = df[col].dt.strftime('%Y-%m-%d')

            df.to_excel(writer, index=False, sheet_name='Sheet1')

            # Get the workbook and worksheet objects
            workbook  = writer.book
            worksheet = writer.sheets['Sheet1']

            # Create a format for center alignment
            center_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

            # Set the column width and apply the center alignment
            for column in df:
                column_width = max(df[column].astype(str).map(len).max(), len(column)) + 2  # Adding some extra space
                col_idx = df.columns.get_loc(column)
                worksheet.set_column(col_idx, col_idx, column_width, center_format)

            writer.close()
            processed_data = output.getvalue()
            return processed_data

        def convert_df_to_pdf(df):
            # Convert date columns to string with only date part
            date_columns = ['Sensor Expiry Date', 'procurement_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')

            # Format datetime columns to string with only date part
            for col in date_columns:
                if col in df.columns:
                    df[col] = df[col].dt.strftime('%Y-%m-%d')

            # Generate HTML for PDF
            html = f"""
            <html>
            <head>
                <style>
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                    th, td {{
                        border: 1px solid black;
                        padding: 5px;
                        text-align: left;
                        word-wrap: break-word;
                    }}
                    th {{
                        background-color: #f2f2f2;
                        text-align: center;
                    }}
                    td:nth-child({df.columns.get_loc('Sensor Expiry Date') + 1}) {{
                        min-width: 100px; /* Adjust the width as needed */
                    }}
                </style>
            </head>
            <body>
                <h1 style="text-align: center;">ProcureTrack Report</h1>
                {df.to_html(index=False)}
            </body>
            </html>
            """
            path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

            pdf = pdfkit.from_string(html, False, configuration=config)
            return pdf

        st.sidebar.header("Download Options")
        if st.sidebar.button("Download Excel"):
            excel_data = convert_df_to_excel(filtered_df)
            st.download_button(label="Download Excel file", data=excel_data, file_name='filtered_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        if st.sidebar.button("Download PDF"):
            pdf_data = convert_df_to_pdf(filtered_df)
            st.download_button(label="Download PDF file", data=pdf_data, file_name='filtered_data.pdf', mime='application/pdf')

if __name__ == "__main__":
    if st.session_state.page == 'login':
        login()
    elif st.session_state.page == 'selection':
        selection_page()
    elif st.session_state.page == 'main':
        main()
    elif st.session_state.page == 'change_password':
        change_password()
    elif st.session_state.page == 'forgot_password':
        forgot_password()
