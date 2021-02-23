import requests
import pandas as pd
import os

# function to retreive active care homes from CQC using their API
def getCareHomes():
    # retrieve a list of care homes in the South West
    url = 'https://api.cqc.org.uk/public/v1/locations?'
    params = {'careHome': 'Y', 'region': 'South West', 'localAuthority': ['Devon', 'Somerset', 'Torbay', 'Plymouth'], 'perPage': 4000, 'partnerCode': 'DSFRS'}
    req = requests.get(url, params=params)
    #print(req.status_code)
    #print(req.headers)
    #print(req.text)
    j = req.json()
    df = pd.DataFrame.from_dict(j.get('locations'))
    #print(df.head(10))
    #print(df.info())
    locationids = df['locationId'].tolist()
    start_time = time.time()
    dfs = []
    counter1 = 0
    for ids in locationids:
        counter1 += 1
        print(counter1)
        loc_details_url = f'https://api.cqc.org.uk/public/v1/locations/{ids}?partnerCode=DSFRS'
        req = requests.get(loc_details_url, timeout=(5, 27)) #time.sleep(0.5),
        j = req.json()
        dfs.append(j)
        #for i in j:
        #    dfs.append(i)
        #if j.get('registrationStatus') == 'Registered':
        #    #print(j.get('registrationStatus'))
        #    lister.append(j.get('registrationStatus'))
        #    counter2 += 1
        #    #print(req.text)
    dfz = pd.DataFrame(dfs)
    dfz.to_csv("cqc_care_homes.csv", index = False)
    print(dfz.head())
    print(dfz.info())
    print('%s seconds' % (time.time() - start_time))
# check csv file exist, if any are missing, create new data
if os.path.exists('cqc_care_homes.csv') == False:
    getCareHomes()
    print('***CQC care home csv generated***')
print('***CQC care home csv already exists***')