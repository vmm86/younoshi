import sys
sys.path.insert(0, '/home/vmm/www/younoshi')

from younoshi import app
application = app

reload(sys)
sys.setdefaultencoding('utf-8')

# from younoshi import *
# create_tables()

# database.create_foreign_key(School, School.city_ID, constraint='FK_School_City')

# database.create_foreign_key(Team, Team.school_ID, constraint='FK_Team_School')
# database.create_foreign_key(Team, Team.age_ID, constraint='FK_Team_Age')

# database.create_foreign_key(SeasonAgeStage, SeasonAgeStage.season_ID, constraint='FK_SAS_Season')
# database.create_foreign_key(SeasonAgeStage, SeasonAgeStage.age_ID, constraint='FK_SAS_Age')
# database.create_foreign_key(SeasonAgeStage, SeasonAgeStage.stage_ID, constraint='FK_SAS_Stage')

# database.create_foreign_key(SeasonAgeStageTeam, SeasonAgeStageTeam.SAS_ID, constraint='FK_SAST_SAS')
# database.create_foreign_key(SeasonAgeStageTeam, SeasonAgeStageTeam.team_ID, constraint='FK_SAST_Team')

# database.create_foreign_key(GameProtocol, GameProtocol.homeTeam_ID, constraint='FK_GP.homeTeam_SAST')
# database.create_foreign_key(GameProtocol, GameProtocol.guestTeam_ID, constraint='FK_GP.guestTeam_SAST')