import pandas as pd
import requests
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import json
import ast
import numpy as np
from datetime import date


response = requests.get("https://api.warframe.market/v2/items")
if response.status_code == 200:
    item_data = response.json()
    base_item_df = pd.DataFrame(item_data['data'])
    
    print(base_item_df.info())
else:
    print(f"Request failed with status code: {response.status_code}")


cleaned_item_df = base_item_df.drop(columns=['id', 'i18n', "subtypes",	"maxAmberStars", "maxCyanStars", "maxRank", "bulkTradable",	"vaulted", "baseEndo", "endoMultiplier"])
cleaned_item_df = cleaned_item_df.rename(columns={'slug': 'name'})
cleaned_item_df["gameRef"] = cleaned_item_df["gameRef"].map(lambda x: x.rsplit("/", 1)[-1])

filter_tags = ["prime"]
mask = cleaned_item_df['tags'].apply(lambda x: any(item in filter_tags for item in x))
filtered_item_df = cleaned_item_df[mask].sort_values(by='name')

mask_sets = filtered_item_df["name"].str.contains(r"_set", case=False, na=False)
filtered_sets_df = filtered_item_df[mask_sets]
filtered_parts_df = filtered_item_df[~mask_sets]


cleaned_relic_df = base_item_df.drop(columns=['id',	"maxAmberStars", "i18n", "ducats", "subtypes", "maxCyanStars", "maxRank", "bulkTradable", "baseEndo", "endoMultiplier"])
cleaned_relic_df = cleaned_relic_df.rename(columns={'slug': 'name'})
cleaned_relic_df.info()

filter_tags = ["relic"]
mask = cleaned_relic_df['tags'].apply(lambda x: any(item in filter_tags for item in x))
filtered_relic_df = cleaned_relic_df[mask].sort_values(by='name')
filtered_relic_df['gameRef'] = filtered_relic_df['gameRef'].apply(lambda x: x.rsplit('/', 1)[-1])


response = requests.get("http://content.warframe.com/PublicExport/Manifest/ExportRelicArcane_en.json!00_fdH29UBNM7od0XMI54PlOQ")
if response.status_code == 200:
    rewards_data = response.json()
    rewards_df = pd.DataFrame(rewards_data['ExportRelicArcane'])
    print(rewards_df.info())
else:
    print(f"Request failed with status code: {response.status_code}")


cleaned_rewards_df = rewards_df.drop(columns=["name", 'codexSecret', 'description', 'excludeFromCodex', 'rarity', 'levelStats', ])
cleaned_rewards_df = cleaned_rewards_df.rename(columns={'uniqueName': 'gameRef'})
cleaned_rewards_df['gameRef'] = cleaned_rewards_df['gameRef'].apply(lambda x: x.rsplit('/', 1)[-1]).str.replace('Bronze', '')

merged_relic_df = pd.merge(filtered_relic_df, cleaned_rewards_df, on='gameRef')

merged_relic_df.info()

rarity_dict = {}
for index, row in merged_relic_df.iterrows():
    for reward in row["relicRewards"]:
        reward_ref = reward['rewardName'].rsplit("/", 1)[-1]
        rarity_dict[reward_ref] = reward['rarity']


vaulted_dict = {x: True for x in filtered_parts_df["gameRef"]}
for index, row in merged_relic_df[merged_relic_df['vaulted'] == False].iterrows():
    for reward in row["relicRewards"]:
        reward_ref = reward['rewardName'].rsplit("/", 1)[-1]
        vaulted_dict[reward_ref] = False

dfs = []
resurg0212 = ("harrow", 
               "nekros", 
               "galatine",
               "knell",  
               "scourge", 
               "tigris", 
               "saryn", 
               "valkyr",
                "cernos",
               "nikana",
               "spira",
               "venka",
              "garuda", 
               "khora", 
               "dual_keres",
               "hystrix",  
               "nagantaka", 
               "corvas", 
               "ivara", 
               "oberon",
               "aksomati",
               "baza",
                "silva_and_aegis",
              "sybaris")

df_0212 = pd.concat([filtered_parts_df[filtered_parts_df["name"].str.startswith(resurg0212)].copy(), filtered_sets_df[filtered_sets_df["name"].str.startswith(resurg0212)].copy()]) 
df_0212["end"] =  pd.to_datetime("2026-02-12")
df_0212["start"] =  pd.to_datetime("2026-01-15")
resurg0219 = ("harrow", 
               "nekros", 
               "galatine",
               "knell",  
               "scourge", 
               "tigris", 
               "saryn", 
               "valkyr",
                "cernos",
               "nikana",
               "spira",
               "venka",
              "garuda", 
               "khora", 
               "dual_keres",
               "hystrix",  
               "nagantaka", 
               "corvas", 
               "ivara", 
               "oberon",
               "aksomati",
               "baza",
                "silva_and_aegis",
              "sybaris",
              "ember",
              "frost",
              "glaive",
              "latron",
              "reaper",
              "sicarus",
              "hydroid",
              "mesa",
              "akjagara",
              "ballistica",
              "nami_skyla",
              "redeemer",
              "loki",
              "volt",
              "bo",
              "wyrm",
              "odonata")

