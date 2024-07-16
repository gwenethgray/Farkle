from player import Player

robot_mean_heuristics = {1: 450, 2: 800, 3: 1150, 4: 1250, 5: 1500, 6: 999999}

class FarkleGame:
    def __init__(self, players: list[Player]=[]):
        self.players = players
        if len(players) == 0:
            # input player data
            self.prompt_add_players()
            
        for i in range(len(self.players)):
            player_i = self.players[i]
            if i == len(self.players) - 1:
                before_i = self.players[:i]
                player_i.opponents = before_i
            else:
                before_i = self.players[:i]
                after_i = self.players[i+1:]
                player_i.opponents = after_i + before_i
            self.players[i] = player_i
        
    def reset(self):
        players = self.players
        self.players = []
        for player in players:
            player.total_score = 0
            self.players.append(player)

    def prompt_add_players(self):
        add_new_player = input("Do you wish to add a player? (yes/no): ")
        while add_new_player not in ["yes", "no"]:
            print("¯\\_(ツ)_/¯")
            add_new_player = input("Sorry, I only know yes and no. Do you wish to add a player? (yes/no): ")
        if add_new_player == "yes":
            new_player_name = input("Enter the player's name. Otherwise, hit enter. ")
            if new_player_name:
                if new_player_name == "Bot":
                    i = 2
                    while new_player_name in [p.name for p in self.players]:
                        new_player_name = f"Bot{i}"
                        i += 1
                    new_player = Player(name=new_player_name, score_safety_caps=robot_mean_heuristics)
                else:
                    use_heuristics = input("Will this player be playing with any strategic score caps? (yes/no): ")
                    while use_heuristics not in ["yes", "no"]:
                        print("¯\\_(ツ)_/¯")
                        use_heuristics = input("Sorry, I only know yes and no. Will this player be playing with any strategic score caps? (yes/no): ")
                    if use_heuristics == "yes":
                        new_player_heuristics_filepath = input("Enter the filepath to the .txt file containing the score caps. Otherwise, hit enter. ")
                        if new_player_heuristics_filepath:
                            # read heuristics file into dictionary
                            new_player = Player(name=new_player_name, score_safety_caps=new_player_heuristics)
                        else:
                            new_player = Player(name=new_player_name)
                    elif use_heuristics == "no":
                        new_player = Player(name=new_player_name)
                    else:
                        print("¯\\_(ツ)_/¯")
                self.players.append(new_player)
                self.prompt_add_players()
            else:
                self.prompt_add_players()
        elif add_new_player == "no":
            print(f"Current players: {[player.name for player in self.players]}")
        else:
            print("¯\\_(ツ)_/¯")
        
    def begin(self, starting_player: int=None):
        if starting_player is None:
            starting_player = random.randint(0, len(self.players) - 1)
        active_player = starting_player
        print(f"Beginning a new game of Farkle. Starting player: {self.players[active_player].name}")
        nsteps = 0
        while not any([player.total_score >= 10000 for player in self.players]):
            # start a new step.
            nsteps += 1
            print(f"Starting a new step. It is now {self.players[active_player].name}'s turn.")
            # active player rolls dice
            turn_result = self.players[active_player].take_turn()
            # process active player's results
            while turn_result["outcome"] != "pass":
                if turn_result["outcome"] == "scratch":
                    # active player didn't get any points, so the next step starts with the next player. exit the processing loop for this step
                    active_player = (active_player + 1) % len(self.players)
                    break
                elif turn_result["outcome"] == "score":
                    # active player scored and decided to keep their points! give next player a chance to steal
                    next_active_player = (active_player + 1) % len(self.players)
                    stolen_turn_result = self.players[next_active_player].steal_dice(running_score=turn_result["running_score"], num_remaining_dice=turn_result["num_remaining_dice"])
                    # process the steal results (which may be that no stealing happens)
                    if stolen_turn_result["outcome"] == "pass":
                        # next player opted not to steal, so increase active player's total score
                        print(f"{self.players[active_player].name} kept {turn_result['running_score']} points! Now passing to {self.players[next_active_player].name}.")
                        self.players[active_player].total_score += turn_result["running_score"]
                        # then pass to the next player. exit the processing loop for this step
                        active_player = next_active_player
                        break
                    elif stolen_turn_result["outcome"] == "scratch":
                        # next player tried to steal but failed, so increase active player's total score
                        self.players[active_player].total_score += turn_result["running_score"]
                        # and skip the would-be thief
                        active_player = (active_player + 2) % len(self.players)
                        break
                    elif stolen_turn_result["outcome"] == "score":
                        # next player successfully stole from active player. process their result and make them the new active player
                        turn_result = stolen_turn_result
                        active_player = next_active_player
                        
        # a player has scored at least 10,000 points! print scoreboard
        print("GAME OVER!\n----------\nScoreboard:")
        sorted_players = sorted(self.players, key=lambda p: p.total_score, reverse=True)
        for player in sorted_players:
            print(f"{player.name} ----- {player.total_score} points")
        print(f"----------\nThis game took {nsteps} steps (original turns).")