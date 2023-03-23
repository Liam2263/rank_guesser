import time

from rlbot.agents.base_script import BaseScript
from rlbot.utils.game_state_util import GameState, BallState, Physics, Vector3, GameInfoState
from rlbot.utils.structures.ball_prediction_struct import BallPrediction
from rlbot.utils.structures.game_data_struct import GameTickPacket


class RankGuesser(BaseScript, GameTickPacket):
    def __init__(self):
        super().__init__("RankGuesser")
        self.packet: GameTickPacket = self.wait_game_tick_packet()
        self.ccexists1s = False
        self.ccexists2s = False
        self.cc1sindex = 0
        self.cc2sindex = []
        self.opsindex2s = []
        self.cc2steam = 0
        self.ccgoals = 0
        self.ccsaves = 0
        self.ccdemo = 0
        self.ccshots = 0
        self.ccowngoals = 0
        self.finalscore = 0
        self.opgoals = 0
        self.opsaves = 0
        self.opdemo = 0
        self.opshots = 0
        self.opowngoals = 0
        self.opfinalscore = 0
        self.opname = "Henry"
        self.opname2s = []
        self.doneranking = False
        self.estrank = "Bronze"
        self.ones = False
        self.twos = False
        self.STOP = False
        self.numberofcars = 0
        self.stop1v1samecyro = 0
        self.cyro2scounter = 0
        self.renderer.begin_rendering()
        for car in self.packet.game_cars:
            if car.physics.location.z > 0:
                self.numberofcars = self.numberofcars + 1

        if self.numberofcars == 2:
            self.ones = True
        elif self.numberofcars == 4:
            self.twos = True

        if self.packet.game_cars[0].name == "Codename Cryo" and self.ones == True:
            self.ccexists1s = True
            self.cc1sindex = 0
            self.stop1v1samecyro = self.stop1v1samecyro + 1
        elif self.packet.game_cars[1].name == "Codename Cryo" and self.ones == True:
            self.ccexists1s = True
            self.cc1sindex = 1
            self.stop1v1samecyro = self.stop1v1samecyro + 1

        if self.twos == True:
            if self.packet.game_cars[0].name == "Codename Cryo" or self.packet.game_cars[0].name == "Codename Cryo (2)":
                self.cc2sindex.append(0)
                self.cyro2scounter = self.cyro2scounter + 1
            else:
                self.opsindex2s.append(0)

            if self.packet.game_cars[1].name == "Codename Cryo" or self.packet.game_cars[1].name == "Codename Cryo (2)":
                self.cc2sindex.append(1)
                self.cyro2scounter = self.cyro2scounter + 1
            else:
                self.opsindex2s.append(1)

            if self.packet.game_cars[2].name == "Codename Cryo" or self.packet.game_cars[2].name == "Codename Cryo (2)":
                self.cc2sindex.append(2)
                self.cyro2scounter = self.cyro2scounter + 1
            else:
                self.opsindex2s.append(2)

            if self.packet.game_cars[3].name == "Codename Cryo" or self.packet.game_cars[3].name == "Codename Cryo (2)":
                self.cc2sindex.append(3)
                self.cyro2scounter = self.cyro2scounter + 1
            else:
                self.opsindex2s.append(3)

            if self.cyro2scounter == 2:
                if self.packet.game_cars[self.cc2sindex[0]].team == 0 and self.packet.game_cars[self.cc2sindex[1]].team == 0:
                    self.ccexists2s = True  
                    self.cc2steam = 0
                if self.packet.game_cars[self.cc2sindex[0]].team == 1 and self.packet.game_cars[self.cc2sindex[1]].team == 1:
                    self.ccexists2s = True
                    self.cc2steam = 1

    def run(self):
        while True:
            time.sleep(0.5)
            self.packet: GameTickPacket = self.wait_game_tick_packet()
            if self.ccexists1s == True and self.ones == True and self.stop1v1samecyro < 2:
                if self.cc1sindex == 0:
                    # Estimate my score
                    self.ccgoals = self.packet.game_cars[1].score_info.goals
                    self.ccsaves = self.packet.game_cars[1].score_info.saves
                    self.ccdemo = self.packet.game_cars[1].score_info.demolitions
                    self.ccshots = self.packet.game_cars[1].score_info.shots
                    self.ccowngoals = self.packet.game_cars[1].score_info.own_goals
                    
                    self.finalscore = self.finalscore + self.ccgoals * 2
                    self.finalscore = self.finalscore + self.ccsaves * 2
                    self.finalscore = self.finalscore + self.ccdemo / 2
                    self.finalscore = self.finalscore + self.ccshots
                    self.finalscore = self.finalscore - self.ccowngoals * 2

                    # Estimate Codename Cyro score
                    self.opgoals = self.packet.game_cars[0].score_info.goals
                    self.opsaves = self.packet.game_cars[0].score_info.saves
                    self.opdemo = self.packet.game_cars[0].score_info.demolitions
                    self.opshots = self.packet.game_cars[0].score_info.shots
                    self.opowngoals = self.packet.game_cars[0].score_info.own_goals
                    
                    self.opfinalscore = self.opfinalscore + self.opgoals * 2
                    self.opfinalscore = self.opfinalscore + self.opsaves * 2
                    self.opfinalscore = self.opfinalscore + self.opdemo / 2
                    self.opfinalscore = self.opfinalscore + self.opshots
                    self.opfinalscore = self.opfinalscore - self.opowngoals * 2

                    self.finalscore = self.finalscore - self.opfinalscore

                    self.doneranking = True
                    self.opname = self.packet.game_cars[1].name
                    if self.finalscore >= -99999 and self.finalscore <= -3:
                        self.estrank = self.opname + ": Bronze"
                    elif self.finalscore >= -2 and self.finalscore <= 12:
                        self.estrank = self.opname + ": Silver"
                    elif self.finalscore >= 13 and self.finalscore <= 18:
                        self.estrank = self.opname + ": Gold"
                    elif self.finalscore >= 19 and self.finalscore <= 28:
                        self.estrank = self.opname + ": Platinum"
                    elif self.finalscore >= 29 and self.finalscore <= 33:
                        self.estrank = self.opname + ": Diamond"
                    elif self.finalscore >= 34 and self.finalscore <= 45:
                        self.estrank = self.opname + ": Champ"
                    elif self.finalscore >= 46 and self.finalscore <= 63:
                        self.estrank = self.opname + ": Grand Champion"
                    elif self.finalscore >= 64:
                        self.estrank = self.opname + ": SSL"
                    self.rankesttest(self.estrank)
                    self.finalscore = 0
                    self.opfinalscore = 0
                elif self.cc1sindex == 1:
                    # Estimate my score
                    self.ccgoals = self.packet.game_cars[0].score_info.goals
                    self.ccsaves = self.packet.game_cars[0].score_info.saves
                    self.ccdemo = self.packet.game_cars[0].score_info.demolitions
                    self.ccshots = self.packet.game_cars[0].score_info.shots
                    self.ccowngoals = self.packet.game_cars[0].score_info.own_goals
                    
                    self.finalscore = self.finalscore + self.ccgoals * 2
                    self.finalscore = self.finalscore + self.ccsaves * 2
                    self.finalscore = self.finalscore + self.ccdemo / 2
                    self.finalscore = self.finalscore + self.ccshots
                    self.finalscore = self.finalscore - self.ccowngoals * 2

                    # Estimate Codename Cyro score
                    self.opgoals = self.packet.game_cars[1].score_info.goals
                    self.opsaves = self.packet.game_cars[1].score_info.saves
                    self.opdemo = self.packet.game_cars[1].score_info.demolitions
                    self.opshots = self.packet.game_cars[1].score_info.shots
                    self.opowngoals = self.packet.game_cars[1].score_info.own_goals
                    
                    self.opfinalscore = self.opfinalscore + self.opgoals * 2
                    self.opfinalscore = self.opfinalscore + self.opsaves * 2
                    self.opfinalscore = self.opfinalscore + self.opdemo / 2
                    self.opfinalscore = self.opfinalscore + self.opshots
                    self.opfinalscore = self.opfinalscore - self.opowngoals * 2

                    self.finalscore = self.finalscore - self.opfinalscore
                    self.opname = self.packet.game_cars[0].name
                    if self.finalscore >= -99999 and self.finalscore <= -3:
                        self.estrank = self.opname + ": Bronze"
                    elif self.finalscore >= -2 and self.finalscore <= 12:
                        self.estrank = self.opname + ": Silver"
                    elif self.finalscore >= 13 and self.finalscore <= 18:
                        self.estrank = self.opname + ": Gold"
                    elif self.finalscore >= 19 and self.finalscore <= 28:
                        self.estrank = self.opname + ": Platinum"
                    elif self.finalscore >= 29 and self.finalscore <= 33:
                        self.estrank = self.opname + ": Diamond"
                    elif self.finalscore >= 34 and self.finalscore <= 45:
                        self.estrank = self.opname + ": Champ"
                    elif self.finalscore >= 46 and self.finalscore <= 63:
                        self.estrank = self.opname + ": Grand Champion"
                    elif self.finalscore >= 64:
                        self.estrank = self.opname + ": SSL"
                    self.rankesttest(self.estrank)
                    self.finalscore = 0
                    self.opfinalscore = 0

            elif self.twos == True and self.ccexists2s == True:
                # Estimate Codename Cyro's ranks first
                print(self.packet.game_cars[0].name)
                self.ccgoals = self.packet.game_cars[self.cc2sindex[0]].score_info.goals
                self.ccsaves = self.packet.game_cars[self.cc2sindex[0]].score_info.saves
                self.ccdemo = self.packet.game_cars[self.cc2sindex[0]].score_info.demolitions
                self.ccshots = self.packet.game_cars[self.cc2sindex[0]].score_info.shots
                self.ccowngoals = self.packet.game_cars[self.cc2sindex[0]].score_info.own_goals
                    
                self.finalscore = self.finalscore + self.ccgoals * 2
                self.finalscore = self.finalscore + self.ccsaves * 2
                self.finalscore = self.finalscore + self.ccdemo / 2
                self.finalscore = self.finalscore + self.ccshots
                self.finalscore = self.finalscore - self.ccowngoals * 2

                self.ccgoals = self.packet.game_cars[self.cc2sindex[1]].score_info.goals
                self.ccsaves = self.packet.game_cars[self.cc2sindex[1]].score_info.saves
                self.ccdemo = self.packet.game_cars[self.cc2sindex[1]].score_info.demolitions
                self.ccshots = self.packet.game_cars[self.cc2sindex[1]].score_info.shots
                self.ccowngoals = self.packet.game_cars[self.cc2sindex[1]].score_info.own_goals

                self.finalscore = self.finalscore + self.ccgoals * 2
                self.finalscore = self.finalscore + self.ccsaves * 2
                self.finalscore = self.finalscore + self.ccdemo / 2
                self.finalscore = self.finalscore + self.ccshots
                self.finalscore = self.finalscore - self.ccowngoals * 2

                # Estimate Opponents rank
                self.opgoals = self.packet.game_cars[self.opsindex2s[0]].score_info.goals
                self.opsaves = self.packet.game_cars[self.opsindex2s[0]].score_info.saves
                self.opdemo = self.packet.game_cars[self.opsindex2s[0]].score_info.demolitions
                self.opshots = self.packet.game_cars[self.opsindex2s[0]].score_info.shots
                self.opowngoals = self.packet.game_cars[self.opsindex2s[0]].score_info.own_goals
                    
                self.opfinalscore = self.opfinalscore + self.opgoals * 2
                self.opfinalscore = self.opfinalscore + self.opsaves * 2
                self.opfinalscore = self.opfinalscore + self.opdemo / 2
                self.opfinalscore = self.opfinalscore + self.opshots
                self.opfinalscore = self.opfinalscore - self.opowngoals * 2

                self.opgoals = self.packet.game_cars[self.opsindex2s[1]].score_info.goals
                self.opsaves = self.packet.game_cars[self.opsindex2s[1]].score_info.saves
                self.opdemo = self.packet.game_cars[self.opsindex2s[1]].score_info.demolitions
                self.opshots = self.packet.game_cars[self.opsindex2s[1]].score_info.shots
                self.opowngoals = self.packet.game_cars[self.opsindex2s[1]].score_info.own_goals
                    
                self.opfinalscore = self.opfinalscore + self.opgoals * 2
                self.opfinalscore = self.opfinalscore + self.opsaves * 2
                self.opfinalscore = self.opfinalscore + self.opdemo / 2
                self.opfinalscore = self.opfinalscore + self.opshots
                self.opfinalscore = self.opfinalscore - self.opowngoals * 2

                self.opfinalscore = self.opfinalscore - self.finalscore
                self.opname2s = [self.packet.game_cars[self.opsindex2s[0]].name, self.packet.game_cars[self.opsindex2s[1]].name]
                if self.opfinalscore >= -99999 and self.opfinalscore <= -3:
                    self.estrank = self.opname2s[0] + ", " + self.opname2s[1] + ": Bronze"
                elif self.opfinalscore >= -2 and self.opfinalscore <= 12:
                    self.estrank = self.opname2s[0] + ", " + self.opname2s[1] + ": Silver"
                elif self.opfinalscore >= 13 and self.opfinalscore <= 18:
                    self.estrank = self.opname2s[0] + ", " + self.opname2s[1] + ": Gold"
                elif self.opfinalscore >= 19 and self.opfinalscore <= 28:
                    self.estrank = self.opname2s[0] + ", " + self.opname2s[1] + ": Platinum"
                elif self.opfinalscore >= 29 and self.opfinalscore <= 33:
                    self.estrank = self.opname2s[0] + ", " + self.opname2s[1] + ": Diamond"
                elif self.opfinalscore >= 34 and self.opfinalscore <= 45:
                    self.estrank = self.opname2s[0] + ", " + self.opname2s[1] + ": Champ"
                elif self.opfinalscore >= 46 and self.opfinalscore <= 63:
                    self.estrank = self.opname2s[0] + ", " + self.opname2s[1] + ": Grand Champion"
                elif self.opfinalscore >= 64:
                    self.estrank = self.opname2s[0] + ", " + self.opname2s[1] + ": SSL"
                self.renderer.begin_rendering()
                if self.cc2steam == 0:
                    self.renderer.draw_string_2d(1175, 75, 2, 2, self.estrank, self.renderer.orange())
                else:
                    self.renderer.draw_string_2d(1175, 75, 2, 2, self.estrank, self.renderer.blue())
                self.renderer.end_rendering()
                self.finalscore = 0
                self.opfinalscore = 0
            else:
                print("Wrong format! Must be 1v1 or 2v2 with one team having full Codename Cyro")
                

    def rankesttest(self, textf):
        print(textf)

                    



# You can use this __name__ == '__main__' thing to ensure that the script doesn't start accidentally if you
# merely reference its module from somewhere
if __name__ == "__main__":
    RankGuessProcess = RankGuesser()
    RankGuessProcess.run()