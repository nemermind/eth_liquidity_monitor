from web3 import Web3

#CONFIG
NODE_ADDRESS = "Alchemy or Quick Node"

web3 = Web3(Web3.HTTPProvider("NODE_ADDRESS"))
uniswap_factory = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
Uniswap_factory_abi = json.loads('Enter ABi')
contract = web3.eth.contract(address=uniswap_factory, abi=Uniswap_factory_abi)
liquidityPairAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" #It's standard for most token to pair with WETH Address so we will be checking these pools.
lp_abi='Enter Uniswap v2 ABI' #Here is Uniswap V2 Address-0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D

def get_token_from_lp(lpAddres):
    uniswap_v2_pair = web3.eth.contract(address=lpAddres,abi=lp_abi)
    tokenA_address = uniswap_v2_pair.functions.token0().call()
    tokenB_address = uniswap_v2_pair.functions.token1().call()
    if tokenA_address == liquidityPairAddress:
       return 0
    elif tokenB_address ==liquidityPairAddress:
       return 1


def get_liquidity_balance(lp_address):
    lp_contract = web3.eth.contract(address=lp_address, abi=lp_abi)
    reserves = lp_contract.functions.getReserves().call()
    index= get_token_from_lp(lp_address)
    balance = reserves[index]
    return balance

event_filter = contract.events.PairCreated.create_filter(fromBlock="latest")
while True:
    try:

        #events = event_filter.get_all_entries()
        events = event_filter.get_new_entries()

        if len(events) > 0:

           for event in events:
               if (event['args']['token1'] == liquidityPairAddress):
                   tokenAddress = event['args']['token0']
               

                   lp_address=contract.functions.getPair(tokenAddress,liquidityPairAddress).call()
   

                   lp_balance= get_liquidity_balance(lp_address)
               

                   tokenLiquidityAmount = float(web3.from_wei(lp_balance, "ether"))
                   print(f"Token Address: {tokenAddress}, Lp Amount{tokenLiquidityAmount}")
