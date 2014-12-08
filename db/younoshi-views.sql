# Запросы для вычисления параметров рейтинга

## участие в матче + 10000

SELECT COUNT(*) * 10000 AS `games` FROM `GameProtocol` AS `GP` 
WHERE (`GP`.`homeTeam_ID` = `T`.`team_ID` OR `GP`.`guestTeam_ID` = `T`.`team_ID`)

## победа в матче + 30000
### победы в основное время дома и в гостях и в дополнительное время дома и в гостях

SELECT COUNT(*) * 30000 AS `wins` FROM `GameProtocol` AS `GP`
WHERE 
    (`GP`.`homeTeamScoreGame` > `GP`.`guestTeamScoreGame` AND `GP`.`homeTeam_ID`  = `T`.`team_ID`) 
OR 
    (`GP`.`homeTeamScoreGame` < `GP`.`guestTeamScoreGame` AND `GP`.`guestTeam_ID` = `T`.`team_ID`)
OR 
    (`GP`.`homeTeamScoreGame` = `GP`.`guestTeamScoreGame` AND 
        ((`homeTeamScore11m` > `guestTeamScore11m` AND `GP`.`homeTeam_ID`  = `T`.`team_ID`) 
        OR 
        (`homeTeamScore11m` < `guestTeamScore11m` AND `GP`.`guestTeam_ID`  = `T`.`team_ID`)) 
    )

## ничья в матче + 10000
??? считается ли ничьёй ничья с победой/проигрышем после дополнительного времени ???

SELECT COUNT(*) * 10000 AS `equals` FROM `GameProtocol` AS `GP`
WHERE 
    `GP`.`homeTeamScoreGame` = `GP`.`guestTeamScoreGame`
AND 
    (`GP`.`homeTeam_ID` = `T`.`team_ID` OR `GP`.`guestTeam_ID` = `T`.`team_ID`)

## забитый мяч + 501
### число забитых мячей дома и в гостях и их сумма

-- SELECT 
-- ((SELECT SUM(`GP`.`homeTeamScoreGame`)  FROM `GameProtocol` AS `GP` WHERE `GP`.`homeTeam_ID`  = `T`.`team_ID`) + 
-- (SELECT SUM(`GP`.`guestTeamScoreGame`) FROM `GameProtocol` AS `GP` WHERE `GP`.`guestTeam_ID` = `T`.`team_ID`)) * 501 AS `scored`

# пропущенный мяч -501
## число пропущенных мячей дома и в гостях и их сумма

-- SELECT 
-- ((SELECT SUM(`GP`.`homeTeamScoreGame`)  FROM `GameProtocol` AS `GP` WHERE `GP`.`guestTeam_ID` = `T`.`team_ID`) + 
-- (SELECT SUM(`GP`.`guestTeamScoreGame`) FROM `GameProtocol` AS `GP` WHERE `GP`.`homeTeam_ID`  = `T`.`team_ID`)) * 501 AS `missed`

## разница забитых и пропущенных мячей * 501

SELECT 
(((SELECT SUM(`GP`.`homeTeamScoreGame`)  FROM `GameProtocol` AS `GP` WHERE `GP`.`homeTeam_ID`  = `T`.`team_ID`) + 
 (SELECT SUM(`GP`.`guestTeamScoreGame`) FROM `GameProtocol` AS `GP` WHERE `GP`.`guestTeam_ID` = `T`.`team_ID`)) - 
((SELECT SUM(`GP`.`homeTeamScoreGame`)  FROM `GameProtocol` AS `GP` WHERE `GP`.`guestTeam_ID` = `T`.`team_ID`) + 
 (SELECT SUM(`GP`.`guestTeamScoreGame`) FROM `GameProtocol` AS `GP` WHERE `GP`.`homeTeam_ID`  = `T`.`team_ID`))) * 501 AS `goals`

## выход в плэй-офф +9000

