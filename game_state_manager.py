import pickle # For saving/loading game state
import os     # For file path operations

from players_and_draft import Draft, Team # Import our previously defined classes

class Game:
    """
    Manages the overall game state, including menus, draft, seasons, and saving/loading.
    """

    def __init__(self, save_dir="saves"):
        self.current_state = "MAIN_MENU" # Possible states: "MAIN_MENU", "NEW_GAME", "LOAD_GAME", "DRAFT", "SEASON", "GAMEPLAY", "END_GAME"
        self.save_directory = save_dir
        os.makedirs(self.save_directory, exist_ok=True) # Ensure save directory exists

        self.user_team = None
        self.all_teams = [] # List of all teams in the league
        self.draft = None
        self.current_season = 0
        self.schedule = [] # List of upcoming games
        self.current_week = 0

        self._initialize_game_data()

    def _initialize_game_data(self):
        """Initializes default game data, or loads if available."""
        # For now, let's create a default set of teams for a new game scenario
        # In a real game, you might load these from a config or database
        team_names = ["Hawks", "Sharks", "Lions", "Dragons", "Vipers", "Bears", "Wolves", "Panthers"]
        team_abbrs = ["HAW", "SHK", "LIO", "DRA", "VIP", "BER", "WOL", "PAN"]

        for i in range(len(team_names)):
            self.all_teams.append(Team(team_names[i], team_abbrs[i]))

        # Assign a default user team for demonstration
        self.user_team = self.all_teams[0] # Let's say the first team is the user's team

    def start_new_game(self, num_draft_players=20, num_teams=4):
        """Sets up a new game, including generating draft players and teams."""
        print("Starting a New Game...")
        # Re-initialize teams if we want a fresh set
        self.all_teams = []
        team_names = ["Hawks", "Sharks", "Lions", "Dragons", "Vipers", "Bears", "Wolves", "Panthers"]
        team_abbrs = ["HAW", "SHK", "LIO", "DRA", "VIP", "BER", "WOL", "PAN"]
        
        for i in range(min(num_teams, len(team_names))): # Ensure we don't go out of bounds
            self.all_teams.append(Team(team_names[i], team_abbrs[i]))

        self.user_team = self.all_teams[0] # User controls the first team
        
        self.draft = Draft(num_draft_players=num_draft_players, num_teams=len(self.all_teams))
        self.draft.teams = self.all_teams # Link the Draft's teams to the Game's teams

        self.current_season = 1
        self.current_week = 0
        self.current_state = "DRAFT" # Move to the draft state

    def run_draft_phase(self):
        """Manages the draft process."""
        print("\n--- Entering Draft Phase ---")
        if not self.draft:
            print("Error: Draft not initialized.")
            return

        self.draft.run_draft() # Execute the automated draft

        print("\n--- Draft Results ---")
        for team in self.all_teams:
            print(f"\n{team.name} ({team.abbreviation}) Roster:")
            for player in team.roster:
                print(f"  - {player.name} ({player.position}) - Ovr: {player.get_overall_rating()}")

        self.current_state = "SEASON" # After draft, move to season

    def advance_week(self):
        """Advances the game to the next week of the season."""
        if self.current_state != "SEASON":
            print("Can only advance week during season.")
            return

        self.current_week += 1
        print(f"\n--- Advancing to Week {self.current_week} of Season {self.current_season} ---")

        # In a real game, this is where you'd simulate games for the week
        # generate stats, check injuries, etc.

        # For demonstration: print user team roster
        print(f"User Team: {self.user_team.name}")
        print("Roster:")
        for player in self.user_team.roster:
            print(f"  - {player.name} ({player.position})")

        # Example condition to end season (e.g., after 17 weeks)
        if self.current_week > 17:
            print("\n--- Season Ended! ---")
            self.current_state = "END_GAME" # Or "OFFSEASON", "PLAYOFFS" etc.

    def save_game(self, filename="game_save.dat"):
        """Saves the current game state to a file."""
        filepath = os.path.join(self.save_directory, filename)
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(self, f)
            print(f"Game saved successfully to {filepath}")
        except Exception as e:
            print(f"Error saving game: {e}")

    @staticmethod
    def load_game(filename="game_save.dat", save_dir="saves"):
        """Loads a game state from a file."""
        filepath = os.path.join(save_dir, filename)
        try:
            with open(filepath, 'rb') as f:
                game_instance = pickle.load(f)
            print(f"Game loaded successfully from {filepath}")
            return game_instance
        except FileNotFoundError:
            print(f"No save file found at {filepath}")
            return None
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def run(self):
        """Main game loop/state machine handler."""
        print("Game initialized. Current state:", self.current_state)
        # This 'run' method will evolve significantly as you add user interaction
        # and different game states. For now, it's a basic demonstration.

        if self.current_state == "MAIN_MENU":
            print("\nWelcome to Retro Football!")
            print("1. New Game")
            print("2. Load Game")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.start_new_game(num_draft_players=20, num_teams=2) # Starting with 2 teams for simplicity
            elif choice == "2":
                loaded_game = Game.load_game()
                if loaded_game:
                    # Replace current game instance with loaded one
                    self.__dict__.update(loaded_game.__dict__)
                    print("Game loaded. Current state:", self.current_state)
            elif choice == "3":
                self.current_state = "EXITING"
                print("Exiting game.")
                return

        while self.current_state != "EXITING":
            if self.current_state == "DRAFT":
                self.run_draft_phase()
                # Automatically transition to SEASON after draft
            elif self.current_state == "SEASON":
                print("\n--- Season Mode ---")
                print("1. Advance Week")
                print("2. Save Game")
                print("3. Exit to Main Menu")
                choice = input("Enter your choice: ")
                if choice == "1":
                    self.advance_week()
                elif choice == "2":
                    self.save_game()
                elif choice == "3":
                    self.current_state = "MAIN_MENU"
                else:
                    print("Invalid choice.")
            elif self.current_state == "MAIN_MENU": # Re-show menu if user exited season
                print("\n--- Main Menu ---")
                print("1. Continue Season") # Only if a season is active
                print("2. New Game")
                print("3. Load Game")
                print("4. Exit")
                choice = input("Enter your choice: ")
                if choice == "1" and self.current_season > 0 and self.current_state != "END_GAME":
                    self.current_state = "SEASON"
                elif choice == "2":
                    self.start_new_game(num_draft_players=20, num_teams=2)
                elif choice == "3":
                    loaded_game = Game.load_game()
                    if loaded_game:
                        self.__dict__.update(loaded_game.__dict__)
                        print("Game loaded. Current state:", self.current_state)
                elif choice == "4":
                    self.current_state = "EXITING"
                    print("Exiting game.")
                    return
                else:
                    print("Invalid choice or no game to continue.")
            elif self.current_state == "END_GAME":
                print("\n--- Game Over / Offseason ---")
                print("1. Start New Game")
                print("2. Exit to Main Menu")
                choice = input("Enter your choice: ")
                if choice == "1":
                    self.start_new_game(num_draft_players=20, num_teams=2)
                elif choice == "2":
                    self.current_state = "MAIN_MENU"
                else:
                    print("Invalid choice.")
            elif self.current_state == "EXITING":
                print("Goodbye!")
                break
            else:
                print(f"Unknown game state: {self.current_state}")
                # Fallback or error handling
                self.current_state = "MAIN_MENU"


# Example Usage (typically run from your main.py or __main__.py file)
if __name__ == "__main__":
    game = Game()
    game.run()
