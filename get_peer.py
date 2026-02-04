import sys
import json
import array
import random
import asyncio
import bittensor as bt
from typing import Any
from hashlib import blake2b
from scalecodec import ScaleBytes
from bittensor.core.async_subtensor import AsyncSubtensor
from async_substrate_interface import AsyncSubstrateInterface

class GetPeer:

    def __init__(self) :
        self.subtensor = None
        self.substrate = None
        self.block_hash_current = None
        self.current_block = 0

    async def init_param(self) :
        self.subtensor = AsyncSubtensor("wss://hz-lite3.chain.opentensor.ai:443")
        self.ip_list = [
            "5.161.103.8",
            "5.161.104.26",
            "5.161.111.253",
            "5.161.123.249",
            "5.161.188.170",
            "5.161.201.173",
            "5.161.202.80",
            "5.161.219.244",
            "5.161.242.141",
            "5.161.48.152",
            "5.161.68.94",
            "178.156.138.74",
            "178.156.191.64",
            "178.156.195.49",
            "178.156.211.171",
            "178.156.228.185",
            "178.156.233.253",
        ]

        self.subtensor_list = [
        ]
        
        for ip in self.ip_list:
            self.subtensor_list.append({
                "ip": ip,
                "dns": "",
                "node": AsyncSubtensor(f"ws://{ip}:9944"),
                "peer_id": ""
            })
        base_url = "wss://hz-lite{}.chain.opentensor.ai:443"
        for i in range (1, 21) :
            if i != 15 :
                self.subtensor_list.append({
                    "ip": "",
                    "dns": base_url.format(i),
                    "node": AsyncSubtensor(base_url.format(i)),
                    "peer_id": ""
                })
        
        self.substrate = self.subtensor.substrate
    
    async def get_peer_list(self) :
        for subtensor_info in self.subtensor_list:
            subtensor = subtensor_info["node"]
            substrate = subtensor_info["node"].substrate
            current_block = await subtensor.get_current_block()
            block_hash_current = await substrate.get_block_hash( block_id=current_block )
            try:
                response = ""
                try :
                    response = await self.rpc_request(substrate, "system_localPeerId", [], block_hash_current)
                except Exception as e:
                    print(f"Get Peer error: {e}")
                    continue
            except Exception as e:
                print(f"Get Peer error: {e}")
                continue
            if "result" in response :
                subtensor_info["peer_id"] = response["result"]

        for subtensor_info in self.subtensor_list:
            print("{\n",
                '    "ip":'+ f'"{subtensor_info["ip"]}"'+",\n",
                '    "dns":'+ f'"{subtensor_info["dns"]}"'+",\n",
                '    "peer_id":'+ f'"{subtensor_info["peer_id"]}"'+"\n",
            "},")
        


    async def get_peer(self) :
        self.current_block = await self.subtensor.get_current_block()
        self.block_hash_current = await self.substrate.get_block_hash( block_id=self.current_block )
        print(self.block_hash_current)
        print(self.current_block)
        try:
            response = ""
            try :
                response = await self.rpc_request(self.substrate, "system_localPeerId", [], self.block_hash_current)
            except Exception as e:
                print(f"Get Peer error: {e}")
                pass
            print(response)
        except Exception as e:
            print(f"Get Peer error: {e}")

        try:
            response = ""
            try :
                response = await self.rpc_request(self.substrate, "system_reservedPeers", [], self.block_hash_current)
            except Exception as e:
                print(f"Get Peer error: {e}")
                pass
            print(response)
        except Exception as e:
            print(f"Get Peer error: {e}")


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
    peer = GetPeer()
    await peer.init_param()
    await asyncio.gather(peer.get_peer_list())

if __name__ == "__main__":
    asyncio.run(main())