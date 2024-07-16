# Farkle

This dice rolling game has unclear origins, with some trademark holders and fans circulating [popular yet unverified claims](https://farklefan.blogspot.com/2012/01/history-of-farkle.html) that it was first played in Iceland in the 14th century (by a conspicuously-named "Sir Albert Farkle") and first referenced in print during the time of Shakespeare. Rules (see the [rules booklet](https://www.cusd80.com/cms/lib/AZ01001175/centricity/domain/1355/Farkle.pdf) published by SmartBoxGames) may vary on scoring, but the game is generally played by rolling 6 dice, setting aside any combinations which are worth points, and optionally re-rolling leftover non-scoring dice. If you fail to roll any scoring combinations, you get no points for the turn... but if you manage to score with all 6 dice, you can roll them all again and keep stacking up points! The first player to reach 10,000 points wins.

My friend Talon introduced me to it using a version where, when a player chooses to keep the points they've acquired and refrain from re-rolling any remaining dice, the next player has the option of "stealing": they can re-roll the remaining dice, and if they get any scoring combinations (even just a single 1 or a single 5), then they take the first player's points for that turn and keep rolling! However, if they "scratch" by failing to score, then they get no points, and then skip their own turn.

### Scoring

Here is a table of the scoring combinations he taught me:

![ScoreTable](https://github.com/user-attachments/assets/fa9487db-c0cd-42a9-9f8b-216beb767fdb)

Fresh out of a course on Monte Carlo simulations, I couldn't stop thinking about finding the optimal strategy for this game. So I implemented the game logic in Python, with automated Players basing their decisions whether or not to re-roll (or steal) a pool of dice on the number of points at stake and the number of dice remaining. It's simple to see that the probability of scoring with just one die is 33%, and the probability increases with the number of dice. Against those odds, I quickly realized while playing that I would never waste my turn trying to steal one die from a previous player; but how many points would it take to tempt me to steal two? Three? Or, from another angle, how many points would I want to accrue on my turn before passing up the option of re-rolling two or more dice? I surely wouldn't want my opponent to have better odds of stealing my bounty than my odds of increasing it.

After simulating billions of turn histories using tens of thousands of variations of sets of "threshold" numbers of points one might want to have accrued before passing up N dice (for each N), and comparing the win rates of all variations, I arrived at a rough approximation of high-performing "score safety caps":

![ScoreSafetyCaps](https://github.com/user-attachments/assets/42af5de9-db9b-42c0-914c-95137e030c6a)

Personally, I would be happy to re-roll 4 or 5 dice with MUCH more than 1500 points on the line, but this preliminary result was not an agent-based model taking the possibility of theft from or by opponents into consideration. To that end, I have been redesigning my implementation of the game logic to include the stealing mechanic, and when I have time, I will train a model with reinforcement learning to determine the optimal strategy for Farkle. For now, I added basic I/O features to the implementation so that any number of human players can play the game on a computer together. You know, in case you're stranded on an island without dice, but you still have a laptop with a long battery life. Enjoy!
