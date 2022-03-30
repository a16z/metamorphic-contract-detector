import os
import re
import streamlit as st
from web3 import Web3
from api.utils import analyze_contract
from dotenv import load_dotenv
load_dotenv()

st.title("Metamorphic Smart Contract Check")
st.caption("Check if a contract is a Metamorphic Smart Contract.")
st.caption("For example, 0x0000000000b92ac90d898eBa87fa5f2483f32234 is a Metamorphic Smart Contract")

RPC_ENDPOINT = os.environ.get('RPC_ENDPOINT')
web3_interface = Web3(Web3.HTTPProvider(RPC_ENDPOINT))

# metamorphic contract address
contract_address = st.text_input(label='Contract Address', value='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')

regex_match = re.match(r"^0x[a-fA-F0-9]{40}$", contract_address)

if regex_match == None:
    raise Exception("Invalid Ethereum Address")

contract_address = web3_interface.toChecksumAddress(contract_address)
code_hash_changed, is_metamorphic, contains_selfdestruct = analyze_contract(web3_interface, contract_address)

st.subheader(f"Code changed since deployment: {code_hash_changed}")
st.subheader(f"Is Metamorphic: {is_metamorphic}")
st.subheader(f"Contains SELFDESTRUCT: {contains_selfdestruct}")


st.subheader("EDUCATIONAL MATERIAL")

# if contains_selfdestruct:
#     st.subheader(f"{contract_address[:5]}...{contract_address[-3:]} might contain the SELFDESTRUCT opcode.")
# else:
#     st.subheader(f"{contract_address[:5]}...{contract_address[-3:]} does NOT contain the SELFDESTRUCT opcode.") 