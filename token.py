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
    st.success("Connected to PulseChain RPC")
else:
    st.error("Failed to connect to PulseChain RPC")

# Session state to manage wallet address
if "wallet_address" not in st.session_state:
    st.session_state.wallet_address = None

# Extract wallet address from query parameters if not in session state
if st.session_state.wallet_address is None:
    wallet_address = st.query_params.get("public_key")
    if wallet_address:
        wallet_address = wallet_address[0] if isinstance(wallet_address, list) else wallet_address
        if wallet_address.startswith("0x") and len(wallet_address) == 42:
            st.session_state.wallet_address = wallet_address

# Handle MetaMask connection and wallet status
if st.session_state.wallet_address:
    st.success(f"Wallet connected: {st.session_state.wallet_address}")
    # Disconnect button
    if st.button("Disconnect Wallet"):
        st.session_state.wallet_address = None
        st.query_params.clear()  # Clear query parameters
        st.success("Wallet disconnected.")
else:
    st.warning("No wallet connected. Please connect your wallet to proceed.")
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

# Display token details if wallet is connected
if st.session_state.wallet_address:
    wallet_address = st.session_state.wallet_address
    try:
        checksum_address = web3.to_checksum_address(wallet_address)

        detected_tokens = []
        for token_name, token_details in tokens.items():
            try:
                token_contract = web3.eth.contract(
                    address=token_details["address"], abi=token_details["abi"]
                )
                raw_balance = token_contract.functions.balanceOf(checksum_address).call()
                decimals = token_contract.functions.decimals().call()

                # Convert balance to human-readable format
                balance = raw_balance / (10 ** decimals)

                if balance > 0:
                    detected_tokens.append(
                        {"name": token_name, "url": token_details["url"], "balance": balance}
                    )
            except Exception:
                pass  # Ignore token errors to continue checking others

        # Display detected tokens
        if detected_tokens:
            st.success("The wallet holds the following tokens:")
            for token in detected_tokens:
                st.markdown(
                    f"- **{token['name']}**: {token['balance']} [Learn more]({token['url']})"
                )
        else:
            st.warning("The wallet does not hold any supported tokens.")
    except Exception as e:
        st.error(f"Error validating wallet: {e}")
