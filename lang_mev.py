import os
import sys
import json
import time
import copy
import array
import random
import socket
import struct
import xxhash
import asyncio
import requests
import websockets
import configparser
import bittensor as bt
from typing import Any, Union
from functools import lru_cache
from scalecodec import ScaleBytes
from collections import defaultdict
from substrateinterface import Keypair
from substrateinterface.utils import ss58
from substrateinterface import SubstrateInterface
from bittensor.core.async_subtensor import AsyncSubtensor
from async_substrate_interface.types import RequestManager
from async_substrate_interface import AsyncSubstrateInterface

class AddStaker:

    def __init__(self) :
        self.wallet_select = 1
        self.monit_select = 3
        self.start_time = 0
        self.unstake_all_alpha_flg = False
        self.next_hash = 0
        self.check_block_unstaked = False
        self.last_block_time = -10000000000
        self.substrate = None
        self.substrate0 = None
        self.substrate2 = None
        self.pending_remove = []
        self.really_danger_accounts = []
        self.substrate_submit = []
        self.subtensor_block = []
        self.removed_balance = []
        self.proxies = ["proxy", "proxy8", "proxy5", "proxy6"]
        self.substrate_arc = None
        self.subtensor = None
        self.monitor_evm = None
        self.monitor_private = None
        self.monitor_local = None
        self.monitor_finney = []
        self.wallet = None
        self.proxy_wallet = None
        self.proxy_keypair = None
        self.meta = None
        self.account_id = None
        self.genesis_hash = None
        self.base_call_proxy = None
        self.base_call_proxy2 = None
        self.base_extrinsic = None
        self.result_extrinsic = []
        self.result_extrinsic2 = []
        self.unstake_extrinsic = None
        self.cancel_extrinsic = None
        self.swap_extrinsic = None
        self.huge_staked_account = ['5CiBL68o8uUKzSDkYoZhKxySAGssjLhy2A7kND4P3krFmvUi', '5GYTkrvLpVSxQzWp1x6brTkgET9ckJgrmZMACsR2XRe7yBqg', '5EKzZQs684ZC4w1sZUzNrrVCDpMfKP9SzSpcDKNwuaJx2epE', '5Fhn6KAipX1u1zTWCFJ5tBPpf4MRAKL74CcmfUeh2bdWjAwi']
        self.huge_accounts = ('5D5TBiHZysJRJrS5YsdaQxePJ4XoHZbssJdSaw4d9BEYiq2U', '5FV99mBYw3tYrMTXXe52PDa69an1AE19aTrpnB4kzxW73yUj', '5DunDrFV6BPbzsgLZUtMQtCq7w9fcUEbM59BUwx5E7N9Bn5E', '5CW8rdA832Qrc8NkFrC5pn4dox7G5ysUaLHm1tDnG5NQUnnC', '5DS3BcDqhkBpn8gD1Es8BAMTTXSs76gTKuUQxDNNeBQ6WjGe', '5CVSCaCXDRydd3Mkdbu2tHLNYxmNTSpy9yRixa1TRGvgRFS8', '5DdfV4KJgkrwyNKPCML87KceNj3in9py2HGiwiGF7KSiJNP9', '5CNChyk2fnVgVSZDLAVVFb4QBTMGm6WfuQvseBG6hj8xWzKP', '5H9brHhMA1km3Dp3YCx75oaimgxEYScxCfxbzQRZ3gHk9x3L', '5EiXej3AwjKqb9mjQAf29JG5HJf9Dwtt8CjvDqA8biprWTiN','5FZiuxCBt8p6PFDisJ9ZEbBaKNVKy6TeemVJd1Z6jscsdjib', '5CrmVKApX6sJybZaL1geHfzvHWeCpbavqrrXgYLCQmhehX2q', '5HiveMEoWPmQmBAb8v63bKPcFhgTGCmST1TVZNvPHSTKFLCv', '5HbDZ6ULuwZegAMSPaS2kaUfBLMDaht5t48RcDrQATSgGCAR', '5GBnPzvPghS8AuCoo6bfnK7JUFHuyUhWSFD4woBNsKnPiEUi', '5E2b2DcMd5W8MBhzTCFt63t2ZEN8RsRgL7oDd7BFYL9aMQux', '5FqBL928choLPmeFz5UVAvonBD5k7K2mZSXVC9RkFzLxoy2s', '5FqqXKb9zonSNKbZhEuHYjCXnmPbX9tdzMCU2gx8gir8Z8a5', '5EZsiQoortPKKaDrh9EMKYgXArE9zyPYnGDthDWnGWzXHWuy', '5DF933pRe3giG2UXsUvMS8497hcoRH6pzqzVjm158JPJ8rqF', '5DsqKdVuoz8i8uLHqe71EMbLtJ7mSY8NbRb7LHbtFC2V9xbP', '5FqqXKb9zonSNKbZhEuHYjCXnmPbX9tdzMCU2gx8gir8Z8a5')
        self.nonce = None
        self.meta = None
        self.fee = 0.00005
        self.alpha_fee = 0.000018
        self.finalized_block = 0
        self.block_hash =None
        self.block_hash_current =None
        self.current_block = 0
        self.current_block_init = 0
        self.current_block_count = 5
        self.block_initializing = False
        self.extrinsic_processing = False
        self.owner_coldkeys = []
        self.tao_in = []
        self.alpha_in = []
        self.lst_price = []
        self.avr_price = []
        self.netuids = [62, 63, 128, 48, 73, 89, 93, 106, 94, 46, 33]
        self.n_price = []
        self.last_add_hash = 0
        self.balance = 0
        self.remain_balance = 0
        self.total_balance = 0
        self.tao_in_emission = []
        self.alpha_in_emission = []
        self.list_chk_ext = array.array('b', [0]) * 1048576
        self.list_chk_acc = array.array('b', [0]) * 256
        self.not_bot = ["5CyfmvqSc9L2vaCR5MfM7q24S3zY5Dxt3oAdTZnn5hj3tw8X", "5H1iUdqpVeT2gxMDQgEPKsVK65eGBY5cgm7QjuwUhGZZHd3i", "5CvqLXd1LhKqQtE8jGicdffrkpVegA7Kb8G4oqZL21NeYT25", "5FxYwfWZWE1NcUA7z1BusDcKSDHW96U7TyPA9X2Wmgcq2DDa", "5H1pmTego8xf5NG6SJ6rPktPLKXFG1ZbBG2T4Z2TY9mjFimr", "5H9AqwmLSMuYunEv9ZEmjKaTuCbrGDtYfVmrjK91CnvC6qo7", "5DccD25B2tR3domkE1SBpGEgDohgk7hEX5g5npQEh4tLSHaj", "5Hq44tCRLEKKL4dVh7jEzHLgBLVijMrmsq95KePBTRpuK6Qz", "5C4hrfkeBZiRUUDVdd7Y3mzgd3MNpCaBk7PnPEb3Gx39SBio", "5GuLYhyfPPMRqu9j57FUBLvQgx3wDjgL3WvqoyKnLjpuYeET"]
        self.mev_bot = ["5DDDpkANMCJZjK4dAcHGMJNahD4ATWQyksAyiaDh9iMNRMzK", "5Hq44tCRLEKKL4dVh7jEzHLgBLVijMrmsq95KePBTRpuK6Qz", "5C4hrfkeBZiRUUDVdd7Y3mzgd3MNpCaBk7PnPEb3Gx39SBio", "5HWeEGLrTKHBQKUeqDVbBxo85WFCqNW1Z7C55huE3kR4bz5g", "5FKfQ3hnVM1tkUMk4sDQw659yzwsHdqJvT25Mz452qic2x1n", "5DccD25B2tR3domkE1SBpGEgDohgk7hEX5g5npQEh4tLSHaj", "5CvqLXd1LhKqQtE8jGicdffrkpVegA7Kb8G4oqZL21NeYT25", "5HW1bU6buPP9RFBV9Hpct5eRM5vickDjAJFNy3L9NjPm8CBg", "5GjsoENUQRHYcfDHqR4bx9o4qyDABAwQ5LKwB6CN7L19REJi"]
        self.lst_mev_bot = array.array('b', [0]) * 1048576
        self.hotkey = '5E2LP6EnZ54m3wS8s1yPvD5c3xo71kQroBw7aUVK32TKeZ5u'
        self.first_run = True
        self.fee = 0.00005
        self.limit_stakings = []
        self.updated_accounts = []
        self.stake_lim = 99
        self.stake_lim2 = 27
        self.stake_lim3 = 10
        self.Block_Staked = 0
        self.max_balance = 0
        self.last_netuid = 0
        self.last_block = 0
        self.last_amounts = []
        self.last_era = None
        self.lock = asyncio.Lock()
        self.log_file_path = "ban_list.json"
        self.addresses = []
        self.log_ban_path = "ban_netuid.json"
        self.ban = []
        self.log_new_account_path = "new_accounts.json"
        self.new_accounts = []
        self.log_bots_path = "bots.json"
        self.bot_accounts = []
        self.log_danger_path = "danger.json"
        self.danger_accounts = []
        self.log_danger_path2 = "danger2.json"
        self.danger_accounts2 = []
        self.danger_accounts_current = []
        self.log_pending_account_path = "pending.json"
        self.pending_accounts = []
        self.lst_pending_accounts = array.array('b', [0]) * 1048576
        self.lst_danger_accounts = array.array('b', [0]) * 1048576
        self.lst_danger_accounts2 = array.array('b', [0]) * 1048576
        self.lst_ban_accounts = array.array('b', [0]) * 1048576
        self.lst_new_accounts = array.array('b', [0]) * 1048576
        self.lst_bots = ["5CMcngJawjS8iCPrAfFLGdi4ag3fqYeK2qdZRQayp1dhQyz9", "5DCbtUdwxYZPy2GtqnvJ4L1o8sfFSiXurj3A3MgNSRH3UREJ", "5DXDkgWH7ZcPeWrbwp3xJ3XvtbPo2tJqg9NhSna7Hu56QSXn", "5CDhyDcALYTyUQC5cSbB88icpfysmTe2jnKw7NhiTUeRtUxA", "5GTU2yhxLQSY18hZ3s2Zr7TzjLdPq1MP79V53s3Ce6RJPrvH", "5FsvCbr7NKa84eR6dAghDjnSpqXe9a6bkBJe5w23RXB3fixu", "5CoEw94gyMvpv8M9f38nkM1h33ZNMvD7JEm3mbHzEQgHEcFC", "5CJCCmqMWa9wwufi4JL9hYbVvjdW9nQK9FbuDoTBXqfXmD97", "5C7wmg1uSgHWiVzURCQjMToQh7tzpPBBfwj8Ph4MkY8fKKDj", "5EnyKmp6diJjkHbiuKGPAzFSKe2K2Ao5ftmzH25gYnMaPRoY", "5DoHC6rPixhTNXnBhxJWQVbg6ZYSH9u5uB4ZMiq5H1gQ4myu", "5GNyVY5jVf5WL1Rht36h8SDucvt3CmskQRE2QpUNjM66cgVP", "5HCDHvqzdGxdA1iwG7VFauKAL9jhGUmaZkuGKmGoNNbuFNgV"]
        self.lst_allows = ["5GdpaARdm1Ton33P3gGer7mEfbpJQt8TdAkmS3AAVauVSffA", "5FZLoPStbbVoyJ6J9zt5Lrgiwkr9YvyWVFVusgFEKqZ16mHW"]
        self.lst_era4 = []
        self.lst_last_era4 = []
        self.subnet_lim = 129
        self.consequtive_staked = 0
        self.lst_bot_staked = []
        self.lst_last_block = []
        self.last_address = None
        self.last_staked_amount = 0
        self.monit_cnt = 0
        self.add_accounts = []
        self.start_time = time.perf_counter()
        self.not_ban = False
        self.never_stake = False
        self.staked_flg = False
        self.unstaked_flg = False
        self.unstaked_all_alpha = False
        self.block_hashs = []
        self.flaged_address = []
        self.recieved = 0
        self.cfg_stakes = []
        self.danger_staked = []
        self.account_cfg = "5CMcngJawjS8iCPrAfFLGdi4ag3fqYeK2qdZRQayp1dhQyz9"
        self.account_fff = "5FFFHCjf9NSxkGSC2s3Nz8j8njgrvgHLMWzXxJebc9cHQ2rw"
        self.account_ddd = "5DDDpkANMCJZjK4dAcHGMJNahD4ATWQyksAyiaDh9iMNRMzK"
        self.account_h1x = "5H1XBWCbEpGJZZDdqe19WvgqbXjxPNzQ7P7fM7iVVTVH49MN"
        self.delay_account = ["5FxYwfWZWE1NcUA7z1BusDcKSDHW96U7TyPA9X2Wmgcq2DDa", "5H6ALLYFhUwTJoHECf8xjkYCncU8DLEqki7SgYQrdSWjssFC", "5Dcf6CAvRqLswpyG9dU2uvDeC9taBndByc1UGKQmdoHWRiBN", "5D2msakpthwJogCTEmV7wV2psLk4TcrUJm4joRwdnVLxztmD", "5HWG9siG3wzUbUEc3Fn4Swqbdi1qHuS3tpZjaKj2myxvwXcd", "5Fv9WKg4n5Kkia3ApF5TqQNdiagZ5wFsJ1azHDvyz4vq679j", "5Ei2xcB99HkkBi8y3JT4fyuPkBsJSAaKyG3XfQ9QKsvuzdxv", "5EXX5wx12NwnR5HSLqdZEJartWcNyugFjSixLP2we3R2Es7H", "5FgwtNozWKz8u6PYRSTUixi5RMDcn11zcVVXdkVUmWWQRV7c", "5EPka3cz6oFKjTS5gSsVM3iHoN1NFnuMtd86MLsHJsxF5cJ7", "5G9b3i2NLa1NCJXf45Q7zMnjrocpW8gCJL2VPcK2gj3W6XqX", "5FNdtnb4tQ8CZPNfMneV3jKwycCaAzMNmhHg9jecQRQGRCG1", "5Fe5xWUdumfp7XyfKWyPJJ8CwwEfsc4g1g45wmngUHZ8xzMt"]
        self.account_epk = "5EPka3cz6oFKjTS5gSsVM3iHoN1NFnuMtd86MLsHJsxF5cJ7"
        self.pre_calc = ["5GYTkrvLpVSxQzWp1x6brTkgET9ckJgrmZMACsR2XRe7yBqg"]
        self.staking_dic = {
            "5C9xyz" : [0.1, 1.2, 2.3],
            "5Dka" : [1.2, 2.3, 3.4]
        }
        self.ext_err_cnt = 0
        self.BM = 1048576
        self.BS = 1048576
        self.account_namsu = ["5F4WQ53KKzFEpvydJsZQNmPJRwaqmCB8hAR2Vh9qLDuHJSn5", "5DJbdxEps4qfFA6X345g9jf9XJoWxZtqikgXk17hoJKNzAdN", "5FcGepXEQvCVf62H3um2RzkgMSH5m3jNkgVQk9gaAGpnnPcN", "5DtaSm9cgtvTzEH9kSAmXVajtfKLGAhqDtUeTzSvdn7QiMoR", "5DCbtUdwxYZPy2GtqnvJ4L1o8sfFSiXurj3A3MgNSRH3UREJ", "5GTQWx3146BUgxZ7ecExT4kzhWhzKQYX3SrN7vCXzhPtxV4i", "5CPgZFJpGrhcz9s3nCvQurNxDTTZLGvgMz78D3fFwwHxzKQU", "5CLhExmKFe6DNCp3GyDqtMiijRWmX53udZdThsAfTDrybSrX", "5Ff3ao5ynrwXuduDLSKmFxMzGv1AgV6Z8eVewuKD9NBLyoso", "5Fy6tGLMyaJFcMZzF5Juhk1zzbitCfHujzgWpfadnRmg7kMk", "5E9LkcRC31Ro2EKLjuFS5o2kTGuXP6ZkEiDvQq1NSmrgHQm9", "5FbdT8f7fLqd8HURpbbyQJ4R8q7EeNxY3MMKKpmydB8C2Pm7", "5FF3K2bAEHJY84wm88ZoDux4V1gZ1EbJ4gR3iLJqrChfm7vV", "5CoH7fEzXEwpETe3H7J4ZN2rqmthmpBA3cupX8EiZ5xvturv", "5CPAw6zzc3mbG7JTQph2WkS8oV3kwehqU7pQqXo8iGoJPAEs", "5GRLSxcmRhKerFuZx1VSC5TurvnXT2p3QqxAYgdzo4oREZSJ", "5EykRaYvckTABAuqt3fH2BFLVHG7pHpqUBDkS5GqCvhLHnND", "5EykRaYvckTABAuqt3fH2BFLVHG7pHpqUBDkS5GqCvhLHnND", "5E26HHMgBAbky7dHyp5Dj9qqmiLEmBcTtNKUDNKcAq9VNyba", "5FHJ8yKoCSrdoUoUL7HPTWs2KEPQKhyE5A7tccsv6ivp6aQK", "5G72MExYN765V7cv67X5dsib7d7tx9jo6mJBM65sRDTEybFk", "5DiKxoJgYBhbqsP5PioNyky1DU2SGtxpDDkJ6SdANuwYwtcc", "5DiKxoJgYBhbqsP5PioNyky1DU2SGtxpDDkJ6SdANuwYwtcc", "5E7QpMeBdToCjxbagEuqYxTEcY5FRmxYzEfmsv4UQRbQGTwr", "5DUS5R7iWs2yQPSJUyQbKxF8tKK4GvAJh7YLuRZoCajomVgL", "5DUS5R7iWs2yQPSJUyQbKxF8tKK4GvAJh7YLuRZoCajomVgL", "5DFAJ4xNsWaSdiWkmjAC5BjNYLSTGuAiadHp7JG8WTP9tzPW", "5DSMHU6i2SAa3hcSJhbcuJpTZjxBgCKBwpLfX1Ljn4wJbBLF", "5CFjGKYXo66XQrXUSrHmfkh4nRbKCyL8ikd6rhhi5rcWkWnz", "5HmTSaf824V2wQ98MRi22XVvtdijjf2LxKtke8GxafFHpSPw", "5GNgCbjvCE4LCZpX1vPf3BbXWrRX6Hy8B36acz8GFNqNLTGG", "5EqUq2f2BRNEqB4mkyQg2kR792UccALtjMCGJ4GaMcwkpiY3", "5HGWhJU41LF29Wypnywsc4CqKmswyBLpLmapkFHVSKBeggj6", "5Dqg2BF7Gi16DZ7CckJn2v6GCw2XoAhrU2strGifzEmzhcJp", "5GzfkTD7b4sHtiAeCncXRmqbq2z51iXARwqiw1333kQwMTpC", "5CSfACSbHJkxW3r4FN2guqkAagNh4ARy8NKj27JvhjuUaNY2", "5CtrNgMhxapwMqjqvc7RBWX6sna6ir2oZsdMeqBV2L5RfWeE", "5HU3Q3FJB1AadubY4RTi341jgDHseBsQBRcakGwR3KHjLezV", "5C4zCjwecw2Afbam2HvT8ct7qLnx9fHmkVaBSfRhb9xDPG4E", "5CcKY2rALCbspzJxBMWDFFXv2oQEQiTCqniTo4rXb6udKcPr", "5GNHLs554j53uSb6DxxSNkCk2LcnY7EAQRJScC1hCjSV51E2", "5CfRKET5nhZ9MdvB1JSC5zYoYpqGY3sW5n1rSRuEbvytLNxQ", "5GjncH1igVEwyaXzG148X48achB1TZt3CcvmoL8hJgFdGbiq", "5EtA1hS42MMHMamn7HaeST8FR25Kb3umC5NjrYRyYH5qc9G9", "5C87wycPgFcSo5mLaW12BHZheDziDM8A3BcRwX3VwETsjXKb", "5DATtfP2sW92zRQd2PJceUWJYQBPqBy889XtT94Xs6X6Wz6C", "5DFC9C3iiHkQESTgUWgLrfR6ZNAWXTTn1c1pjQ5p29DnKsKd", "5GbTANKzusp3U17ewsf9a6j8Rd89Ym8HejVPsZzMRiF25pak", "5EDDeGrNorwu2ES8BxM4apd9UNBeqZY1t6jU2ipiFoSGtNqC", "5DkrUUqdafyaYyCpVgHSBpohfikdL9Fo9jbXXXuWwTVqtVb7", "5FnbqU7TLY3HQg8g3vyyeM8QrbZULiSDZi6JUVVW1opgU63T", "5G4BiFQdrMx1rKCT3VUUAVwhNvQVgzdtheJozAh3HiqqoPH3", "5C4xMHUfSPG4XAf4LCgwRsBAsqFDVQSDx6yCx25ZQL1pAAZL", "5CGEZK9JZ6mYbCCkePtfLjUPhrprWMAm2Ntc4xfqiMvQj3jk", "5DFC9C3iiHkQESTgUWgLrfR6ZNAWXTTn1c1pjQ5p29DnKsKd", "5GTF18c7XqHw7zzjUW5NVKesVu2ewBFt82e851GQXZsGFbAG", "5CMZ6m5jTULJkn6qmXzFa6sJfQSgnU4cko5pMXoN4nj7Uipf", "5DkG51HK6JJftxbFBA2gWcjEjuNF6go2LHudMC2s9cuoVFy1", "5FvVQs72yKVHHwT8g7ovwjbD7rYnmEXP2DLpeQXnK5dqF8RJ", "5CDhyDcALYTyUQC5cSbB88icpfysmTe2jnKw7NhiTUeRtUxA", "5GTU2yhxLQSY18hZ3s2Zr7TzjLdPq1MP79V53s3Ce6RJPrvH", "5FsvCbr7NKa84eR6dAghDjnSpqXe9a6bkBJe5w23RXB3fixu", "5CoEw94gyMvpv8M9f38nkM1h33ZNMvD7JEm3mbHzEQgHEcFC", "5CJCCmqMWa9wwufi4JL9hYbVvjdW9nQK9FbuDoTBXqfXmD97", "5C7wmg1uSgHWiVzURCQjMToQh7tzpPBBfwj8Ph4MkY8fKKDj", "5DoHC6rPixhTNXnBhxJWQVbg6ZYSH9u5uB4ZMiq5H1gQ4myu", "5GNyVY5jVf5WL1Rht36h8SDucvt3CmskQRE2QpUNjM66cgVP", "5HCDHvqzdGxdA1iwG7VFauKAL9jhGUmaZkuGKmGoNNbuFNgV", "5GWoqXesG9JuQDSLjCmkNxgnwVP11gezBxA17W8ZVPKkmNNS", "5DLVCwG6crwt2ZiQeuityQARXDYRXsLxLnzKqTwLL3N6kyyL", "5CiBL68o8uUKzSDkYoZhKxySAGssjLhy2A7kND4P3krFmvUi", "5GYTkrvLpVSxQzWp1x6brTkgET9ckJgrmZMACsR2XRe7yBqg", "5EKzZQs684ZC4w1sZUzNrrVCDpMfKP9SzSpcDKNwuaJx2epE", "5Fhn6KAipX1u1zTWCFJ5tBPpf4MRAKL74CcmfUeh2bdWjAwi", "5Cf1fdkq32v1GZR9sqoeHNTVaWuy9v4F8BgbDTe8FmNsbYBd", "5GeQecw6xPrkD9a6UBfv1bvsEqVMAQTNQYhBq15PtYEV2EpR", "5CDmdPyNCprq9XX15iCNoVKqr6xdoTuCzn6c1Kwe54euovgY", "5DD21xF9ZUpEnGNFtU7GCpPoC8upW2YDEGp3hLySRELPDPiH", "5HgPxvpu3zfhpb244zbJpGPjqA6nnujjYAtXHDTkgBqDtVUk", "5CXiBGRmWXXA7SrqZGa2EPsrLeWEg66BZ49hpqBqkg9EovgY", "5GbpcVYjdXUY4W1tizceh6HCb2NTZrVaNwnz8328X6k37h1D", "5FxxDAzLxwcxEaLXKUoD3C5jgCZiVkS9UTspYnoJ3s3u3TcL", "5GHJLk58L5oZMoKt7pcbqx54eFd3enirFJJj9iJ8drPXshaU", "5DcKD7mYvo6z6cQBMCddm38Lted6H1D6LPyLHz6y8Va1kuys", "5GnX8BfVa3HB412HNpTw4GxmwcX7Q73ThgvKfcRjK6ZXeQ1b", "5DsshGbeRNHFLLndPD4bNRT7D2TAaWxZd8km29xEGFJwt9eN", "5Dw6wQ913yJqVLXugeKzXZkbPd8hLDqdRXjhVgjNh1tFvqqq", "5GQxMzzwhVV15mGFyTKkA5kBrDKQyZ3YgGV7kRCzAhg4LYJa", "5DcKD7mYvo6z6cQBMCddm38Lted6H1D6LPyLHz6y8Va1kuys", "5HRGG8VYsbuETZWbfhF8A4DCF1DyxRco5yGB1W83R1a15XsD", "5G737LvRBxt2b1StSfkozurj9zY6nPS2aztT8ereCFfhGZJU", "5DiDrCLLkf2Q1Qf98GADFT42rhFsZsfDKEJq3gm9CkMCobbM", "5CSntXS7jnnSk3WN1Sqw742sQbmvecHUykodQYBUrao4pQRf", "5EoChQnVBQez8NMqgv7NvLBnFV9XYCK7APPdKiT1FkVLgSTW", "5G737LvRBxt2b1StSfkozurj9zY6nPS2aztT8ereCFfhGZJU", "5EXB6W7TXZ1dMUStT433XaariNCPHXe96EAqpx5yYG49B6Y9", "5Egt4wshK5qoPJoY4711Pk3uX1WEXiKrYFo5s7XaqUtvJaLu", "5HmaeEa8sNtJ5DKkTwbdGSS4YLcHtGoEjY7QnNnMWxuNLcJD", "5C8PPeVMLyoPUcrFYJwLpaAvMwwJAyqPtAv7ggFM4h5mPs4n", "5C8QpXdeQgRg7CrbUkmca9QQQs4vBu8qnyacwt5hZ2FtyRVM", "5Cw8WWYSX2bDeffwgaFmUnijsy3eKgUREanZSKq95CfXG9V8", "5CX8iCf1PFgWgBswiXdgi3wYHu5eDYic7DGRvDVh9LGXYZnx", "5Egt4wshK5qoPJoY4711Pk3uX1WEXiKrYFo5s7XaqUtvJaLu", "5Egt4wshK5qoPJoY4711Pk3uX1WEXiKrYFo5s7XaqUtvJaLu", "5FQppbn4AUHYiS6XtwomHDd67VvsCzSysmzkrkEUuJq2KfHv", "5FgYvqEG9ue3tHJLUAhpRodBx3BXHccsDmQSDrT67EKCqbeo", "5DhhvZ8QZ1M4pm17uuBDw1usSw7eGM9mCLerix53v3nxp8z4", "5GENZ5KU2mpGTqNdt6oeobrJzBA11Dxn2649nuStf4dXZgRq", "5ETtwZML19jakzHYJe2Cu2ZTP2ndNTVp4N85bPz48QMwoJzM", "5H3oEExzj2sPe2MDXudMkDAPfzuXwB5LaYMUGwj3DH4Vgywf", "5F4Pwj3QvizdDq8RiQF4vrchHH6PfNYMoroMVFSZsXjsjoxf", "5ChmYFkyLTqhexnbFLWCkAMukmEmhfXWymSVNrF4BQVfrmSC", "5CcTN6Upzo8mgqj38KNi2QRTuUpZGqYPMzDKfgR68YQ61zKP", "5CAEY4RTDNQFFahiP9gyDCdHjo9cU2HAZHju6yWucgfrrmSC", "5G4UfZRng5zPmKMkGh42W1wEXyn2cvEaL9gPYszwX4LV55NU", "5EnyKmp6diJjkHbiuKGPAzFSKe2K2Ao5ftmzH25gYnMaPRoY", "5E1vqtFiwFvVLz3YYx6pLvHbGuyf224X2pAQU7bYAPfE2FVE", "5CXdz3nKzCYpYXxuvs2J49Y8k9iErh1pmYZGfmRUWb3mPVkM", "5CtdSmFBuur8bGQWcRyNe5nHG9pPYveNMnxg189qe1fUupnW", "5FHFj93RD9HoMqEwUWSQRoVwh3FCmYnQYzEuGbSmY5zfnRhf", "5DxGiM7RyZUZfMGJs8gziEK7Ts9P2EuRPaMKhnADDGnSirXk", "5GZmah9zNxZZ8pFBNPquvwYz5Nhvo7giGvbjnB1xN3uufhS8", "5EFUZKRkDANebjfR1xiuawmJgSkGYaBVKUdhtcryWuDTUCxP", "5FTuyXS15j48vAT42dEgs66JSzLPhmZ95vGjEebJ8b61uA8X", "5GWQibF5X1X99959Lxheydnwg89hYpJNnGwyAugPJxXC47t4", "5Df4WDpdJtfPwdXVaECiuQoAQdUhGKwXyrrMMmm6JBFhrHdh", "5HmWjutHqxFSH4kttKdAPuiqyd6XNuUWKQikvWZqtV8PYxEY", "5Engbqy2Mt2bj9wgZ5sY4YvLKVtt2SGFCiqP5tTYSopPLEFt","5CMcngJawjS8iCPrAfFLGdi4ag3fqYeK2qdZRQayp1dhQyz9","5GnPxouRnGdth2K5dCWev28afLwrxf1haqopLYEYkwj4D7DB","5GE6vuUoEs3JBos7bxV8cGSQkUty62wZCnBo4Xqjg6Qvvaxb","5EPboJyPmKnPYvL5sEriNmRZD76scDEZZsNWbmTz1RxNdcA8","5FjxQ1fPgbttCsA5CsB2roGGmaZei5cxV3TDNUPQ7mmhux4L","5DcsfsdU6T4c81R2xgS8e9gMaJK2iJfroycpuRQfhYG1KMQD","5HYhG3zrKTN1KcBaVizoZZPsjMvDZSiYFgTrwQZoFJGU6ZJ9","5DDYBkARBwVwiMkWphRKTfrBQ6LSzkH2eBQCAXJ5RZivS3bL","5H1cTQUrkCFVwYk2HutWEK8L83VdkoNWLpYBZJizpLn3NjqN","5CyLpWy6khibKUA9d11KDbdqEt5yfihLRewoJmYZjKXjRsNv","5DRumhq1Pwv86KQeb4cwaDGVwfMDrLrEZ2p9khqmiz2748az","5GGtwG1f5CrRAtjBvagS1brtmTQpmHoy2WzqD4ffkK4WrrBn","5HY3raTdUodu1zRReQBSxbKwYZtqSw71sB1H8UdLnn5FuvAA","5FqK94qHoUiVQiT5WR1a9WgerjZ3A1k5R8jR2Y8cFuqF11US","5HTe4giUHRdA8hgKytwdTR3xJorKH8P3CYYkmkRrhpmXPEkF","5CFgBHNMHiCpnooJ6joDPPQ3DSw8fUeXFMpG1AvzcmJxJRpr","5DwCWBuB8iF4o87fx5ZhzbQf2qyyDu71bnWE12aPh6qkmdvK","5DvVW6C3VwU8AdF8aPfNU5Wjpie3F4fBobHdnRZNcjp7wnQR","5D1yGcd8Lq3pGfVp8FKibJNAGMJKhTKm4DoHxN7DLEMonvub","5CG9nVmwgnC5SpjjTzdH9y2iG3TX7zhbs4nbPf3fnK9RQ6mA","5DfEiSySK3mwCT6CaXwvr3vuTC3dBMUKMWXXTmiNNj66zpuN","5EswHwwtTPDuhkbaTMXoEYjBZwumDVzgxTMjWXzEBncJ1Cjk", "5FjP8fFbMb6pEHfRZyRegsmwRUMDuLFNcaBu1TerWMPEKgNh", "5FnNaMjkPH6BEM9jdZXoGXfFKAbAq2Whh4kYtXoLE7Pitgdb", "5GenYL1aa6wwY6UhEx4aEP1SovVVcrWRv6LqbCeE9JrZX36H", "5GmmKv524RmeG1nDRuqLpjkRqNkNZnZf5fFWZAzQM3BQBxhe", "5GenYL1aa6wwY6UhEx4aEP1SovVVcrWRv6LqbCeE9JrZX36H", "5FqqXKb9zonSNKbZhEuHYjCXnmPbX9tdzMCU2gx8gir8Z8a5", "5GyDVXqfcXuKfMYk8oGK9hUvQHxttJoShLkhU8WuWBYYt9ak", "5Gdu3SSzmdDBgkCg9XbyN7dYUaSUaSTo2GbT2prgwYmNtPpo", "5HSpWhtMBQBmQE4AoZL91xdMuWTtG5MJBPkYhCC6n7CodhiJ", "5HHHHHzgLnYRvnKkHd45cRUDMHXTSwx7MjUzxBrKbY4JfZWn", "5FxqjWP4zutWm98WKVSmTANT2Dnw4F5xfRztSwmsy6m9yV77", "5DS527oHrT44NKyjQU8m9HBRc8YHta7dsKtcm4k9rQsExxg8", "5HYijYoBkCYmEZUasyr7vER36WpANHXEZfsfR4CcVtav6yLE", "5G4YtUfbHx1Wc8PFzktCT1DsF9vHyxCX6nDzNtUQzhfBjfb8", "5GBcsvxFzt6mjwtiKtHnSMQdAX3Ya4gRCa61Li28NkzNfC4i", "5HNQHYSMAmGf7U4Ac1FrMPXABbbh2CGUDLh6dFVjiDVhayyL", "5EcevSxSRrkpyWEsVFkTaFSbEctUBiZMakXiwkyyELmVqfWB", "5Gq2mhtv4RYVc6HSQ5hNMXLoAJmz6HbVo5XwexHYKojAwQVS", "5Gbo53EgDqfijRrEzFtZQdC71LSg2XJrA5NjegSqN46bCL9z", "5FkBJBKBFKwts5Samc5ppQrfUS4Secpp5vdw65R6wTq9RNUT", "5EHGTQ8ESCEwjMXrCzoVrXLiCpDyrSgZnZkncGgqFLoNVRuq", "5Cfbradw9xMQPQgdyfjDAjv8uYbGoUa7jeYBVeG5A1SfDiAr", "5EepovsYhN9nKnLnknCNxhTcKmsp9TLx6kXE1wDBjeCRvsAC", "5FCfTQkEBLe5rGUVeF6fh3MELz9WaHGvrnn9puEB7rnuB2Jq", "5EhoTqxDAozJ4RME4SJ9Rb9PAz86LWY2yo7g7wDfXKhPexha", "5H3BbMZmwiegRzKYLtJM6Tbp37EqyboF4LGLwHMaggWFrK7m", "5EvMDk46Cfu8ieaamxq9n34hWDqpY6zmQ8HbF45T6mCNjRti", "5EcevSxSRrkpyWEsVFkTaFSbEctUBiZMakXiwkyyELmVqfWB", "5CMg25T19X7k7qfvJxaqBjaaNehMn3JtiihRsQZpuKY5Zege", "5Da7Ey8QqUhcK66fpyybtYjeqX3rbxAiUvQ6geHnNmkPfJwk", "5Fe5xWUdumfp7XyfKWyPJJ8CwwEfsc4g1g45wmngUHZ8xzMt", "5HbHzJNM4GjSv8xbo6aHPxevk4MiLxX5Tw3NKWa2x4jHZmT7", "5D586a3WfXBCWVqNcLSKwgtqNboVH8s6zhLrjRMj5qNTtL4F", "5HbHYvSdwZu8vDUKFX4xNqMWmWZnzd1AGAc1tKs1HAzghhjv", "5EYx2ANtYkaKp8XBcE8xsx7MGkxaWcqwdHnrfWcyXGSJPQze", "5HSmYtpFC9eXKqT5JRMxGnHhwSVkM2W8vuukem51VZH3F5SF", "5HVTMRJFkwjLYA4Q6pNixZ5eu1qzcVc9XgVnySspRHjiKRNo", "5CoEw94gyMvpv8M9f38nkM1h33ZNMvD7JEm3mbHzEQgHEcFC", "5Hip4EFdchZ46GHidPPsDTfqppYwoeqAfkhNn2XK5Hh4eKNC", "5EHw4fGsBekyMfjYRjxhDqJt2EZigjVdx3A4RfiEMqvscYYv", "5DD21xF9ZUpEnGNFtU7GCpPoC8upW2YDEGp3hLySRELPDPiH", "5G9UpUj9yXFkHGn7TpuNkDvRDFoP9AHVkMqMPohSeao9Yob6", "5E4sL6arsPzCHyUwkcJxrQuPRQDbWTbGSyD2EVhzaMvmURjS", "5HjRUtDYfBEQ924qBT7Ab4c8CNG4Y88XKJ7uv1y2n5yMPwyy", "5HYhG3zrKTN1KcBaVizoZZPsjMvDZSiYFgTrwQZoFJGU6ZJ9", "5HVVJuJVTMMtxJMgtUWnKmWyr2kzudRGQqjYJzs6i47tfqa5", "5FEeGpPZLNv9vGBSGQvF6Lium3YonESfmKSGpAQ1BF2F68vc", "5F1LwiYpgLyZkN1kPKht1su2VQqETv9M2G39TTvVNDWSX9Yk", "5Ft2hk5JBxDACrTACWZjRPZquXQ41ymAUrKHpLjKurZd3CiM", "5CUJnQALBhS9BXE9sufg8WxNJV1bAcXXyutWJK4U5H8NFJhR", "5DeXvE8JgJ13Mq6axVJrzPPqfD6JRr4kMGjjraHBZNdJrY3y", "5Fe68QcGh3G1SfmVEXJqRbqLRqNDQkzG3u63vstTc6gqFtUm", "5E2BNp29y9zzowLz9otuETy2KLon8yWTPsUg63wCmDKzez7k", "5D2eqBdSEZYemHZsZD2pAGbgGVQwKSWgELFsiQQ1PiMu6GHz", "5FvSdNxAAZTJPMJDywzhKhAc65Vy5XiTQECxaUowGUWeGH7p", "5CfQudee6RBh1GQhJLnsrpoXmYjcRKh8dbX9bu8MPdAaYBR2", "5G6Xi8syEpSw4Q1J6pMVF2TLWeqcvXWDXH9wdaFYC9MkHgfh", "5C7L3Ef4fKEnpFaPDvrTwnaFkRfgAjDAj2WTqhTxNBt1N3Sy", "5HBxBDWi7XYrbM3JDCfjrPbk1p1o54iy7T44Ezpk6DsT51zM", "5EWp8TsgW7x9HeAXqgEGEsjV4SJ5hZ3sqp7wwq4TEGdgFNso", "5GpMKvhoBcvV2EspiLZjJYn1ny7H6sQxcKxPPaQvLEwpZhnd", "5He947y9k7bUGtGWCKG7Um5tRYtDtiWpYY9VYDN6g95vkhyo", "5HQoWzSHngxmVEAvskZ5yqFKzd6eq2pdNk6fSetjpaPrfBnB", "5FNdtnb4tQ8CZPNfMneV3jKwycCaAzMNmhHg9jecQRQGRCG1", "5Fe5xWUdumfp7XyfKWyPJJ8CwwEfsc4g1g45wmngUHZ8xzMt"]

    def connection_made(self, transport):
        print(f"Listening for pulses on port {self.port}...")

    def datagram_received(self, data, addr):
        self.recieved += 1
        if data == b'0' :
            self.monit_select = 0
        else :
            self.monit_select = 1
        if self.recieved % 120 == 0 :
            print("recieving.... on port")

    def error_received(self, exc):
        print(f"Error received: {exc}")

    def connection_lost(self, exc):
        print("Connection closed")
        if exc:
            print(f"Error: {exc}")

    async def run_client(self):
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: self,
            local_addr=('0.0.0.0', 18888),
            family=socket.AF_INET
        )
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            transport.close()

    def _load_addresses(self) :
        if not os.path.exists(self.log_file_path):
            return []
        try:
            with open(self.log_file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading addresses: {e}")
            return []

    def save_address(self, address: str) :
        if address not in self.addresses and address != None and address not in ("5CtxwMYHEJjhv1YGoz6FoxuPAZinWtxYrB7pJiyS6UW7Ghjy", "5GdpaARdm1Ton33P3gGer7mEfbpJQt8TdAkmS3AAVauVSffA") :
            hash_val = xxhash.xxh32(address).intdigest() & 0xFFFFF
            self.addresses.append(address)
            self.lst_ban_accounts[hash_val] = 1
            self._save_all_addresses()

    def remove_address(self, address: str, hash_val) :
        if address in self.addresses and address != None:
            print("removed address : ", address)
            self.addresses.remove(address)
            self.lst_ban_accounts[hash_val] = 0
            self._save_all_addresses()

    def _save_all_addresses(self) :
        try:
            with open(self.log_file_path, 'w') as f:
                json.dump(self.addresses, f, indent=2)
        except IOError as e:
            print(f"Error saving addresses: {e}")

    def _load_addresses_ban(self) :
        if not os.path.exists(self.log_ban_path):
            return []
        try:
            with open(self.log_ban_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading addresses: {e}")
            return []

    def save_address_ban(self, netuid) :
        if netuid not in self.ban :
            self.ban.append(netuid)
        self._save_all_addresses_ban()

    def _save_all_addresses_ban(self) :
        try:
            with open(self.log_ban_path, 'w') as f:
                json.dump(self.ban, f, indent=2)
        except IOError as e:
            print(f"Error saving addresses: {e}")

    def _load_addresses_danger(self) :
        if not os.path.exists(self.log_danger_path):
            return []
        try:
            with open(self.log_danger_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading addresses: {e}")
            return []

    def save_address_danger(self, address: str) :
        if address not in self.danger_accounts and address != None and address != "5CtxwMYHEJjhv1YGoz6FoxuPAZinWtxYrB7pJiyS6UW7Ghjy":
            print("Danger Address : ", address)
            hash_val = xxhash.xxh32(address).intdigest() & 0xFFFFF
            self.danger_accounts.append(address)
            self.lst_danger_accounts[hash_val] = 1
            self._save_all_addresses_danger()

    def _save_all_addresses_danger(self) :
        try:
            with open(self.log_danger_path, 'w') as f:
                json.dump(self.danger_accounts, f, indent=2)
        except IOError as e:
            print(f"Error saving addresses: {e}")

    def _load_addresses_danger2(self) :
        if not os.path.exists(self.log_danger_path2):
            return []
        try:
            with open(self.log_danger_path2, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading addresses: {e}")
            return []

    def save_address_danger2(self, address: str) :
        if address not in self.danger_accounts2 and address != None and address not in self.huge_staked_account :
            print("Danger Address Special : ", address)
            hash_val = xxhash.xxh32(address).intdigest() & 0xFFFFF
            self.danger_accounts2.append(address)
            self.really_danger_accounts.append(address)
            self.lst_danger_accounts2[hash_val] = 1
            self._save_all_addresses_danger2()

    def _save_all_addresses_danger2(self) :
        try:
            with open(self.log_danger_path2, 'w') as f:
                json.dump(self.danger_accounts2, f, indent=2)
        except IOError as e:
            print(f"Error saving addresses: {e}")

    def _load_addresses_new(self) :
        if not os.path.exists(self.log_new_account_path):
            return []
        try:
            with open(self.log_new_account_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading addresses: {e}")
            return []

    def save_address_new(self, block_number, address: str) :
        self.new_accounts.append((block_number, address))
        self.lst_new_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1
        self._save_all_addresses_new()

    def remove_address_new(self, address: str, hash_val) :
        for new_account_data in self.new_accounts :
            block_number, add = new_account_data
            if add == address :
                self.lst_new_accounts[hash_val] = 0
                self.new_accounts.remove(new_account_data)
                self._save_all_addresses_new()
                return

    def _save_all_addresses_new(self) :
        try:
            with open(self.log_new_account_path, 'w') as f:
                json.dump(self.new_accounts, f, indent=2)
        except IOError as e:
            print(f"Error saving addresses: {e}")

    def _load_addresses_pending(self) :
        if not os.path.exists(self.log_pending_account_path):
            return []
        try:
            with open(self.log_pending_account_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading addresses: {e}")
            return []

    def save_address_pending(self, block_number, address: str) :
        self.pending_accounts.append((block_number, address))
        self.lst_pending_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1
        self._save_all_addresses_pending()

    def _save_all_addresses_pending(self) :
        try:
            with open(self.log_pending_account_path, 'w') as f:
                json.dump(self.pending_accounts, f, indent=2)
        except IOError as e:
            print(f"Error saving addresses: {e}")

    def _load_bots(self) :
        if not os.path.exists(self.log_bots_path):
            return []
        try:
            with open(self.log_bots_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading addresses: {e}")
            return []

    async def check_bot(self, address: str) :
        print("bot checking... ", address)
        balance = await self.subtensor.get_balance(address)
        stakes = await self.get_stakes(address, False)
        tao_bal = balance.tao + stakes[0] / 1000000000.0
        stake_flg = 0
        add_hash = xxhash.xxh32(address).intdigest() & 0xFFFFF

        if self.lst_danger_accounts[add_hash] :
            return True

        for i in range(1, self.subnet_lim) :
            if 1.0 * self.tao_in[i] / self.alpha_in[i] * stakes[i] > 2000000000 :
                stake_flg += 1
                tao_bal += 1.0 * self.tao_in[i] / self.alpha_in[i] * stakes[i] / 1000000000.0

        if tao_bal < 8 :
            print("low balane")
            return False
        if tao_bal > 110 :
            print("High balane")
            return False
        if stake_flg == 0 or stake_flg > 2:
            print("No staking bot")
            return False
        return True  

    async def save_bot(self, address: str) :
        if address in self.not_bot :
            return
        if await self.check_bot(address) == False :
            return
        temp = []
        for bot in self.bot_accounts :
            block, add = bot
            if add != address :
                temp.append(bot)
        temp.append((self.current_block, address))
        self.bot_accounts = temp
        self._save_all_bots()

    def _save_all_bots(self) :
        try:
            with open(self.log_bots_path, 'w') as f:
                json.dump(self.bot_accounts, f, indent=2)
        except IOError as e:
            print(f"Error saving addresses: {e}")

    async def reload_bots(self) :
        temp = []
        for account in self.bot_accounts :
            block_number, bot = account
            if block_number > self.current_block - 50 :
                if await self.check_bot(bot) :
                    temp.append(account)
        self.bot_accounts = temp
        self._save_all_bots()
        print("Bots :")
        for account in self.bot_accounts :
            print(" ", account)


    def hex_to_ss58(self, hex_string, ss58_format=42):
        if hex_string.startswith('0x'):
            hex_string = hex_string[2:]
        
        keypair = Keypair(
            public_key=bytes.fromhex(hex_string),
            ss58_format=ss58_format
        )
        return keypair.ss58_address

    async def check_substrate(self, substrate) :
        try :
            await asyncio.wait_for(substrate.rpc_request("author_pendingExtrinsics", []), timeout=1)
            subtensor = AsyncSubtensor(substrate.url)
            block = await subtensor.get_current_block()
            if block > 6461461 and block < 7000000 :
                return True
            return False
        except Exception as e :
            return False

    async def init_param(self):
        self.substrate_arc = AsyncSubstrateInterface(url="wss://archive.chain.opentensor.ai:443")
        self.monitor_evm = AsyncSubstrateInterface(url="wss://evm.chain.opentensor.ai:443", use_remote_preset=True,)
        self.monitor_private = AsyncSubstrateInterface(url="wss://private.chain.opentensor.ai:443", use_remote_preset=True,)
        self.monitor_local = AsyncSubstrateInterface(url="ws://127.0.0.1:9944", use_remote_preset=True,)
        base_url = "wss://hz-lite{}.chain.opentensor.ai:443"
        for i in range (1, 21) :
            if i != 15 :
                self.monitor_finney.append(AsyncSubstrateInterface(url=base_url.format(i), use_remote_preset=True,))

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
            if await self.check_substrate(fast_substrates[i * 4 + self.monit_select]) :
                self.subtensor_block.append(AsyncSubtensor(network = fast_substrates[i * 4 + self.monit_select].url))

        good_nodes = []
        for substrate in good_substrates :
            if await self.check_substrate(substrate) :
                if substrate.url == "ws://178.156.196.61:9944" and self.wallet_select == 0 and self.monit_select == 0 :
                    continue
                if substrate.url == "ws://178.156.152.192:9944" and self.wallet_select == 1 and self.monit_select == 0 :
                    continue
                good_nodes.append(substrate)
            else :
                print(substrate.url)

        random.seed(self.monit_select * 4 + self.wallet_select)
        self.substrate_submit.append(AsyncSubstrateInterface(url = "ws://5.161.103.8:9944", use_remote_preset=remote_preset,))
        self.substrate_submit = random.sample(good_nodes, 5)
        self.substrate_submit.append(self.monitor_private)

        if await self.check_substrate(self.monitor_local) :
            print("local")
            if self.monit_select > 0 :
                self.substrate_submit.insert(0, self.monitor_local)

        self.subtensor = AsyncSubtensor(network = self.substrate_submit[0].url)
        self.substrate0 = SubstrateInterface(url = self.substrate_submit[0].url)
        self.substrate = self.substrate_submit[0]

        self.addresses = self._load_addresses()
        self.ban = self._load_addresses_ban()
        print("Ban Netuids :")
        print(self.ban)

        self.danger_accounts = self._load_addresses_danger()
        self.danger_accounts2 = self._load_addresses_danger2()
        for account in self.huge_staked_account :
            if account in self.danger_accounts2 :
                self.danger_accounts2.remove(account)

        print(len(self.addresses))

        for i in range(0, self.subnet_lim) :
            self.add_accounts.append("")
            self.removed_balance.append(0)

        for address in self.danger_accounts :
            self.lst_danger_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1

        for address in self.danger_accounts2 :
            self.lst_danger_accounts2[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1

        for address in self.addresses :
            self.lst_ban_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1

        for address in self.account_namsu :
            self.lst_ban_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1
            if address not in self.addresses :
                self.addresses.append(address)
        for address in self.delay_account :
            self.lst_ban_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1
            if address not in self.addresses :
                self.addresses.append(address)
        for address in self.lst_bots :
            self.lst_ban_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1
            if address not in self.addresses :
                self.addresses.append(address)
        self._save_all_addresses()

        for address in self.mev_bot :
            self.lst_mev_bot[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1            

        for i in range(self.subnet_lim) :
            self.lst_last_block.append(0)
            self.cfg_stakes.append(0)
            self.danger_staked.append(0)

        saved_new_accounts = self._load_addresses_new()
        current_block = await self.substrate.get_block_number(None)
        for account in saved_new_accounts :
            block_number, address = account
            if block_number > current_block - 50000 :
                self.new_accounts.append(account)
                self.lst_new_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1
        self._save_all_addresses_new()

        saved_pending_accounts = self._load_addresses_pending()
        for account in saved_pending_accounts :
            block_number, address = account
            if block_number > current_block - 50000 :
                self.pending_accounts.append(account)
                self.lst_pending_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1
        self._save_all_addresses_pending()

        for account in self.pre_calc :
            await self.get_stakes(account)

        self.bot_accounts = self._load_bots()
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
        await self.reload_bots()

        for account in self.danger_accounts2 :
            balance = await self.get_total_balance(account)
            if balance > 5 :
                self.really_danger_accounts.append(account)

        print("really danger accounts")
        for account in self.really_danger_accounts :
            print(account)

        await self.substrate.init_runtime()
        if self.wallet_select == 0 :
            with open("/root/.bittensor/wallets/pw.json", "r") as f:
                passwords = json.load(f)
            self.wallet = bt.wallet(name="real2", path="~/.bittensor/wallets")
            self.proxy_wallet = bt.wallet(name=self.proxies[self.monit_select], path="~/.bittensor/wallets")
        else :
            with open("/root/.real/wallets/pw.json", "r") as f:
                passwords = json.load(f)
            self.wallet = bt.wallet(name="real", path="~/.real/wallets")
            self.proxy_wallet = bt.wallet(name=self.proxies[self.monit_select], path="~/.real/wallets")
        self.proxy_keypair = self.proxy_wallet.get_coldkey(password = passwords["proxy_wallet_password"][:-3])
        self.account_id = f"0x{self.proxy_keypair.public_key.hex()}"
        self.meta = self.substrate.runtime.metadata
        self.genesis_hash = await self.substrate.get_block_hash(0)
        for i in range(self.subnet_lim) :
            self.limit_stakings.append(self.stake_lim)
            self.result_extrinsic.append(None)
            self.result_extrinsic2.append(None)
        print("done!")
        self.base_call_proxy = self.substrate.runtime_config.create_scale_object(type_string="Call", metadata=self.meta)
        self.base_call_proxy2 = self.substrate.runtime_config.create_scale_object(type_string="Call", metadata=self.meta)
        self.base_extrinsic = self.substrate.runtime_config.create_scale_object(type_string="Extrinsic", metadata=self.meta)
        self.nonce = await self.substrate.get_account_nonce(self.proxy_wallet.coldkeypub.ss58_address)
        for i in range(self.subnet_lim) :
            self.lst_bot_staked.append(0)
        await self.init_block(True)
        await self.process_unstake(100)

    async def get_total_balance(self, contact_add, reuse_dic = True) :
        balance_info = await self.subtensor.get_balance(contact_add)
        balance = balance_info.tao
        stakes = await self.get_stakes(contact_add, reuse_dic)
        for i in range(self.subnet_lim) :
            balance += stakes[i] * self.lst_price[i] / 1000000000.0
        return balance

    async def get_stakes(self, contact_add, reuse_dic = True) :
        rao = []
        for i in range(self.subnet_lim) :
            rao.append(0)

        if reuse_dic and contact_add in self.staking_dic :
            for netuid in range(self.subnet_lim) :
                rao[netuid] = self.staking_dic[contact_add][netuid]
        else :
            try :
                delegations = await self.subtensor.get_stake_for_coldkey(coldkey_ss58=contact_add,)
            except Exception as e:
                return rao
            for record in delegations :
                if record.netuid < self.subnet_lim :
                    rao[record.netuid] += record.stake.rao
            self.staking_dic[contact_add] = []
            self.staking_dic[contact_add].clear()
            for netuid in range(self.subnet_lim) :
                self.staking_dic[contact_add].append(rao[netuid])

        py_list = [rao[i] for i in range(self.subnet_lim)]
        return py_list

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
            self.nonce = await self.substrate.get_account_nonce(self.proxy_wallet.coldkeypub.ss58_address)
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
            self.nonce = await self.substrate.get_account_nonce(self.proxy_wallet.coldkeypub.ss58_address) + 1
            await asyncio.sleep(4)
            await self.unstaking_process()

        for i in range(self.subnet_lim) :
            self.removed_balance[i] = 0

        print(f"Block     : {self.current_block}")


        await self.substrate.init_runtime()
        self.meta = self.substrate.runtime.metadata
        self.base_call_proxy = self.substrate.runtime_config.create_scale_object(type_string="Call", metadata=self.meta)
    
        if self.Block_Staked == 0 :
            self.nonce = await self.substrate.get_account_nonce(self.proxy_wallet.coldkeypub.ss58_address)

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

        cur_staked = await self.get_stakes(self.wallet.coldkeypub.ss58_address, False)

        self.staked_flg = False
        for i in range(self.subnet_lim) :
            if cur_staked[i] > 1000000 :
                self.staked_flg = True
                break

        if self.staked_flg == False :
            self.Block_Staked = 0
        elif self.Block_Staked == 0 :
            self.nonce = await self.substrate.get_account_nonce(self.proxy_wallet.coldkeypub.ss58_address)
            await self.unstaking_process()
            self.Block_Staked = 1

        block_hash = self.substrate0.get_chain_head()
        events = self.substrate0.get_events(block_hash)
        self.block_hash_current = await self.substrate.get_block_hash( block_id=self.current_block )
        self.block_hashs.append((self.current_block, self.block_hash_current))
        while len(self.block_hashs) > 5 :
            self.block_hashs.pop(0)

        if self.current_block % 7200 == 0 :
            self.new_accounts.clear()
            self.lst_new_accounts = array.array('b', [0]) * 1048576
            saved_new_accounts = self._load_addresses_new()
            for account in saved_new_accounts :
                block, address = account
                if block > self.current_block - 70000 :
                    self.new_accounts.append(account)
                    self.lst_new_accounts[xxhash.xxh32(address).intdigest() & 0xFFFFF] = 1
            self._save_all_addresses_new()

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

        for i in range(self.subnet_lim) :
            self.limit_stakings[i] = self.get_limit(i)

        for event in events:
            if event.value['event_id'] == 'NewAccount':
                new_address = event.value['event']['attributes']['account']
                balance = await self.subtensor.get_balance(new_address)
                if balance.tao < 100 :
                    self.save_address_new(self.current_block, new_address)

        cur_balance = await self.subtensor.get_balance(self.wallet.coldkeypub.ss58_address)
        balance = cur_balance.tao

        staked_bal = float(cur_staked[0]) / 1000000000.0
        if self.staked_flg :
            for i in range(1, self.subnet_lim) :
                if cur_staked[i] > 1000 and self.alpha_in[i] > 1 : 
                    slipage = 1.0 * (self.alpha_in[i] + float(cur_staked[i]) / 1000000000.0) / self.alpha_in[i]
                    staked_bal += self.lst_price[i] * float(cur_staked[i]) / 1000000000.0
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

        if self.current_block % 99 == 0 :
            await self.reload_bots()
        full_block = self.substrate0.get_block(block_number=self.current_block)
        # full_block = await self.substrate_arc.get_block(block_number=6201050)
        if full_block and 'extrinsics' in full_block:
            self.updated_accounts.clear()
            start_time = time.perf_counter()
            await self.process_full_block(full_block, danger_flg)

            if block_staked :
                if self.Block_Staked == 0 :
                    if self.balance != 0 :
                        if self.balance > balance + 0.07 and self.not_ban:
                            if self.last_address in self.flaged_address :
                                self.save_address(self.last_address)
                            else :
                                self.flaged_address.append(self.last_address)

        cfg_stakes = await self.get_stakes(self.account_cfg, False)
        fff_stakes = await self.get_stakes(self.account_fff, False)
        ddd_stakes = await self.get_stakes(self.account_ddd, False)
        h1x_stakes = await self.get_stakes(self.account_h1x, False)
        for i in range(self.subnet_lim) :
            self.lst_bot_staked[i] = 0
            # self.danger_staked[i] = epk_stakes[i]
            self.danger_staked[i] = 0
            self.cfg_stakes[i] = max(cfg_stakes[i], fff_stakes[i])
            self.cfg_stakes[i] = max(self.cfg_stakes[i], ddd_stakes[i])
            self.cfg_stakes[i] = max(self.cfg_stakes[i], h1x_stakes[i])

        for delay_account in self.delay_account :
            delay_stakes = await self.get_stakes(delay_account)
            # epk_stakes = await self.get_stakes(self.account_epk)
            for i in range(self.subnet_lim) :
                self.cfg_stakes[i] += delay_stakes[i]

        danger_accounts_real = []
        remove_danger_accounts = []
        new_pending = []
        lst_danger = self.really_danger_accounts
        for account in self.really_danger_accounts :
            if account not in danger_accounts_real :
                danger_accounts_real.append(account)
                staked_info = await self.get_stakes(account, False)
                balance_tao = await self.subtensor.get_balance(account)
                balance = balance_tao.tao
                cnt = 0
                for i in range(self.subnet_lim) :
                    if self.danger_staked[i] < staked_info[i] :
                        self.danger_staked[i] = staked_info[i]
                    balance += staked_info[i] * self.lst_price[i] / 1000000000.0
                    if i > 0 and staked_info[i] > 100000000000 :
                        cnt += 1
                if balance < 5 or cnt > 3 :
                    if account != '5EC7StAPcUuR3STRvUEDph2LDmQgyELrLiz5sjz5APieyJLw':
                        if account in self.pending_remove :
                            remove_danger_accounts.append(account)
                        if account not in new_pending :
                            new_pending.append(account)
        self.pending_remove = new_pending

        staked_5fkf = await self.get_stakes("5FKfQ3hnVM1tkUMk4sDQw659yzwsHdqJvT25Mz452qic2x1n", False)
        staked_5gul = await self.get_stakes("5GuLYhyfPPMRqu9j57FUBLvQgx3wDjgL3WvqoyKnLjpuYeET", False)
        for i in range(self.subnet_lim) :
            if staked_5fkf[i] > 10000000 : 
                if self.danger_staked[i] < staked_5fkf[i] + staked_5gul[i] :
                    self.danger_staked[i] = staked_5fkf[i] + staked_5gul[i]

        print("danger accounts real")
        for account in danger_accounts_real :
            print(account)

        for account in remove_danger_accounts :
            self.really_danger_accounts.remove(account)

        for bot in self.lst_bots :
            staked_info = await self.get_stakes(bot)
            for i in range(self.subnet_lim) :
                if self.lst_bot_staked[i] < staked_info[i] :
                    self.lst_bot_staked[i] = staked_info[i]

        for account in self.bot_accounts :
            block_number, bot = account
            if bot not in self.lst_bots :
                staked_info = await self.get_stakes(bot)
                for i in range(self.subnet_lim) :
                    if self.lst_bot_staked[i] < staked_info[i] :
                        self.lst_bot_staked[i] = staked_info[i]


        if self.current_block % 50 == 0 :
            self.list_chk_ext = array.array('b', [0]) * 1048576
        for i in range(256) :
            self.list_chk_acc[i] = 0

        for netuid in range(self.subnet_lim) :
            proxy_call = self.substrate.runtime_config.create_scale_object(type_string="Call", metadata=self.meta)
            proxy_call.encode(
                {
                    "call_module": "SubtensorModule",
                    "call_function": "add_stake_limit",
                    "call_args": {
                        "hotkey": self.hotkey,
                        "netuid": netuid,
                        "limit_price" : self.calc_limit(netuid, self.limit_stakings[netuid]),
                        "amount_staked": int(self.limit_stakings[netuid] * 1000000000),
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
                        "hotkey": self.hotkey,
                        "netuid": netuid,
                        "limit_price" : self.calc_limit2(netuid, self.limit_stakings[netuid]),
                        "amount_staked": int(self.limit_stakings[netuid] * 1000000000),
                        "allow_partial": False,
                    },
                }
            )
            self.result_extrinsic[netuid] = self.create_extrinsic(proxy_call, self.finalized_block, self.block_hash)
            self.result_extrinsic2[netuid] = self.create_extrinsic(proxy_call2, self.finalized_block, self.block_hash)

        last_time = time.perf_counter()
        print("Delay:", last_time - start_time)

        self.block_initializing = False

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

    async def process_full_block(self, full_block, danger_flg) :

        stake_flg = False
        self.not_ban = False
        for idx, extrinsic in enumerate(full_block['extrinsics']):
            call = extrinsic['call']
            call_function = call['call_function']['name']
            str_call = str(extrinsic)
            if 'liquidity' in str_call or 'modify_position' in str_call or 'set_fee_rate' in str_call :
                call_function0, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount, target_address, transfer_amount = await self.process_call_str(call)
                if self.owner_coldkeys[netuid] in str_call :
                    print(f"Ban Netuid : {netuid}")
                    self.save_address_ban(netuid)
            if call_function not in ('add_stake', 'add_stake_limit', 'proxy', 'batch_all', 'force_batch', 'batch', 'swap_stake', 'swap_stake_limit', 'transfer_allow_death', 'transfer_keep_alive', 'transfer_all', 'remove_stake', 'remove_stake_limit', 'unstake_all', 'transfer_stake', 'unstake_all_alpha') :
                continue
            era = extrinsic['era']
            era_period = 100
            
            real_account = extrinsic['address'].value
            real_hash = xxhash.xxh32(real_account).intdigest() & 0xFFFFF

            if call_function != 'proxy' :
                self.updated_accounts.append(extrinsic['address'].value)

            if era == '00':
                era_period = 100
            elif hasattr(era, 'value'):
                era_data = era.value
                if isinstance(era_data, tuple) and len(era_data) >= 2:
                    era_period = era_data[0]

            if extrinsic['address'].value == self.proxy_wallet.coldkeypub.ss58_address :
                stake_flg = True
                real_account, (call_function, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount) = await self.process_proxy_call_str(call)
                self.last_netuid = netuid
                continue

            if call_function in ('add_stake', 'add_stake_limit', 'swap_stake', 'swap_stake_limit') :
                call_function0, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount, target_address, transfer_amount = await self.process_call_str(call)
                real_account = extrinsic['address'].value
                if amount_staked == None :
                    amount_staked = alpha_amount
                if amount_staked == None :
                    amount_staked = 0

                add_hash = xxhash.xxh32(real_account).intdigest() & 0xFFFFF
                nuid = netuid
                if call_function in ('swap_stake', 'swap_stake_limit') :
                    nuid = netuid2
                if ((self.lst_ban_accounts[add_hash] or self.lst_new_accounts[add_hash] or self.lst_pending_accounts[add_hash]) and (era_period == 4 or amount_staked < 4000000000 or self.lst_price[nuid] < 0.0015)) or self.lst_danger_accounts[add_hash] :
                    await self.save_bot(real_account)

                if stake_flg and danger_flg and netuid1 == self.last_netuid :
                    self.save_address_danger(real_account)

            elif call_function in ('remove_stake', 'remove_stake_limit', 'unstake_all', 'unstake_all_alpha') :
                call_function0, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount, target_address, transfer_amount = await self.process_call_str(call)
                real_account = extrinsic['address'].value
                if stake_flg and danger_flg :
                    if call_function in ('unstake_all', 'unstake_all_alpha') :
                        if await self.detect_stake(real_account, self.last_netuid, self.current_block - 1) :
                            self.save_address_danger(real_account)
                    else :
                        if netuid == self.last_netuid and amount_unstaked > 10000000000 :
                            self.save_address_danger(real_account)

            elif call_function in ('transfer_allow_death', 'transfer_keep_alive', 'transfer_all') :
                call_function0, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount, target_address, transfer_amount = await self.process_call_str(call)
                real_account = extrinsic['address'].value

                real_hash = xxhash.xxh32(real_account).intdigest() & 0xFFFFF
                target_hash = xxhash.xxh32(target_address).intdigest() & 0xFFFFF

                if transfer_amount == None :
                    continue

                if real_account in self.huge_accounts and transfer_amount >= 10000000000 :
                    self.save_address_pending(self.current_block, target_address)
                elif self.lst_danger_accounts2[real_hash] and transfer_amount >= 1000000000 and target_address not in self.huge_accounts and target_address not in self.huge_staked_account :
                    self.save_address_danger2(target_address)
                elif self.lst_danger_accounts[real_hash] and transfer_amount >= 3000000000 and target_address not in self.huge_accounts :
                    self.save_address_danger(target_address)
                if transfer_amount >= 100000000000 :
                    if self.lst_danger_accounts2[target_hash] == 0 :
                        if self.lst_ban_accounts[target_hash] == 1 :
                            self.remove_address(target_address, target_hash)
                        if self.lst_new_accounts[target_hash] == 1 :
                            self.remove_address_new(target_address, target_hash)

            elif call_function != 'proxy' and era_period == 4 and call_function != 'transfer_stake' :
                call_function0, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount, target_address, transfer_amount = await self.process_call_str(call)
                real_account = extrinsic['address'].value
                self.updated_accounts.append(real_account)

                add_hash = xxhash.xxh32(real_account).intdigest() & 0xFFFFF
                if self.lst_ban_accounts[add_hash] or self.lst_new_accounts[add_hash] or self.lst_danger_accounts[add_hash] or self.lst_pending_accounts[add_hash] :
                    await self.save_bot(real_account)

            elif call_function == 'proxy' :
                real_account, (call_function, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount) = await self.process_proxy_call_str(call)
                if amount_staked == None :
                    amount_staked = alpha_amount
                if amount_staked == None :
                    amount_staked = 0

                if call_function in ('batch_all', 'force_batch', 'batch') :
                    add_hash = xxhash.xxh32(real_account).intdigest() & 0xFFFFF
                    if self.lst_ban_accounts[add_hash] or self.lst_new_accounts[add_hash] or self.lst_danger_accounts[add_hash] or self.lst_pending_accounts[add_hash] :
                        await self.save_bot(real_account)

                elif call_function in ('add_stake', 'add_stake_limit', 'swap_stake', 'swap_stake_limit') and (era_period == 4 or amount_staked < 4000000000) :
                    add_hash = xxhash.xxh32(real_account).intdigest() & 0xFFFFF
                    if self.lst_ban_accounts[add_hash] or self.lst_new_accounts[add_hash] or self.lst_danger_accounts[add_hash] or self.lst_pending_accounts[add_hash] :
                        await self.save_bot(real_account)
                    if call_function == 'swap_stake' and netuid1 == self.last_netuid and netuid2 == 0 and real_account == "5GuLYhyfPPMRqu9j57FUBLvQgx3wDjgL3WvqoyKnLjpuYeET" :
                        self.not_ban = True

                if "transfer_stake" in str(extrinsic) :
                    call_function0, netuid1, netuid2, alpha_amount, target_address = await self.process_transfer_str(call)
                    real_hash = xxhash.xxh32(real_account).intdigest() & 0xFFFFF
                    if self.lst_danger_accounts2[real_hash] :
                        self.save_address_danger2(target_address)
                    self.updated_accounts.append(target_address)
                    await self.save_bot(target_address)

            elif call_function  in ('batch_all', 'force_batch', 'batch') :
                real_account = extrinsic['address'].value
                ext_str = str(extrinsic)
                netuid_str = str(self.last_netuid) + "}"

                if "swap_stake" in ext_str or "add_stake" in ext_str :
                    await self.save_bot(real_account)

                if "unstake_all" in ext_str and stake_flg and danger_flg :
                    if await self.detect_stake(real_account, self.last_netuid, self.current_block - 1) :
                        self.save_address_danger(real_account)

                if "remove_stake" in ext_str and netuid_str in ext_str and stake_flg and danger_flg :
                    self.save_address_danger(real_account)

                if "transfer_stake" in ext_str :
                    real_hash = xxhash.xxh32(real_account).intdigest() & 0xFFFFF
                    if self.lst_danger_accounts2[real_hash] :
                        self.save_address_danger2(target_address)
                    call_function0, netuid1, netuid2, alpha_amount, target_address = await self.process_transfer_str(call)
                    self.updated_accounts.append(target_address)
                    await self.save_bot(target_address)

            elif call_function == "transfer_stake" :
                call_function0, netuid1, netuid2, alpha_amount, target_address = await self.process_transfer_str(call)
                real_account = extrinsic['address'].value
                self.updated_accounts.append(target_address)
                real_hash = xxhash.xxh32(real_account).intdigest() & 0xFFFFF
                if self.lst_danger_accounts2[real_hash] :
                    self.save_address_danger2(target_address)
                await self.save_bot(target_address)

    def get_limit(self, netuid) :
        if self.tao_in[netuid] < 500 :
            return self.stake_lim3
        elif self.tao_in[netuid] < 5000 :
            return  self.stake_lim2
        return self.stake_lim

    async def unstaking_process(self) :
        await self.substrate.init_runtime()
        self.meta = self.substrate.runtime.metadata                      
        self.base_call_proxy = self.substrate.runtime_config.create_scale_object(type_string="Call", metadata=self.meta)
        self.current_block = await self.subtensor.get_current_block()
        self.finalized_block = self.current_block - 2
        self.block_hash = await self.substrate.get_block_hash( block_id=self.finalized_block )
        cnt = 2
        while await self.Unstake(4, 20000) == False and cnt > 0 :
            cnt -= 1
            await asyncio.sleep(0.2)

    async def process_cancel(self) :
        print("cancelling...")
        try :
            await self.rpc_request(self.substrate_submit[0], "author_submitExtrinsic", [str(self.cancel_extrinsic.data)], self.block_hash)
        except Exception as e: 
            print("cancel error")
        
    async def process_stake(self, contact_add, netuid, amount, limit_price, tip, source_netuid = -1, batch_flg = False) :
        add_hash = xxhash.xxh32(contact_add).intdigest() & 0xFFFFF
        if netuid != 0 :
            amount_origin = amount
            print(contact_add, netuid, amount)
        if netuid == 0 or self.Block_Staked > 1 or self.never_stake or self.staked_flg or netuid in self.ban or self.block_initializing or self.lst_danger_accounts2[add_hash] or self.danger_staked[netuid] * self.lst_price[netuid] > 9900000000 or batch_flg:
            return False

        amount_staked = self.get_limit(netuid)
        remove_val_limit = 17000000000
        if self.tao_in[netuid] > 50000 :
            remove_val_limit = 49000000000
        elif self.tao_in[netuid] < 300 :
            remove_val_limit = 5000000000
        remove_val = 0
        cfg_staked_val = 0
        tao_in = 0
        alpha_in = 0
        if netuid < self.subnet_lim :
            remove_val = self.lst_bot_staked[netuid] * self.lst_price[netuid]
            if remove_val > remove_val_limit :
                remove_val = remove_val_limit
            if remove_val < (self.removed_balance[netuid] + self.danger_staked[netuid]) * self.lst_price[netuid]:
                remove_val = (self.removed_balance[netuid] + self.danger_staked[netuid]) * self.lst_price[netuid]
            cfg_staked_val = self.cfg_stakes[netuid] * self.lst_price[netuid]
            tao_in = self.tao_in[netuid]
            alpha_in = self.alpha_in[netuid]

        if tao_in > alpha_in or tao_in < 30:
            return False

        if amount > 99000000000 :
            remove_val = 0
        if amount < remove_val + 100000000 :
            return False

        amount_tao = float(amount) / 1000000000.
        if amount_staked < amount_tao :
            amount_staked = amount_tao
        if amount < cfg_staked_val + 100000000 :
            amount_staked *= 0.1
        if amount_staked > self.stake_lim :
            amount_staked = self.stake_lim
        if amount_staked > self.remain_balance :
            amount_staked = self.remain_balance
        amount0 = amount

        amount -= remove_val

        if limit_price != None :
            limit_stake = (float(limit_price) / 1000000000. / self.lst_price[netuid] - 1) * 0.49 * self.tao_in[netuid] - float(amount0) / 1000000000.
            limit_stake *= 0.9
            if amount_staked > limit_stake :
                amount_staked = limit_stake

        if amount_staked < 0.01:
            return False

        slipage = 1.0 * (tao_in + amount_staked) / tao_in + 0.0005
        amount_alpha = amount_staked / self.lst_price[netuid] / slipage
        reward = 2 * amount_tao * amount_staked / tao_in - amount_staked * 0.001

        taoT = float(tao_in + amount_staked)
        if tao_in > 500 :
            if self.monit_select == 0 :
                taoT += 1

        limit = self.calc_limit(netuid, amount_staked)
        if amount_tao > 49 or reward > 1 :
            limit = self.calc_limit2(netuid, amount_staked)

        print(netuid, amount_tao, reward)

        if reward > 0.01 and amount_tao > amount_staked * 0.02 and amount_tao > 0.1 and amount_alpha > 10 and amount_staked > 1:
            start_time = time.perf_counter()
            self.Block_Staked = 2
            self.last_netuid = netuid
            if await self.AddStake(int(amount_staked * 1000000000), netuid, limit, 4, tip) :
                if batch_flg == False :
                    if source_netuid == -1 :
                        balance = await self.subtensor.get_balance(contact_add)
                        if balance.rao < amount_origin :
                            print(balance.rao, amount_origin)
                            await self.process_cancel()
                    if source_netuid >= 0 :
                        stakes = await self.get_stakes(contact_add, False)
                        if stakes[source_netuid] < amount_origin / self.lst_price[source_netuid] :
                            await self.process_cancel()

                self.remain_balance -= amount_staked
                print(time.perf_counter() - start_time)
                self.last_block = self.current_block
                self.last_add_hash = add_hash
                self.last_address = contact_add
                self.last_staked_amount = amount_origin / self.lst_price[netuid]
                self.swap_extrinsic = None
                self.unstake_extrinsic = None
                self.unstaked_all_alpha = False
                print("Staked! ", contact_add, netuid, amount_tao, limit_price, amount_staked, int(limit * 1000000000), reward)
                next_finalized_block = self.current_block - 1
                next_hash = 0
                flg = False
                for e in self.block_hashs :
                    (n, h) = e
                    if n == next_finalized_block :
                        next_hash = h
                        flg = True
                        break

                if flg == False :
                    next_hash = await self.substrate.get_block_hash( block_id=next_finalized_block )

                proxy_call_swap = self.substrate.runtime_config.create_scale_object(type_string="Call", metadata=self.meta)
                proxy_call_swap.encode(
                    {
                        "call_module": "SubtensorModule",
                        "call_function": "unstake_all_alpha",
                        "call_args": {
                            "hotkey": self.hotkey,
                        },
                    }
                )
                self.swap_extrinsic = self.create_extrinsic(proxy_call_swap, next_finalized_block, next_hash, 0)
                self.unstake_all_alpha_flg = True
                self.next_hash = next_hash

            else :
                self.Block_Staked = 0

    async def process_unstake_all_alpha(self) :
        while True :
            await asyncio.sleep(0.5)
            current_time = time.perf_counter()
            if current_time > self.start_time + 11 and self.unstake_all_alpha_flg :
                print("Unstaking...")
                await self.unstake_all_alpha(self.next_hash)

    async def process_unstake(self, era_period) :
        cnt = 10
        while cnt > 0 :
            if await self.UnstakeAll(era_period) :
                return True
            await asyncio.sleep(0.5)
            if cnt % 3 == 1 :
                era_period *= 2
            cnt = cnt - 1
            if era_period > 32 :
                era_period = 100
        sys.exit(1)

    async def detect_stake(self, contact_add, netuid, block_number = None) :
        delegations = await self.subtensor.get_stake_for_coldkey(
            coldkey_ss58=contact_add, block=block_number,
        )
        for record in delegations :
            if record.netuid == netuid and record.stake.rao > 1000000000 :
                return True
        return False

    async def process_remove(self, contact_add, netuid, amount) :
        self.removed_balance[netuid] += amount
        print(f"R {contact_add}, {netuid}, {amount}")
        if self.Block_Staked == 2 and netuid == self.last_netuid and self.removed_balance[netuid] > self.last_staked_amount :
            await self.process_cancel()

    async def process_call(self, contact_add, call, era_period, batch_flg = False) :
        data = await self.process_call_str(call)
        call_function, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount, target_address, transfer_amount = data

        if call_function in ('swap_stake', 'swap_stake_limit', 'move_stake') :
            if netuid1 != None and netuid2 != None and netuid1 != netuid2 :
                if netuid1 > 0 :
                    await self.process_remove(contact_add, netuid1, alpha_amount)
                if netuid1 > 0 and batch_flg :
                    return
                if contact_add in self.staking_dic and alpha_amount != None:
                    stakes = await self.get_stakes(contact_add)
                    if stakes[0] < alpha_amount :
                        return
                amount_staked = 1.0 * alpha_amount * self.lst_price[netuid1]
                if limit_price == None or limit_price == 0 :
                    await self.process_stake(contact_add, netuid2, amount_staked, None, 0, netuid1, batch_flg)
                else :
                    new_limit = int(self.lst_price[netuid1] * 1000000000 * 1000000000 / limit_price)
                    await self.process_stake(contact_add, netuid2, amount_staked, new_limit, 0, netuid1, batch_flg)

        elif call_function in ('add_stake', 'add_stake_limit') :
            if netuid != 0 and amount_staked != None:
                await self.process_stake(contact_add, netuid, amount_staked, limit_price, 0, -1, batch_flg)

        elif call_function in ('remove_stake', 'remove_stake_limit') :
            if netuid != 0 and amount_unstaked != None:
                await self.process_remove(contact_add, netuid, amount_unstaked)

        elif call_function in ('unstake_all', 'unstake_all_alpha') :
            stakes = await self.get_stakes(contact_add, True)
            for i in range(1, self.subnet_lim) :
                if stakes[i] > 1000 :
                    await self.process_remove(contact_add, i, stakes[i])

        elif call_function in ('transfer_allow_death', 'transfer_keep_alive', 'transfer_all') :
            call_function0, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount, target_address, transfer_amount = await self.process_call_str(call)
            real_account = contact_add

            if target_address != None and transfer_amount != None:
                real_hash = xxhash.xxh32(real_account).intdigest() & 0xFFFFF
                target_hash = xxhash.xxh32(target_address).intdigest() & 0xFFFFF
                if self.lst_danger_accounts2[real_hash] and transfer_amount >= 1000000000 and target_address not in self.huge_accounts :
                    self.save_address_danger2(target_address)
        
    async def process_call_proxy(self, contact_add, call) :
        real_account, (call_function, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount) = await self.process_proxy_call_str(call)

        if call_function in ('add_stake', 'add_stake_limit') :
            pass
            # await self.process_stake(real_account, netuid, amount_staked, limit_price, 0, -1, True)

        elif call_function in ('swap_stake', 'swap_stake_limit', 'move_stake') :
            # print(contact_add, netuid1, netuid2, alpha_amount)
            if netuid1 > 0 :
                await self.process_remove(contact_add, netuid1, alpha_amount)
            if netuid1 == 0 and netuid2 != None and netuid1 != netuid2 :
                amount_staked = 1.0 * alpha_amount * self.lst_price[netuid1]
                if limit_price == None or limit_price == 0 :
                    await self.process_stake(contact_add, netuid2, amount_staked, None, 0, netuid1, True)
                else :
                    new_limit = int(1000000000 * 1000000000 / limit_price )
                    await self.process_stake(contact_add, netuid2, amount_staked, new_limit, 0, netuid1, True)

        elif call_function in ('remove_stake', 'remove_stake_limit') :
            if netuid != 0 and amount_unstaked != None:
                await self.process_remove(contact_add, netuid, amount_unstaked)

        elif call_function in ('unstake_all', 'unstake_all_alpha') :
            stakes = await self.get_stakes(real_account, True)
            for i in range(1, self.subnet_lim) :
                if stakes[i] > 1000 :
                    await self.process_remove(contact_add, i, stakes[i])

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

    async def monit(self, substrates, debug = False) :
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

    async def unstake_process(self, subtensor, next_hash) :
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

    async def unstake_all_alpha(self, next_hash) :
        tasks = []
        for subtensor in self.subtensor_block:
            tasks.append(asyncio.create_task(self.unstake_process(subtensor, next_hash)))
        await asyncio.gather(*tasks)


    async def check_block(self):
        try:
            async def block_handler(block_header, subtensor):
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

            async def process_handler(subtensor) :
                future = asyncio.Future()
                try :
                    handler = lambda bh, sub=subtensor: block_handler(bh, sub)
                    await subtensor.substrate.subscribe_block_headers(handler)
                except Exception as e:
                    await future

            subscription_tasks = []
            for subtensor in self.subtensor_block:
                subscription_tasks.append(process_handler(subtensor))
                if len(subscription_tasks) > 2 :
                    break

            await asyncio.gather(*subscription_tasks)

        except Exception as e:
            print(f"Subscription error: {e}")
            sys.exit(1)
        finally:
            for subtensor in self.subtensor_block:
                await subtensor.substrate.close()

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
            return []
        if "result" in result[payload_id][0]:
            return result[payload_id][0]
        else:
            return []

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

    async def process_transfer_str(self, call) :
        call_str = str(call)
        call_str = call_str.replace("'", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace(" ", "").replace("call_args:","")
        parts = call_str.split(",")
        call_function = None
        netuid1 = None
        netuid2 = None
        alpha_amount = None
        destination_coldkey = None
        i = 0
        n = len(parts)
        while i < n:
            part = parts[i]
            try :
                part_split = part.split(":")
                if len(part_split) != 2 :
                    i += 1
                    continue
                left = part_split[0]
                right = part_split[1]
                if 'call_function' in left :
                    call_function = right
                    i += 1
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
                if 'alpha_amount' in right :
                    name, val = parts[i+2].split(":")
                    alpha_amount = int(val)
                    i += 3
                    continue
                if 'destination_coldkey' in right :
                    name, val = parts[i+2].split(":")
                    destination_coldkey = val
                    i += 3
                    continue
            except Exception as e:
                pass
            i += 1
            continue
        return (call_function, netuid1, netuid2, alpha_amount, destination_coldkey)

    async def process_proxy_call_str(self, call) :
        call_str = str(call)
        call_str = call_str.replace("'", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace(" ", "").replace("call_args:","")
        parts = call_str.split(",")
        real_account = None
        call_function = None
        netuid = None
        netuid1 = None
        netuid2 = None
        amount_staked = None
        amount_unstaked = None
        alpha_amount = None
        limit_price = None
        i = 0
        n = len(parts)
        while i < n:
            part = parts[i]
            try :
                left, right = part.split(":")
                if 'real' in right :
                    name, val = parts[i+2].split(":")
                    real_account = val
                    i += 3
                    continue
                if 'call_function' in left :
                    if right != 'proxy' :
                        call_function = right
                    i += 1
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
        return real_account, (call_function, netuid, amount_staked, amount_unstaked, limit_price,  netuid1, netuid2, alpha_amount)

    async def get_transfer_target_add(self, call) :
        call_str = str(call)
        call_str = call_str.replace("'", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace(" ", "").replace("call_args:","")
        parts = call_str.split(",")
        address = None
        i = 0
        n = len(parts)
        while i < n:
            part = parts[i]
            try :
                left, right = part.split(":")
                if 'dest' in right :
                    name, val = parts[i+2].split(":")
                    address = val
                    break
            except Exception as e:
                pass
            i += 1
            continue
        return address

    async def UnstakeAll(self, era):
        call = await self.substrate.compose_call(
            call_module="SubtensorModule",
            call_function="unstake_all",
            call_params={
                "hotkey": self.hotkey,
            },
        )

        proxy_extrinsic = await self.substrate.compose_call(
            call_module="Proxy",
            call_function="proxy",
            call_params={
                "real": self.wallet.coldkeypub.ss58_address,  # Main account
                "force_proxy_type": None,  # Use default proxy type
                "call": call,  # The actual unstake_all call
            },
        )

        extrinsic = None
        if era == 100 :
            extrinsic = await self.substrate.create_signed_extrinsic(
                call=proxy_extrinsic,
                keypair=self.proxy_keypair,  
                nonce=self.nonce,
            )
        else :
            extrinsic = await self.substrate.create_signed_extrinsic(
                call=proxy_extrinsic,
                keypair=self.proxy_keypair, 
                nonce=self.nonce,
                era={"period": era},
                tip = 3000
            )
        return await self.SubmitExtrinsic(extrinsic)

    async def AddStake(self, amount_staked, netuid, limit_price, era_period, tip) :
        fast_flg = False
        if amount_staked == int(self.limit_stakings[netuid] * 1000000000) :
            fast_flg = True
            extrinsic = self.result_extrinsic[netuid]
            if limit_price > self.calc_limit(netuid, self.limit_stakings[netuid]) :
                extrinsic = self.result_extrinsic2[netuid]
        else :
            proxy_call = self.base_call_proxy
            proxy_call.encode(
                {
                    "call_module": "SubtensorModule",
                    "call_function": "add_stake_limit",
                    "call_args": {
                        "hotkey": self.hotkey,
                        "netuid": netuid,
                        "amount_staked": amount_staked,
                        "limit_price": limit_price,
                        "allow_partial": False,
                    },
                }
            )
            extrinsic = self.create_extrinsic(proxy_call, self.finalized_block, self.block_hash)
        return await self.SubmitExtrinsic(extrinsic)

    async def Unstake(self, era_period, tip = 0) :
        proxy_call = self.base_call_proxy2
        proxy_call.encode(
            {
                "call_module": "SubtensorModule",
                "call_function": "unstake_all",
                "call_args": {
                    "hotkey": self.hotkey,
                },
            }
        )
        extrinsic = self.create_extrinsic(proxy_call, self.finalized_block, self.block_hash, tip)
        return await self.SubmitExtrinsic(extrinsic)

    async def SubmitExtrinsic(self, extrinsic) :
        try:
            async with self.lock :
                response = ""
                try :
                    tasks = []
                    for substrate in self.substrate_submit :
                        task = self.rpc_request(substrate, "author_submitExtrinsic", [str(extrinsic.data)], self.block_hash)
                        tasks.append(task)
                    responses = await asyncio.gather(*tasks, return_exceptions=True)
                    response = responses[0]
                except Exception as e:
                    pass

                if "result" in response :
                    self.nonce += 1
                    return True
                else :
                    print("Extrinsic Error!")
                    self.ext_err_cnt += 1
                    if self.ext_err_cnt > 10 :
                        sys.exit(1)
                    return False
        except Exception as e:
            print(f"Extrinsic error: {e}")
            self.ext_err_cnt += 1
            if self.ext_err_cnt > 7 :
                sys.exit(1)
            return False

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
                    data=blake2b(signature_payload.data.data, digest_size=32).digest()
                )
            signature_version = self.proxy_keypair.crypto_type
            signature = self.proxy_keypair.sign(signature_payload.data)
            value = {
                "account_id": self.account_id,
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

async def main():
    addstaker = AddStaker()
    await addstaker.init_param()
    random.seed(2 * addstaker.monit_select + addstaker.wallet_select)
    monitors = random.sample(addstaker.monitor_finney, 13)
    monitors.append(addstaker.monitor_private)

    await asyncio.gather(addstaker.check_block(),
                         addstaker.monit0(addstaker.substrate_submit),
                         addstaker.process_unstake_all_alpha(),
                         addstaker.monit([monitors[0], monitors[1]]),
                         addstaker.monit([monitors[2], monitors[3]]),
                         addstaker.monit([monitors[4], monitors[5]]),
                         addstaker.monit([monitors[6], monitors[7]]),
                         addstaker.monit([monitors[8], monitors[9]]),
                         addstaker.monit([monitors[10], monitors[11]]),
                         addstaker.monit([monitors[12], monitors[13]], True),
                         )

if __name__ == "__main__":
    asyncio.run(main())