df_0219 = pd.concat([filtered_parts_df[filtered_parts_df["name"].str.startswith(resurg0219)].copy(), filtered_sets_df[filtered_sets_df["name"].str.startswith(resurg0219)].copy()]) 
df_0219["end"] =  pd.to_datetime("2026-02-19")
df_0219["start"] =  pd.to_datetime("2026-02-12")

resurg0319 = ("atlas", "vauban", "tekko", "dethcube", "akstiletto", "fragor")
df_0319 = pd.concat([filtered_parts_df[filtered_parts_df["name"].str.startswith(resurg0319)].copy(), filtered_sets_df[filtered_sets_df["name"].str.startswith(resurg0319)].copy()]) 
df_0319["end"] =  pd.to_datetime("2026-03-19")
df_0319["start"] =  pd.to_datetime("2026-02-20")

dfs.extend([df_0212, df_0219, df_0319])

resurgance_df =  pd.concat(dfs, ignore_index=True)


today = date.today()
folder_name = "Data/Price_Data"
parts_price_list = f"{today}.csv"
output_path_list = os.path.join(os.getcwd(), folder_name, parts_price_list)
filtered_df = pd.concat([filtered_parts_df, filtered_sets_df], ignore_index=True)
if not os.path.isfile(output_path_list):
    dfs = []
    for index, row in filtered_df.iterrows():
        api_url = f"https://api.warframe.market/v2/orders/item/{row['name']}/top"
        response = requests.get(api_url)
        if response.status_code == 200:
            order_data = response.json()
            sell_order_df = pd.DataFrame(order_data['data']['sell'])
            buy_order_df = pd.DataFrame(order_data['data']['buy'])
    
    
            sell_order_df['gameRef'] = row['gameRef']
            buy_order_df['gameRef'] = row['gameRef']
            
            if 'set' in row['name'].lower():
                sell_order_df['vaulted'] = None
                buy_order_df['vaulted'] = None
            else:
                sell_order_df['vaulted'] = vaulted_dict.get(row['gameRef'], True)
                buy_order_df['vaulted'] = vaulted_dict.get(row['gameRef'], True)
        
            sell_order_df['type'] = 'sell'
            buy_order_df['type'] = 'buy'
    
            sell_order_df['name'] = row['name']
            buy_order_df['name'] = row['name']
    
            sell_order_df['date'] = today
            buy_order_df['date'] = today
    
            dfs.extend([buy_order_df, sell_order_df])
        else:
            print(f"Request failed with status code: {response.status_code}")
    base_order_df =  pd.concat(dfs, ignore_index=True)
    base_order_df.info()
 
else:
    print(f"{output_path_list} Already Exists")
    base_order_df = pd.read_csv(output_path_list) 

set_items_df = base_order_df[base_order_df['name'].str.contains(r"_set", case=False, na=False)]
#set_items_df.head()

base_order_df['base_name'] = (
    base_order_df['name']
    .str.lower()
    .str.split('_prime')
    .str[0]
    + '_prime'
)


part_vaulted_map = (
    base_order_df[~base_order_df['name'].str.contains(r"_set$", case=False, na=False)]
    .groupby('base_name')['vaulted']
    .max()   # If ANY part is True → set becomes True
)


is_set = base_order_df['name'].str.contains(r"_set$", case=False, na=False)

base_order_df.loc[is_set, 'vaulted'] = (
    base_order_df.loc[is_set, 'base_name']
    .map(part_vaulted_map)
)

#base_order_df.info()

cleaned_order_df = base_order_df.copy()

if not os.path.isfile(output_path_list):
    cleaned_order_df = cleaned_order_df.drop(columns=['id', 'createdAt', 'updatedAt', 'itemId', 'user', 'visible', 'rank']).dropna()

cleaned_order_df["platinum"] = cleaned_order_df["platinum"].astype(int)
cleaned_order_df["quantity"] = cleaned_order_df["quantity"].astype(int)
cleaned_order_df["perTrade"] = cleaned_order_df["perTrade"].astype(int)
cleaned_order_df["vaulted"] = cleaned_order_df["vaulted"].astype(bool)
cleaned_order_df["date"] = pd.to_datetime(cleaned_order_df["date"])

final_df = cleaned_order_df.copy()
#final_df.info()

orders_df = final_df.copy()

orders_df['rarity'] = orders_df['gameRef'].map(rarity_dict).dropna()

is_set = orders_df['name'].str.contains(r"_set$", case=False, na=False)
orders_df.loc[is_set, 'rarity'] = "SET"

orders_df.info()

orders_df['index'] = range(len(orders_df))


df_merged = orders_df.merge(resurgance_df, on='gameRef', how='left')
df_merged['in_range'] = (df_merged['date'] >= df_merged['start']) & \
                        (df_merged['date'] <= df_merged['end'])
resurgance_status = df_merged.groupby('index')['in_range'].any()

orders_df['resurgance'] = orders_df['index'].map(resurgance_status).fillna(False)
orders_df.drop('index', axis=1, inplace=True)