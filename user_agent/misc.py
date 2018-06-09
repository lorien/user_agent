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
    total = sum(w for v, w in applicants)
    assert total > 0
    rw = uniform(0, total)
    pr = 0
    for v, w in applicants:
        if pr + w > rw:
            return v
        pr += w


