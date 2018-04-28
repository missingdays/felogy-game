from dictionary_loader import EnglishDictionaryLoader, RussianDictionaryLoader, Word

class WordLoader:
	def __init__(self):
		self.real_words = {}
		self.fake_words = {}

		self.load_for(language="english")
		self.load_for(language="russian")

	def load_for(self, language):
		self.real_words[language] = load_dictionary(language)
		self.fake_words[language] = load_fake_words(language + "/markov-chain-size-3.txt")

	def get_real_words_for(self, language):
		return self.real_words[language]

	def get_fake_words_for(self, language):
		return self.fake_words[language]

def save_words(words, lang, model):
	with open('data/{}/{}.txt'.format(lang, model), 'w+', encoding='utf-8') as f:
		for word in words:
			print(word, file=f)

def load_fake_words(file):
	words = []

	with open('data/' + file, encoding='utf-8') as f:
		for line in map(lambda x: x.strip('\n'), f):
			words.append(Word(line.lower()))

	return words

def load_dictionary(lang):
	if lang == 'english':
		return EnglishDictionaryLoader('data/english/dictionary.txt').load()
	elif lang == 'russian':
		return RussianDictionaryLoader('data/russian/dictionary.txt').load()

if __name__ == "__main__":
	print([word for word in load_dictionary('russian')][:10])