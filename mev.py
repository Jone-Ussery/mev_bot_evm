
import os
import sys
import time
import json
import array
import random
import logging
import asyncio
import xxhash
import hashlib
import bittensor as bt
from scalecodec import ScaleBytes
from substrateinterface import Keypair
from bittensor.core.async_subtensor import AsyncSubtensor
from dotenv import load_dotenv
from substrateinterface import SubstrateInterface
from async_substrate_interface import AsyncSubstrateInterface

load_dotenv()
logging.basicConfig()
logger = logging.getLogger("MEV_Bot")
logger.setLevel(logging.DEBUG)

MainKeySeed = os.getenv("MAIN_KEY")
MainKeyAddress = os.getenv("MAIN_KEY_ADDRESS")
CortexValidator = os.getenv("Validator")

SUBNTET_LIMIT = 129

STAKE_LIMIT = 99
STAKE_LIMIT2 = 27
STAKE_LIMIT3 = 10

TAO_INT = 1000000000
TAO_FLOAT = 1000000000.0

class MevBot:
    def __init__(self):
        self.monit_select = 3
        self.server_finney: list[AsyncSubstrateInterface] = []
        self.server_local: list[AsyncSubstrateInterface] = []
        self.server_private:AsyncSubstrateInterface = None
        self.subtensor_for_block: list[AsyncSubtensor] = []
        self.subtensor_for_submit: list[AsyncSubstrateInterface] = []
        self.subtensor:AsyncSubtensor = None
        self.substrate:SubstrateInterface = None
        self.substrate0:SubstrateInterface = None
        self.main_wallet: Keypair = None
        self.main_wallet_address: str = None
        self.main_wallet_id = None
        self.main_wallet_nonce = 0
        self.main_wallet_balance = 0
        self.next_hash = 0
        self.removed_balance = []
        self.lst_last_block =[]
        self.lst_price = []
        self.tao_in = []
        self.alpha_in = []
        self.owner_coldkeys = []
        self.list_chk_ext = array.array('b', [0]) * 1048576
        self.list_chk_acc = array.array('b', [0]) * 256
        self.Block_Staked = 0
        self.max_balance = 0
        self.last_netuid = 0
        self.last_block = 0
        self.never_stake = False
        self.staked_flg = False
        self.unstaked_flg = False
        self.unstaked_all_alpha = False
        self.block_hashs = []
        self.result_extrinsic = []
        self.result_extrinsic2 = []
        self.limit_stakings = []
        self.staking_dic = {
            "5C9xyz" : [],
        }
        
        self.unstake_extrinsic = None
        self.cancel_extrinsic = None
        self.swap_extrinsic = None
        self.block_hash_current =None
        self.last_block_time = -10000000000
        self.start_time = 0
        self.finalized_block = 0
        self.current_block = 0
        self.current_block_init = 0
        self.current_block_count = 5
        self.unstake_all_alpha_flg = False
        self.block_initializing = False
        self.extrinsic_processing = False
        self.lock = asyncio.Lock()
        
        self.log_file_path = "ban_list.json"
        self.log_ban_path = "ban_netuid.json"
        self.log_new_account_path = "new_accounts.json"
        self.log_bots_path = "bots.json"
        self.log_danger_path = "danger.json"
        self.log_danger_path2 = "danger2.json"
        self.log_pending_account_path = "pending.json"
        self.ban = []
        self.new_accounts = []
        self.bot_accounts = []
        self.danger_accounts = []
        self.danger_accounts2 = []
        self.danger_accounts_current = []
        self.pending_accounts = []
        self.lst_pending_accounts = array.array('b', [0]) * 1048576
        self.lst_danger_accounts = array.array('b', [0]) * 1048576
        self.lst_danger_accounts2 = array.array('b', [0]) * 1048576
        self.lst_ban_accounts = array.array('b', [0]) * 1048576
        self.lst_new_accounts = array.array('b', [0]) * 1048576
        self.lst_era4 = []
        self.lst_last_era4 = []
    
    async def check_substrate(self, substrate) :
        try :
            await asyncio.wait_for(substrate.rpc_request("author_pendingExtrinsics", []), timeout=1)
            subtensor = AsyncSubtensor(substrate.url)
            block = await subtensor.get_current_block()
            if block > 7000000 and block < 9000000 :
                return True
            return False
        except Exception as e :
            return False

    async def check_block(self):
        try:
            async def block_handler(block_header, subtensor: AsyncSubtensor):
                current_time = time.perf_counter()
                if current_time > self.last_block_time + 4:
                    first_block = False
                    if self.last_block_time < 0:
                        first_block = True
                    self.last_block_time = current_time
                    if not first_block:
                        self.subtensor = subtensor
                        self.substrate = subtensor.substrate
                        self.substrate0 = SubstrateInterface(url = self.substrate.url)
                        await self.init_block()

            async def process_handler(subtensor: AsyncSubtensor):
                future = asyncio.Future()
                try :
                    handler = lambda bh, sub=subtensor: block_handler(bh, sub)
                    await subtensor.substrate.subscribe_block_headers(handler)
                except Exception as e:
                    await future

            subscription_tasks = []
            for subtensor in self.subtensor_for_block:
                subscription_tasks.append(process_handler(subtensor))
                if len(subscription_tasks) > 2 :
                    break

            await asyncio.gather(*subscription_tasks)

        except Exception as e:
            print(f"Subscription error: {e}")
            sys.exit(1)
        finally:
            for subtensor in self.subtensor_for_block:
                await subtensor.substrate.close()


    async def init_param(self):
        # Initialization logic here
        logger.debug("MEV Bot parameters initialized.")
        
        start_time = time.perf_counter()
        self.start_time = start_time
        
        self.server_private = AsyncSubstrateInterface(url="wss://private.chain.opentensor.ai:443", use_remote_preset=True,)
        self.server_local = AsyncSubstrateInterface(url="ws://127.0.0.1:9944", use_remote_preset=True,)
        base_url = "wss://hz-lite{}.chain.opentensor.ai:443"
        for i in range (1, 21) :
            if i != 15 :
                self.server_finney.append(AsyncSubstrateInterface(url=base_url.format(i), use_remote_preset=True,))
        
        remote_preset = True
        good_substrates = [
            AsyncSubstrateInterface(url = "ws://5.161.242.141:9944", use_remote_preset=remote_preset,),
            AsyncSubstrateInterface(url = "ws://5.161.111.253:9944", use_remote_preset=remote_preset,),
            AsyncSubstrateInterface(url = "ws://178.156.195.49:9944", use_remote_preset=remote_preset,),
        ]
        fast_substrates = [
            AsyncSubstrateInterface(url = "ws://5.161.201.173:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://5.161.80.201:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://178.156.155.134:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://5.161.61.18:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://178.156.196.61:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://5.161.142.128:9944", use_remote_preset=remote_preset,),
            AsyncSubstrateInterface(url = "ws://5.161.202.80:9944", use_remote_preset=remote_preset,),
            AsyncSubstrateInterface(url = "ws://5.161.219.244:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://5.161.110.26:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://5.161.135.245:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://5.161.188.96:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://5.161.140.217:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://5.161.232.48:9944", use_remote_preset=remote_preset,),
            AsyncSubstrateInterface(url = "ws://5.161.103.8:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://5.161.48.32:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://178.156.166.13:9944", use_remote_preset=remote_preset,),
            AsyncSubstrateInterface(url = "ws://178.156.138.74:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://178.156.193.197:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://5.161.49.199:9944", use_remote_preset=remote_preset,),
            # AsyncSubstrateInterface(url = "ws://178.156.174.2:9944", use_remote_preset=remote_preset,),
        ]

        for i in range(5) :
            if await self.check_substrate(fast_substrates[i * 2 + self.monit_select]) :
                self.subtensor_for_block.append(AsyncSubtensor(network = fast_substrates[i * 2 + self.monit_select].url))

        good_nodes = []
        for substrate in good_substrates :
            if await self.check_substrate(substrate) :
                good_nodes.append(substrate)
            else :
                print(substrate.url)

        random.seed(self.monit_select * 4)
        self.subtensor_for_submit.append(AsyncSubstrateInterface(url = "ws://5.161.103.8:9944", use_remote_preset=remote_preset,))
        self.subtensor_for_submit = random.sample(good_nodes, 5)
        self.subtensor_for_submit.append(self.server_private)
        self.substrate = self.subtensor_for_submit[0]
        substrate = self.subtensor_for_submit[0]
        
        if await self.check_substrate(self.server_local) :
            print("add local server to submit list")
            if self.monit_select > 0 :
                self.subtensor_for_submit.insert(0, self.server_local)
        
        
        for i in range(SUBNTET_LIMIT) :
            self.lst_last_block.append(0)
            
        await substrate.init_runtime()
        
        # init wallets
        main_wallet_json = json.dumps({
            "encoded":MainKeySeed,
            "encoding":{"content":["pkcs8","sr25519"],"type":["scrypt","xsalsa20-poly1305"],"version":"3"},
            "address": MainKeyAddress,
            "meta":{"genesisHash":"","name":"Proxy","whenCreated":1746590034919}
        })
        self.main_wallet = Keypair.create_from_encrypted_json(main_wallet_json, "jinryong")
        self.main_wallet_address = MainKeyAddress
        self.main_wallet_id = f"0x{self.main_wallet.public_key.hex()}"
        self.meta = substrate.runtime.metadata
        self.genesis_hash = await substrate.get_block_hash(0)
        
        self.base_extrinsic = substrate.runtime_config.create_scale_object(type_string="Extrinsic", metadata=self.meta)
        self.nonce = await substrate.get_account_nonce(self.main_wallet_address)
        
        # init price list
        
        self.current_block = await self.subtensor.get_current_block()
        self.current_block_init = self.current_block
        subnets_ = await self.subtensor.all_subnets()
        tao_in= []
        alpha_in = []
        self.lst_price = []
        for subnet in subnets_ :
            tao_in.append(subnet.tao_in.tao)
            alpha_in.append(subnet.alpha_in.tao)
            if subnet.tao_in.tao > 10 :
                self.lst_price.append(subnet.tao_in.tao / subnet.alpha_in.tao)
            else :
                self.lst_price.append(1.0)
            self.owner_coldkeys.append(subnet.owner_coldkey)
        self.lst_price[0] = 1
        self.tao_in = tao_in
        self.alpha_in = alpha_in
        
        await self.init_block(True)


    async def monit0(self, substrates) :
        sleep_time = 0.1
        while True:
            cnt = 0
            for substrate in substrates :
                cnt += 1
                cur_time = 0
                await self.rpc_request(
                    substrate,
                    "author_pendingExtrinsics",
                    [],
                    self.block_hash_current
                )
                await asyncio.sleep(sleep_time)
                
    async def monit(self, substrates: list[AsyncSubstrateInterface], debug = False) :
        cnt = 0
        select = 0
        self.monit_cnt = 0
        while True:
            if debug :
                cnt += 1
                if cnt % 10000 == 0 :
                    print(cnt, time.perf_counter() - self.start_time)
                    self.monit_cnt += 1
                    if self.monit_cnt == 10 :
                        sys.exit(0)
                    if cnt == 30000 :
                        if self.current_block == self.current_block_init :
                            sys.exit(0)
            current_time = 0
            if debug and cnt % 2000 == 0 :
                current_time = time.perf_counter()
            response = await self.rpc_request(
                substrates[select],
                "author_pendingExtrinsics",
                [],
                self.block_hash_current
            )
            select = 1 - select
            if debug and cnt % 2000 == 0 :
                print(time.perf_counter() - current_time)
            pending_extrinsics = response.get("result", [])
            for extrinsic_data in pending_extrinsics:
                await self.process_extrinsic(extrinsic_data)   
                
                
    async def process_extrinsic(self, extrinsic_data):
        try:
            ext_hash = xxhash.xxh32(extrinsic_data).intdigest() & 0xFFFFF
        except Exception as e:
            print(f"Hash generation failed: {str(e)}")
            return False

        if self.list_chk_ext[ext_hash] :
            return
        self.list_chk_ext[ext_hash] = True
        if self.extrinsic_processing :
            return
        self.extrinsic_processing = True

        ext_len = len(extrinsic_data) // 2
        scale_byte = ScaleBytes(extrinsic_data)
        scale_bytes = scale_byte.data
        contact_add = None
        call_function = ""
        amount_staked = 0
        limit_price = None
        netuid = 0
        pre_calc_flg = False
        # if ext_len < 450 :
        #     if ext_len in (150, 151, 152, 159, 160, 161) :
        #         add_idx = ext_len - 151
        #         if ext_len > 158 :
        #             add_idx = ext_len - 160
        #         if not (add_idx == 1 and int(scale_bytes[104]) < 3 and int(scale_bytes[105]) == 0 and int(scale_bytes[106]) == 0) :
        #             pubkey_bytes = scale_bytes[4:36]
        #             keypair = Keypair(public_key=pubkey_bytes, ss58_format=42)
        #             contact_add = keypair.ss58_address
        #             if scale_bytes[107 + add_idx] == 0x02 :
        #                 call_function = 'add_stake'
        #             elif scale_bytes[107 + add_idx] == 0x03 :
        #                 call_function = 'remove_stake'
        #             elif scale_bytes[107 + add_idx] == 0x58 :
        #                 call_function = 'add_stake_limit'
        #             elif scale_bytes[107 + add_idx] == 0x59 :
        #                 call_function = 'remove_stake_limit'
        #             netuid = int(scale_bytes[140+add_idx])
        #             amount_staked = int.from_bytes(scale_bytes[142+add_idx:150+add_idx], 'little')
        #             if ext_len > 158 :
        #                 limit_price = int.from_bytes(scale_bytes[150+add_idx:158+add_idx], 'little')
        #             add_hash = xxhash.xxh32(contact_add).intdigest() & 0xFFFFF
        #             if self.lst_ban_accounts[add_hash] == 0 and self.lst_new_accounts[add_hash] == 0 and self.lst_mev_bot[add_hash] == 0 :
        #                 if call_function == 'add_stake' or call_function == 'add_stake_limit' :
        #                     await self.process_stake(contact_add, netuid, amount_staked, limit_price, 0, -1, False)
        #             if call_function in ('remove_stake', 'remove_stake_limit') :
        #                 await self.process_remove(contact_add, netuid, amount_staked)
        #     else :
        decoded = self.substrate.runtime_config.create_scale_object(type_string="Extrinsic", metadata=self.meta)
        decoded.decode(scale_byte)
        call = decoded['call']
        call_function = call['call_function']['name']

        if call_function in ('add_stake', 'add_stake_limit', 'proxy', 'swap_stake', 'swap_stake_limit', 'move_stake', 'remove_stake', 'remove_stake_limit', 'unstake_all', 'unstake_all_alpha', 'batch_all', 'batch', 'force_batch', 'transfer_allow_death', 'transfer_keep_alive', 'transfer_all') :
        # if call_function in ('add_stake', 'add_stake_limit', 'swap_stake', 'swap_stake_limit') :

            contact_add = decoded['address'].value
            add_hash = xxhash.xxh32(contact_add).intdigest() & 0xFFFFF
            era = decoded['era']
            era_period = 100
            if era == '00':
                era_period = 100
            elif hasattr(era, 'value'):
                era_data = era.value
                if isinstance(era_data, tuple) and len(era_data) >= 2:
                    era_period = era_data[0]

            if self.lst_ban_accounts[add_hash] == 0 and self.lst_new_accounts[add_hash] == 0 :

                if call_function in ('batch_all', 'force_batch', 'batch') :
                    # pass
                    calls = decoded['call']['call_args'][0]['value']
                    n = len(calls)
                    if era_period > 4 :
                        for _call in calls :
                            await self.process_call(contact_add, _call, era_period, True)
                elif call_function == 'proxy' :
                    # pass
                    if era_period > 4 :
                        await self.process_call_proxy(contact_add, call)
                else :
                    if era_period > 4 :
                        await self.process_call(contact_add, call, era_period)

        self.extrinsic_processing = False
        
    async def init_block(self, first_init = False) :
        start_time = time.perf_counter()
        self.start_time = start_time
        self.monit_cnt = 0
        self.unstake_all_alpha_flg = False
        print("--------------------------------")
        self.block_initializing = True
        
        block_staked = False
        if self.Block_Staked > 0 :
            block_staked = True
            self.Block_Staked -= 1

        if self.current_block % 10 == 0 or self.current_block_count > 0:
            if self.current_block_count > 0 :
                self.current_block_count -= 1
            self.nonce = await self.substrate.get_account_nonce(self.main_wallet_address)
            self.current_block = await self.subtensor.get_current_block()
        else :
            self.current_block += 1
        
        self.finalized_block = self.current_block - 2
        flg = False
        for e in self.block_hashs :
            (n, h) = e
            if n == self.finalized_block :
                self.block_hash = h
                flg = True
                break

        if flg == False :
            print("got block hash!")
            self.block_hash = await self.substrate.get_block_hash( block_id=self.finalized_block )
        
        if self.Block_Staked == 1 :
            if self.unstaked_all_alpha == False :
                response = ""
                try :
                    response = await self.rpc_request(self.substrate, "author_submitExtrinsic", [str(self.swap_extrinsic.data)], self.block_hash)
                except Exception as e:
                    pass
                if "result" in response :
                    self.nonce += 1
                    print("Fast Swapped!")
                    self.unstaked_all_alpha = True
                else :
                    print("Extrinsic Error!")
            self.nonce = await self.substrate.get_account_nonce(self.main_wallet_address) + 1
            await asyncio.sleep(4)
            await self.unstaking_process()
        
        for i in range(SUBNTET_LIMIT) :
            self.removed_balance[i] = 0

        print(f"Block     : {self.current_block}")
        await self.substrate.init_runtime()
        self.meta = self.substrate.runtime.metadata
        
        if self.Block_Staked == 0 :
            self.nonce = await self.substrate.get_account_nonce(self.main_wallet_address)

        cancel_call = self.substrate.runtime_config.create_scale_object(type_string="Call", metadata=self.meta)
        cancel_call.encode(
            {
                "call_module": "SubtensorModule",
                "call_function": "unstake_all_alpha",
                "call_args": {
                    "hotkey": self.hotkey,
                },
            }
        )
        self.cancel_extrinsic = self.create_extrinsic(cancel_call, self.finalized_block, self.block_hash)
        
        cur_staked = await self.get_stakes(self.main_wallet_address, False)
        
        self.staked_flg = False
        for i in range(SUBNTET_LIMIT) :
            if cur_staked[i] > 1000000 :
                self.staked_flg = True
                break

        if self.staked_flg == False :
            self.Block_Staked = 0
        elif self.Block_Staked == 0 :
            self.nonce = await self.substrate.get_account_nonce(self.main_wallet_address)
            await self.unstaking_process()
            self.Block_Staked = 1
        
        
        block_hash = self.substrate0.get_chain_head()
        events = self.substrate0.get_events(block_hash)
        self.block_hash_current = await self.substrate.get_block_hash( block_id=self.current_block )
        self.block_hashs.append((self.current_block, self.block_hash_current))
        while len(self.block_hashs) > 5 :
            self.block_hashs.pop(0)
        
        # lang_tao: for new account's bot attack prevention
        # if self.current_block % 7200 == 0 :
        #     self.new_accounts.clear()
        #     self.lst_new_accounts = array.array('b', [0]) * 1048576
        #     saved_new_accounts = self._load_addresses_new()
        #     for account in saved_new_accounts :
        #         block, address = account
        #         if block > self.current_block - 70000 :
        #             self.new_accounts.append(account)
        #             self.lst_new_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1
        #     self._save_all_addresses_new()
        
        subnets_ = await self.subtensor.all_subnets()
        tao_in= []
        alpha_in = []
        self.lst_price.clear()
        for subnet in subnets_ :
            tao_in.append(subnet.tao_in.tao)
            alpha_in.append(subnet.alpha_in.tao)
            if subnet.tao_in.tao > 10 :
                self.lst_price.append(subnet.tao_in.tao / subnet.alpha_in.tao)
            else :
                self.lst_price.append(1.0)

        self.tao_in = tao_in
        self.alpha_in = alpha_in
        self.tao_in[0] = 1
        self.alpha_in[0] = 1
        self.lst_price[0] = 1
        
        for i in range(SUBNTET_LIMIT) :
            self.limit_stakings[i] = self.get_limit(i)

        # lang_tao: for new account's bot attack prevention
        # for event in events:
        #     if event.value['event_id'] == 'NewAccount':
        #         new_address = event.value['event']['attributes']['account']
        #         balance = await self.subtensor.get_balance(new_address)
        #         if balance.tao < 100 :
        #             self.save_address_new(self.current_block, new_address)
        
        cur_balance = await self.subtensor.get_balance(self.main_wallet_address)
        balance = cur_balance.tao

        staked_bal = float(cur_staked[0]) / TAO_FLOAT
        if self.staked_flg :
            for i in range(1, self.subnet_lim) :
                if cur_staked[i] > 1000 and self.alpha_in[i] > 1 : 
                    slipage = 1.0 * (self.alpha_in[i] + float(cur_staked[i]) / TAO_FLOAT) / self.alpha_in[i]
                    staked_bal += self.lst_price[i] * float(cur_staked[i]) / TAO_FLOAT
        if staked_bal < 0.001 :
            self.Block_Staked = 0
            
        danger_flg = False
        total_balance = staked_bal + balance
        if self.total_balance > total_balance + 0.2 :
            danger_flg = True
        self.total_balance = total_balance
        
        print("Balance   :", self.total_balance, staked_bal)
        
        if self.Block_Staked == 0 :
            if self.staked_flg :
                self.consequtive_staked += 1
            else :
                self.consequtive_staked = 0
            if self.consequtive_staked > 10 :
                sys.exit(0)
            self.balance = balance
            self.remain_balance = balance
            if self.max_balance < balance :
                self.max_balance = balance
            if self.staked_flg == False and balance < 98.5 :
                print("staking disabled...")
                self.never_stake = True
            else :
                self.never_stake = False

        print(self.Block_Staked, self.never_stake, self.staked_flg)
        if self.Block_Staked == 1 :
            self.staked_flg = False

        # if self.current_block % 99 == 0 :
        #     await self.reload_bots()
        # full_block = self.substrate0.get_block(block_number=self.current_block)
        # # full_block = await self.substrate_arc.get_block(block_number=6201050)
        # if full_block and 'extrinsics' in full_block:
        #     self.updated_accounts.clear()
        #     start_time = time.perf_counter()
        #     await self.process_full_block(full_block, danger_flg)

        #     if block_staked :
        #         if self.Block_Staked == 0 :
        #             if self.balance != 0 :
        #                 if self.balance > balance + 0.07 and self.not_ban:
        #                     if self.last_address in self.flaged_address :
        #                         self.save_address(self.last_address)
        #                     else :
        #                         self.flaged_address.append(self.last_address)

        # cfg_stakes = await self.get_stakes(self.account_cfg, False)
        # fff_stakes = await self.get_stakes(self.account_fff, False)
        # ddd_stakes = await self.get_stakes(self.account_ddd, False)
        # h1x_stakes = await self.get_stakes(self.account_h1x, False)
        # for i in range(self.subnet_lim) :
        #     self.lst_bot_staked[i] = 0
        #     # self.danger_staked[i] = epk_stakes[i]
        #     self.danger_staked[i] = 0
        #     self.cfg_stakes[i] = max(cfg_stakes[i], fff_stakes[i])
        #     self.cfg_stakes[i] = max(self.cfg_stakes[i], ddd_stakes[i])
        #     self.cfg_stakes[i] = max(self.cfg_stakes[i], h1x_stakes[i])

        # for delay_account in self.delay_account :
        #     delay_stakes = await self.get_stakes(delay_account)
        #     # epk_stakes = await self.get_stakes(self.account_epk)
        #     for i in range(self.subnet_lim) :
        #         self.cfg_stakes[i] += delay_stakes[i]

        # danger_accounts_real = []
        # remove_danger_accounts = []
        # new_pending = []
        # lst_danger = self.really_danger_accounts
        # for account in self.really_danger_accounts :
        #     if account not in danger_accounts_real :
        #         danger_accounts_real.append(account)
        #         staked_info = await self.get_stakes(account, False)
        #         balance_tao = await self.subtensor.get_balance(account)
        #         balance = balance_tao.tao
        #         cnt = 0
        #         for i in range(self.subnet_lim) :
        #             if self.danger_staked[i] < staked_info[i] :
        #                 self.danger_staked[i] = staked_info[i]
        #             balance += staked_info[i] * self.lst_price[i] / 1000000000.0
        #             if i > 0 and staked_info[i] > 100000000000 :
        #                 cnt += 1
        #         if balance < 5 or cnt > 3 :
        #             if account != '5EC7StAPcUuR3STRvUEDph2LDmQgyELrLiz5sjz5APieyJLw':
        #                 if account in self.pending_remove :
        #                     remove_danger_accounts.append(account)
        #                 if account not in new_pending :
        #                     new_pending.append(account)
        # self.pending_remove = new_pending

        # staked_5fkf = await self.get_stakes("5FKfQ3hnVM1tkUMk4sDQw659yzwsHdqJvT25Mz452qic2x1n", False)
        # staked_5gul = await self.get_stakes("5GuLYhyfPPMRqu9j57FUBLvQgx3wDjgL3WvqoyKnLjpuYeET", False)
        # for i in range(self.subnet_lim) :
        #     if staked_5fkf[i] > 10000000 : 
        #         if self.danger_staked[i] < staked_5fkf[i] + staked_5gul[i] :
        #             self.danger_staked[i] = staked_5fkf[i] + staked_5gul[i]

        # print("danger accounts real")
        # for account in danger_accounts_real :
        #     print(account)

        # for account in remove_danger_accounts :
        #     self.really_danger_accounts.remove(account)

        # for bot in self.lst_bots :
        #     staked_info = await self.get_stakes(bot)
        #     for i in range(self.subnet_lim) :
        #         if self.lst_bot_staked[i] < staked_info[i] :
        #             self.lst_bot_staked[i] = staked_info[i]

        # for account in self.bot_accounts :
        #     block_number, bot = account
        #     if bot not in self.lst_bots :
        #         staked_info = await self.get_stakes(bot)
        #         for i in range(self.subnet_lim) :
        #             if self.lst_bot_staked[i] < staked_info[i] :
        #                 self.lst_bot_staked[i] = staked_info[i]


        if self.current_block % 50 == 0 :
            self.list_chk_ext = array.array('b', [0]) * 1048576
        for i in range(256) :
            self.list_chk_acc[i] = 0

        for netuid in range(SUBNTET_LIMIT) :
            proxy_call = self.substrate.runtime_config.create_scale_object(type_string="Call", metadata=self.meta)
            proxy_call.encode(
                {
                    "call_module": "SubtensorModule",
                    "call_function": "add_stake_limit",
                    "call_args": {
                        "hotkey": CortexValidator,
                        "netuid": netuid,
                        "limit_price" : self.calc_limit(netuid, self.limit_stakings[netuid]),
                        "amount_staked": int(self.limit_stakings[netuid] * TAO_INT),
                        "allow_partial": False,
                    },
                }
            )
            proxy_call2 = self.substrate.runtime_config.create_scale_object(type_string="Call", metadata=self.meta)
            proxy_call2.encode(
                {
                    "call_module": "SubtensorModule",
                    "call_function": "add_stake_limit",
                    "call_args": {
                        "hotkey": CortexValidator,
                        "netuid": netuid,
                        "limit_price" : self.calc_limit2(netuid, self.limit_stakings[netuid]),
                        "amount_staked": int(self.limit_stakings[netuid] * TAO_INT),
                        "allow_partial": False,
                    },
                }
            )
            self.result_extrinsic[netuid] = self.create_extrinsic(proxy_call, self.finalized_block, self.block_hash)
            self.result_extrinsic2[netuid] = self.create_extrinsic(proxy_call2, self.finalized_block, self.block_hash)

        last_time = time.perf_counter()
        print("Delay:", last_time - start_time)

        self.block_initializing = False

    def create_extrinsic(self, proxy_call, finalized_block, block_hash, tip = 0) :
        call = self.substrate.runtime_config.create_scale_object(type_string="Call", metadata=self.meta)
        call.encode(
            {
                "call_module": "Proxy",
                "call_function": "proxy",
                "call_args": {
                    "real": self.wallet.coldkeypub.ss58_address,
                    "force_proxy_type": None,
                    "call": proxy_call,
                },
            }
        )

        era = {"period": 4, "current" : finalized_block}
        era_obj = self.substrate.runtime_config.create_scale_object("Era")
        era_obj.encode(era)
        signature_payload = self.substrate.runtime_config.create_scale_object("ExtrinsicPayloadValue")
        signature_payload.type_mapping = [["call", "CallBytes"]]
        signed_extensions = self.meta.get_signed_extensions()
        if "CheckMortality" in signed_extensions:
            signature_payload.type_mapping.append(["era", signed_extensions["CheckMortality"]["extrinsic"]])
        if "CheckEra" in signed_extensions:
            signature_payload.type_mapping.append(["era", signed_extensions["CheckEra"]["extrinsic"]])
        if "CheckNonce" in signed_extensions:
            signature_payload.type_mapping.append(["nonce", signed_extensions["CheckNonce"]["extrinsic"]])
        if "ChargeTransactionPayment" in signed_extensions:
            signature_payload.type_mapping.append(["tip", signed_extensions["ChargeTransactionPayment"]["extrinsic"]])
        if "ChargeAssetTxPayment" in signed_extensions:
            signature_payload.type_mapping.append(["asset_id", signed_extensions["ChargeAssetTxPayment"]["extrinsic"]])
        if "CheckMetadataHash" in signed_extensions:
            signature_payload.type_mapping.append(["mode", signed_extensions["CheckMetadataHash"]["extrinsic"]])
        if "CheckSpecVersion" in signed_extensions:
            signature_payload.type_mapping.append(["spec_version",signed_extensions["CheckSpecVersion"]["additional_signed"],])
        if "CheckTxVersion" in signed_extensions:
            signature_payload.type_mapping.append(["transaction_version",signed_extensions["CheckTxVersion"]["additional_signed"],])
        if "CheckGenesis" in signed_extensions:
            signature_payload.type_mapping.append(["genesis_hash",signed_extensions["CheckGenesis"]["additional_signed"],])
        if "CheckMortality" in signed_extensions:
            signature_payload.type_mapping.append(["block_hash",signed_extensions["CheckMortality"]["additional_signed"],])
        if "CheckEra" in signed_extensions:
            signature_payload.type_mapping.append(["block_hash", signed_extensions["CheckEra"]["additional_signed"]])
        if "CheckMetadataHash" in signed_extensions:
            signature_payload.type_mapping.append(["metadata_hash",signed_extensions["CheckMetadataHash"]["additional_signed"],])

        call_data = str(call.data)
        payload_dict = {
            "call": call_data,
            "era": era,
            "nonce": self.nonce,
            "tip": tip,
            "spec_version": self.substrate.runtime.runtime_version,
            "genesis_hash": self.genesis_hash,
            "block_hash": block_hash,
            "transaction_version": self.substrate.runtime.transaction_version,
            "asset_id": {"tip": tip, "asset_id": None},
            "metadata_hash": None,
            "mode": "Disabled",
        }
        try :
            signature_payload.encode(payload_dict)
            if signature_payload.data.length > 256:
                signature_payload =  ScaleBytes(
                    data=hashlib.blake2b(signature_payload.data.data, digest_size=32).digest()
                )
            signature_version = self.main_wallet.crypto_type
            signature = self.main_wallet.sign(signature_payload.data)
            value = {
                "account_id": self.main_wallet_id,
                "signature": f"0x{signature.hex()}",
                "call_function": call.value["call_function"],
                "call_module": call.value["call_module"],
                "call_args": call.value["call_args"],
                "nonce": self.nonce,
                "era": era,
                "tip": tip,
                "asset_id": {"tip": tip, "asset_id": None},
                "mode": "Disabled",
                "signature_version" : 1,
            }
            extrinsic = self.substrate.runtime_config.create_scale_object(type_string="Extrinsic", metadata=self.meta)
            extrinsic.encode(value)
            return extrinsic
        except Exception as e:
            return None

    def get_limit(self, netuid) :
        if self.tao_in[netuid] < 500 :
            return STAKE_LIMIT3
        elif self.tao_in[netuid] < 5000 :
            return  STAKE_LIMIT2
        return STAKE_LIMIT
    
    def calc_limit(self, netuid, amount_tao) :
        param = 1.27
        if amount_tao < 20 :
            param = 1.2
        slipage = 1.0 * (self.tao_in[netuid] + amount_tao * param) / self.tao_in[netuid]
        return int(self.lst_price[netuid] * slipage * slipage * 1000000000 * 1.001)

    def calc_limit2(self, netuid, amount_tao) :
        param = 1.5
        if amount_tao < 20 :
            param = 1.27
        slipage = 1.0 * (self.tao_in[netuid] + amount_tao * param) / self.tao_in[netuid]
        return int(self.lst_price[netuid] * slipage * slipage * 1000000000 * 1.001)

    async def rpc_request(
        self,
        substrate: AsyncSubstrateInterface,
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
            return []
        if "result" in result[payload_id][0]:
            return result[payload_id][0]
        else:
            return []
        
        
    async def process_unstake_all_alpha(self) :
        while True :
            await asyncio.sleep(0.5)
            current_time = time.perf_counter()
            if current_time > self.start_time + 11 and self.unstake_all_alpha_flg :
                print("Unstaking...")
                await self.unstake_all_alpha(self.next_hash)
               
    async def unstake_all_alpha(self, next_hash) :
        tasks = []
        for subtensor in self.subtensor_for_block:
            tasks.append(asyncio.create_task(self.unstake_process(subtensor, next_hash)))
        await asyncio.gather(*tasks)
 
    async def unstake_process(self, subtensor:AsyncSubtensor, next_hash) :
        current_block = self.current_block
        cnt = 0
        while self.unstaked_all_alpha == False :
            block = await subtensor.get_current_block()
            if block == current_block :
                continue
            response = ""
            try :
                if self.unstaked_all_alpha == False:
                    response = await self.rpc_request(subtensor.substrate, "author_submitExtrinsic", [str(self.swap_extrinsic.data)], next_hash)
                else :
                    break
            except Exception as e:
                pass
            if "result" in response :
                self.nonce += 1
                self.unstaked_all_alpha = True
                print("Fast Swapped!")
            else :
                cnt += 1
                print("Extrinsic Error!")
                if cnt > 10 :
                    sys.exit(0)
                    
    async def process_call_str(self, call) :
        call_str = str(call)
        call_str = call_str.replace("'", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace(" ", "").replace("call_args:","")
        parts = call_str.split(",")
        call_function = None
        netuid = None
        netuid1 = None
        netuid2 = None
        amount_staked = None
        amount_unstaked = None
        alpha_amount = None
        limit_price = None
        target_address = None
        transfer_amount = None
        i = 0
        n = len(parts)
        while i < n:
            part = parts[i]
            try :
                left, right = part.split(":")
                if 'call_function' in left :
                    call_function = right
                    i += 1
                    continue
                if 'dest' in right and 'destination_netuid' not in right :
                    name, val = parts[i+2].split(":")
                    target_address = val
                    i += 3
                    continue
                if 'value' in right :
                    name, val = parts[i+2].split(":")
                    transfer_amount = int(val)
                    i += 3
                    continue
                if 'origin_netuid' in right :
                    name, val = parts[i+2].split(":")
                    netuid1 = int(val)
                    i += 3
                    continue
                if 'destination_netuid' in right :
                    name, val = parts[i+2].split(":")
                    netuid2 = int(val)
                    i += 3
                    continue
                if 'netuid' in right :
                    name, val = parts[i+2].split(":")
                    netuid = int(val)
                    i += 3
                    continue
                if 'amount_staked' in right :
                    name, val = parts[i+2].split(":")
                    amount_staked = int(val)
                    i += 3
                    continue
                if 'amount_unstaked' in right :
                    name, val = parts[i+2].split(":")
                    amount_unstaked = int(val)
                    i += 3
                    continue
                if 'alpha_amount' in right :
                    name, val = parts[i+2].split(":")
                    alpha_amount = int(val)
                    i += 3
                    continue
                if 'limit_price' in right :
                    name, val = parts[i+2].split(":")
                    limit_price = int(val)
                    i += 3
                    continue
            except Exception as e:
                pass
            i += 1
            continue
        return (call_function, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount, target_address, transfer_amount)

    async def get_stakes(self, contact_add, reuse_dic = True) :
        rao = []
        for i in range(SUBNTET_LIMIT) :
            rao.append(0)

        if reuse_dic and contact_add in self.staking_dic :
            for netuid in range(SUBNTET_LIMIT) :
                rao[netuid] = self.staking_dic[contact_add][netuid]
        else :
            try :
                delegations = await self.subtensor.get_stake_for_coldkey(coldkey_ss58=contact_add,)
            except Exception as e:
                return rao
            for record in delegations :
                if record.netuid < SUBNTET_LIMIT :
                    rao[record.netuid] += record.stake.rao
            self.staking_dic[contact_add] = []
            self.staking_dic[contact_add].clear()
            for netuid in range(SUBNTET_LIMIT) :
                self.staking_dic[contact_add].append(rao[netuid])

        py_list = [rao[i] for i in range(SUBNTET_LIMIT)]
        return py_list

        
async def main():
    mev_bot = MevBot()
    await mev_bot.init_param()
    random.seed(2 * mev_bot.monit_select)
    monitors = random.sample(mev_bot.server_finney, 13)
    monitors.append(mev_bot.server_private)

    await asyncio.gather(mev_bot.check_block(),
                         mev_bot.monit0(mev_bot.subtensor_for_submit),
                         mev_bot.process_unstake_all_alpha(),
                         mev_bot.monit([monitors[0], monitors[1]]),
                         mev_bot.monit([monitors[2], monitors[3]]),
                         mev_bot.monit([monitors[4], monitors[5]]),
                         mev_bot.monit([monitors[6], monitors[7]]),
                         mev_bot.monit([monitors[8], monitors[9]]),
                         mev_bot.monit([monitors[10], monitors[11]]),
                         mev_bot.monit([monitors[12], monitors[13]], True),
                         )
    
if __name__ == "__main__":
    asyncio.run(main())