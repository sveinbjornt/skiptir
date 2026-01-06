#!/usr/bin/env python3

### Test script for hyphenation pattern lists
### Certain custom pattern lists (e.g. is_1985_corrected) are hard-coded into this file
### – change as needed.
###
### Author: Kristján Rúnarsson (krunars@gmail.com)
###
### Call this script thus:
###   hyphenation_test.py [GOLD STANDARD] [TEST INPUT]
### where [GOLD STANDARD] is the filename of a hand-corrected standard hyphenation list
### and [TEST INPUT] is the name of a file containing unhyphenated words for testing.
### The script assumes that all of the test input is represented in the gold standard.

import sys
from Pyphen import pyphen

# dictionary of hyphenated words
standard_hyphenated_words = {}
# dictionary of hyphenation positions for words
standard_hyphenation_positions = {}
# import gold standard (hand-corrected test data)
with open(sys.argv[1], 'r') as gold_standard:
  # find hyphens and log their position
  for line in gold_standard:
    split_word = line.strip().split('-')
    current_hyphen_position = 0
    hyphen_positions = []
    for part in split_word[:-1]:
      current_hyphen_position += len(part)
      hyphen_positions.append(current_hyphen_position)
    # if there was no split, we don't enter the for-loop
    # and hyphen_positions remains empty
    
    # hyphenated word added to dictionary
    standard_hyphenated_words[''.join(split_word)] = line.strip()
    
    # hyphen positions added to dictionary
    standard_hyphenation_positions[''.join(split_word)] = hyphen_positions


# preparing Pyphen hyphenator objects for the different sets of hyphenation patterns
# (including loading hyphenation dictionaries from file)

# make subclass of Pyphen that includes name
class NamedHyphenator(pyphen.Pyphen):
  # note that this subclass has been configured with a default left minimum
  # of 1 and a right minimum of 2, the standard for Icelandic
  def __init__(self, filename=None, lang=None, left=1, right=2, cache=True, name='[UNNAMED HYPHENATOR]'):
    super().__init__(filename, lang, left, right, cache)
    self.name = name

# Jörgen Pind's patterns generated from IBM data in 1987, modified in 1988
hyphenator_pind = NamedHyphenator(lang='is_JPind_1988', name='J. Pind’s 1988 patterns')

# Skipta from 1985 (built into Pyphen)
hyphenator_old = NamedHyphenator(lang='is', name='Original Skipta patterns (1985)')

# Skipta from 1985 (built into Pyphen)
hyphenator_unchanged = NamedHyphenator(lang='is_1985_unchanged_list', name='New patterns from 1985 list')

# Skipta with corrections to the hyphenation list but no additions
hyphenator_corrected = NamedHyphenator(lang='is_1985_corrected', name='Corrected')

# Skipta with corrections and additions
hyphenator_with_additions = NamedHyphenator(lang='is_2020_alpha', name='Corrected with additions')

# Skipta with more additions
hyphenator_with_more_additions = NamedHyphenator(lang='is_2020_alpha2_extra', name='Corrected with more additions')

hyphenators = [hyphenator_pind,
  hyphenator_old,
  hyphenator_unchanged,
  hyphenator_corrected,
  hyphenator_with_additions,
  hyphenator_with_more_additions]

# collecting 
with open(sys.argv[2], 'r') as test_input:
  test_words = [line.strip() for line in test_input]

# print table header
print('\t'.join(['HYPHENATOR', 'Perfect words', 'Okay words', 'Bad words', 'Good hyphens', 'Bad hyphens']))

# test each hyphenator in turn and print results
for hyphenator in hyphenators:
  
  # counters:
  
  # words that were hyphenated perfectly (all correct points identified and no incorrect hyphens inserted)
  perfect_words = 0
  # words that had no bad hyphens but didn't have all possible hyphens
  okay_words = 0
  # words that had one ore more bad hyphens
  bad_words = 0
  # all possible hyphenation points, calculated from the gold standard
  all_hyphens = 0
  # hyphens that were found in a correct position
  good_hyphens = 0
  # incorrectly placed hyphens
  bad_hyphens = 0
  
  # open output file for this hyphenator (input filename + -output.txt)
  output_file = open(sys.argv[2]+f'-output-{hyphenator.name.replace(" ", "_")}.txt', 'w')
  output_file.write(f'Hyphenating words according to {hyphenator.name}; showing errors below.\n' \
  f'Correct hyphenations from the gold standard are shown in the left column\n' \
  f'next to differing actual hyphenations in the right column.\n\n')
  
  for word in test_words:
    actual_hyphenation_points = hyphenator.positions(word)
    standard_hyphenation_points = standard_hyphenation_positions[word]
    all_points = len(standard_hyphenation_points)
    good_points = 0
    bad_points = 0
    
    for point in actual_hyphenation_points:
      # assuming that there is no Pyphen data for “nonstandard hyphenation”
      assert point.data == None
      if point in standard_hyphenation_points:
        good_points += 1
      else:
        bad_points += 1
    
    if bad_points == 0:
      if good_points == all_points:
        perfect_words += 1
      else:
        okay_words += 1
    else:
      bad_words += 1
      
    all_hyphens += all_points
    good_hyphens += good_points
    bad_hyphens += bad_points
    
    # print hyphenations that differ from the standard to the output file (not to stdout)
    if not good_points == all_points:
      # standard on left, actual on right
      output_file.write(standard_hyphenated_words[word] + '\t' + hyphenator.inserted(word, hyphen='-') + '\n')
  
  # close output file
  output_file.close()
  
  # calculate results:
  percentage_perfect_words = 100 * perfect_words / len(test_words)
  percentage_okay_words = 100 * okay_words / len(test_words)
  percentage_bad_words = 100 * bad_words / len(test_words)
  
  percentage_good_hyphens = 100 * good_hyphens / all_hyphens
  percentage_bad_hyphens = 100 * bad_hyphens / all_hyphens
  
  # print table line for hyphenator
  print('\t'.join(
    [hyphenator.name,
    f'{percentage_perfect_words}%',
    f'{percentage_okay_words}%',
    f'{percentage_bad_words}%',
    f'{percentage_good_hyphens}%',
    f'{percentage_bad_hyphens}%']
  ))
