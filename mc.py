import markovify
from util import get_dictionary, save_words

dictionary_set = set()
LANGUAGE = 'english'

def generate_text():
	dictionary = get_dictionary(LANGUAGE)

	text = ''

	for word, definition in dictionary:
		dictionary_set.add(word)

		word = "".join(map(lambda x: " {} ".format(x), word))
		text += word + '.'

	return text

def is_bad_word(word):
	return len(word) > 10

def generate_words(model):

	words = set()

	while True:
		try:
			new_words = ''.join(model.chain.walk()).split('.')

			for new_word in new_words:
				if new_word in words or new_word in dictionary_set:
					continue

				if is_bad_word(new_word):
					continue

				words.add(new_word)

				if len(words) % 1000 == 0:
					print('generated {} words'.format(len(words)))

		except KeyboardInterrupt:
			break

	save_words(words=words, lang=LANGUAGE, model='markov-chain-size-4')

if __name__ == "__main__":
	print('Generating text')

	text = generate_text()
	
	print('Fitting model')
	model = markovify.Text(text, state_size=4)

	print('Generating words')

	generate_words(model)