SELECT COUNT(*) * 9000 AS `playoff` FROM `SeasonAgeStageTeam` AS `SAST` 
LEFT JOIN `SeasonAgeStage` AS `SAS`   ON (`SAST`.`SAS_ID`  = `SAS`.`SAS_ID`)
LEFT JOIN `Stage`          AS `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`)
WHERE `SAST`.`team_ID` = `T`.`team_ID` AND `Stage`.`stageType` = "P"

## победа в серии 11-метровых ударов плэй-офф +10000

SELECT COUNT(DISTINCT `GP_ID`) * 10000 AS `playoff11m` FROM `GameProtocol` AS `GP`
LEFT JOIN `SeasonAgeStageTeam` AS `SAST`  ON (`GP`.`SAS_ID`    = `SAST`.`SAS_ID`) 
LEFT JOIN `SeasonAgeStage`     AS `SAS`   ON (`SAST`.`SAS_ID`  = `SAS`.`SAS_ID`) 
LEFT JOIN `Stage`              AS `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`) 
WHERE
    `Stage`.`stageType` = "P"
AND
    `GP`.`homeTeamScoreGame` = `GP`.`guestTeamScoreGame` 
AND 
    ((`homeTeamScore11m` > `guestTeamScore11m` AND `GP`.`homeTeam_ID`  = `T`.`team_ID`) 
     OR 
    (`homeTeamScore11m`  < `guestTeamScore11m` AND `GP`.`guestTeam_ID` = `T`.`team_ID`))

## участие в полуфинале плэй-офф +28000

SELECT COUNT(DISTINCT `GP_ID`) * 28000 AS `playoffSemifinal` FROM `GameProtocol` AS `GP` 
LEFT JOIN `SeasonAgeStageTeam` AS `SAST`  ON (`GP`.`SAS_ID`    = `SAST`.`SAS_ID`) 
LEFT JOIN `SeasonAgeStage`     AS `SAS`   ON (`SAST`.`SAS_ID`  = `SAS`.`SAS_ID`) 
LEFT JOIN `Stage`              AS `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`) 
WHERE
    `Stage`.`stageType` = "P"
AND 
    (`GP`.`homeTeam_ID` = `T`.`team_ID` OR `GP`.`guestTeam_ID` = `T`.`team_ID`)
AND
    `GP`.`is_Semifinal` = 1

## участие в финале плэй-офф +38000

SELECT COUNT(DISTINCT `GP_ID`) * 38000 AS `playoffFinal` FROM `GameProtocol` AS `GP` 
LEFT JOIN `SeasonAgeStageTeam` AS `SAST`  ON (`GP`.`SAS_ID`    = `SAST`.`SAS_ID`) 
LEFT JOIN `SeasonAgeStage`     AS `SAS`   ON (`SAST`.`SAS_ID`  = `SAS`.`SAS_ID`) 
LEFT JOIN `Stage`              AS `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`) 
WHERE
    `Stage`.`stageType` = "P"
AND 
    (`GP`.`homeTeam_ID` = `T`.`team_ID` OR `GP`.`guestTeam_ID` = `T`.`team_ID`)
AND
    `GP`.`is_Final` = 1

-----------------------------------------
# Запрос для создания вида `teamRating` #
-----------------------------------------
CREATE VIEW `teamRating` AS 
SELECT DISTINCT 
`Se`.`season_ID`, `Se`.`seasonName`, 
`C`.`city_ID`,     `C`.`cityName`, 
`Sc`.`school_ID`, `Sc`.`schoolName`, 
`T`.`team_ID`,     `T`.`teamName`,
`A`.`age_ID`,      `A`.`ageName`,

CAST((SELECT COUNT(*) FROM `GameProtocol` AS `GP` 
WHERE (`GP`.`homeTeam_ID` = `T`.`team_ID` OR `GP`.`guestTeam_ID` = `T`.`team_ID`)) AS SIGNED) 
AS `games`,

