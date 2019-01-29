import math

class TextModel:
    def __init__(self, model_name):
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation_freq = {}


    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of word stem: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of each type of punctuation : ' + str(len(self.punctuation_freq)) + '\n'
        return s

    def add_string(self, s):
        """
        Analyzes the string txt and adds its pieces
        to all of the dictionaries in this text model.
        """

        for eachelem in s:
            if eachelem in ",.;'?!:":
                if eachelem in self.punctuation_freq:
                    self.punctuation_freq[eachelem] += 1
                else:
                    self.punctuation_freq[eachelem] = 1
        word_list_unclean = s
        for eachpunc in '.?!':
            word_list_unclean.replace(eachpunc, '.')
        for eachelem in word_list_unclean.split('.'):
            if len(eachelem) != 0:
                if len(eachelem.split()) in self.sentence_lengths:
                    self.sentence_lengths[len(eachelem.split())] += 1
                else:
                    self.sentence_lengths[len(eachelem.split())] = 1
        word_list = clean_text(s)
        for w in word_list:
            if len(w) >= 1:
                w_stem = stem(w)
                if w in self.words:
                    self.words[w] += 1
                else:
                    self.words[w] = 1
                if len(w) in self.word_lengths:
                    self.word_lengths[len(w)] += 1
                else:
                    self.word_lengths[len(w)] = 1
                if w_stem in self.stems:
                    self.stems[w_stem] += 1
                else:
                    self.stems[w_stem] = 1

    def add_file(self, filename):
        """
        adds all of the text in the file identified by filename to the model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()
        self.add_string(text)

    def save_model(self):
        """
        saves the TextModel object self by writing its various feature dictionaries to files
        """
        words_file = self.name + '_words'
        word_lengths_file = self.name + '_word_length'
        stem_file = self.name + '_stems'
        sent_len_file = self.name + '_sentence_lengths'
        punc_freq_file = self.name + '_punctuation_freq'
        f = open(words_file, 'w')
        f.write(str(self.words))
        f.close()
        f = open(word_lengths_file, 'w')
        f.write(str(self.word_lengths))
        f.close()
        f = open(stem_file, 'w')
        f.write(str(self.stems))
        f.close()
        f = open(sent_len_file, 'w')
        f.write(str(self.sentence_lengths))
        f.close()
        f = open(punc_freq_file, 'w')
        f.write(str(self.punctuation_freq))
        f.close()

    def read_model(self):
        """
        reads the stored dictionaries for the called TextModel object from their files and assigns them to the attributes of the called TextModel
        """
        words_file = self.name + '_words'
        word_lengths_file = self.name + '_word_length'
        stem_file = self.name + '_stems'
        sent_len_file = self.name + '_sentence_lengths'
        punc_freq_file = self.name + '_punctuation_freq'
        f = open(words_file, 'r')
        w_str = f.read()
        f.close()
        self.words = dict(eval(w_str))

        f = open(word_lengths_file, 'r')
        w_l_str = f.read()
        f.close()
        self.word_lengths = dict(eval(w_l_str))

        f = open(stem_file, 'r')
        s_str = f.read()
        f.close()
        self.stems = dict(eval(s_str))

        f = open(sent_len_file, 'r')
        s_l_str = f.read()
        f.close()
        self.sentence_lengths = dict(eval(s_l_str))

        f = open(punc_freq_file, 'r')
        p_f_str = f.read()
        f.close()
        self.punctuation_freq = dict(eval(p_f_str))

    def similarity_scores(self, other):
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_freq_score = compare_dictionaries(other.punctuation_freq, self.punctuation_freq)

        return [word_score, word_lengths_score, stem_score, sentence_lengths_score, punctuation_freq_score]

    def classify(self, source1, source2):
        score1 = self.similarity_scores(source1)
        score2 = self.similarity_scores(source2)
        print('scores for ' + source1.name + ':' + str(score1))
        print('scores for ' + source2.name + ':' + str(score2))

        weighted_sum1 = 10*score1[0] + 4*score1[1] + 8*score1[2] + 6*score1[3] + 7*score1[4]
        weighted_sum2 = 10*score2[0] + 4*score2[1] + 8*score2[2] + 6*score2[3] + 7*score2[4]
        if weighted_sum1 > weighted_sum2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        else:
            print(self.name + ' is more likely to have come from ' + source2.name)


def clean_text(txt):
    """
    takes a string of text txt as a parameter and returns a list containing the words in txt after it has been “cleaned”
    """
    wordlist = txt.split()
    for i in range(len(wordlist)):
        if wordlist[i] != '':
            wordlist[i] = wordlist[i].lower()
            if wordlist[i][-1] in ",.;'?!:":
                wordlist[i] = wordlist[i][:-1]
    return wordlist

def stem(s):
    """
    return the stem of s
    """
    word = s

    if len(s) > 1:
        if word[-1] == 's':
            word = stem(word[:-1])
        elif word[-1] == 'y':
            word = word[:-1]
            word += 'i'
        if word[-2:] == 've':
            word = word[:-1]
        elif word[-2:] == 'er':
            word = word[:-2]
        elif word[-2:] == 'ed':
            word = word[:-2]
        elif word[-2:] == 'li':
            word = word[:-2]
        if word[-3:] == 'ing':
            if  len(word) >= 5 and word[-4] == word[-5]:
                word = word[:-4]
            else:
                word = word[:-3]

        if word[-3:] == 'ent':
            word = word[:-3]
        if word[-6:] == 'biliti':
            word = word[:-6]
            word += 'ble'
        else:
            return word
    else:
        return word

def compare_dictionaries(d1, d2):
    score = 0
    total = 0
    for eachkey in d1:
        total += d1[eachkey]
    for eachkey in d2:
        if eachkey in d1:
            score += d2[eachkey] * math.log(d1[eachkey]/total)
        else:
            score += d2[eachkey] * math.log(0.5/total)

    return score
def test():
    """ your docstring goes here """
    source1 = TextModel('Prize essay winner of 2014')
    source1.add_file('2014winner.txt')

    source2 = TextModel('Prize essay winner of 2015')
    source2.add_file('2015winner.txt')

    new1 = TextModel('WR120')
    new1.add_file('wr120.txt')
    new1.classify(source1, source2)
    print()


    new2 = TextModel('Prize essay winner of 2010')
    new2.add_file('2010winner.txt')
    new2.classify(source1, source2)
    print()

    new3 = TextModel("Prize essay winner of 2011")
    new3.add_file('2011winner.txt')
    new3.classify(source1, source2)
    print()


    new4 = TextModel("Shakespeare's works")
    new4.add_file('shakespeare.txt')
    new4.classify(source1, source2)
    print()
