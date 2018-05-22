import autocomplete

# load pickled python Counter objects representing our predictive models
# I use Peter Norvigs big.txt (http://norvig.com/big.txt) to create the predictive models
autocomplete.load()

# imagine writing "the b"
autocomplete.predict('the','b')
