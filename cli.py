import typer
from web3 import Web3

from metamorphic_detect import analyze_contract

app = typer.Typer()


def color_text(res: bool) -> typer.style:
    if res:
        return typer.style("TRUE", fg=typer.colors.RED, bold=True)
    else:
        return typer.style("FALSE", fg=typer.colors.GREEN, bold=True)


@app.command("inspect-contract")
def inpsect_contract(contract_address: str, api_key: str):

    provider = "https://eth-mainnet.alchemyapi.io/v2/" + api_key

    web3_interface = Web3(Web3.HTTPProvider(provider))

    (
        code_hash_changed,
        contains_metamorphic_init_code,
        contains_selfdestruct,
        contains_delegatecall,
        deployed_by_contract,
        deployer_contains_create2,
    ) = analyze_contract(web3_interface, contract_address)

    typer.echo(f"Code Changed: {color_text(code_hash_changed)}")
    typer.echo(
        f"Contains Metamorphic Init Code: {color_text(contains_metamorphic_init_code)}"
    )
    typer.echo(f"Contains SELFDESTRUCT: {color_text(contains_selfdestruct)}")
    typer.echo(f"Contains DELEGATECALL: {color_text(contains_delegatecall)}")
    typer.echo(f"Deployed by Contract: {color_text(deployed_by_contract)}")
    typer.echo(f"Deployer Contains CREATE2: {color_text(deployer_contains_create2)}")


if __name__ == "__main__":
    app()
