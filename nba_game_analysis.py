
import re

class Solution:

        def players_stats(self, team):
            # keywords to seach in DESCRIPTION
            stat_keywords = {"player_name":"{}", "FG": "{} makes 2-pt", "FGA": "{} misses 2-pt ", "3P": "{} makes 3-pt", "3PA": "{} misses 3-pt", "STL": "steal by {}", "FT": "{} makes free throw", "FTA": "{} misses free throw", "TOV": "Turnover by {}", "ORB": "Offensive rebound by {}", "DRB": "Defensive rebound by {}", "AST": "assist by {}", "BLK": "block by {}", "PF": "foul by {}"}
            # desired format for DATA
            output_format = ["player_name", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
           
            final_output = []

            # FG (Field Goal) = 3P + 2P
            # FGA (Field Goal Attempts) = 3PA + 2PA 
            # FG% = FG/FGA
            # FT (Free throw)
            # FTA (Free throw attempt) = FT + FT (missed)
            # FT% = FT/FTA
            # TRB (Total rebound) = ORB (Offensive rebound) + DRB (Deffensive rebound)
            # PF (Personal fouls)
            # PTS (Game points) = 2 * 2P + 3 * 3P + FT

            for player in team:
                each_stat = {i:0 for i in output_format}    # initializing for each individual player
                for categ, text in stat_keywords.items():
                    for line in array_of_play:
                        if (text.format(player) in line):   # if our keyword is found, iterating the stats
                            each_stat[categ] += 1   
                  
                each_stat["player_name"] = player
                
                # Calculating the value of each category

                # 3PA carries 3 pt misses, FG = 2 pt makes, FGA = 2 pt misses, FTA = misses free throw

                each_stat["3PA"] += each_stat["3P"]     # 3PA = 3 pt misses + 3P
                if (each_stat["3PA"] != 0):     
                    each_stat["3P%"] = round(each_stat["3P"] / each_stat["3PA"], 3)

                each_stat["FGA"] += (each_stat["3PA"] + (each_stat["FG"]))     # FGA = 2 pt misses + (3 PA) + 2 pt makes (FG - 3P)    
                each_stat["FG"] += each_stat["3P"]      # FG = 2 pt makes + 3P
                if (each_stat["FGA"] != 0):
                    each_stat["FG%"] = round(each_stat["FG"] / each_stat["FGA"], 3)

                each_stat["FTA"] += each_stat["FT"]
                if (each_stat["FTA"] != 0):
                    each_stat["FT%"] = round(each_stat["FT"] / each_stat["FTA"], 3)
                
                each_stat["TRB"] = each_stat["ORB"] + each_stat["DRB"]
                each_stat["PTS"] = (each_stat["FG"] - each_stat["3P"])*2 + each_stat["3P"]*3 + each_stat["FT"]
                
                final_output.append(each_stat)

            return final_output


        def analyse_nba_game(self, array_of_play):

            header = "PERIOD|REMAINING_SEC|RELEVANT_TEAM|AWAY_TEAM|HOME_TEAM|AWAY_SCORE|HOME_SCORE|DESCRIPTION"
            array_of_play.insert(0, header)
            total_array = [i.split('|') for i in array_of_play]    # inserting header and splitting by categories

            index_description = total_array[0].index("DESCRIPTION")
            index_rel_team = total_array[0].index("RELEVANT_TEAM")
            index_home_team = total_array[0].index("HOME_TEAM")
            index_away_team = total_array[0].index("AWAY_TEAM")

            home_team = []
            away_team = []
            home_team_name = total_array[1][index_home_team]
            away_team_name = total_array[1][index_away_team]

            for i in total_array[1:]:

                match = re.search(r'[A-Z]. [A-Z]\w+', i[index_description])    # searching for name of the player
                remove_match = re.search("foul by ", i[index_description])     # discarding this line

                if (match and not remove_match):                # separating players by teams
                    if (i[index_rel_team] == home_team_name):
                        if (match[0] not in home_team):   
                            home_team.append(match[0])
                    else:
                        if (match[0] not in away_team):   
                            away_team.append(match[0])

            home_team_data = self.players_stats(home_team)
            away_team_data = self.players_stats(away_team)        

            final_format = {"home_team": {"name": home_team_name, "players_data": home_team_data}, "away_team": {"name": away_team_name, "players_data": away_team_data}}

            return final_format

        def print_nba_game_stats(self, team_dict):

            players_data = team_dict["players_data"]
            header_stat = players_data[0].keys()

            for i in header_stat:   # print the header
                print(i, end=' ')
            print(end='\n')

            values_list = []
            for i in players_data:
                values_list.append(list(i.values()))
            totals = []

            for j in range(1, len(values_list[0])):    # summing total scores
                each_sum = 0
                for i in values_list:
                    each_sum += i[j]
                totals.append(round(each_sum, 3))    
            totals.insert(0, "Teams Total")
    
            for i in range(len(players_data)):      # displaying each player's scores
                for j in players_data[i].values():
                    print(j, end=' ')
                print(end='\n')
            for i in totals:
                print(i, end=' ')



my_join = ''                
with open("nba_game.txt", 'r') as game:     # Input is text, that we convert into array of strings
    my_join = my_join.join(game)

array_of_play = my_join.split('\n')



data = Solution()

team_dict = data.analyse_nba_game(array_of_play)
print(team_dict)    # Part 1
data.print_nba_game_stats(team_dict["home_team"]) # Part 2


