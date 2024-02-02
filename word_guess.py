import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import randint
import time

# Function for calculating lexical diversity of the given text.
def lexical_diversity(text):
    return len(set(text)) / len(text)

# ---------------------------------------------------------------------------------------------------------------------------------------------

# Preprocessing function to tokenize, lemmatize and get the first 50 nouns from the lemmatized text.
def preprocess(tokenized_anatomy):
    
    # filtering words that are stopwords and have length less than 5 characters and converting them to lower case through list comprehension.
    tokenized_anatomy = [t.lower() for t in tokenized_anatomy if t.isalpha() and t not in stopwords.words('english') and len(t)>5]
    
    # lemmatizer to convert words to its base form.
    wnl = WordNetLemmatizer()
    lemmatized_anatomy = [wnl.lemmatize(t) for t in tokenized_anatomy]
    
    # --------Displaying only 20 words from the lists, just remove the '[:20]' suffix to display whole list ------------
    
    # making a set of lemmas list to get the distinct words.
    unique_lemmas = list(set(lemmatized_anatomy))
    print("\n \n20 Unique lemmas in the text:\n", unique_lemmas[:20])
    
    time.sleep(5)
    
    # pos_tags method used to assign the type of the word with respect to the english grammer- nouns, verbs, adjectives, etc.
    pos_tags = nltk.pos_tag(unique_lemmas)
    print("\npos_tags of the 20 unique lemmas:\n", pos_tags[:20])
    
    time.sleep(5)
    
    # Getting a list of nouns from the pos_tags dictionary.
    nouns = [tokens for tokens, pos in pos_tags if pos.startswith("NN")]
    print("\nList of nouns: (Displaying 20 for compactness)\n", nouns[:20])
    
    time.sleep(5)
    
    print("\nNumber of tokens:", len(tokenized_anatomy))
    print("Number of nouns:", len(nouns))
    
    return tokenized_anatomy, nouns

# ----------------------------------------------------------------------------------------------------------------------------------------------

# function for guessing game.
def guess_game(points, most_common_words):
    # generating a random integer between 1-50.
    random_number = randint(1, 50)
    
    #list and string of dashes for displaying guessing progress to user. 
    dash_list=[]
    dash_string = ""
    input_list=[]
    
    # getting a random word of index random_number from the most common words list.
    random_word = most_common_words[random_number].upper()
    # print("Word is :", random_word) (test code)
    random_word_length = len(random_word)
    
    # creating a list and string of dashes of the length of the random word generated.
    for i in range(random_word_length):
        dash_list.append('_')
    dash_string = ' '.join(dash_list)
    
    # Game begins here - we check if the points > 0 and there are any letters left to guess.
    while(points > 0 and '_' in dash_string):
        print("\nCurrent Points:", points)
        print("\n", dash_string)
        chr = input("Guess the letter:").upper()
        
        # condition for the same input character entered again. 
        if chr in input_list:
            print("\nAlready entered the letter, enter another!!!")  
            print("Eliminated letters: ", ' , '.join(input_list))
        
        # condition for input being more than one character
        elif len(chr)>1:
            print("You need to enter a letter, not a word")
            
        # condition for input other than alphabet being entered.
        elif chr.isalpha() == False:
            print("You need to enter a letter!!!")
        
        # checking if the input character is in the given word.
        elif chr in random_word and chr not in input_list:
            
            # generating list of indexed the input character is present in.
            res = [i for i in range(random_word_length) if random_word.startswith(chr, i)]
            
            # changing the dash_list with the characters input until current point to show the users.
            for i in range(len(res)):
                dash_list[res[i]] = chr
                
            # creating string with spaces for a neat display of progress.
            dash_string = ' '.join(dash_list)
            
            # updating list so that user should get appropriate message for repeating inputs.
            input_list.append(chr)
            points+=1
            print("Correct! Points is incremented by 1")
        
        
        # condition for wrong guess.   
        elif chr not in random_word and chr.isalpha(): 
            print("\nErrr! Wrong letter :(")
            points -=1
            input_list.append(chr)
        
        
    
    # if all points lost before guessing the word, display losing message and the word.
    if points ==0 and '_' in dash_string:
        print("\nSorry you lost! The word is:", random_word)
    
    # if all letters guessed correctly before losing points, display winning message. 
    elif points>0 and '_' not in dash_string:
        print("\nCongratulations! You found the word!: ", random_word)   
    
    # returning current points to carry over to the next round
    return points

# --------------------------------------------------------------------------------------------------------------------------------------------

def main():
    # opening the given text file about anatomy
    with open('anat19.txt', 'r') as f:
        anatomy = f.read()

    # remove newline characters
    anatomy = anatomy.replace('\n', ' ')

    # split the text into tokens using word_tokenize method of nltk
    tokenized_anatomy = word_tokenize(anatomy)
    
    # calling the function to calculate lexical diversity of the given text
    lex_value = lexical_diversity(tokenized_anatomy)
    print("\n \nLexical Diversity of anat.txt: ", "{:.2f}".format(lex_value))

    # getting list of all tokens and nouns in the given text file
    tokens, nouns = preprocess(tokenized_anatomy)

    # creating a dictionary of nouns and their counts in the tokens list
    noun_dict = {}

    # assigning keys of nouns and their values of counts to the noun_dict dictionary
    for noun in nouns:
        noun_dict[noun] = tokens.count(noun)

    # print(noun_dict) (test code)

    # sorting the noun_dict in descending order
    sorted_noun_count = sorted(noun_dict.items(), key=lambda x:x[1], reverse=True )

    # getting top 50 nouns according to their frequency in the tokens list
    top_50_nouns = dict(sorted_noun_count[:50])

    time.sleep(5)

    # converting the dictionary to the list of nouns without their counts
    most_common_words = list(top_50_nouns.keys())
    print("\n \n50 most common nouns in anatomy.txt:\n", most_common_words)

    time.sleep(3)

    print("\n \n Getting 'rope' ready for hangman (game) ................")
    
    # just a delay so that the user can mentally prepare to play the game
    time.sleep(5)

    print("\n \n \n")
    print("--------------------------------------------------------------------------------------------------------------------------------")
    print("WELCOME TO THE HANGMAN GAME!!!:")
    print("You have 5 points initially which would be deducted for every wrong guess of the letter")
    print("There are 50 random words chosen from the topic of anatomy.")
    print("You will be prompted if you want to play again or quit at the end of every round.")
    print("--------------------------------------------------------------------------------------------------------------------------------")

    # assigning 5 points to the user.
    points = 5
    
    # initializing the game continuing value to yes
    yes_or_no = 'Y'

    print("\nLets begin!")
    
    # while loop for continuing game
    while(yes_or_no == 'Y' or yes_or_no =='y'):
        # calling the function to play the game and getting current value of points
        points = guess_game(points, most_common_words)
        
        #getting input for whether user wants to continue or quit. 
        yes_or_no = input("\nPlay again? Y/N: ")
        
        # display byebye message if user wants to leave.
        if(yes_or_no != 'Y' and yes_or_no != 'y'):
            print("\n \nThanks for playing!\n \n")
            
        # print(points) (test code)
        
        # if points are zero, then reset the value so that user can play forever.
        if points == 0:
            points = 5
            
        # capping points at 10 because of taxes
        elif points > 10:
            points = 10
            
# -------------------------------------------------------------------------------------------------------------------------------------------        
main()