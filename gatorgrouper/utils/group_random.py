""" Promotes diversity by grouping using randomization approach. """

import logging
import random
from typing import List, Union
from gatorgrouper.utils import group_scoring


# pylint: disable=bad-continuation
def group_random_group_size(responses: str, grpsize: int) -> List[List[str]]:
    """ Calculate number of groups based on desired students per group """
    # number of groups = number of students / minimum students per group
    numgrp = int(len(responses) / grpsize)

    return group_random_num_group(responses, numgrp)


def group_random_num_group(responses: str, numgrp: int) -> List[List[str]]:
    """ group responses using randomization approach """

    intensity = 100
    # Intensity is the value that represents the number of attempts made to group
    optimized_groups = list()
    # Optimized Groups holds the groups after scoring maximization
    top_ave = 10000000
    # Top Average is our check to see if the group made is better than the group we have
    while intensity > 0:
        # number of students placed into a group
        stunum = 0
        iterable = iter(responses)
        # number of students in each group (without overflow)
        grpsize = int(len(responses) / numgrp)
        groups = list()
        for _ in range(0, numgrp):
            group = list()
            while len(group) is not grpsize and stunum < len(responses):
                group.append(next(iterable))
                stunum = stunum + 1
            groups.append(group)
        # deal with the last remaining students
        if len(responses) % stunum != 0:
            logging.info("Overflow students identified; distributing into groups.")
        for _x in range(0, len(responses) % stunum):
            groups[_x].append(next(iterable))
            stunum = stunum + 1

        # scoring and return
        conflict_scores, conflict_ave = [], 0
        conflict_scores, conflict_ave = group_scoring.score_groups(groups)
        scores, ave = [], 0
        scores, ave = group_scoring.score_groups(groups)
        logging.info("scores: %d", str(scores))
        logging.info("average: %d", ave)
        logging.info("conflict scores : " + str(conflict_scores))
        logging.info("conflict average : " + str(conflict_ave))
        intensity -= 1

        if top_ave > conflict_ave:
            # TODO: Account for conflict score with average
            top_ave = conflict_ave
            optimized_groups = groups

    return optimized_groups


def shuffle_students(
    responses: Union[str, List[List[Union[str, bool]]]]
) -> List[List[Union[str, bool]]]:
    """ Shuffle the responses """
    shuffled_responses = responses[:]
    random.shuffle(shuffled_responses)
    return shuffled_responses
