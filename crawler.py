import requests
import datetime
import json
import re
from tqdm import trange, tqdm
from classes import *

class HKJCHandler():

    @staticmethod
    def initiate_session():

        session = requests.Session()
        r = session.get('http://bet.hkjc.com')

        return session, r.cookies

    @staticmethod
    def fetch_all_odds():

        session = requests.Session()
        r = session.get('http://bet.hkjc.com')

        matches = []
            
        odds_url = f'http://bet.hkjc.com/football/getJSON.aspx?jsontype=odds_allodds.aspx'
        result = session.post(
            odds_url,
            headers=dict(referer='http://bet.hkjc.com'),
            cookies=r.cookies
        )

        e = True
        trial = 1

        while e:

            print(f'Trial {trial}...')
        
            try:
                response = json.loads(result.text)
                
                for j in tqdm(response):

                    if j['definedPools'] == []:
                        
                        odds_url = \
                            f'http://bet.hkjc.com/football/getJSON.aspx?jsontype=odds_allodds.aspx&matchid={j["matchID"]}'
                        result = session.post(
                            odds_url,
                            headers=dict(referer='http://bet.hkjc.com'),
                            cookies=r.cookies
                        )
                        match = Match(next(
                            item for item in json.loads(result.text) if item["matchID"] == j["matchID"]
                        ))
                        
                    else:
                        
                        match = Match(j)

                    matches.append(match)

                e = False
            except json.decoder.JSONDecodeError:
                e = True
                trial += 1

                session = requests.Session()
                r = session.get('http://bet.hkjc.com')

                matches = []
                    
                odds_url = f'http://bet.hkjc.com/football/getJSON.aspx?jsontype=odds_allodds.aspx'
                result = session.post(
                    odds_url,
                    headers=dict(referer='http://bet.hkjc.com'),
                    cookies=r.cookies
                )

        return matches

if __name__ == '__main__':

    # session, cookies = HKJCHandler.initiate_session()
    HKJCHandler.fetch_all_odds()