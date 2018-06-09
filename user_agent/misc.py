# -*- coding: utf-8 -*-

from random import uniform


def weighted_choice(applicants):
    """
    A weighted version of `random.choice`.

    :param applicants: value-to-weight mappings
    :type applicants: dict or tuple or list

    """
    if isinstance(applicants, dict):
        applicants = applicants.items()
    total = sum(w for c, w in applicants)
    rw = uniform(0, total)
    pr = 0
    for c, w in choices:
        if pr + w > rw:
            return c
        pr += w


