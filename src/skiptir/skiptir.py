#!/usr/bin/env python3

import sys
import re
from Pyphen import pyphen

# prepare the Pyphen hyphenator object
# (includes loading hyphenation dictionary from file)
hyphenator = pyphen.Pyphen(lang='is_2020_alpha2_extra', left=1, right=2)

# Hyphenates a string of text, preserving its whitespace intact.
# The hyphenation mode can be specified as well as the particular
# hyphen character to be used (soft hyphen, U+00AD, by default).
def hyphenate(input_text, hyphenation_mode='pattern', hyphen_character='\u00AD'):
  if hyphenation_mode == None:
    hyphenation_mode = 'pattern'
    
  output_text = ''
  
  if hyphenation_mode == 'pattern':
    # list for separated words and strings of whitespace from the input
    # guaranteed to return the first string as '' or whitespace
    words_and_whitespace = re.split(r'(\S+)', input_text)
  
    # corresponding list for the hyphenated output
    hyphenated_words_and_whitespace = []
    # first string will be whitespace (or an empty string)
    is_space = True
  
    for item in words_and_whitespace:
      if is_space:
        # add the spaces directly to the output
        hyphenated_words_and_whitespace.append(item)
        # the next item will not be whitespace
        is_space = False
      else: # i.e. if it's a word
        # hyphenate the word (note that the hyphen is a soft hyphen (U+00AD))
        hyphenated_words_and_whitespace.append(hyphenator.inserted(item, hyphen=hyphen_character))
        # the next item will be whitespace
        is_space = True

    output_text = ''.join(hyphenated_words_and_whitespace)
    
    return output_text
  
  else:
    return ''

# Hyphenates text from standard input and prints the result
# to standard output.
def main():
  import argparse
  
  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', default='pattern')
  parser.add_argument('--hyphen', default='\u00AD')
  args = parser.parse_args()
  
  input_text = sys.stdin.read()
  print(hyphenate(input_text, hyphenation_mode=args.mode, hyphen_character=args.hyphen))

if __name__ == '__main__':
    main()
