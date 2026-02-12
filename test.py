import os
import logging
import bittensor as bt
from scalecodec import ScaleBytes
from substrateinterface import Keypair
from bittensor.core.async_subtensor import AsyncSubtensor
from dotenv import load_dotenv
from substrateinterface import SubstrateInterface
from async_substrate_interface import AsyncSubstrateInterface
from web3 import Web3


load_dotenv()
logging.basicConfig()
logger = logging.getLogger("MEV_Bot")
logger.setLevel(logging.DEBUG)

MainKeySeed = os.getenv("MAIN_KEY")
MainKeyAddress = os.getenv("MAIN_KEY_ADDRESS")
CortexValidator = os.getenv("Validator")



w3 = Web3(Web3.HTTPProvider("https://evm.chain.opentensor.ai:443"))

contract_address = Web3.to_checksum_address("0x0000000000000000000000000000000000000805")

stake_abi = [
    {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "hotkey",
        "type": "bytes32"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "limit_price",
        "type": "uint256"
      },
      {
        "internalType": "bool",
        "name": "allow_partial",
        "type": "bool"
      },
      {
        "internalType": "uint256",
        "name": "netuid",
        "type": "uint256"
      }
    ],
    "name": "addStakeLimit",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  }
]
