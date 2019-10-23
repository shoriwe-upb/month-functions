import cmd
import dependencies


# API to work with the month methods
class InteractiveCommand(cmd.Cmd):
	def __init__(self):
		super().__init__(cmd.Cmd)
		self.month = dependencies.Month()
		self.loaded = False

	def do_print(self, line):
		self.month.print()

	def do_change(self, line):
		"Usage: change DAY TEMP"
		try:
			day, temperature = line.split(" ")
			self.month[int(day)] = int(temperature)
		except:
			if not self.loaded:
				print("Data loaded:", self.loaded)
			print("Usage: change DAY TEMP")

	def do_generate(self, line):
		"Usage: generate [INT INT]"
		try:
			if not len(line):
				min_temp, max_temp = 18, 30
			else:
				min_temp, max_temp = line.split(" ")
			weeks = dependencies.generate(int(min_temp), int(max_temp))
			self.month.load_weeks(weeks)
			self.loaded = True
		except ValueError:
			print("Error doing the data generation")
			print("Usage: generate [INT INT]")
			print()

	def do_average_per_week(self, line):
		if self.loaded:
			for week_index, week in enumerate(self.month.week_average()):
				print(f"Week {week_index+1}: {week}")
		else:
			print('No data loaded')

	def do_week_peaks(self, line):
		try:
			for week_index, week in enumerate(self.month.temperature_peaks_in_weeks()):
				print(f"Week {week_index+1}")
				print("Minimum:", *week["min"])
				print("Maximum:", *week["max"])
				print()
		except Exception as e:
			print()

	def do_month_peaks(self, line):
		try:
			week = self.month.temperature_peaks_in_month()
			print("Minimum:", *week["min"])
			print("Maximum:", *week["max"])
			print()
		except IndexError:
			if not self.loaded:
				print("Data loaded:", self.loaded)
			else:
				print("Unknow error")
	
	def do_exit(self, line):
		exit(-1)


if __name__ == "__main__":
	control = InteractiveCommand()
	control.cmdloop()

