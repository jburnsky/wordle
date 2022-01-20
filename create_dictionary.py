import pandas as pd
import sys

# OPTIONAL: change the length of the secret word or the frequency cutoff
# default value is 5 and 4, respectively
if len(sys.argv) == 3:
	length = int(sys.argv[1])
	freq = float(sys.argv[2])
elif len(sys.argv) == 2:
	length = int(sys.argv[1])
	freq = 4
else:
	length = 5
	freq = 4

# read in the subtlex csv
subtlex = pd.read_csv('SUBTLEX-US frequency list with PoS and Zipf information.csv')

# we only care about the word, the POS, the frequency and the length
subtlex_basic = subtlex[['Word', 'Zipf-value', 'Dom_PoS_SUBTLEX', 'nCharacters']]

# we dont want names, interjections, etc.
good_tags = ['Noun', 'Verb', 'Preposition', 'Adjective', 'Adverb', 'Conjunction', 'Determiner', 'Article']
good_words = subtlex_basic[subtlex_basic.Dom_PoS_SUBTLEX.isin(good_tags)]

# we only want words with a length of X letter
letters =  good_words[good_words['nCharacters']==length]

# we only want words with a frequency of Y
frequent = letters[letters['Zipf-value']>freq]

# just slice out the words
words = frequent[['Word']]

words.to_csv(f'words_{length}.csv', index = False)