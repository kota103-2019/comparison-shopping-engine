from nltk
nltk.download('punkt')

word_input = "OPPO A5s 2GB/32GB-Black (Garansi Resmi)"
word_decapital = word_input.lower()
print(word_decapital)

word_rep = word_decapital.replace("/", " ")
word_rep = word_rep.replace("-", " ")

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
no_punct = ""
for char in word_rep:
   if char not in punctuations:
       no_punct = no_punct + char

print(no_punct)

word_tokens = nltk.word_tokenize(no_punct)

for i in range(len(word_tokens)):
  print(word_tokens[i], i)

# print (word_tokens)
