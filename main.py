from FarkleGame import FarkleGame

if __name__ == '__main__':
    print("Hello and welcome to Farkle!")
    print("FYI: When adding new players, you may type \"Bot\" to create a robot player with a pre-loaded strategy.")
    start = input("Start a new game? (yes/no): ")
    while start not in ["yes", "no"]:
        print("¯\\_(ツ)_/¯")
        start = input("Sorry, I only know yes and no. Say no to quit. Start a new game? (yes/no): ")
    if start == "yes":
        game = FarkleGame()
        game.begin()
    elif start == "no":
        quit()
    else:
        print("¯\\_(ツ)_/¯")