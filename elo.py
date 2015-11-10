#!/usr/bin/python3
# Copyright (c) 2015 Bart Massey
# Elo Rating update calculator
# for Smash match (assumes 5-game match)
# http://en.wikipedia.org/wiki/Elo_rating_system

from sys import argv

# UCSF uses 32 for weaker players,
# 16 for masters.
k = 32

# Current rating of a.
ra = int(argv[1])
# Current rating of b.
rb = int(argv[2])
# Score difference in the match.
s = int(argv[3])

# Expected score of a based on ratings.
ea = 1 / (1 + 10**((rb - ra) / 400))

# Normalized actual score of a.
ns = (s + 3) / 6

# Print adjusted Elo rating of a.
print(ra + k * (ns - ea))
