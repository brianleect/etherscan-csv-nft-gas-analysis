# nft-manual-mint-analysis
Analyzes .csv exports of NFT transfer logs from etherscan to have a breakdown regarding gas prices

## Context
During peak bull market for NFTs, the lack of tools & information regarding competitiveness of mints led to the development of this simple tool which provides breakdown of cost & time taken from any NFT mint of interest.

We leverage on the easily accessible .csv exports etherscan provides as the data source, coupled with some manual inspection of mint txn by the user to aid the analysis.

## Steps
1. Export CSV of NFT of interest from etherscan & store it at `csv_exports` folder (E.g. [LAG](https://etherscan.io/exportData?type=tokentxns-nft&contract=0x9c99d7f09d4a7e23ea4e36aec4cb590c5bbdb0e2&a=&decimal=0))
2. Specify config parameters at `settings.py`
    - filename (E.g. 'lag.csv')
    - method_name (E.g. "_public Sale Mint") (Refer to etherscan column name)
    - defined_price_each (E.g. 0.05) (Price of each mint, totalTxnValue/numberOfMints)
    - gas_consumed (E.g. 130000) (Estimated via any relevant mint txn, totalGasConsumed/numberOfMints)
    - is_free_mint (Set to true if it's a free mint else False)
    - (Optional) analyze_all_blocks (Reduce noise, Set to true for all blocks else only start & end)
    - (Optional) start_block (Ignore earlier segments by setting start block)
    - (Optional) end_block (Ignore later segments by setting end block)
3. Run `main.py` , and observe output to console or at `stats_dump/{filename}` 

![image](https://user-images.githubusercontent.com/63389110/209989720-e97ee469-14bc-4403-906b-4e7a3aa6d7ef.png)

![image](https://user-images.githubusercontent.com/63389110/209989851-4d394e9c-47e8-4af6-adf4-c2c5856f5de0.png)
![image](https://user-images.githubusercontent.com/63389110/209989889-704ea4e0-668d-4110-a0cb-fd3c2daf7863.png)

## Limitations
1. Significant amount of **manual input** with potential room for mistake
    - For non-technical uses, determining gas consumed per unit might be a little challenging if litle guidance is provided
    - More prone to errors due to typo of filename or misconfiguration e.g. forgeting to set free mint etc

2. Etherscan limits to 5k transfer logs export (What if we have 50k mints?) 
    - An example would be the otherside mint by Yuga Labs.
    - There's no known workaround using etherscan exports as minimum export duration is within a day.

Solution is to build an analyzer ground up relying on only **on-chain data** which I'll go into detail in a separate repo (here)[https://github.com/brianleect/nft-onchain-mint-analysis] (WIP).

## Design choices / Thoughts / Common Questions

1. Why was etherscan used as a data source?
    - Most reliable site which most crypto users are familiar with as well.
    - Exports were easily accessible, however, only downside is lack of API access to retrieve the data thus requiring manual exports here
    - Alternatives such as Covalent was explored as well, however retrieval took too long and it was not especially reliable.

