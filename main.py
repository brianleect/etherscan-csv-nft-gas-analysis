from settings import filename, method_name, gas_consumed, analyze_all_blocks, start_block, is_free_mint, end_block, defined_price_each
import csv


def format_time(seconds):
    second_f = seconds % 60
    min_f = seconds//60
    hour_f = min_f//60

    if hour_f > 0:
        min_f -= hour_f * 60

    if hour_f > 0:
        return str(hour_f) + 'h' + str(min_f) + 'm' + str(second_f) + 's'
    if min_f > 0:
        return str(min_f) + 'm' + str(second_f) + 's'

    return str(second_f) + 's'


def getCost(transaction_list):
    info_list = []
    for transaction in transaction_list:

        # Note we are temporarily assuming that free mints only allow 1 per transaction
        if is_free_mint:
            info_list.append(float(transaction[header['TxnFee(ETH)']]))
        else:
            total_minted_local = round(
                float(transaction[header['Value_IN(ETH)']])/price_each)

            info_list.append(
                float(transaction[header['TxnFee(ETH)']])/total_minted_local)

    return info_list


def getStats(info_list):
    print("Average", round(sum(info_list)/len(info_list), 5))
    print("Median:", round(info_list[int(len(info_list)/2)], 5))
    print("10th percentile", round(info_list[int(len(info_list)/10)], 5))
    print("90th percentile", round(info_list[int(len(info_list)/10*9)], 5))
    print("Min:", round(min(info_list), 5))
    print("Max:", round(max(info_list), 5))


def gasToMintCost(gas):
    return round(gas*gas_consumed/10**9 + price_each, 5)


def getGasStats(info_list):
    avg = round(sum(info_list)/len(info_list)/gas_consumed*10**9, 5)
    median = round(info_list[int(len(info_list)/2)]/gas_consumed*10**9, 5)
    tenth = round(info_list[int(len(info_list)/10)]/gas_consumed*10**9, 5)
    ninetyth = round(info_list[int(len(info_list)/10*9)]/gas_consumed*10**9, 5)
    min_gas = round(min(info_list)/gas_consumed*10**9, 5)
    max_gas = round(max(info_list)/gas_consumed*10**9, 5)

    print("Successful tx:", len(info_list))
    print("Average", avg, '/', gasToMintCost(avg))
    print("Median:", median, '/', gasToMintCost(median))
    print("10th percentile", tenth, '/', gasToMintCost(tenth))
    print("90th percentile", ninetyth, '/', gasToMintCost(ninetyth))
    print("Min:", min_gas, '/', gasToMintCost(min_gas))
    print("Max:", max_gas, '/', gasToMintCost(max_gas))


header_list = ['Txhash', 'Blockno', 'UnixTimestamp', 'DateTime', 'From', 'To', 'ContractAddress',
               'Value_IN(ETH)', 'Value_OUT(ETH)', 'CurrentValue @ $4122.28/Eth', 'TxnFee(ETH)',
               'TxnFee(USD)', 'Historical $Price/Eth', 'Status', 'ErrCode', 'Method']

header = {k: v for v, k in enumerate(header_list)}

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)

    total_price = 0
    successful_mint = []
    failed_mint = []
    price_each = 100
    free_mint = 0
    most_repeated_method = {}

    # TODO: Get mint method based on most repeated statement

    # Get all valid mints first
    for row in datareader:
        # Avoid initial header case
        try:
            block_no = int(row[header['Blockno']])
        except:
            continue

        # Ignore certain blocks prior to certain mints
        if block_no < start_block or block_no > end_block:
            continue

        if row[header['Method']] == method_name:
            # Gets successful mints
            if row[header['ErrCode']] == '':

                # Ignore free mints to prevent 0 division issue
                if float(row[header['Value_IN(ETH)']]) == 0:
                    free_mint += 1
                # Determines the price of each mint by checking for lowest successful price that IS NOT 0
                elif float(row[header['Value_IN(ETH)']]) <= price_each:
                    price_each = float(row[header['Value_IN(ETH)']])

                successful_mint.append(row)

            # Gets failed mints
            else:
                failed_mint.append(row)

# Changes price to 0 the mint was completely free
if is_free_mint:
    price_each = 0

# Overwrites price_each if we define price in settings
if defined_price_each != -1:
    price_each = defined_price_each


# Calculating gas loss from failed mint
gas_loss = 0
for mint in failed_mint:
    gas_loss += float(mint[header['TxnFee(ETH)']])

# Calculate duration by taking first successful_mint - last
block_duration_blk = int(successful_mint[-1][header['Blockno']]) - \
    int(successful_mint[0][header['Blockno']]) + 1
block_duration_seconds = int(successful_mint[-1][header['UnixTimestamp']]) - \
    int(successful_mint[0][header['UnixTimestamp']])

print("Price each:", round(price_each, 3))
print("Total transactions:", len(successful_mint) + len(failed_mint))
print("Total successful transactions:", len(successful_mint))
print("Total failed transactions", len(failed_mint),
      "/ Gas lost:", round(gas_loss, 2))
print("Total free mints:", free_mint)
print("Duration taken:", block_duration_blk,
      "Blocks /", format_time(block_duration_seconds))

total_minted = free_mint
total_minted_local = 0
base_cost_list = []
gas_cost_list = []
block_dict = {}
print('-------------------------')
print('Successful mint analysis')

for mint in successful_mint:

    if not is_free_mint:

        # Ignore 0 value if detected
        if float(mint[header['Value_IN(ETH)']]) == 0:
            continue

        total_minted_local = round(
            float(mint[header['Value_IN(ETH)']])/price_each)
        gas_cost_list.append(
            float(mint[header['TxnFee(ETH)']])/total_minted_local)
        base_cost_list.append(
            float(mint[header['TxnFee(ETH)']])/total_minted_local + price_each)
    else:
        gas_cost_list.append(float(mint[header['TxnFee(ETH)']]))
        base_cost_list.append(
            float(mint[header['TxnFee(ETH)']]))

    total_minted += total_minted_local

    # Append based on block
    if mint[header['Blockno']] not in block_dict:
        block_dict[mint[header['Blockno']]] = [mint]
    else:
        block_dict[mint[header['Blockno']]].append(mint)

print("Total minted in public:", total_minted)

print('-------------\nCost analysis (Eth)')
getStats(base_cost_list)

print('---------------\nGas Analysis (Gwei)')
getGasStats(gas_cost_list)

print('--------------------\nBlock Analysis')
print("Total blocks:", len(block_dict))

if analyze_all_blocks == True:
    for block in block_dict:
        print(block)
        getGasStats(getCost(block_dict[block]))
        print('---------------')
else:
    block_dict_list = list(block_dict)
    print(block_dict_list[0])
    getGasStats(getCost(block_dict[block_dict_list[0]]))
    print('---------------')
    print(block_dict_list[-1])
    getGasStats(getCost(block_dict[block_dict_list[-1]]))
    print('---------------')