CAST((SELECT COUNT(*) FROM `GameProtocol` AS `GP` 
WHERE (`GP`.`homeTeamScoreGame` > `GP`.`guestTeamScoreGame` AND `GP`.`homeTeam_ID` = `T`.`team_ID`) 
OR (`GP`.`homeTeamScoreGame` < `GP`.`guestTeamScoreGame` AND `GP`.`guestTeam_ID` = `T`.`team_ID`) 
OR (`GP`.`homeTeamScoreGame` = `GP`.`guestTeamScoreGame` AND ((`homeTeamScore11m` > `guestTeamScore11m` AND `GP`.`homeTeam_ID` = `T`.`team_ID`) OR (`homeTeamScore11m` < `guestTeamScore11m` AND `GP`.`guestTeam_ID`  = `T`.`team_ID`)))) AS SIGNED) 
AS `wins`,

CAST((SELECT COUNT(*) FROM `GameProtocol` AS `GP` 
WHERE `GP`.`homeTeamScoreGame` = `GP`.`guestTeamScoreGame` AND (`GP`.`homeTeam_ID` = `T`.`team_ID` OR `GP`.`guestTeam_ID` = `T`.`team_ID`)) AS SIGNED) 
AS `equals`,

CAST(((SELECT SUM(`GP`.`homeTeamScoreGame`) FROM `GameProtocol` `GP` WHERE (`GP`.`homeTeam_ID` = `T`.`team_ID`)) + (SELECT SUM(`GP`.`guestTeamScoreGame`) FROM `GameProtocol` `GP` WHERE (`GP`.`guestTeam_ID` = `T`.`team_ID`))) AS SIGNED) 
AS `scored`,

CAST(((SELECT SUM(`GP`.`homeTeamScoreGame`) FROM `GameProtocol` `GP` WHERE (`GP`.`guestTeam_ID` = `T`.`team_ID`)) + (SELECT SUM(`GP`.`guestTeamScoreGame`) FROM `GameProtocol` `GP` WHERE (`GP`.`homeTeam_ID` = `T`.`team_ID`))) AS SIGNED) 
AS `missed`,

CAST((SELECT (`scored` - `missed`)) AS SIGNED) 
AS `goals`,

CAST((SELECT COUNT(*) FROM `SeasonAgeStageTeam` AS `SAST` 
LEFT JOIN `SeasonAgeStage` AS `SAS`   ON (`SAST`.`SAS_ID`  = `SAS`.`SAS_ID`) 
LEFT JOIN `Stage`          AS `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`) 
WHERE `SAST`.`team_ID` = `T`.`team_ID` AND `Stage`.`stageType` = "P") AS SIGNED) 
AS `playoff`,

CAST((SELECT COUNT(DISTINCT `GP_ID`) FROM `GameProtocol` AS `GP` 
LEFT JOIN `SeasonAgeStageTeam` AS `SAST`  ON (`GP`.`SAS_ID`    = `SAST`.`SAS_ID`) 
LEFT JOIN `SeasonAgeStage`     AS `SAS`   ON (`SAST`.`SAS_ID`  = `SAS`.`SAS_ID`) 
LEFT JOIN `Stage`              AS `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`) 
WHERE `Stage`.`stageType` = "P" AND `GP`.`homeTeamScoreGame` = `GP`.`guestTeamScoreGame` 
AND ((`homeTeamScore11m` > `guestTeamScore11m` AND `GP`.`homeTeam_ID`  = `T`.`team_ID`) OR (`homeTeamScore11m` < `guestTeamScore11m` AND `GP`.`guestTeam_ID` = `T`.`team_ID`))) AS SIGNED) 
AS `playoff_11m`,

CAST((SELECT COUNT(DISTINCT `GP_ID`) FROM `GameProtocol` AS `GP` 
LEFT JOIN `SeasonAgeStageTeam` AS `SAST`  ON (`GP`.`SAS_ID`    = `SAST`.`SAS_ID`) 
LEFT JOIN `SeasonAgeStage`     AS `SAS`   ON (`SAST`.`SAS_ID`  = `SAS`.`SAS_ID`) 
LEFT JOIN `Stage`              AS `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`) 
WHERE `Stage`.`stageType` = "P" AND (`GP`.`homeTeam_ID` = `T`.`team_ID` OR `GP`.`guestTeam_ID` = `T`.`team_ID`) AND `GP`.`is_Semifinal` = 1) AS SIGNED) 
AS `playoff_SF`,

