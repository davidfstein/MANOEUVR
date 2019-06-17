from models.group import Group
from models.subject import Subject
from parse_subject_csv import parse_subject_csv
from write_groups_csv import write_groups
from models import model_utils
import argparse
import random
import math
import multiprocessing
import timeit

def generate_subjects(path):
    TestSubject = Subject
    subject_dict = parse_subject_csv(path)
    subjects = []
    for subject in subject_dict:
        subjects.append(TestSubject(subject))
    return subjects

def generate_groups(num_groups):
    return [Group([], i) for i in range(num_groups)]

def add_subject_least_difference(groups, subject, subjects_per_group):
    total_differences = []
    for group in groups:
        if len(group.subjects) == subjects_per_group:
            total_differences.append(math.inf)
            continue
        theoretical_total = group.combined_score + subject.combined
        total_difference = 0
        for other_group in groups:
            if other_group == group:
                continue
            total_difference += abs(theoretical_total - other_group.combined_score)
        total_differences.append(total_difference)
    min_diff = math.inf
    min_index = 0
    for i in range(len(total_differences)):
        if total_differences[i] < min_diff:
            min_diff = total_differences[i]
            min_index = i
    groups[min_index].add_subject(subject)

def score_range(groups):
    max_score = 0
    min_score = math.inf
    for group in groups:
        if group.combined_score < min_score:
            min_score = group.combined_score
        if group.combined_score > max_score:
            max_score = group.combined_score
    return max_score - min_score

def best_groups(subjects, iterations, num_groups, subjects_per_group, results):
    best_groups = None
    best_range = math.inf
    for _ in range(iterations):
        random.shuffle(subjects)
        groups = generate_groups(num_groups)
        for subject in subjects:
            add_subject_least_difference(groups, subject, subjects_per_group)
        group_range = score_range(groups)
        if group_range < best_range:
            best_range = group_range
            best_groups = groups
    results.append(best_groups)
    return best_groups

def multi(subjects, iterations, num_groups, subjects_per_group):
    manager = multiprocessing.Manager()
    result = manager.list()
    sub_iters = math.floor(iterations / 8)
    jobs = []
    for _ in range(8):
        p = multiprocessing.Process(target=best_groups, args=(subjects, sub_iters, num_groups, subjects_per_group, result, ))
        jobs.append(p)
        p.start()
    
    for job in jobs:
        job.join()
    return result

def multi_best(groups):
    best_groups = None
    best_range = math.inf
    for group in groups:
        group_range = score_range(group)
        if group_range < best_range:
            best_range = group_range
            best_groups = group
    return best_groups

def main():

    start_time = timeit.default_timer()

    userInput = argparse.ArgumentParser(description=
        'Requires a CSV file as input. Returns a csv file with subjects split into groups.')
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-f', '--file', action='store', type=str,
                                help='Path to the csv file containing subjects.')
    requiredNamed.add_argument('-i', '--iterations', action='store', type=int,
                                help='The number of iterations to shuffle the subjects and greedily find a low variabilty grouping.')
    requiredNamed.add_argument('-g', '--groups', action='store', type=int,
                                help='The number of desired groups.')
    requiredNamed.add_argument('-s', '--SubjectsPerGroup', action='store', type=int,
                                help='The number of desired subjects per group.')

    args = userInput.parse_args()
    input_file = args.file
    iterations = args.iterations
    groups = args.groups
    subjects_per_group = args.SubjectsPerGroup

    subjects = generate_subjects(input_file)
    groups = multi(subjects, iterations, groups, subjects_per_group)
    best = multi_best(groups)
    print(score_range(best))
    write_groups(best)

    print('Execution time %f' % (timeit.default_timer() - start_time))

if __name__ == '__main__':
    main()
