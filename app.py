import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Omni User Bulk Delete Tool",
    page_icon="🗑️",
    layout="wide"
)

# Title and description
st.title("Omni User Bulk Delete Tool")
st.markdown("""
This tool allows you to bulk delete embed users from your Omni instance.
Please provide your API token and upload a CSV file containing user IDs.
""")

# Sidebar for API configuration
with st.sidebar:
    st.header("Configuration")
    api_token = st.text_input("API Token", type="password", help="Enter your Omni API token")
    org_domain = st.text_input("Organization Domain", help="Enter your Omni organization domain (e.g., myorg.omniapp.co)")

# Main content
uploaded_file = st.file_uploader("Upload CSV file with user IDs", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())
        
        # Validate that the CSV has the required column
        required_column = "user_id"
        if required_column not in df.columns:
            st.error(f"CSV must contain a '{required_column}' column!")
        else:
            if st.button("Start Deletion Process", type="primary"):
                if not api_token or not org_domain:
                    st.error("Please provide both API token and organization domain in the sidebar!")
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Process each user ID
                    total_users = len(df)
                    success_count = 0
                    failed_users = []
                    
                    for index, row in df.iterrows():
                        user_id = str(row[required_column]).strip()
                        status_text.text(f"Processing user ID: {user_id}")
                        
                        try:
                            # Make DELETE request to Omni API
                            response = requests.delete(
                                f"https://{org_domain}/api/scim/v2/embed/users/{user_id}",
                                headers={
                                    "Content-Type": "application/json",
                                    "Authorization": f"Bearer {api_token}"
                                }
                            )
                            
                            if response.status_code == 204:
                                success_count += 1
                            else:
                                failed_users.append({
                                    "user_id": user_id,
                                    "status_code": response.status_code,
                                    "error": response.text
                                })
                        
                        except Exception as e:
                            failed_users.append({
                                "user_id": user_id,
                                "error": str(e)
                            })
                        
                        progress_bar.progress((index + 1) / total_users)
                    
                    # Display results
                    st.success(f"Successfully deleted {success_count} out of {total_users} users")
                    
                    if failed_users:
                        st.error("Failed to delete some users:")
                        st.dataframe(pd.DataFrame(failed_users))
                        
                        # Option to download failed users report
                        failed_df = pd.DataFrame(failed_users)
                        st.download_button(
                            "Download Failed Users Report",
                            failed_df.to_csv(index=False),
                            "failed_deletions.csv",
                            "text/csv"
                        )
    
    except Exception as e:
        st.error(f"Error processing CSV file: {str(e)}")

# Add usage instructions
with st.expander("Usage Instructions"):
    st.markdown("""
    ### How to use this tool:
    
    1. Enter your Omni API token in the sidebar
    2. Enter your organization domain (e.g., myorg.omniapp.co)
    3. Prepare a CSV file with a column named 'user_id' containing the IDs of users to delete
    4. Upload the CSV file
    5. Review the preview of the data
    6. Click 'Start Deletion Process' to begin
    
    ### CSV Format:
    Your CSV file should have a column named 'user_id' containing the Omni user IDs to be deleted.
    
    Example:
    ```
    user_id
    9e8719d9-276a-4964-9395-a493189a247c
    86b31265-3724-4e6a-ad7a-901aa06af7f3
    ```
    
    ### Note:
    - This operation is irreversible
    - Make sure you have the correct permissions
    - The tool will provide a report of any failed deletions
    """) 