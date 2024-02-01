# Decoding Chip Assignment App

This Streamlit app streamlines the process of assigning decoding chips to specific decoders.

Key Features:

User-friendly interface for selecting run types, chips, and decoders.
Integrates with Slack to send direct messages to assigned decoders with detailed run information.
Queries ...DB to retrieve loaded chips for a given library subset, ensuring accurate data.
Prevents over-assignment of chips by dynamically adjusting dropdown options.
Dependencies:

Streamlit
JSON
Requests
...DB (for database access)
Installation:

Install required libraries: pip install streamlit json requests ...-core
Set up a Slack webhook URL and update the WEBHOOK_URL variable accordingly.
Customize the DECODERS dictionary with the names and Slack member IDs of your decoders.
Usage:

Run the app: streamlit run app.py
Follow the prompts in the app to select run type, library, chips, and decoder.
Click "Send to #chip-assignments!" to dispatch the assignment via Slack.
Additional Notes:

The app generates dummy chips to guide user selection and prevent over-assignment.
Refresh the page after each assignment to ensure accurate dropdown options.
