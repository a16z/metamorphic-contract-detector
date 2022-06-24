import os

import streamlit as st
from dotenv import load_dotenv
from web3 import Web3

from metamorphic_detect import analyze_contract
from streamlit_text import (
    BYTECODE_BREAKDOWN,
    CREATE2_DRODOWN_ONE,
    CREATE2_DROPDOWN_TWO,
    DETECTING_METAMORPHIC_CONTRACTS_DROPDOWN,
    INTRO,
    MALICIOUS_EXAMPLE_DROPDOWN,
    NEXT_STEPS,
    STEP_BY_STEP_WALKTHROUGH_DROPDOWN_ONE,
    STEP_BY_STEP_WALKTHROUGH_DROPDOWN_TWO,
    STEP_BY_STEP_WALKTHROUGH_DROPDOWN_THREE,
)

load_dotenv()


provider = "https://eth-mainnet.alchemyapi.io/v2/" + os.environ.get("ALCHEMY_API_KEY")
web3_interface = Web3(Web3.HTTPProvider(provider))


st.title("Metamorphic Contract Detector")

st.caption("Enter a smart contract address to analyze.")

contract_address = st.text_input(
    label="Contract Address", value="0x00000000008c9782FF4EB38e9293eE3DFA75FA9e"
)

col1, col2 = st.columns(2)
try:
    (
        code_hash_changed,
        contains_metamorphic_init_code,
        contains_selfdestruct,
        contains_delegatecall,
        deployed_by_contract,
        deployer_contains_create2,
    ) = analyze_contract(web3_interface, contract_address)

    col1.metric("Code Has Changed", "YES" if code_hash_changed else "NO")
    col2.metric(
        "Contains Metamorphic Init Code",
        "YES" if contains_metamorphic_init_code else "NO",
    )
    col1.metric("Contains SELFDESTRUCT", "YES" if contains_selfdestruct else "NO")
    col2.metric("Contains DELEGATECALL", "YES" if contains_delegatecall else "NO")
    col1.metric("Created by Contract", "YES" if deployed_by_contract else "NO")
    col2.metric(
        "Deployer Contains CREATE2", "YES" if deployer_contains_create2 else "NO"
    )
except:
    col1.metric("Code Has Changed", "Invalid Address")
    col2.metric("Contains Metamorphic Init Code", "Invalid Address")
    col1.metric("Contains SELFDESTRUCT", "Invalid Address")
    col2.metric("Contains DELEGATECALL", "Invalid Address")
    col1.metric("Created by Contract", "Invalid Address")
    col2.metric("Deployer Contains CREATE2", "Invalid Address")


st.markdown("***")

st.markdown(INTRO)


with st.expander("Detecting metamorphic smart contracts"):
    st.markdown(DETECTING_METAMORPHIC_CONTRACTS_DROPDOWN)


with st.expander(
    "How a malicious actor can use metamorphic contracts to steal people’s funds"
):
    st.markdown(MALICIOUS_EXAMPLE_DROPDOWN)


with st.expander("How CREATE2 opens up the possibility of metamorphism "):
    st.markdown(CREATE2_DRODOWN_ONE)
    st.image("./images/create2.png")
    st.markdown(CREATE2_DROPDOWN_TWO)


with st.expander("How a metamorphic contract actually works"):
    st.markdown(STEP_BY_STEP_WALKTHROUGH_DROPDOWN_ONE)
    st.image("./images/anatomy.jpg")
    st.markdown(STEP_BY_STEP_WALKTHROUGH_DROPDOWN_TWO)
    st.image("./images/bytecode.png")
    st.markdown(STEP_BY_STEP_WALKTHROUGH_DROPDOWN_THREE)

with st.expander("Next steps"):
    st.markdown(NEXT_STEPS)

with st.expander("Metamorphic init code breakdown"):
    st.markdown(BYTECODE_BREAKDOWN)

st.markdown("Created By [Michael Blau](https://twitter.com/blauyourmind)")
