STOP = 0x00
JUMPDEST = 0x5B
PUSH1 = 0x60
PUSH32 = 0x7F
RETURN = 0xF3
REVERT = 0xFD
INVALID = 0xFE
SELFDESTRUCT = 0xFF
CREATE2 = 0xF5
DELEGATECALL = 0xF4

HALTING = [STOP, RETURN, REVERT, INVALID, SELFDESTRUCT]

is_halting = lambda opcode: any([opcode == h for h in HALTING])
is_push = lambda opcode: opcode >= PUSH1 and opcode <= PUSH32


def contains_selfdestruct(runtime_code: str) -> bool:
    """Check if the runtime code contains the SELFDESTRUCT opcode"""
    return contains_opcode(runtime_code, SELFDESTRUCT)


def contains_create2(runtime_code: str) -> bool:
    """Check if the runtime code contains the CREATE2 opcode"""
    return contains_opcode(runtime_code, CREATE2)


def contains_delegatecall(runtime_code: str) -> bool:
    """Check if the runtime code contains the DELEGATECALL opcode"""
    return contains_opcode(runtime_code, DELEGATECALL)


def contains_opcode(runtime_code: str, opcode: int) -> bool:
    """Check if the runtime code contains a specific opcode

    Credit:
        This function is a python implementation of code found here:
        https://github.com/MrLuit/selfdestruct-detect/blob/master/src/index.ts

    Args:
        runtime_code (str): deployed smart contract runtime bytecode as a hex string (i.e., "0x...")
        opcode (int): the opcode to search for in the runtime code

    Returns:
        bool: does the runtime code contain the given opcode?
    """
    runtime_code_bytes = bytearray.fromhex(runtime_code[2:])

    halted = False
    i = 0

    while i < len(runtime_code_bytes):

        oc = runtime_code_bytes[i]

        if oc == opcode and not halted:
            return True
        elif oc == JUMPDEST:
            halted = False
        elif is_halting(oc):
            halted = True
        elif is_push(oc):
            i += oc - PUSH1 + 0x02
            continue

        i += 1

    return False
