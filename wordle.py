import sys
import pandas as pd

# OPTIONAL: change the length of the secret word ;default value is 5
length = int(sys.argv[1]) if len(sys.argv) == 2 else 5

# you always get 1 extra attempt per letter
attempts = length+1

# select a word
words = pd.read_csv(f'words_{length}.csv')
target = words.sample().iloc[0]['Word']

# break it up into letters
target_letters = list(target.lower())

# here we allow all words in
words_plus = pd.read_csv('SUBTLEX-US frequency list with PoS and Zipf information.csv')
words_plus = words_plus['Word'].tolist()

print(f'\n\nYou have {attempts} attempts to guess the secret {length}-letter word!\nIf a letter in the word you guess is in the same position as the secret word,\nit will be marked in \033[1;42m green \033[0m. If a letter in the word you guess is in the secret\nword, but in another position, it will be marked in \033[1;43m yellow \033[0m.\nOtherwise, the letter will simply not be marked if it does not appear\nin the secret word.')

# initialize a counter
guess_counter = 1

# initialize a guess
guess = 'x' * length

while guess != target:

	# if youve made 6 guesses the game is over
	if guess_counter > attempts:
		print(f'The secret word was {target}. Better luck next time!')
		sys.exit()

	# make a guess
	guess = input(f"\nGuess {guess_counter}: ")

	# if youre guess wasn't long enough guess again
	while len(guess) != length:
		print(f'Your guess must be {length} characters!')
		guess = input(f"\nGuess {guess_counter}: ")		

	# if its not a real word guess again
	while guess not in words_plus:
		print('Your guess is not a known word! Check your spelling.')
		guess = input(f"\nGuess {guess_counter}: ")				

	# break up the guess into letters
	letters = list(guess.lower())

	# initialize lists to keep track of correctness of the guess
	green = []
	yellow = []
	white = []

	# when a letter is in the right place, a duplicate in the wrong place should
	# be grey not yellow so we need to keep track of these things
	remaining_letters = target_letters[:]

	# go through each letter to see if its in the word and in the right position
	for i in range(len(letters)):
		if letters[i] == target_letters[i]:
			green.append(i)
			remaining_letters.remove(target_letters[i])
	
	# now see if the letter appears elsewhere in the word
	for i in range(len(letters)):
		if letters[i] in remaining_letters:
			yellow.append(i)
			remaining_letters.remove(letters[i])
		else:
			white.append(i)
			continue

	# initialize the feedback prinout
	feedback = []
	
	# color code each letter
	for i in range(len(letters)):
		if i in green:
			feedback.append('\033[1;42m ' + str(letters[i]) + ' \033[0m')
		elif i in yellow:
			feedback.append('\033[1;43m ' + str(letters[i]) + ' \033[0m')
		else:
			feedback.append('\033[1;37m ' + str(letters[i]) + ' \033[0m')

	feedback2 = ' '.join(feedback)
	print(feedback2)

	# print congrats if you guess it
	if letters == target_letters:
		print(f'\nCongratulations!! The secret word was {target} \n\n')

	guess_counter += 1