# Metamorphic Contract Detector API

## Instructions

start app: ```uvicorn api.app:app --reload```
http://127.0.0.1:8000/ismetamorphic/0x00000000b7ca7E12DCC72290d1FE47b2EF14c607

## Install

First you will need to install [poetry](https://python-poetry.org/docs/)
```
git clone <insert link>
cd <project dir>
poetry install
```


## Usage

Add the instructions to use the project. If this section gets long, consider making separate usage or example pages.
```
poetry run uvicorn api.app:app --reload
poetry run streamlit run streamlit_app.py
```

## Test Metamorphic Contracts on ETH Mainnet

0x00000000b7ca7E12DCC72290d1FE47b2EF14c607
0x000000009B988FbecFd83C55252f78592E609648
0x1d6E8BAC6EA3730825bde4B005ed7B2B39A2932d
NOT WORK: 0x055658fa70d40a5fa3d0e3e66c29f7e7add08553
NOT Work: 0xF1f640cdFBFa9A5b408c3D53282AD56e1C76FeF6 (identify wrong block deployment)

## Related Work and Credits
- https://github.com/MrLuit/selfdestruct-detect/blob/master/src/index.ts
- https://ethereum-magicians.org/t/potential-security-implications-of-create2-eip-1014/2614
- https://github.com/0age/metamorphic


## Disclaimer
_This code is being provided as is. No guarantee, representation or warranty is being made, express or implied, as to the safety or correctness of the code. It has not been audited and as such there can be no assurance it will work as intended, and users may experience delays, failures, errors, omissions or loss of transmitted information. Nothing in this repo should be construed as investment advice or legal advice for any particular facts or circumstances and is not meant to replace competent counsel. It is strongly advised for you to contact a reputable attorney in your jurisdiction for any questions or concerns with respect thereto. a16z is not liable for any use of the foregoing, and users should proceed with caution and use at their own risk. See a16z.com/disclosure for more info._