import requests
from bs4 import BeautifulSoup
import datetime
import json
import re

class HKJCHandler(object):

	base_url = 'http://bet.hkjc.com/'
	
	# racecard_url = 'http://racing.hkjc.com/racing/Info/meeting/RaceCard/English/Local/'
	# odds_url = 'http://bet.hkjc.com/racing/getJSON.aspx?type=winplaodds&date=2018-07-01&venue=ST&start=10&end=10'
	# race_day_url = 'http://racing.hkjc.com/racing/SystemDataPage/racing/meeting-reminder-iframe-SystemDataPage.aspx?lang=English'

	@staticmethod
	def get_current_going():

		result = requests.get(
			url=HKJCHandler.race_day_url,
			headers=dict(referer=HKJCHandler.base_url)
		)

		soup = BeautifulSoup(result.text, 'html.parser')

		going = soup.find_all('font', 'body_text_ri')[1].text.replace('\r\n\t\t\t\t\t\t\t\t\t', '').strip()

		going = going.split(' ')[3]
		penetrometer = soup.find_all('td')[1].text

		return going, penetrometer

	@staticmethod
	def get_latest_changes():

		result = requests.get(
			url=HKJCHandler.race_day_url,
			headers=dict(referer=HKJCHandler.base_url)
		)

		soup = BeautifulSoup(result.text, 'html.parser')

		changes = soup.find(id='reminderChanges').find('table').find_all('div', id=lambda x: x.startswith('localchange'))

		for change in changes:

			race_no = change['id'][11:]
			print(race_no)

			for tr in change.find_all('tr'):

				c = {}

				change_text = tr.text.replace('\r\n', '').replace('\t', '').strip()

				change_text = [x for x in change_text.split(' ')[:-2] if len(x) > 0]

				print(change_text)

				if change_text[0] == 'Horse':

					horse_no = change_text[1]

					if change_text[2] == ',':

						c['type'] = 'scratch'
						c['horse_no'] = horse_no

						if change_text[-1] == 'Promoted.':

							c['replacement'] = ' '.join(change_text[change_text.index('starter') + 1:-1])

					elif 'Rider' in change_text:

						c['type'] = 'jockey'
						c['horse_no'] = horse_no
						c['jockey'] = ' '.join(change_text[change_text.index('to') + 1:])[:-1]

					elif 'carry' in change_text:

						c['type'] = 'weight'
						c['horse_no'] = horse_no
						c['weight'] = change_text[-1][:-4]


	@staticmethod
	def get_win_pla_odds(date, venue, race_no):

		result = requests.get(
			url='http://bet.hkjc.com/racing/getJSON.aspx?type=winplaodds&date=' +
				date.strftime('%Y-%m-%d') + '&venue=' + venue + '&start=' + race_no +
				'&end=' + race_no,
			headers=dict(referer=HKJCHandler.base_url)
		)

		win_odds, pla_odds = json.loads(result.text)['OUT'].split('@@@')[1].split('#')

		win_odds = [float(x.split('=')[1]) for x in win_odds.split(';')[1:]]
		pla_odds = [float(x.split('=')[1]) for x in pla_odds.split(';')[1:]]

		return win_odds, pla_odds

	@staticmethod
	def get_qpl_odds(date, venue, race_no):

		result = requests.get(
			url='http://bet.hkjc.com/racing/getJSON.aspx?type=qpl&date=' +
				date.strftime('%Y-%m-%d') + '&venue=' + venue + '&raceno=' + race_no,
			headers=dict(referer=HKJCHandler.base_url)
		)

		return [list(map(int, x.split('=')[0].split('-'))) + [float(x.split('=')[1])]
				for x in json.loads(result.text)['OUT'].split('@@@')[1].split(';')[1:]]

	@staticmethod
	def get_qin_odds(date, venue, race_no):

		result = requests.get(
			url='http://bet.hkjc.com/racing/getJSON.aspx?type=qin&date=' +
				date.strftime('%Y-%m-%d') + '&venue=' + venue + '&raceno=' + race_no,
			headers=dict(referer=HKJCHandler.base_url)
		)

		return [list(map(int, x.split('=')[0].split('-'))) + [float(x.split('=')[1])]
		        for x in json.loads(result.text)['OUT'].split('@@@')[1].split(';')[1:]]

	@staticmethod
	def get_race_cards():

		result = requests.get(
			url='http://racing.hkjc.com/racing/Info/meeting/RaceCard/english/Local/',
			headers=dict(referer=HKJCHandler.base_url)
		)

		races = [x['href']
			for x in
			BeautifulSoup(result.text, 'html.parser').find('div', 'raceNum').find_all('a')
			if x['href'].startswith('/racing/Info/meeting/RaceCard/english/Local')
		]

		racecard = BeautifulSoup(result.text, 'html.parser').find('table', 'tableBorderBlue tdAlignC')
		race_no = 1

		with open('hkjc-racecard.txt', 'w+') as f:

			f.write('\t'.join(
				[
					'race_no', 'horse_no', 'horse_previous_results', 'horse_name', 'horse_id', 'actual_weight',
					'jockey', 'draw', 'trainer', 'rating', 'rating_change', 'body_weight', 'body_weight_change',
					'previous_time', 'age', 'gear'
				]
			) + '\n')

		for tr in racecard.find('tbody').find_all('tr')[3:]:

			tds = tr.find_all('td')
			horse_no = tds[0].text.strip()
			horse_previous = tds[1].text.strip()
			horse_name = tds[3].text.strip()
			horse_id = tds[4].text.strip()
			actual_weight = tds[5].text.strip()
			jockey = tds[6].text.strip()
			if jockey.find('(') > 0:
				jockey = jockey[:jockey.find('(')]
			draw = tds[7].text.strip()
			trainer = tds[9].text.strip()
			rating = tds[10].text.strip()
			rating_change = tds[11].text.strip()
			body_weight = tds[12].text.strip()
			body_weight_change = tds[13].text.strip()
			try:
				previous_time = tds[14].text.strip()
				previous_time = \
					int(previous_time.split('.')[0]) * 60 + \
					int(previous_time.split('.')[1]) + \
					int(previous_time.split('.')[2]) / 100
			except:
				previous_time = 0.0
			age = tds[14].text.strip()
			gear = tds[19].text.strip()

			with open('hkjc-racecard.txt', 'a+') as f:

				f.write('\t'.join(
					[
						str(race_no), horse_no, horse_previous, horse_name, horse_id, actual_weight,
						jockey, draw, trainer, rating, rating_change, body_weight, body_weight_change,
						str(previous_time), age, gear
					]
				).replace('\xa0', '') + '\n')

		for race in races:

			race_no += 1

			result = requests.get(
				url='http://racing.hkjc.com' + race,
				headers=dict(referer=HKJCHandler.base_url)
			)

			racecard = BeautifulSoup(result.text, 'html.parser').find('table', 'tableBorderBlue tdAlignC')

			for tr in racecard.find('tbody').find_all('tr')[3:]:

				tds = tr.find_all('td')
				horse_no = tds[0].text.strip()
				horse_previous = tds[1].text.strip()
				horse_name = tds[3].text.strip()
				if horse_name.find('Withdrawn') > 0:
					continue
				horse_id = tds[4].text.strip()
				actual_weight = tds[5].text.strip()
				jockey = tds[6].text.strip()
				if jockey.find('(') > 0:
					jockey = jockey[:jockey.find('(')]
				draw = tds[7].text.strip()
				trainer = tds[9].text.strip()
				rating = tds[10].text.strip()
				rating_change = tds[11].text.strip()
				body_weight = tds[12].text.strip()
				body_weight_change = tds[13].text.strip()
				try:
					previous_time = tds[14].text.strip()
					previous_time = \
						int(previous_time.split('.')[0]) * 60 + \
						int(previous_time.split('.')[1]) + \
						int(previous_time.split('.')[2]) / 100
				except:
					previous_time = 0.0
				age = tds[15].text.strip()
				gear = tds[20].text.strip()

				with open('hkjc-racecard.txt', 'a+') as f:

					f.write('\t'.join(
						[
							str(race_no), horse_no, horse_previous, horse_name, horse_id, actual_weight,
							jockey, draw, trainer, rating, rating_change, body_weight, body_weight_change,
							str(previous_time), age, gear
						]
					).replace('\xa0', '') + '\n')



if __name__ == '__main__':

	c = HKJCHandler()

	temp = c.get_race_cards()

	pass