import regex as re
# the_string='09:00\n12:30'
the_string='hi-welcome'
if re.search('[a-zA-Z]', the_string):
    print("true")
else:
    print("false")


