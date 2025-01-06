import streamlit as st
from web3 import Web3

# PulseChain RPC Endpoint
pulsechain_rpc = "https://rpc.pulsechain.com"
web3 = Web3(Web3.HTTPProvider(pulsechain_rpc))

# Token contract details
tokens = {
    "TEED": {
        "address": "0xA55385633FFFab595E21880Ed7323cFD7D11Cd25",
        "name": "TEED",
        "url": "https://drteed.substack.com/p/journal-of-dr-teed",
        "abi": [
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
        ],
    },
    "WUPIUPU": {
        "address": "0x12B3E0d79c5dFda3FfA55D57C9697bD509dBf7B0",
        "name": "WUPIUPU",
        "url": "https://mrlefthouse.pls.fyi/",
        "abi": [
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
        ],
    },
}

# Initialize Streamlit app
st.title("TokenGate App")
st.markdown("Check your wallet for supported tokens.")

# Check RPC connection
if web3.is_connected():
    st.success("Connected to PulseChain")
else:
    st.error("Failed to connect to PulseChain")

# MetaMask connection button
st.markdown(
    """
    <h1>MetaMask Authentication</h1>
    <p>Click the button below to connect your MetaMask wallet:</p>
    <a href="https://bestofworlds.se/web3/" target="_blank">
        <button style="padding: 10px 20px; background-color: #1f1f1f; color: white; border: none; border-radius: 5px; cursor: pointer;">
            Connect MetaMask
        </button>
    </a>
    """,
    unsafe_allow_html=True,
)

# Extract wallet address from query parameters
query_params = st.query_params
wallet_address = query_params.get("public_key")

# Debug: Show query parameters
st.write("Query Params: ", query_params)

# Handle wallet address
if wallet_address:
    wallet_address = wallet_address[0] if isinstance(wallet_address, list) else wallet_address
    st.write(f"Connected Wallet Address: {wallet_address}")

    # Validate wallet address
    if wallet_address.startswith("0x") and len(wallet_address) == 42:
        try:
            # Convert wallet address to checksum
            checksum_address = web3.to_checksum_address(wallet_address)
            st.write(f"Checksum Wallet Address: {checksum_address}")

            # Check each token in the wallet
            for token_name, token_details in tokens.items():
                try:
                    token_contract = web3.eth.contract(
                        address=token_details["address"], abi=token_details["abi"]
                    )
                    raw_balance = token_contract.functions.balanceOf(checksum_address).call()
                    decimals = token_contract.functions.decimals().call()
                    token_symbol = token_contract.functions.symbol().call()

                    # Convert balance to human-readable format
                    balance = raw_balance / (10 ** decimals)

                    st.write(f"Token: {token_symbol}")
                    st.write(f"Balance: {balance} {token_symbol}")
                    st.markdown(f"[Learn more about {token_name}]({token_details['url']})")

                    if balance > 0:
                        st.success(f"The wallet holds {balance} {token_symbol}.")
                    else:
                        st.warning(f"The wallet does not hold any {token_symbol} tokens.")
                except Exception as e:
                    st.error(f"Error fetching balance for {token_name}: {e}")

        except Exception as e:
            st.error(f"Error validating wallet address: {e}")
    else:
        st.warning("Invalid wallet address format.")
else:
    st.warning("Connect your MetaMask wallet to proceed.")
