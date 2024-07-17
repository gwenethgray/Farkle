import matplotlib.pyplot as plt

robot_mean_heuristics = {1: 450, 2: 800, 3: 1150, 4: 1250, 5: 1500, 6: 999999}
robot_median_heuristics = {1: 550, 2: 1000, 3: 1200, 4: 1150, 5: 1450, 6: 999999}

N_histories = 10000
scores = {"mean": [], "median": [], "random": []}

for i in range(N_histories):
    game = FarkleGame(players=[
        Player(name="MeanRobot", score_safety_caps=robot_mean_heuristics),
        Player(name="MedianRobot", score_safety_caps=robot_median_heuristics),
        Player(name="RandomRobot", score_safety_caps="random")])
    game.begin()
    scores["mean"].append(game.players[0].total_score)
    scores["median"].append(game.players[1].total_score)
    scores["random"].append(game.players[2].total_score)

fig, ax = plt.subplots(figsize=(8,6))

for algorithm, data in scores.items():
    plt.hist(data, alpha=0.5, label=algorithm)
    
plt.legend(loc='upper right') 
plt.title('FarkleBot Algorithms')
plt.ylabel("Frequency")
plt.xlabel("Score")
plt.show()