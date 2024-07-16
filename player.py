from turn import Turn
import random
from typing import Optional

class Player:
    def __init__(self, name: str, opponents: list[Optional['Player']]=[], total_score: int=0, score_safety_caps: Optional[dict[int, int]]=None):
        self.name = name
        self.opponents = opponents # starting from the person to your right
        self.total_score = total_score
        self.score_safety_caps = score_safety_caps
    
    def add_opponents(self, players: list[Optional['Player']]):
        for player in players:
            if player.name == self.name:
                raise Exception(f"Two players have the name {player.name}. Please start over and make sure all players have different names.")
            else:
                self.opponents.append(player)
        
    def take_turn(self, stolen_running_score: int=0):
        new_turn = Turn(active_player_name=self.name, running_score=stolen_running_score, N=6)
        turn_result = new_turn.simulate(self.score_safety_caps)
        return turn_result
    
    def steal_dice(self, running_score: int, num_remaining_dice: int):
        if self.score_safety_caps is None:
            steal = input(f"Steal {num_remaining_dice} dice and {running_score} points from {self.opponents[-1].name}? (yes/no): ")
            while steal not in ["yes", "no"]:
                steal = input(f"Your running score this turn is {self.running_score + max_score[0]}, and you have {num_remaining_dice} remaining dice. Will {self.name} roll again? (yes/no): ")
            if steal == "yes":
                # steal logic
                print(f"{self.name} stole {num_remaining_dice} dice from {self.opponents[-1].name}!")
                stolen_turn = Turn(active_player_name=self.name, running_score=running_score, N=num_remaining_dice)
                stolen_turn_result = stolen_turn.simulate(score_safety_caps=None)
                if stolen_turn_result["outcome"] == "scratch":
                    print(f"{self.name} tried and failed to steal {num_remaining_dice} dice and {running_score} points from {self.opponents[-1].name}. Skipping {self.name}'s turn!")
                    return {"outcome": "scratch", "running_score": 0, "num_remaining_dice": None}
                elif stolen_turn_result["outcome"] == "score":
                    print(f"{self.name} stole {num_remaining_dice} dice and {stolen_turn_result['running_score']} points from {self.opponents[-1].name}!")
                    return self.take_turn(stolen_running_score=stolen_turn_result["running_score"])
            elif steal == "no":
                # choosing not to steal the dice
                print(f"{self.name} opted not to steal {num_remaining_dice} dice and {running_score} points from {self.opponents[-1].name}.")
                return {"outcome": "pass", "running_score": 0, "num_remaining_dice": num_remaining_dice}
            else:
                raise Exception("Player entered a non-yes/no answer when prompted to roll again. Crashing.")
        elif self.score_safety_caps == "random":
            if random.randint(0, 1):
                # sure, try it!
                print(f"{self.name} stole {num_remaining_dice} dice from {self.opponents[-1].name}!")
                stolen_turn = Turn(active_player_name=self.name, running_score=running_score, N=num_remaining_dice)
                # if score with the stolen dice, proceed with this player's strategy
                stolen_turn_result = stolen_turn.simulate(score_safety_caps=self.score_safety_caps)
                if stolen_turn_result["outcome"] == "scratch":
                    # womp womp, did not score with the stolen dice. skip your turn!
                    print(f"{self.name} tried and failed to steal {num_remaining_dice} dice and {running_score} points from {self.opponents[-1].name}. Skipping {self.name}'s turn!")
                    return {"outcome": "scratch", "running_score": 0, "num_remaining_dice": None}
                elif stolen_turn_result["outcome"] == "score":
                    # scored! now take your turn, starting with the stolen running score
                    return self.take_turn(stolen_running_score=stolen_turn_result["running_score"])
                else:
                    raise Exception("Stolen turn result outcome was neither scratch, nor score, nor pass.")
            else:
                # choosing not to steal the dice
                print(f"{self.name} opted not to steal {num_remaining_dice} dice and {running_score} points from {self.opponents[-1].name}.")
                return {"outcome": "pass", "running_score": 0, "num_remaining_dice": num_remaining_dice}
        else:
            # check safety caps
            if running_score <= self.score_safety_caps[num_remaining_dice]:
                # sure, try it!
                print(f"{self.name} stole {num_remaining_dice} dice from {self.opponents[-1].name}!")
                stolen_turn = Turn(active_player_name=self.name, running_score=running_score, N=num_remaining_dice)
                # if score with the stolen dice, proceed with this player's strategy
                stolen_turn_result = stolen_turn.simulate(score_safety_caps=self.score_safety_caps)
                if stolen_turn_result["outcome"] == "scratch":
                    # womp womp, did not score with the stolen dice. skip your turn!
                    print(f"{self.name} tried and failed to steal {num_remaining_dice} dice and {running_score} points from {self.opponents[-1].name}. Skipping {self.name}'s turn!")
                    return {"outcome": "scratch", "running_score": 0, "num_remaining_dice": None}
                elif stolen_turn_result["outcome"] == "score":
                    # scored! now take your turn, starting with the stolen running score
                    return self.take_turn(stolen_running_score=stolen_turn_result["running_score"])
                else:
                    raise Exception("Stolen turn result outcome was neither scratch, nor score, nor pass.")
            else:
                # choosing not to steal the dice
                print(f"{self.name} opted not to steal {num_remaining_dice} dice and {running_score} points from {self.opponents[-1].name}.")
                return {"outcome": "pass", "running_score": 0, "num_remaining_dice": num_remaining_dice}