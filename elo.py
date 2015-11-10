# Copyright (c) 2015 Benjamin and Barton Massey
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Elo calculation
# http://en.wikipedia.org/wiki/Elo_rating_system

# Given the current rating of a, the current rating
# of b, and the new score normalized from 1 (a wins) to
# 0 (b wins), return an updated rating.
def update(ra, rb, s, k=32):
    # Expected score of a based on ratings.
    ea = 1 / (1 + 10**((rb - ra) / 400))
    # Adjusted ratig of a
    return ra + k * (s - ea)
