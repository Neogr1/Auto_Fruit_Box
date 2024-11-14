def pseudo_genetic_algorithm(grid, Policy, num_epoch=10, max_depth=5, max_iter=10):
    max_score = 0
    best_boxes = []

    for epoch in range(num_epoch):
        print("EPOCH:", epoch)
        for depth in range(max_depth):
            determined_boxes = best_boxes[:depth]
            for _ in range(max_iter):
                policy = Policy(grid, boxes=determined_boxes)
                boxes = policy.execute()
                score = policy.get_score()
                if score > max_score:
                    print("Found", score)
                    max_score = score
                    best_boxes = boxes
    
    print("Expected score:", max_score)
    return best_boxes


if __name__ == "__main__":
    import random
    import Policy

    grid = [[random.randint(1, 9) for _ in range(17)] for _ in range(10)]
    pseudo_genetic_algorithm(grid, Policy=Policy.GreedySelection_PositionFirst)
    for row in grid:
        print(*row)