# Generate output to measure time spent on processing
from datetime import datetime
import time
from pwdpy import PasswordGenerator

start = time.time()

pgen4 = PasswordGenerator(
    length=1,
    symbols=False,
    numbers=True,
    uppercase=False,
    lowercase=False)

password = pgen4.generate()
#print(len(pgen4.NUMBERS+pgen4.LOWER_CASE+pgen4.UPPER_CASE+pgen4.SYMBOLS))
#print(pgen4.NUMBERS+pgen4.LOWER_CASE+pgen4.UPPER_CASE+pgen4.SYMBOLS)

print("password: " + password)

guess = ""
found = False

print(pgen4.getStrength())

exit()

while found == False:
    # Max base is 92, the len of 5479231608oyjbwsqzimtalrfnvudgcxphkePGWUCZNXEOKVJYHAQMIDLTSFRB'?[^)&|:{/%@!`$}=,+;(]_\-#*."~
    for j in pgen4.getMaxDomain():
        if password == guess + j:
            print("Guessed it! : " + guess + j)
            found = True

#    done = time.time()
#    elapsed = done - start
#    print("{} : {}".format(i*j, elapsed))
