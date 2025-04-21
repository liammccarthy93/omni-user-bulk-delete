# Omni User Bulk Delete Tool

A Streamlit application for bulk deleting embed users from your Omni instance.

## Features

- Bulk delete Omni embed users using CSV input
- Progress tracking for deletion process
- Error handling and reporting
- Downloadable report for failed deletions
- Secure API token handling

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd omni-user-bulk-delete
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. Prepare a CSV file with a column named 'user_id' containing the Omni user IDs to delete
2. Launch the application
3. Enter your Omni API token and organization domain in the sidebar
4. Upload your CSV file
5. Review the data preview
6. Click "Start Deletion Process"

### CSV Format

Your CSV file should have the following format:

```csv
user_id
9e8719d9-276a-4964-9395-a493189a247c
86b31265-3724-4e6a-ad7a-901aa06af7f3
```

## Security Notes

- API tokens are handled securely and are not stored
- The application runs locally on your machine
- Make sure you have the necessary permissions before using the tool
- Double-check the user IDs before starting the deletion process

## Error Handling

- Failed deletions are tracked and reported
- A downloadable CSV report of failed deletions is provided
- Each error includes the user ID and the specific error message

## Contributing

Feel free to submit issues and enhancement requests! 