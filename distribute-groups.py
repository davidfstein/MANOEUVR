import random
import math

class Mouse():
    def __init__(self, weight, height):
        self.weight = weight
        self.height = height
        self.combined = weight + height
        self.rank = 0

    def __str__(self):
        return "Weight: " + str(self.weight) + " Height: " + str(self.height) + " Combined: " + str(self.combined) + " Rank: " + str(self.rank)

    def set_rank(self, rank):
        self.rank = rank

    
def generate_mice():
    random.seed(1)
    weights = [random.uniform(2,10) for _ in range(48)]
    lengths = [random.uniform(20,25) for _ in range(48)]
    weight_iter = iter(weights)
    length_iter = iter(lengths)
    mice = []
    for _ in range(len(weights)):
        mice.append(Mouse(next(weight_iter), next(length_iter)))
    return mice

def rank_mice(mice):
    sorted_mice = sorted(mice, key=lambda mouse: mouse.combined)
    ranked_mice = []
    for i in range(len(sorted_mice)):
        ranked_mice.append(sorted_mice[i])
        ranked_mice[i].rank = i
    return ranked_mice

def print_mice(mice):
    for mouse in mice:
        print(mouse)

class Group():
    def __init__(self, mice, num):
        self.mice = mice
        self.group_num = num
        self.combined_score = 0
    
    def set_group_num(self, num):
        self.group_num = num

    def add_mouse(self, mouse):
        self.mice.append(mouse)
        self.combined_score += mouse.combined

    def __str__(self):
        return str([str(mouse) for mouse in self.mice])

def generate_groups(num_groups):
    return [Group([], i) for i in range(num_groups)]

def add_mouse_least_difference(groups, mouse, mice_per_group):
    total_differences = []
    for group in groups:
        if len(group.mice) == mice_per_group:
            total_differences.append(math.inf)
            continue
        theoretical_total = group.combined_score + mouse.combined
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
    groups[min_index].add_mouse(mouse)

def add_mice_to_group(group, mice, mice_per_group):
    start_index = group.group_num * (mice_per_group / 2)
    end_index = len(mice) - group.group_num * (mice_per_group / 2)
    mice_for_group = mice[int(start_index):int(start_index + (mice_per_group / 2))] + mice[int(end_index - (mice_per_group / 2)):int(end_index)]
    for mouse in mice_for_group:
        group.add_mouse(mouse)

def total_mice_weight(group):
    total = 0
    for mouse in group.mice:
        total += mouse.combined
    return total

def score_range(groups):
    max_score = 0
    min_score = math.inf
    for group in groups:
        if group.combined_score < min_score:
            min_score = group.combined_score
        if group.combined_score > max_score:
            max_score = group.combined_score
    return max_score - min_score

def best_groups(mice, iterations, num_groups, mice_per_group):
    best_groups = None
    best_range = math.inf
    for _ in range(iterations):
        random.shuffle(mice)
        groups = generate_groups(num_groups)
        for mouse in mice:
            add_mouse_least_difference(groups, mouse, mice_per_group)
        group_range = score_range(groups)
        if group_range < best_range:
            best_range = group_range
            best_groups = groups
        # print("Best range: " + str(best_range) + " Group range: " + str(group_range))
    return best_groups

if __name__ == '__main__':
    mice = generate_mice()
    # ranked_mice = rank_mice(mice)
    # groups = generate_groups(6)
    # print("Normal Distribution Strategy: \n")
    # for group in groups:
    #     add_mice_to_group(group, mice, 8)
    print("Greedy Strategy: \n")
    # for mouse in mice:
    #     add_mouse_least_difference(groups, mouse, 8)
    groups = best_groups(mice, 100000, 6, 8)
    for group in groups:
        print(str(total_mice_weight(group)) + " " + str(len(group.mice)))
    print("Difference range: " + str(score_range(groups)))


