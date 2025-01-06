import streamlit as st
from web3 import Web3

# PulseChain RPC Endpoint
pulsechain_rpc = "https://rpc.pulsechain.com"
web3 = Web3(Web3.HTTPProvider(pulsechain_rpc))

# Token contract details
token_contract_address = "0xA55385633FFFab595E21880Ed7323cFD7D11Cd25"
token_abi = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
]

# Initialize the token contract
token_contract = web3.eth.contract(address=token_contract_address, abi=token_abi)

# Prompt the user to connect MetaMask
st.markdown(
    """
    <h1>Connect MetaMask</h1>
    <a href="https://bestofworlds.se/web3/" target="_blank" style="padding: 10px 20px; background-color: #1f1f1f; color: white; text-decoration: none; border-radius: 5px;">
        Connect MetaMask
    </a>
    """,
    unsafe_allow_html=True,
)

# Extract wallet address from query parameters
query_params = st.experimental_get_query_params()
wallet_address = query_params.get("wallet_address")

if wallet_address:
    wallet_address = wallet_address[0]  # Handle case where it's a list
    try:
        # Convert wallet address to checksum
        checksum_address = web3.to_checksum_address(wallet_address)
        st.write(f"Checksum Wallet Address: {checksum_address}")

        # Fetch token balance
        raw_balance = token_contract.functions.balanceOf(checksum_address).call()
        decimals = token_contract.functions.decimals().call()
        token_symbol = token_contract.functions.symbol().call()

        # Convert balance to human-readable format
        balance = raw_balance / (10 ** decimals)
        st.write(f"Token: {token_symbol}")
        st.write(f"Balance: {balance} {token_symbol}")

        if balance > 0:
            st.success(f"The wallet holds {balance} {token_symbol}.")
        else:
            st.warning(f"The wallet does not hold any {token_symbol} tokens.")
    except Exception as e:
        st.error(f"Error fetching token balance: {e}")
else:
    st.warning("Please connect MetaMask and refresh the page.")
