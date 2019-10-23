import statistics
import random


class Month(object):
	def __init__(self):
		self.__ref = "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
		self.weeks = []

	def __setitem__(self, key, value):
		current_day = 1
		if type(key) != int:
			if key < 1 or key > 31:
				raise IndexError
			raise ValueError
		if type(value) not in (int, float):
			raise ValueError
		if len(self.weeks):
			for week_index, week in enumerate(self.weeks):
				for day_index, day in enumerate(week):
					if key == current_day:
						self.weeks[week_index][day_index] = value
						return None
					current_day += 1
		else:
			raise IndexError

	def load_weeks(self, weeks_to_load):
		self.weeks.clear()
		for index, week in enumerate(weeks_to_load):
			if index == 4:  # The last week of the month is without seven days
				self.weeks.append(week[:3])
			else:
				self.weeks.append(week)

	def temperature_peaks_in_weeks(self):
		for week in self.weeks:
			result = {"min": [week[0], self.__ref[0]], "max": [week[0], self.__ref[0]]}
			for index, day in enumerate(week):
				if day < result["min"][0]:
					result["min"][0] = day
					result["min"][1] = self.__ref[index]
				if day > result["max"][0]:
					result["max"][0] = day
					result["max"][1] = self.__ref[index]
			yield result

	def week_average(self):
		for week in self.weeks:
			yield statistics.mean(week)

	def temperature_peaks_in_month(self):
		result = {
			"min": [self.weeks[0][0], self.__ref[0], 1],
			"max": [self.weeks[0][0], self.__ref[0], 1]
		}
		day = 1
		day_name = 0
		for week in self.weeks:
			for day_temp in week:
				if day_temp < result["min"][0]:
					result["min"][0] = day_temp
					result["min"][1] = self.__ref[day_name]
					result["min"][2] = day
				if day_temp > result["max"][0]:
					result["max"][0] = day_temp
					result["max"][1] = self.__ref[day_name]
					result["max"][2] = day
				day += 1
				day_name += 1
				if day_name > 6:
					day_name = 0
		return result

	def print(self):
		sizes_ = [0, 0, 0, 0, 0, 0, 0]
		for day_index in range(7):
			for line_index, line in enumerate([self.__ref] + self.weeks):
				if not (day_index > 2 and line_index == 5):
					size_ = len(str(line[day_index]))
					if sizes_[day_index] < size_:
						sizes_[day_index] = size_
		lines = []
		for line in [self.__ref] + self.weeks:
			values = []
			for index in range(7):
				try:
					values.append(" " * (sizes_[index] - len(str(line[index]))) +
																			str(line[index]))
				except IndexError:
					pass
			str_line = "# " + " # ".join(values) + " #"
			lines.append(str_line)
			lines.append("#" * len(str_line))
		lines.insert(0, "#" * len(lines[0]))
		print("\n".join(lines))
		print()


def generate(min_, max_):
	return [[random.randint(min_, max_) for day_ in range(7)]
									for week_ in range(5)]

