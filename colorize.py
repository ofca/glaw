def colorize(text, color):
	colors = {
		'pink': '\033[95m',
		'blue': '\033[94m',
		'green': '\033[92m',
		'yellow': '\033[93m',
		'red': '\033[91m'
	}

	end = '\033[0m'

	return colors[color] + text + end