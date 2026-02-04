import sys
import json
import array
import random
import asyncio
from pathlib import Path
import bittensor as bt
from typing import Any
from hashlib import blake2b
from scalecodec import ScaleBytes
from bittensor.core.async_subtensor import AsyncSubtensor
from async_substrate_interface import AsyncSubstrateInterface

class SyncPeers:
    def __init__(self):
        self.peer_list = []
        self.subtensor = None
        self.substrate = None
        self.block_hash_current = None
        self.current_block = 0

    async def init_param(self):
        print("SyncPeers init_param")
        peer_list_path = Path("peer_list.json")
        if not peer_list_path.is_file():
            peer_list_path = Path(__file__).resolve().parent / "peer_list.json"
        try:
            with peer_list_path.open("r", encoding="utf-8") as peer_file:
                self.peer_list = json.load(peer_file)
        except FileNotFoundError:
            print(f"peer_list.json not found at {peer_list_path}")
            self.peer_list = []
        except json.JSONDecodeError as error:
            print(f"Failed to parse peer_list.json: {error}")
            self.peer_list = []

        self.subtensor = AsyncSubtensor("ws://127.0.0.1:9904")
        self.substrate = self.subtensor.substrate

    async def sync(self):
        reserved_peers = await self.get_reserved_peers()
        if reserved_peers:
            self.peer_list = [
                peer_info
                for peer_info in self.peer_list
                if peer_info.get("peer_id") not in reserved_peers
            ]
            print(f"Reserved Peers: {reserved_peers}")
            print(f"Peer List to add: {self.peer_list}")
        for peer_info in self.peer_list:
            peer_str = ""
            if peer_info["ip"] != "":
                peer_str = f"/ip4/{peer_info["ip"]}/tcp/30333/ws/p2p/{peer_info["peer_id"]}"
            else:
                peer_str = f"/dns/{peer_info["dns"]}/tcp/30333/ws/p2p/{peer_info["peer_id"]}"
            await self.add_reserved_peer(peer_str)

    
    async def add_reserved_peer(self, peer):
        print(f"Add Reserved Peer: {peer}")
        current_block = await self.subtensor.get_current_block()
        block_hash_current = await self.substrate.get_block_hash( block_id=current_block )
        try:
            response = ""
            try :
                response = await self.rpc_request(self.substrate, "system_addReservedPeer", [peer], block_hash_current)
                print(response)
            except Exception as e:
                print(f"Add Reserved Peer error: {e}")         
        except Exception as e:
            print(f"Add Reserved Peer error: {e}")


    async def get_reserved_peers(self):
        current_block = await self.subtensor.get_current_block()
        block_hash_current = await self.substrate.get_block_hash( block_id=current_block )
        try:
            response = ""
            try :
                response = await self.rpc_request(self.substrate, "system_reservedPeers", [], block_hash_current)
                if "result" in response:
                    return response["result"]
            except Exception as e:
                print(f"Get Peer error: {e}")
                return []            
        except Exception as e:
            print(f"Get Peer error: {e}")
        
        return []

    async def rpc_request(
        self,
        substrate,
        method: str,
        params,
        block_hash
    ) -> Any:
        payload_id = f"000000{random.randint(0, 7000)}"
        payloads = [
            substrate.make_payload(
                payload_id,
                method,
                params + [block_hash],
            )
        ]
        result = await substrate._make_rpc_request(payloads)
        if "error" in result[payload_id][0]:
            print("result: ", result)
            return []
        if "result" in result[payload_id][0]:
            return result[payload_id][0]
        else:
            print("result: ", result)
            return []


async def main():
    peer = SyncPeers()
    await peer.init_param()
    await asyncio.gather(peer.sync())

if __name__ == "__main__":
    asyncio.run(main())