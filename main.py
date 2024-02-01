import streamlit as st
import json
import requests

from ..._core.db import library

WEBHOOK_URL = (
    ...
)
# dict with decoders name and slack member id
DECODERS = {
    "None": "",
    "...": "...",
    "...": "...",
    "...": "...",
    "...": "...",
    "...": "...",
}


# function to send slack dm to decoders
def slack_dm(assign_to, text):

    # Send a message to the channel
    response = requests.post(
        WEBHOOK_URL,
        json.dumps(
            {
                "text": f'<@{DECODERS[assign_to]}> has been assigned {text["Run type"]}(s)!\n\nLibrary: {text["Library"]}\n\nIf the decoder is not present please reassign the run(s).'
            }
        ),
    )

    # loop through "Runs" dict and send formatted message
    for run, chips in text["Runs"].items():
        response = requests.post(WEBHOOK_URL, json.dumps({"text": f"{run}: {chips}"}))


# function to query into ...db for loaded chips given a provided subset
def generate_chip_list(subset):

    # datajoint with loaded chips + library subset specified by subset param
    chips = (
        (library.LoadedChips * library.LibrarySubsets & {"subset_name": subset})
        .fetch(format="frame")
        .reset_index()
    )

    # return chip_name column as a list to use in streamlit dropdown
    return chips["chip_name"].tolist()


def main():

    # empty dict for selected chips/run
    assigned_runs = {
        "Runs": {},
    }

    st.header("Decoding Chip Assignment")

    # select new run or rehyb
    new_or_rehyb = st.selectbox(
        "Are you assigning or new run or rehyb?: ",
        ["None", "New run", "Rehyb"],
        index=0,
    )
    assigned_runs["Run type"] = new_or_rehyb

    # number input for amount of "runs" to assign
    num_flow_cells = st.number_input(
        "How many 12 chippers would you like to assign?: ", min_value=1, step=1
    )

    # subset specification for generate_chip_list function
    subset = st.text_input("Please specify a library ('TSM-0XXX'): ").upper()
    st.write(subset)
    assigned_runs["Library"] = subset
    chip_list = generate_chip_list(subset=subset)

    # for loop to create dropdowns based on num_flow_cell input
    for i in range(num_flow_cells):
        # insert dummy chips at top of list
        chip_list.insert(0, "Dummy chip")
        chip_list.insert(1, "Dummy chip")
        # adding selections into assigned_runs["Runs"] dict
        assigned_runs["Runs"][f"Run {i + 1}"] = st.multiselect(
            "Choose up to 12 chips to assign: ", chip_list, key=i
        )
        chip_list = [
            option
            for option in chip_list
            if option not in assigned_runs["Runs"][f"Run {i + 1}"]
        ]

    # dropdown to select what decoder to send slack message to
    assign_to = st.selectbox(
        "Choose the decoder you wish to assign these runs to: ", DECODERS, index=0
    )
    assigned_runs["Decoder"] = assign_to

    # displaying decoder selection and chips that will be assigned
    st.write("You've chosen: ", assign_to)
    st.write("Chips selected: ", assigned_runs)

    # if not none show button
    if assign_to != "None":
        # if button pushed call slack_dm()
        if st.button("Send to #chip-assignments!"):
            slack_dm(assign_to, assigned_runs)
            st.write("Please refresh the page before assigning something new.")
            st.balloons()
