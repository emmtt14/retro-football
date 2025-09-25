import random

# --- Player Class ---
class Player:
    """Represents a single football player with various attributes."""

    def __init__(self, name, position, speed, strength, skill, age=22, potential=80):
        self.name = name
        self.position = position # e.g., "QB", "RB", "WR", "DE", "LB"
        self.speed = speed       # Rating 1-99
        self.strength = strength # Rating 1-99
        self.skill = skill       # Rating 1-99 (e.g., catching for WR, tackling for LB)
        self.age = age           # Player's age, can impact potential and decline
        self.potential = potential # Hidden potential rating 1-99, affects development
        self.team = None         # Team the player is drafted by

    def __str__(self):
        """String representation of the player."""
        return (f"{self.name} ({self.position}) - "
                f"Spd: {self.speed}, Str: {self.strength}, Skl: {self.skill}")

    def get_overall_rating(self):
        """Calculates a simple overall rating for the player."""
        # You can customize this formula based on position importance
        if self.position in ["QB", "RB", "WR", "TE"]:
            return int((self.speed + self.strength + self.skill) / 3)
        elif self.position in ["DE", "DT", "LB", "CB", "S"]:
            return int((self.speed + self.strength + self.skill) / 3)
        else: # Offensive Line
            return int((self.strength + self.strength + self.skill) / 3)


# --- Team Class ---
class Team:
    """Represents a football team."""

    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation # e.g., "PHI", "DAL"
        self.roster = []

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

    def add_player(self, player):
        """Adds a player to the team's roster."""
        self.roster.append(player)
        player.team = self # Assign the team to the player


# --- Draft Class ---
class Draft:
    """Manages the player generation and drafting process."""

    OFFENSIVE_POSITIONS = ["QB", "RB", "WR", "WR", "TE", "C", "G", "G", "T", "T"]
    DEFENSIVE_POSITIONS = ["DE", "DE", "DT", "DT", "LB", "LB", "CB", "CB", "S", "S"]
    ALL_POSITIONS = OFFENSIVE_POSITIONS + DEFENSIVE_POSITIONS

    def __init__(self, num_draft_players=20, num_teams=2):
        self.num_draft_players = num_draft_players
        self.available_players = self._generate_players(num_draft_players)
        self.drafted_players = []
        self.teams = self._generate_teams(num_teams)
        self.current_pick = 0 # Tracks which player is next to be picked

    def _generate_players(self, count):
        """Generates a list of random players for the draft pool."""
        players = []
        for i in range(count):
            name = f"Player {i+1:03d}" # e.g., Player 001
            position = random.choice(self.ALL_POSITIONS)
            speed = random.randint(50, 95)
            strength = random.randint(50, 95)
            skill = random.randint(50, 95)
            age = random.randint(21, 24)
            potential = random.randint(60, 99)
            players.append(Player(name, position, speed, strength, skill, age, potential))
        return sorted(players, key=lambda p: p.get_overall_rating(), reverse=True) # Sorted by overall rating

    def _generate_teams(self, count):
        """Generates a list of teams."""
        team_names = ["Hawks", "Sharks", "Lions", "Dragons", "Vipers", "Bears", "Wolves", "Panthers"]
        team_abbrs = ["HAW", "SHK", "LIO", "DRA", "VIP", "BER", "WOL", "PAN"]
        
        teams = []
        for i in range(count):
            name = team_names[i % len(team_names)]
            abbr = team_abbrs[i % len(team_abbrs)]
            teams.append(Team(name, abbr))
        return teams

    def display_available_players(self):
        """Prints the list of players currently available in the draft."""
        print("\n--- Available Players for Draft ---")
        if not self.available_players:
            print("No players left in the draft pool.")
            return

        print(f"| {'Idx':<3} | {'Name':<10} | {'Pos':<4} | {'Spd':<3} | {'Str':<3} | {'Skl':<3} | {'Ovr':<3} |")
        print("-" * 50)
        for i, player in enumerate(self.available_players):
            print(f"| {i:<3} | {player.name:<10} | {player.position:<4} | {player.speed:<3} | {player.strength:<3} | {player.skill:<3} | {player.get_overall_rating():<3} |")

    def draft_player(self, team, player_index):
        """Drafts a player by a given team."""
        if not self.available_players:
            print("Draft pool is empty. No more players to draft.")
            return False

        if 0 <= player_index < len(self.available_players):
            player = self.available_players.pop(player_index)
            team.add_player(player)
            self.drafted_players.append(player)
            self.current_pick += 1
            print(f"--- {player.name} ({player.position}) drafted by {team.name} ({team.abbreviation})! ---")
            return True
        else:
            print("Invalid player index. Please choose an available player.")
            return False

    def run_draft(self):
        """Automates a simple draft process for multiple teams."""
        print("\n--- Starting Draft ---")
        num_teams = len(self.teams)
        picks_per_team = self.num_draft_players // num_teams

        # Simple round-robin draft order
        for i in range(picks_per_team):
            for team_index in range(num_teams):
                if not self.available_players:
                    print("\nDraft concluded - no more players available.")
                    return

                current_team = self.teams[team_index]
                
                # For simplicity, teams pick the highest overall player available
                # A more complex AI could be implemented here
                if self.available_players:
                    self.draft_player(current_team, 0) # Always pick the first player (highest rated)
                    # Optional: Display current rosters after each pick
                    # print(f"\n{current_team.name} Roster Size: {len(current_team.roster)}")
                    # for p in current_team.roster:
                    #     print(f"  - {p}")
                    # self.display_available_players() # To see the pool shrink


# Example Usage (for testing purposes, you'd typically run this from a main game file)
if __name__ == "__main__":
    print("Initializing Draft System...")
    my_draft = Draft(num_draft_players=20, num_teams=2) 

    print("\n--- Initial Available Players ---")
    my_draft.display_available_players()

    print("\n--- Starting Automated Draft ---")
    my_draft.run_draft()

    print("\n--- Final Rosters ---")
    for team in my_draft.teams:
        print(f"\n{team.name} ({team.abbreviation}) Roster:")
        if not team.roster:
            print("  (Empty)")
            continue
        for player in team.roster:
            print(f"  - {player.name} ({player.position}) - Ovr: {player.get_overall_rating()}")

    print("\nDraft Complete!")
    my_draft.display_available_players() # Should be empty
