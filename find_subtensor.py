import asyncio
import websockets
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Set
import argparse
from substrateinterface import Keypair
from substrateinterface.utils import ss58
from substrateinterface import SubstrateInterface
from bittensor.core.async_subtensor import AsyncSubtensor
from async_substrate_interface.types import RequestManager
from async_substrate_interface import AsyncSubstrateInterface


class SubTensorNodeFinder:
    def __init__(self, base_ip: str = "178.156", port: int = 9944, timeout_ms: int = 10):
        
        self.base_ip = base_ip
        self.port = port
        self.timeout_ms = timeout_ms
        self.timeout_sec = timeout_ms / 1000.0
        self.available_nodes = set()
    
    def generate_ips(self) -> List[str]:
        ips = []
        for third_octet in range(0, 256):  # 0 to 255 for third octet
            for fourth_octet in range(1, 255):  # 1 to 254 for fourth octet (skip .0 and .255)
                ips.append(f"{self.base_ip}.{third_octet}.{fourth_octet}")
        return ips
    
    async def check_websocket_node(self, ip: str) -> bool:
        """Check if WebSocket endpoint is available and responsive"""
        ws_url = f"ws://{ip}:{self.port}"
        
        try:
            start_time = time.time()
            async with websockets.connect(ws_url, timeout=self.timeout_sec) as websocket:
                response_time = (time.time() - start_time) * 1000
                
                if response_time <= self.timeout_ms:
                    # Test with a simple message or ping
                    await websocket.ping()
                    return True
                
        except (websockets.exceptions.WebSocketException, 
                asyncio.TimeoutError, 
                ConnectionRefusedError,
                OSError) as e:
            pass
        
        return False
    
    def check_port_only(self, ip: str) -> bool:
        """Fast port check without WebSocket handshake"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout_sec)
                result = sock.connect_ex((ip, self.port))
                return result == 0
        except:
            return False
    
    async def fast_scan_with_websocket_validation(self):
        """Fast port scan followed by WebSocket validation"""
        ips = self.generate_ips()
        print(f"🔍 Scanning {len(ips)} IPs in range {self.base_ip}.*.*...")
        
        # First, do fast port scanning
        open_ports = set()
        with ThreadPoolExecutor(max_workers=200) as executor:
            futures = {executor.submit(self.check_port_only, ip): ip for ip in ips}
            
            for future in as_completed(futures):
                ip = futures[future]
                try:
                    if future.result():
                        open_ports.add(ip)
                        print(f"📍 Found open port: {ip}:{self.port}")
                except:
                    continue
        
        print(f"\n✅ Found {len(open_ports)} nodes with open ports, validating WebSocket...")
        
        # Then validate WebSocket connection
        tasks = []
        for ip in open_ports:
            task = asyncio.create_task(self.validate_websocket(ip))
            tasks.append(task)
        
        for completed_task in asyncio.as_completed(tasks):
            try:
                ip, is_valid = await completed_task
                if is_valid:
                    self.available_nodes.add(ip)
                    print(f"🎯 Valid WebSocket node: {ip}:{self.port}")
            except:
                continue
    
    async def validate_websocket(self, ip: str) -> tuple:
        """Validate WebSocket connection for a specific IP"""
        try:
            ws_url = f"ws://{ip}:{self.port}"
            if await self.check_substrate(AsyncSubstrateInterface(url=ws_url)) :
            # async with websockets.connect(ws_url, timeout=self.timeout_sec) as websocket:
            #     # Send ping to verify it's actually a WebSocket
            #     await websocket.ping()
                return (ip, True)
            else :
                return (ip, False)
        except:
            return (ip, False)
    
    async def comprehensive_scan(self):
        """Comprehensive scan with detailed results"""
        ips = self.generate_ips()
        print(f"🔍 Comprehensive scan of {len(ips)} IPs...")
        
        tasks = []
        for ip in ips:
            task = asyncio.create_task(self.detailed_node_check(ip))
            tasks.append(task)
        
        results = []
        for completed_task in asyncio.as_completed(tasks):
            try:
                result = await completed_task
                if result['available']:
                    self.available_nodes.add(result['ip'])
                    print(f"✅ {result['ip']}: {result['response_time']:.2f}ms")
                results.append(result)
            except:
                continue
        
        return results
    
    async def detailed_node_check(self, ip: str) -> Dict:
        """Detailed check with response time measurement"""
        ws_url = f"ws://{ip}:{self.port}"
        
        try:
            start_time = time.time()
            async with websockets.connect(ws_url, timeout=self.timeout_sec) as websocket:
                connect_time = (time.time() - start_time) * 1000
                
                # Test ping response
                ping_start = time.time()
                await websocket.ping()
                ping_time = (time.time() - ping_start) * 1000
                
                total_time = max(connect_time, ping_time)
                
                return {
                    'ip': ip,
                    'available': total_time <= self.timeout_ms,
                    'response_time': total_time,
                    'connect_time': connect_time,
                    'ping_time': ping_time
                }
                
        except Exception as e:
            return {
                'ip': ip,
                'available': False,
                'response_time': float('inf'),
                'error': str(e)
            }
    
    def get_available_nodes(self) -> List[str]:
        """Get sorted list of available nodes"""
        return sorted(self.available_nodes)
    
    def save_results(self, filename: str = "subtensor_nodes.txt"):
        """Save results to file"""
        with open(filename, 'w') as f:
            f.write(f"SubTensor Nodes found at {time.ctime()}\n")
            f.write("=" * 50 + "\n")
            for node in self.get_available_nodes():
                f.write(f"ws://{node}:{self.port}\n")
        
        print(f"📁 Results saved to {filename}")

    async def check_substrate(self, substrate) :
        try :
            await asyncio.wait_for(substrate.rpc_request("author_pendingExtrinsics", []), timeout=1)
            return True
        except Exception as e :
            return False

async def main():
    parser = argparse.ArgumentParser(description="Find SubTensor nodes")
    parser.add_argument("--fast", action="store_true", help="Use fast port scanning mode")
    parser.add_argument("--detailed", action="store_true", help="Use detailed scanning mode")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout in milliseconds (default: 10)")
    
    args = parser.parse_args()

    my_ip_list = [
        "178.156.208.139",
    ]
    
    print("🌐 SubTensor Node Finder")
    print("=" * 50)
    
    finder = SubTensorNodeFinder(
        base_ip="178.156",
        port=9944,
        timeout_ms=args.timeout
    )
    
    start_time = time.time()
    
    if args.fast:
        print("🚀 Using fast scanning mode...")
        await finder.fast_scan_with_websocket_validation()
    elif args.detailed:
        print("📊 Using detailed scanning mode...")
        await finder.comprehensive_scan()
    else:
        print("⚡ Using default fast scanning mode...")
        await finder.fast_scan_with_websocket_validation()
    
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 50)
    print("📋 SCAN RESULTS:")
    print("=" * 50)
    
    available_nodes = finder.get_available_nodes()
    
    if available_nodes:
        print(f"✅ Found {len(available_nodes)} available SubTensor nodes:")
        for node in available_nodes:
            if node not in my_ip_list:
                print(f'"{node}",')
    else:
        print("❌ No available SubTensor nodes found")
    
    print(f"⏰ Scan completed in {elapsed_time:.2f} seconds")
    
    if available_nodes:
        print(f"✅ Found {len(available_nodes)} available SubTensor nodes:")
        for node in available_nodes:
            if node not in my_ip_list:
                print(f'"{node}",')
    # Save results to file
    if available_nodes:
        finder.save_results()

if __name__ == "__main__":
    # Install required package: pip install websockets
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Scan interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")