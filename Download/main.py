import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from iso3166 import countries
import requests
import timeit

columns = [
    'Country',
    'alpha3',
    'date',
    'School closing',
    'Workplace closing',
    'Cancel public events',
    'Restrictions on gatherings',
    'Close public transport',
    'Stay at home requirements',
    'Restrictions on internal movement',
    'International travel controls',
    'Income support',
    'Debt/contract relief',
    'Fiscal measures',
    'International support',
    'Public information campaigns',
    'Testing policy',
    'Contact tracing',
    'Emergency investment in healthcare',
    'Investment in vaccines'
]

polic_df = pd.DataFrame(columns=columns)

date_N_days_ago = datetime.now() - timedelta(days=10)
datelist = pd.date_range(start="2020-01-01", end=date_N_days_ago).to_list()

global_data = []
d = []

for country in countries:
    print(f"{country}")
    for date in datelist[:]:
        buffer = []

        country_name = country.name
        country_alpha3 = country.alpha3
        country_date = str(date.date())
        country_url = f"https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/actions/{country_alpha3}/{country_date}"

        buffer.append(country_name)
        buffer.append(country_alpha3)
        buffer.append(country_date)
        buffer.append(country_url)

        d.append(buffer)


def save_to_list(country_req, URL):
    buffer = []

    country_name = URL[0]
    country_alpha3 = URL[1]
    country_date = URL[2]

    if country_req != 0:
        if 'policyActions' in country_req:

            buffer.append(country_name)
            buffer.append(country_alpha3)
            buffer.append(country_date)

            politcs = country_req['policyActions']
            for polic_index in range(17):
                if polic_index < len(politcs):
                    if 'policyvalue' in politcs[polic_index]:
                        buffer.append(politcs[polic_index]['policyvalue'])
                    else:
                        buffer.append(None)
                else:
                    buffer.append(None)
    if len(buffer) == 0:
        print(URL[3])
    else:
        print("Please waiting...")
    global_data.append(buffer)


def fetch(session, url_array):
    with session.get(url_array[3], timeout=240) as response:
        country_req = response.json()
        save_to_list(country_req, url_array)


def main(urls_array):
    with ThreadPoolExecutor(max_workers=15) as executor:
        with requests.Session() as session:
            executor.map(fetch, [session] * len(urls_array), urls_array)
            executor.shutdown(wait=False)



start = timeit.default_timer()

main(d[:500])

stop = timeit.default_timer()
print('Time: ', stop - start)

# for i in global_data:
#     if len(i) != 0:
#         buffer_series = pd.Series(i, index=polic_df.columns)
#         polic_df = polic_df.append(buffer_series, ignore_index=True)
#
# for i in polic_df.columns:
#     print(polic_df[i].value_counts())
#     print("===================================")

# polic_df.to_csv("polic.csv", index=False)
