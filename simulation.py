# simulation.py
import random
from gameplay import Gameplay

class SeasonSimulator:
    """
    Simulates a full season of games, including a schedule and standings.
    """
    def __init__(self, teams, weeks=17):
        self.teams = teams
        self.num_weeks = weeks
        self.schedule = self._generate_schedule()
        self.standings = {team.name: {"wins": 0, "losses": 0} for team in teams}

    def _generate_schedule(self):
        """Generates a simple, round-robin style schedule."""
        schedule = []
        team_names = [team.name for team in self.teams]
        num_teams = len(team_names)
        
        # For simplicity, a basic non-repeating schedule for a small league
        # A more realistic schedule is much more complex
        
        if num_teams % 2 != 0:
            team_names.append("BYE") # Add a dummy team for odd number of teams

        for week in range(self.num_weeks):
            week_games = []
            temp_teams = team_names[:]
            
            # Simple rotation method for scheduling
            home_teams = temp_teams[:num_teams//2]
            away_teams = temp_teams[num_teams//2:]
            
            for i in range(len(home_teams)):
                if home_teams[i] != "BYE" and away_teams[i] != "BYE":
                    home_team_obj = next(t for t in self.teams if t.name == home_teams[i])
                    away_team_obj = next(t for t in self.teams if t.name == away_teams[i])
                    week_games.append((home_team_obj, away_team_obj))
            
            schedule.append(week_games)
            
            # Rotate the teams for the next week's matchups
            if num_teams > 2:
                first = temp_teams.pop(1)
                temp_teams.append(first)
                team_names = temp_teams
        
        return schedule

    def run_season(self):
        """Runs the simulation for an entire season."""
        print(f"\n--- Starting Season {self.num_weeks} Weeks ---")
        for week, games in enumerate(self.schedule):
            print(f"\n-- Simulating Week {week + 1} --")
            for home_team, away_team in games:
                print(f"Simulating game: {away_team.name} vs. {home_team.name}")
                game = Gameplay(home_team, away_team)
                game.start_game()
                self.update_standings(game)
        
        self.display_standings()
        print("\n--- End of Season ---")

    def update_standings(self, game):
        """Updates the win/loss records based on a game's outcome."""
        home_score = game.score[game.home_team.name]
        away_score = game.score[game.away_team.name]
        
        if home_score > away_score:
            self.standings[game.home_team.name]["wins"] += 1
            self.standings[game.away_team.name]["losses"] += 1
        elif away_score > home_score:
            self.standings[game.away_team.name]["wins"] += 1
            self.standings[game.home_team.name]["losses"] += 1
        # No ties for simplicity

    def display_standings(self):
        """Prints the final season standings."""
        print("\n--- Final Season Standings ---")
        # Sort teams by wins
        sorted_teams = sorted(self.teams, key=lambda team: self.standings[team.name]["wins"], reverse=True)
        
        for team in sorted_teams:
            record = self.standings[team.name]
            print(f"{team.name:<10}: {record['wins']} W - {record['losses']} L")

# Example Usage: (Will be called from the GameState Manager)
if __name__ == "__main__":
    from players_and_draft import Team, Player, Draft

    # Create and draft players into teams
    draft = Draft(num_draft_players=20, num_teams=4)
    draft.run_draft()
    
    # Run the season with the drafted teams
    season = SeasonSimulator(draft.teams, weeks=3) # Short season for demonstration
    season.run_season()
