# etherscan-csv-nft-gas-analysis
Analyzes .csv exports of transactions from etherscan to have a breakdown regarding gas prices

## Context
During peak bull market for NFTs, the lack of tools & information regarding competitiveness of mints led to the development of this simple tool which provides breakdown of cost & time taken from any NFT mint of interest.

We leverage on the easily accessible .csv exports etherscan provides as the data source, coupled with some manual inspection of mint txn by the user to aid the analysis.

## Steps
1. Export CSV of NFT of interest from etherscan (E.g. [LAG](https://etherscan.io/exportData?type=tokentxns-nft&contract=0x9c99d7f09d4a7e23ea4e36aec4cb590c5bbdb0e2&a=&decimal=0))
2. Specify config parameters at `settings.py`
    - filename (E.g. 'lag.csv')
    - method_name (E.g. "_public Sale Mint") (Refer to etherscan column name)
    - defined_price_each (E.g. 0.05) (Price of each mint, totalTxnValue/numberOfMints)
    - gas_consumed (E.g. 130000) (Estimated via any relevant mint txn, totalGasConsumed/numberOfMints)
    - is_free_mint (Set to true if it's a free mint else False)
    - (Optional) analyze_all_blocks (Reduce noise, Set to true for all blocks else only start & end)
    - (Optional) start_block (Ignore earlier segments by setting start block)
    - (Optional) end_block (Ignore later segments by setting end block)
3. Run `main.py`

![image](https://user-images.githubusercontent.com/63389110/209989720-e97ee469-14bc-4403-906b-4e7a3aa6d7ef.png)
