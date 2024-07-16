from dice import Dice

score_types = {
    "1 1": "100",
    "1 5": "50",
    "2 1": "200",
    "2 5": "100",
    "3 1": "1000",
    "3 2": "200",
    "3 3": "300",
    "3 4": "400",
    "3 5": "500",
    "3 6": "600",
    "4 1": "2000",
    "4 2": "400",
    "4 3": "600",
    "4 4": "800",
    "4 5": "1000",
    "4 6": "1200",
    "5 1": "4000",
    "5 2": "800",
    "5 3": "1200",
    "5 4": "1600",
    "5 5": "2000",
    "5 6": "2400",
    "6 1": "8000",
    "6 2": "1600",
    "6 3": "2400",
    "6 4": "3200",
    "6 5": "4000",
    "6 6": "4800",
    "Straight": "1500+newturn",
    "2 Triples": "1500+newturn",
    "3 Pairs": "1500+newturn",
    "Last Two Non-scoring Pair": "0+newturn"
}

class Turn:
    def __init__(self, active_player_name: str, dice: list[Dice]=None, running_score: int=0, N: int=None):
        self.active_player_name = active_player_name
        self.dice = dice
        self.running_score = running_score
        if dice is None and N is not None:
            self.dice = [Dice(i).roll() for i in range(N)]
        elif all([d.state is None for d in self.dice]):
            self.dice = [d.roll() for d in self.dice]
    
    def roll_dice(self):
        new_dice = [d.roll() for d in self.dice]
        self.dice = new_dice
    
    def get_dice_vals(self):
        return [d.state for d in self.dice]
    
    def check_dice_counts(self, dice):
        counts = {i: dice.count(i) for i in range(1,7)}
        return counts
    
    def check_score_options(self):
        vals = self.get_dice_vals()
        options = []
        counts = self.check_dice_counts(vals)
        max_count = max(counts.values())
        num_pairs = 0
        num_triples = 0
        for num, count in counts.items():
            count_string = f"{count} {num}"
            if count_string in score_types.keys():
                options.append(count_string)
                if count == 2:
                    num_pairs += 1
                    if num in [1, 5]:
                        options.append(f"1 {num}")
                elif count == 3:
                    num_triples += 1
        if num_pairs == 3:
            options.append("3 Pairs")
        elif num_triples == 2:
            options.append("2 Triples")
        elif all([i in vals for i in range(1,7)]):
            options.append("Straight")
        return options
    
    def sort_score_options(self):
        def convert_option_score(opt):
            try:
                return [int(score_types[opt]), 0, opt]
            except:
                _ = score_types[opt].split("+")
                return [int(_[0]), 1, opt]
        option_scores = list(map(convert_option_score, self.check_score_options()))
        sorted_option_scores = sorted(option_scores, key=lambda _: (_[1], _[0]), reverse=True)
        return sorted_option_scores
    
    def check_max_score(self):
        vals = self.get_dice_vals()
        options = self.check_score_options()
        sorted_option_scores = self.sort_score_options()
        print(f"{self.active_player_name} has the following scoring options: {sorted_option_scores}")
        for new_turn_option in ["3 Pairs", "2 Triples", "Straight"]:
            if new_turn_option in options:
                print(f"A new turn option was in the roll! ({new_turn_option})")
                return [1500, f"{0} dice remaining", []]
        # what is the maximum number of dice I can withold and reroll? is the average value of a new turn greater than the greatest total score combination I can get with these dice?
        total_score = 0
        remaining_dice = self.dice
        remaining_counts = self.check_dice_counts(vals)
        used_options = []
        for option in sorted_option_scores:
            # can i still use this with remaining dice?
            remaining_counts = self.check_dice_counts([d.state for d in remaining_dice])
            freq, val = tuple(map(lambda _: int(_), option[2].split(" ")))
            if freq <= remaining_counts[val]:
                # yes i can
                remaining_counts[val] -= freq
                total_score += option[0]
                used_options.append(option)
                print(f"Selected scoring option: {option}")
                # remove used dice from remaining dice
                while freq > 0:
                    for i, die in enumerate(remaining_dice):
                        if die.state == val:
                            #remaining_dice.remove(die)
                            print(f"Removing a {val} from dice pool.")
                            remaining_dice.pop(i)
                            freq -= 1
        if any([count == 2 for count in remaining_counts.values()]) and len(remaining_dice) == 2: # ??? -> or any([option[1] == 1 for option in used_options]):
            # last 2 non-scoring dice are the same number, go again!
            return [total_score, f"{0} dice remaining", []]
        else:
            return [total_score, f"{len(remaining_dice)} dice remaining", remaining_dice]
    
    def simulate(self, score_safety_caps: dict[int, int]):
        # score safety caps = {
        #    1: if 1 die remains and score is <= X1, reroll. if you already have > X1 points, quit while you're ahead
        #    2: if 2 dice remain and score is <= X2, reroll. if you already have > X2 points, quit while you're ahead
        #    3: etc
        #    ... }
        self.roll_dice()
        print(f"{self.active_player_name}'s dice were: {','.join([str(val) for val in self.get_dice_vals()])}")
        max_score = self.check_max_score()
        num_remaining_dice = int(max_score[1].split(" ")[0])
        if num_remaining_dice == 0:
            # used all the dice! roll 6 again
            print(f"{self.active_player_name} was able to score with all 6 dice! They will roll 6 more, with a running score of {self.running_score + max_score[0]} for this turn!")
            new_turn = Turn(active_player_name=self.active_player_name, N=6, running_score=self.running_score + max_score[0])
            return new_turn.simulate(score_safety_caps)
        elif max_score[0] == 0:
            # Farkle!
            print(f"Scratch! {self.active_player_name} did not roll any scoring combinations, so they gained no points.")
            return {"outcome": "scratch", "running_score": 0, "num_remaining_dice": None}
        else:
            if score_safety_caps is None:
                roll_again = input(f"Your running score this turn is {self.running_score + max_score[0]}, and you have {num_remaining_dice} remaining dice. Will {self.active_player_name} roll again? (yes/no): ")
                while roll_again not in ["yes", "no"]:
                    roll_again = input(f"Will {self.active_player_name} roll again? (yes/no): ")
                if roll_again == "yes":
                    print(f"{self.active_player_name} rerolled {num_remaining_dice} dice.")
                    new_turn = Turn(active_player_name=self.active_player_name, N=num_remaining_dice, running_score=self.running_score + max_score[0])
                    return new_turn.simulate(score_safety_caps)
                elif roll_again == "no":
                    return {"outcome": "score", "running_score": self.running_score + max_score[0], "num_remaining_dice": num_remaining_dice}
                else:
                    raise Exception("Player entered a non-yes/no answer when prompted to roll again. Crashing.")
            elif score_safety_caps == "random":
                if random.randint(0, 1):
                    # use the unused dice
                    print(f"{self.active_player_name} rerolled {num_remaining_dice} dice.")
                    new_turn = Turn(active_player_name=self.active_player_name, N=num_remaining_dice, running_score=self.running_score + max_score[0])
                    return new_turn.simulate(score_safety_caps)  ##  , opponent)
                else:
                    # quit while you're ahead, but opponent gets a chance to steal
                    print(f"{self.active_player_name} opted not to reroll {num_remaining_dice} dice.")
                    return {"outcome": "score", "running_score": self.running_score + max_score[0], "num_remaining_dice": num_remaining_dice}
            else:
                if self.running_score + max_score[0] <= score_safety_caps[num_remaining_dice]:
                    # use the unused dice
                    print(f"{self.active_player_name} rerolled {num_remaining_dice} dice.")
                    new_turn = Turn(active_player_name=self.active_player_name, N=num_remaining_dice, running_score=self.running_score + max_score[0])
                    return new_turn.simulate(score_safety_caps)  ##  , opponent)
                else:
                    # quit while you're ahead, but opponent gets a chance to steal
                    print(f"{self.active_player_name} opted not to reroll {num_remaining_dice} dice.")
                    return {"outcome": "score", "running_score": self.running_score + max_score[0], "num_remaining_dice": num_remaining_dice}