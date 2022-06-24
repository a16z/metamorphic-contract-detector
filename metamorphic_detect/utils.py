import re


def validate_eth_address(address: str) -> bool:
    """Check that an address is a valid Ethereum address

    Args:
        address (str): Ethereum address

    Returns:
        bool: Is this address a valid Ethereum address
    """
    regex_match = re.match(r"^0x[a-fA-F0-9]{40}$", address)

    if regex_match == None:
        return False
    else:
        return True
