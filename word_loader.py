class WordLoader:
	def __init__(self):
		self.real_words = {}
		self.fake_words = {}

		self.load_for(language="english")

	def load_for(self, language):
		self.real_words[language] = load_dictionary(language)
		self.fake_words[language] = load_fake_words(language + "/markov-chain-size-3.txt")

	def get_real_words_for(self, language):
		return self.real_words[language]

	def get_fake_words_for(self, language):
		return self.fake_words[language]

class Word:
	def __init__(self, word):
		self.word = word
		self.definition = ''

	def __str__(self):
		return 'Word(word={}, definition={})'.format(self.word, self.definition)

	def __repr__(self):
		return str(self)

	def __iter__(self):
		yield self.word
		yield self.definition

	def serialize(self):
		return {'word': self.word, 'definition': self.definition}

def save_words(words, lang, model):
	with open('data/{}/{}.txt'.format(lang, model), 'w+') as f:
		for word in words:
			print(word, file=f)

def filter_text(text):
	return ''.join(c for c in text if c.isalpha() or c.isspace())

def filter_words(words):
	pass

def load_fake_words(file):
	words = []

	with open('data/' + file) as f:
		for line in map(lambda x: x.strip('\n'), f):
			words.append(Word(line.lower()))

	return words

def is_definition(line):
	return line.upper() == line and line != ''

def load_dictionary(lang):
	words = []
	current_word = None

	with open('data/{}/dictionary.txt'.format(lang)) as f:
		for line in map(lambda x: x.strip('\n'), f):

			if current_word is None:
				current_word = Word(line.lower())
				continue

			if is_definition(line):
				words.append(current_word)
				current_word = Word(line.lower())
			else:
				current_word.definition += line + '\n'

	words.append(current_word)

	filter_words(words)

	return words
