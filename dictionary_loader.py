class DictionaryLoader:
	def is_word(self, word):
		return word.upper() == word and word != ''

class Word:
	def __init__(self, word, definition=''):
		self.word = word
		self.definition = definition

	def __str__(self):
		return 'Word(word={}, definition={})'.format(self.word, self.definition)

	def __repr__(self):
		return str(self)

	def __iter__(self):
		yield self.word
		yield self.definition

	def serialize(self):
		return {'word': self.word, 'definition': self.definition}

class EnglishDictionaryLoader(DictionaryLoader):
	def __init__(self, filename):
		self.filename = filename

	def load(self):
		words = []
		current_word = None

		with open(self.filename) as f:
			for line in map(lambda x: x.strip('\n'), f):

				if current_word is None:
					current_word = Word(line.lower())
					continue

				if self.is_word(line):
					words.append(current_word)
					current_word = Word(line.lower())
				else:
					current_word.definition += line + '\n'

		words.append(current_word)

		return words

class RussianDictionaryLoader(DictionaryLoader):
	def __init__(self, filename):
		self.filename = filename

	def load(self):
		words = []

		with open(self.filename, encoding='utf-8') as f:
			for line in map(lambda x: x.strip('\n'), f):
				row = line.split(',')

				if len(row) == 1:
					continue

				if not self.is_word(row[0]):
					continue

				word = row[0].lower()
				definition = ','.join(row[1:]).lower()

				if self.is_bad_word(word) or self.is_bad_definition(definition):
					continue

				words.append(Word(word, definition))

		return words

	def is_bad_word(self, word):
		return ''.join(c for c in word if c.isalpha()) != word

	def is_bad_definition(self, word):
		return "_" in word
