import json

class Parser(object):

	def __init__(self, datfile):
		
		self.datfile = datfile
		self.scoring_stats = ["Sand Save Percentage", "Scrambling", "Scrambling from the Fringe",
								"Putts Per Round", "Putting - Inside 10'", "1-Putts per Round",
								"2-Putts per Round", "3-Putts per Round", "Putting from Inside 5'"]
		self.ball_striking_stats = ["Greens or Fringe in Regulation", "GIR Percentage - 100-125 yards",
								"GIR Percentage - 125-150 yards", "GIR Percentage - 150-175 yards",
								"GIR Percentage - 175-200 yards", "Going for the Green",
								"GIR Percentage - 200+ yards", "Driving Accuracy Percentage",
								"Greens in Regulation Percentage"]

	def get_data(self):

		with open(self.datfile) as json_data:
			self.d = json.load(json_data)
			json_data.close()
			return (self.d)

	def get_year_data(self, year):
		'''Returns only data from specified year'''
		
		current_year_data = []
		data = self.get_data()
		for line in data:
			if line['Year'] == str(year):
				current_year_data.append(line)
		return (current_year_data)

	def format_data(self, year):

		non_percent = ["1-Putts per Round", "2-Putts per Round", 
		"3-Putts per Round", "Putts Per Round"]

		data = self.get_year_data(year)
		for line in data:
			if line['Stat'] in non_percent:
				pass
			else:
				line['First'] = line['First'] + "%"
				line['Top 10'] = line['Top 10'] + "%"
				line['Top 25'] = line['Top 25'] + "%"
				line['Top 100'] = line['Top 100'] + "%"
				line['Last'] = line['Last'] + "%"
		return (data)

	def categorize_data(self, year):
		'''Returns current year data in proper format for Jinja templating'''

		scoring_data = []
		ball_striking_data = []

		data = self.format_data(year)
		for line in data:
			if line['Stat'] in self.ball_striking_stats:
				ball_striking_data.append(line)
			elif line['Stat'] in self.scoring_stats:
				scoring_data.append(line)
		all_data = [ball_striking_data, scoring_data]
		return (all_data)


	def rename_data(self, year, category):

		data = self.categorize_data(year)
		for line in data[category]:
			if line['Stat'] == "Putting - Inside 10'":
				line['Stat'] = "Putting (inside 10ft)"
			elif line['Stat'] == "Sand Save Percentage":
				line['Stat'] = "Scrambling (sand)"
			elif line['Stat'] == "Scrambling from the Fringe":
				line['Stat'] = "Scrambling (from fringe)"
			elif line['Stat'] == "Putting from Inside 5'":
				line['Stat'] = "Putting (inside 5ft)"
			elif line['Stat'] == "GIR Percentage - 100-125 yards":
				line['Stat'] = "GIR (100-125 yds)"
			elif line['Stat'] == "GIR Percentage - 125-150 yards":
				line['Stat'] = "GIR (125-150 yds)"
			elif line['Stat'] == "GIR Percentage - 150-175 yards":
				line['Stat'] = "GIR (150-175 yds)"
			elif line['Stat'] == "GIR Percentage - 175-200 yards":
				line['Stat'] = "GIR (175-200 yds)"
			elif line['Stat'] == "GIR Percentage - 200+ yards":
				line['Stat'] = "GIR (200+ yds)"
			elif line['Stat'] == "Greens in Regulation Percentage":
				line['Stat'] = "GIR"
			elif line['Stat'] == "Driving Accuracy Percentage":
				line['Stat'] = "Driving Accuracy"

		return (data[category])

	
	def sort_data(self, year):
		
		ball_striking_data = self.rename_data(year, 0)
		scoring_data = self.rename_data(year, 1)
		
		sorted_ball_striking_data = sorted(ball_striking_data, key = lambda x : x['Stat'])
		sorted_scoring_data = sorted(scoring_data, key = lambda x : x['Stat'])
		sorted_data = [sorted_ball_striking_data, sorted_scoring_data]
		return (sorted_data)

	def get_ballstriking_data(self, year):
		
		data = self.sort_data(year)
		ball_striking_data = data[0]
		return (ball_striking_data)

	def get_scoring_data(self, year):
		
		data = self.sort_data(year)
		scoring_data = data[1]
		return (scoring_data)



