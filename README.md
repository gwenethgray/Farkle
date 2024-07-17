# Farkle

This dice rolling game has unclear origins, with some trademark holders and fans circulating [popular yet unverified claims](https://farklefan.blogspot.com/2012/01/history-of-farkle.html) that it was first played in Iceland in the 14th century (by a conspicuously-named "Sir Albert Farkle") and first referenced in print during the time of Shakespeare. Rules (see the [rules booklet](https://www.cusd80.com/cms/lib/AZ01001175/centricity/domain/1355/Farkle.pdf) published by SmartBoxGames) may vary on scoring, but the game is generally played by rolling 6 dice, setting aside any combinations which are worth points, and optionally re-rolling leftover non-scoring dice. If you fail to roll any scoring combinations, you get no points for the turn... but if you manage to score with all 6 dice, you can roll them all again and keep stacking up points! The first player to reach 10,000 points wins.

My friend Talon introduced me to it using a version where, when a player chooses to keep the points they've acquired and refrain from re-rolling any remaining dice, the next player has the option of "stealing": they can re-roll the remaining dice, and if they get any scoring combinations (even just a single 1 or a single 5), then they take the first player's points for that turn and keep rolling! However, if they "scratch" by failing to score, then they get no points, and then skip their own turn.

### Scoring

Here is a table of the scoring combinations he taught me:

![score-combinations](https://github.com/user-attachments/assets/a1312159-c530-4691-8358-774742654135)

Fresh out of a course on Monte Carlo simulations, I couldn't stop thinking about finding the optimal strategy for this game. So I implemented the game logic in Python, with automated Players basing their decisions whether or not to re-roll (or steal) a pool of dice on the number of points at stake and the number of dice remaining. It's simple to see that the probability of scoring with just one die is 33%, and the probability increases with the number of dice. Against those odds, I quickly realized while playing that I would never waste my turn trying to steal one die from a previous player; but how many points would it take to tempt me to steal two? Three? Or, from another angle, how many points would I want to accrue on my turn before passing up the option of re-rolling two or more dice? I surely wouldn't want my opponent to have better odds of stealing my bounty than my odds of increasing it.

I computed distributions of cumulative scores reached, and rate of scratching, when starting from a roll of N dice, where N in {1, 6}:

![farkle-score-distributions](https://github.com/user-attachments/assets/7638a567-912a-42ff-9497-5e3cd340e41d)

After simulating billions of turn histories using ten thousand variations of sets of "threshold" numbers of points one might want to have accrued before passing up N dice (a 5-dimensional tensor of threshold sets, since I would never consider passing on rolling 6 dice), I obtained the total score, scratch frequency (number of 0 scores divided by number of turns), mean score per turn, and median score per turn for each variation. Then, I computed weights in two ways: first by dividing the mean score by the scratch frequency, then by dividing the median score by the scratch frequency. Finally, for both methods, I selected the top 5 variations by weight and calculated the mean score threshold for 1 die, 2 dice, etc., and used the resulting two heuristics to guide the decisions of two types of "bot" players: MeanBot and MedianBot. When I simulated 10,000 games with one MeanBot, one MedianBot, and one bot player that simply made random decisions, these were the histograms of their total end-of-game scores:

![farklebot-algorithms](https://github.com/user-attachments/assets/fe83294f-7f69-4c83-b398-a0964626c775)

Clearly, MeanBot was the most successful. These were the winning score thresholds, which MeanBot used:

![ScoreSafetyCaps](https://github.com/user-attachments/assets/42af5de9-db9b-42c0-914c-95137e030c6a)

Personally, I would be happy to re-roll 4 or 5 dice with MUCH more than 1500 points on the line, but this preliminary result was not an agent-based model taking the possibility of theft from or by opponents into consideration. To that end, I have been redesigning my implementation of the game logic to include the stealing mechanic, and when I have time, I will train a model with reinforcement learning to determine the optimal strategy for Farkle. For now, I added basic I/O features to the implementation so that any number of human players can play the game on a computer together. You know, in case you're stranded on an island without dice, but you still have a laptop with a long battery life. Enjoy!