CAST((SELECT COUNT(DISTINCT `GP_ID`) FROM `GameProtocol` AS `GP` 
LEFT JOIN `SeasonAgeStageTeam` AS `SAST`  ON (`GP`.`SAS_ID`    = `SAST`.`SAS_ID`) 
LEFT JOIN `SeasonAgeStage`     AS `SAS`   ON (`SAST`.`SAS_ID`  = `SAS`.`SAS_ID`) 
LEFT JOIN `Stage`              AS `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`) 
WHERE `Stage`.`stageType` = "P" AND (`GP`.`homeTeam_ID` = `T`.`team_ID` OR `GP`.`guestTeam_ID` = `T`.`team_ID`) AND `GP`.`is_Final` = 1) AS SIGNED) 
AS `playoff_F`,

CAST((SELECT ROUND (( (`games` * 10000) + (`wins` * 30000) + (`equals` * 10000) + (`goals` * 501) + (`playoff` * 9000) + (`playoff_11m` * 10000) + (`playoff_SF` * 28000) + (`playoff_F` * 38000)) / `games`)) AS SIGNED) 
AS `teamRating`

FROM `Team` AS `T` 
LEFT JOIN `School`             AS `Sc`   ON (`T`.`school_ID`  = `Sc`.`school_ID`)
LEFT JOIN `City`               AS `C`    ON (`Sc`.`city_ID`   = `C`.`city_ID`)
LEFT JOIN `Age`                AS `A`    ON (`A`.`age_ID`     = `T`.`age_ID`)
LEFT JOIN `SeasonAgeStageTeam` AS `SAST` ON (`SAST`.`team_ID` = `T`.`team_ID`)
LEFT JOIN `SeasonAgeStage`     AS `SAS`  ON (`SAS`.`SAS_ID`   = `SAST`.`SAS_ID`)
LEFT JOIN `Season`             AS `Se`   ON (`Se`.`season_ID` = `SAS`.`season_ID`)

ORDER BY `teamRating` DESC

-------------------------------------------
# Запрос для создания вида `schoolRating` #
-------------------------------------------
CREATE VIEW `schoolRating` AS 
SELECT 
    `teamRating`.`season_ID`  AS `season_ID`,
    `teamRating`.`seasonName` AS `seasonName`,
    `teamRating`.`city_ID`    AS `city_ID`,
    `teamRating`.`cityName`   AS `cityName`,
    `teamRating`.`school_ID`  AS `school_ID`,
    `teamRating`.`schoolName` AS `schoolName`,

CAST(SUM(`teamRating`.`games`)       AS SIGNED) AS `games`,
CAST(SUM(`teamRating`.`wins`)        AS SIGNED) AS `wins`,
CAST(SUM(`teamRating`.`equals`)      AS SIGNED) AS `equals`,
CAST(SUM(`teamRating`.`scored`)      AS SIGNED) AS `scored`,
CAST(SUM(`teamRating`.`missed`)      AS SIGNED) AS `missed`,
CAST(SUM(`teamRating`.`goals`)       AS SIGNED) AS `goals`,
CAST(SUM(`teamRating`.`playoff`)     AS SIGNED) AS `playoff`,
CAST(SUM(`teamRating`.`playoff_11m`) AS SIGNED) AS `playoff_11m`,
CAST(SUM(`teamRating`.`playoff_SF`)  AS SIGNED) AS `playoff_SF`,
CAST(SUM(`teamRating`.`playoff_F`)   AS SIGNED) AS `playoff_F`,
CAST(SUM(`teamRating`.`teamRating`)  AS SIGNED) AS `schoolRating` 

FROM `teamRating` 
GROUP BY `school_ID` 
ORDER BY `schoolRating` DESC
