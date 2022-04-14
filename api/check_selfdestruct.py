STOP = 0x00
JUMPDEST = 0x5B
PUSH1 = 0x60
PUSH32 = 0x7F
RETURN = 0xF3
REVERT = 0xFD
INVALID = 0xFE
SELFDESTRUCT = 0xFF
HALTING = [STOP, RETURN, REVERT, INVALID, SELFDESTRUCT]

is_halting = lambda opcode: any([opcode == h for h in HALTING])
is_push = lambda opcode: opcode >= PUSH1 and opcode <= PUSH32


def might_selfdestruct(deployed_code: str) -> bool:
    """Check if deployed smart contract code might contain a selfdestruct opcode

    Credit:
        This function is a python implementation of code found here:
        https://github.com/MrLuit/selfdestruct-detect/blob/master/src/index.ts

    Args:
        deployed_code (str): deployed smart contract bytecode in hex

    Returns:
        bool: does the deployed code contain the selfdestruct opcode
    """
    deployment_code_bytes = bytearray.fromhex(deployed_code[2:])

    halted = False
    i = 0

    while i < len(deployment_code_bytes):

        opcode = deployment_code_bytes[i]

        if opcode == SELFDESTRUCT and not halted:
            return True
        elif opcode == JUMPDEST:
            halted = False
        elif is_halting(opcode):
            halted = True
        elif is_push(opcode):
            i += opcode - PUSH1 + 0x02
            continue

        i += 1

    return False
