#!/usr/bin/python3
# Copyright (c) 2015 Benjamin and Barton Massey
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Elo Rating update calculator
# for Smash match (assumes 5-game match)
# http://en.wikipedia.org/wiki/Elo_rating_system

from sys import argv
import elo

# UCSF uses 32 for weaker players,
# 16 for masters.
k = 32

# Current rating of a.
ra = int(argv[1])
# Current rating of b.
rb = int(argv[2])
# Score difference in the match.
s = int(argv[3])

# Normalized actual score of a.
ns = (s + 3) / 6

# Print adjusted Elo rating of a.
print(elo.update(ra, rb, s, k=k))
