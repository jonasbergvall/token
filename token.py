import streamlit as st
from streamlit.components.v1 import html
from web3 import Web3

# PulseChain RPC Endpoint
pulsechain_rpc = "https://rpc.pulsechain.com"
web3 = Web3(Web3.HTTPProvider(pulsechain_rpc))

# Token contract details
token_contract_address = "0xA55385633FFFab595E21880Ed7323cFD7D11Cd25"  # TEED Contract Address
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

# Check RPC connection
if web3.is_connected():
    st.success("Connected to PulseChain")
else:
    st.error("Failed to connect to PulseChain")

st.markdown("""
    <h1>MetaMask Authentication</h1>
    <button id="connectButton" style="padding: 10px 20px; background-color: #1f1f1f; color: white; border: none; border-radius: 5px; cursor: pointer;">
        Connect MetaMask
    </button>
    <script>
        async function connectMetaMask() {
            if (typeof window.ethereum !== 'undefined') {
                try {
                    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                    const publicKey = accounts[0];

                    // Redirect to Streamlit app with the public key
                    const baseUrl = window.location.origin;
                    const queryParams = new URLSearchParams({ public_key: publicKey });
                    window.location.href = `${baseUrl}?${queryParams.toString()}`;
                } catch (error) {
                    alert("Error connecting to MetaMask: " + error.message);
                }
            } else {
                alert("MetaMask is not installed. Please install MetaMask to proceed.");
            }
        }

        document.getElementById('connectButton').addEventListener('click', connectMetaMask);
    </script>
""", unsafe_allow_html=True)


# Extract wallet address from query parameters
query_params = st.query_params
wallet_address = query_params.get("public_key")

# Ensure the wallet_address is properly extracted
if isinstance(wallet_address, list):  # Handle list case
    wallet_address = wallet_address[0]

# Debugging
st.write(f"Raw Query Parameters: {query_params}")
st.write(f"Extracted Wallet Address: {wallet_address}")

# Validate wallet address
if wallet_address and wallet_address.startswith("0x") and len(wallet_address) == 42:
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
