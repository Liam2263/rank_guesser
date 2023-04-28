import time

from rlbot.agents.base_script import BaseScript
from rlbot.utils.game_state_util import GameState, BallState, Physics, Vector3, GameInfoState
from rlbot.utils.structures.ball_prediction_struct import BallPrediction
from rlbot.utils.structures.game_data_struct import GameTickPacket


class RankGuesser(BaseScript, GameTickPacket):
    def __init__(self):
        super().__init__("RankGuesser")
        self.packet: GameTickPacket = self.wait_game_tick_packet()
        self.blue_team = []
        self.orange_team = []
        self.validtotalcars = True
        self.blue_team_search = []
        self.orange_team_search = []
        self.first_tick = True
        self.total_cars = 0
        for car in self.packet.game_cars:
            if car.physics.location.z > 0:
                self.total_cars = self.total_cars + 1
        
    def initialize_agent(self):
        self.packet: GameTickPacket = self.wait_game_tick_packet()
        self.blue_team = []
        self.orange_team = []
        self.validtotalcars = True
        self.first_tick = True
        self.blue_team_search = []
        self.orange_team_search = []
    
    def searchteam(self, team):
        list_of_eligible_bots = ["Necto", "Nexto", "Botimus Prime"]
        if len(team) == 1:
            # 1s
            if team[0].name == "Necto":
                return [True, "Necto"]
            elif team[0].name == "Nexto":
                return [True, "Nexto"]
            elif team[0].name == "Botimus Prime":
                return [True, "Botimus Prime"]
            return [False, "Nothing"]
        elif len(team) == 2:
            # 2s
            if team[0].name == "Necto" and team[1].name == "Necto (2)":
                return [True, "Necto"]
            elif team[0].name == "Nexto" and team[1].name == "Nexto (2)":
                return [True, "Nexto"]
            elif team[0].name == "Botimus Prime" and team[1].name == "Botimus Prime (2)":
                return [True, "Botimus Prime"]
            return [False, "Nothing"]
        elif len(team) == 3:
            # 3s
            if team[0].name == "Necto" and team[1].name == "Necto (2)" and team[2].name == "Necto (3)":
                return [True, "Necto"]
            elif team[0].name == "Nexto" and team[1].name == "Nexto (2)" and team[2].name == "Nexto (3)":
                return [True, "Nexto"]
            elif team[0].name == "Botimus Prime" and team[1].name == "Botimus Prime (2)" and team[2].name == "Botimus Prime (3)":
                return [True, "Botimus Prime"]
            return [False, "Nothing"]
        else:
            print("MatchMaker ERROR: No decoys seen")
            return [False, "Nothing"]

    def run(self):
        while True:
            time.sleep(1)
            self.packet: GameTickPacket = self.wait_game_tick_packet()

            if self.first_tick:
                for i in self.packet.game_cars:
                    if i.team == 0 and i.physics.location.z > 0:
                        self.blue_team.append(i)
                    elif i.team == 1 and i.physics.location.z > 0:
                        self.orange_team.append(i)

                self.blue_team_search = self.searchteam(self.blue_team)
                self.orange_team_search = self.searchteam(self.orange_team)
                self.first_tick = False

            if self.total_cars > 6:
                # Error 101
                print("MatchMaker ERROR: Teams have greater than 3 players")
                return
            else:
                Op_team = None
                Op_team_bot = "None"
                Our_team = None
                Op_team_score = 0
                Our_team_score = 0
                if self.blue_team_search[0] == True and self.orange_team_search[0] == False:
                    Op_team = self.blue_team
                    Op_team_bot = self.blue_team_search[1]
                    Our_team = self.orange_team
                elif self.orange_team_search[0] == True and self.blue_team_search[0] == False:
                    Op_team = self.orange_team
                    Op_team_bot = self.orange_team_search[1]
                    Our_team = self.blue_team
                else:
                    # Error 201
                    print("MatchMaker ERROR: Both teams are full of decoys or no decoys seen at all")
                    print("BlueSearch: " + str(self.blue_team_search[0]))
                    print("OrangeSearch: " + str(self.orange_team_search[0]))
                    return
                
                # Scoring System
                for i in Op_team:
                    goals = i.score_info.goals
                    saves = i.score_info.saves
                    shots = i.score_info.shots
                    own_goals = i.score_info.own_goals

                    Op_team_score = Op_team_score + goals * 2
                    Op_team_score = Op_team_score - own_goals
                    Op_team_score = Op_team_score + saves
                    Op_team_score = Op_team_score + shots

                for i in Our_team:
                    goals = i.score_info.goals
                    saves = i.score_info.saves
                    shots = i.score_info.shots
                    own_goals = i.score_info.own_goals

                    Our_team_score = Our_team_score + goals * 2
                    Our_team_score = Our_team_score - own_goals
                    Our_team_score = Our_team_score + saves
                    Our_team_score = Our_team_score + shots

                #Ranking System
                if Op_team_bot == "Necto":
                    # NECTO
                    print("Debug5")
                    diff = Our_team_score - Op_team_score
                    if True:
                        if diff <= -70:
                            print("Bronze")
                        elif diff <= -50 and diff >= -69:
                            print("Silver")
                        elif diff <= -30 and diff >= -49:
                            print("Gold")
                        elif diff <= -11 and diff >= -29:
                            print("Platinum")
                        elif diff <= 10 and diff >= -10:
                            print("Diamond")
                        elif diff <= 25 and diff >= 11:
                            print("Champ")
                        elif diff <= 40 and diff >= 26:
                            print("Grand Champion")
                        elif diff >= 41:
                            print("SuperSonicLegend (SSL)")
                        
                elif Op_team_bot == "Nexto":
                    # NEXTO
                    diff = Our_team_score - Op_team_score
                    if True:
                        if diff <= -111:
                            print("Bronze")
                        elif diff <= -90 and diff >= -110:
                            print("Silver")
                        elif diff <= -70 and diff >= -90:
                            print("Gold")
                        elif diff <= -45 and diff >= -70:
                            print("Platinum")
                        elif diff <= -26 and diff >= -45:
                            print("Diamond")
                        elif diff <= -11 and diff >= -25:
                            print("Champ")
                        elif diff <= 10 and diff >= -10:
                            print("Grand Champion")
                        elif diff >= 41:
                            print("SuperSonicLegend (SSL)")
                elif Op_team_bot == "Botimus Prime":
                    # BOTIMUS PRIME
                    diff = Our_team_score - Op_team_score
                    if True:
                        if diff <= -46:
                            print("Bronze")
                        elif diff <= -26 and diff >= -45:
                            print("Silver")
                        elif diff <= -11 and diff >= -25:
                            print("Gold")
                        elif diff <= 10 and diff >= -10:
                            print("Platinum")
                        elif diff <= 10 and diff >= -10:
                            print("Diamond")
                        elif diff <= 25 and diff >= 11:
                            print("Champ")
                        elif diff <= 40 and diff >= 26:
                            print("Grand Champion")
                        elif diff >= 41:
                            print("SuperSonicLegend (SSL)")

if __name__ == "__main__":
    RankGuesser = RankGuesser()
    RankGuesser.run()


                