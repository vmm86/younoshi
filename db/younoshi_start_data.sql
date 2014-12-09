SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

--
-- Структура таблицы `User`
--
CREATE TABLE IF NOT EXISTS `User` (
    `user_ID`      INT         NOT NULL AUTO_INCREMENT,
    `userLogin`    VARCHAR(32) NOT NULL,
    `userPassword` VARCHAR(32) NOT NULL,
    `userName`     VARCHAR(32) NOT NULL,
    PRIMARY KEY (`user_ID`))
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=2 ;

INSERT INTO `User` (`user_ID`, `userLogin`, `userPassword`, `userName`) VALUES
(1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'Администратор'),
(2, 'demo',  'fe01ce2a7fbac8fafaed7c982a04e229', 'Демо-пользователь');

--
-- Структура таблицы `City`
--
CREATE TABLE IF NOT EXISTS `City` (
    `city_ID`  INT          NOT NULL AUTO_INCREMENT,
    `cityName` VARCHAR(128) NOT NULL,
    PRIMARY KEY (`city_ID`))
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=1 ;

--
-- Структура таблицы `School`
--
CREATE TABLE IF NOT EXISTS `School` (
    `school_ID`  INT          NOT NULL AUTO_INCREMENT,
    `city_ID`    INT          NOT NULL,
    `schoolName` VARCHAR(128) NOT NULL,
    PRIMARY KEY (`school_ID`),
    INDEX `INDEX_FK_School_City` (`city_ID` ASC),
    UNIQUE INDEX `UNIQUE_School_City` (`school_ID` ASC, `city_ID` ASC),
    CONSTRAINT `FK_School_City`
        FOREIGN KEY (`city_ID`)
        REFERENCES `City` (`city_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=1 ;

--
-- Структура таблицы `Team`
--
CREATE TABLE IF NOT EXISTS `Team` (
    `team_ID`   INT          NOT NULL AUTO_INCREMENT,
    `school_ID` INT          NOT NULL,
    `age_ID`    INT          NOT NULL,
    `teamName`  VARCHAR(128) NOT NULL,
    PRIMARY KEY (`team_ID`),
    INDEX `INDEX_FK_Team_School`          (`school_ID` ASC),
    INDEX `INDEX_FK_Team_Age`             (`age_ID` ASC),
    UNIQUE INDEX `UNIQUE_School_Team_Age` (`school_ID` ASC, `team_ID` ASC, `age_ID` ASC),
    CONSTRAINT `FK_Team_School`
        FOREIGN KEY (`school_ID`)
        REFERENCES `School` (`school_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `FK_Team_Age`
        FOREIGN KEY (`age_ID`)
        REFERENCES `Age` (`age_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=1 ;

--
-- Структура таблицы `Age`
--
CREATE TABLE IF NOT EXISTS `Age` (
    `age_ID`  INT NOT NULL AUTO_INCREMENT,
    `ageName` INT NOT NULL,
    PRIMARY KEY (`age_ID`))
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=9 ;

INSERT INTO `Age` (`age_ID`, `ageName`) VALUES
(1, 10), (2, 11), (3, 12), (4, 13), 
(5, 14), (6, 15), (7, 16), (8, 17);

--
-- Структура таблицы `Season`
--
CREATE TABLE IF NOT EXISTS `Season` (
    `season_ID`  INT          NOT NULL AUTO_INCREMENT,
    `seasonName` VARCHAR(128) NOT NULL,
    PRIMARY KEY (`season_ID`))
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=1 ;

--
-- Структура таблицы `Stage`
--
CREATE TABLE IF NOT EXISTS `Stage` (
    `stage_ID`  INT          NOT NULL AUTO_INCREMENT,
    `stageType` CHAR         NOT NULL COMMENT 'G - групповой этап\nZ - зональный этап\nF - финальный этап',
    `stageName` VARCHAR(128) NOT NULL,
    PRIMARY KEY (`stage_ID`))
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=14 ;

INSERT INTO `Stage` (`stage_ID`, `stageType`, `stageName`) VALUES
(1, 'P', 'плэй-офф'),
(2, 'G', '1-я группа'),  (3, 'G', '2-я группа'),  (4, 'G', '3-я группа'), (5,  'G', '4-я группа'), (6,  'G', '5-я группа'),
(7, 'Z', 'г. Белгород'), (8, 'Z', 'г. Волжский'), (9, 'Z', 'г. Воронеж'), (10, 'Z', 'г. Курск'),   (11, 'Z', 'г. Орёл'), (12, 'Z', 'г. Смоленск'), (13, 'Z', 'г. Тамбов');

--
-- Структура таблицы `GameType`
--
CREATE TABLE IF NOT EXISTS `GameType` (
    `gameType_ID`  INT         NOT NULL AUTO_INCREMENT,
    `gameTypeName` VARCHAR(16) NOT NULL COMMENT 'CHA - Первенство\nCUP - Кубок',
    PRIMARY KEY (`gameType_ID`))
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=3 ;

INSERT INTO `GameType` (`gameType_ID`, `gameTypeName`) VALUES
(1, 'CHA'), (2, 'CUP');

--
-- Структура таблицы `SeasonAgeStage`
--
CREATE TABLE IF NOT EXISTS `SeasonAgeStage` (
    `SAS_ID`      INT  NOT NULL AUTO_INCREMENT,
    `season_ID`   INT  NOT NULL,
    `gameType_ID` INT  NOT NULL,
    `age_ID`      INT  NOT NULL,
    `stage_ID`    INT  NOT NULL,
    `startDate`   DATE NULL,
    `finishDate`  DATE NULL,
    PRIMARY KEY (`SAS_ID`),
    INDEX `INDEX_FK_SAS_Season` (`season_ID` ASC),
    INDEX `INDEX_FK_SAS_Stage` (`stage_ID` ASC),
    INDEX `INDEX_FK_SAS_Age` (`age_ID` ASC),
    INDEX `INDEX_FK_SAS_GameType` (`gameType_ID` ASC),
    UNIQUE INDEX `UNIQUE_Season_Age_Stage` (`season_ID` ASC, `age_ID` ASC, `stage_ID` ASC),
    CONSTRAINT `FK_SAS_Season`
        FOREIGN KEY (`season_ID`)
        REFERENCES `Season` (`season_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `FK_SAS_Age`
        FOREIGN KEY (`age_ID`)
        REFERENCES `Age` (`age_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `FK_SAS_Stage`
        FOREIGN KEY (`stage_ID`)
        REFERENCES `Stage` (`stage_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `FK_SAS_GameType`
        FOREIGN KEY (`gameType_ID`)
        REFERENCES `GameType` (`gameType_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=1 ;

--
-- Структура таблицы `SeasonAgeStageTeam`
--
CREATE TABLE IF NOT EXISTS `SeasonAgeStageTeam` (
    `SAS_ID`      INT NOT NULL,
    `SAST_ID`     INT NOT NULL AUTO_INCREMENT,
    `team_ID`     INT NOT NULL,
    `substage_ID` INT NULL DEFAULT 0,
    PRIMARY KEY (`SAST_ID`),
    INDEX `INDEX_FK_SAST_SAS` (`SAS_ID` ASC),
    INDEX `INDEX_FK_SAST_Team` (`team_ID` ASC),
    INDEX `INDEX_FK_SAST_Stage` (`substage_ID` ASC),
    UNIQUE INDEX `UNIQUE_SAS_Team` (`SAS_ID` ASC, `team_ID` ASC, `substage_ID` ASC),
    CONSTRAINT `FK_SAST_SAS`
        FOREIGN KEY (`SAS_ID`)
        REFERENCES `SeasonAgeStage` (`SAS_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `FK_SAST_Team`
        FOREIGN KEY (`team_ID`)
        REFERENCES `Team` (`team_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `FK_SAST_Stage`
        FOREIGN KEY (`substage_ID`)
        REFERENCES `Stage` (`stage_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=1 ;

--
-- Структура таблицы `GameProtocol`
--
CREATE TABLE IF NOT EXISTS `GameProtocol` (
    `SAS_ID`             INT        NOT NULL,
    `GP_ID`              INT        NOT NULL AUTO_INCREMENT,
    `gameNumber`         INT        NOT NULL,
    `tourNumber`         INT        NOT NULL,
    `stageNumber`        TINYINT(1) NULL DEFAULT 0,
    `gameDate`           DATE       NOT NULL,
    `homeTeam_ID`        INT        NOT NULL,
    `guestTeam_ID`       INT        NOT NULL,
    `homeTeamScoreGame`  INT        NOT NULL,
    `guestTeamScoreGame` INT        NOT NULL,
    `homeTeamScore11m`   INT        NULL DEFAULT NULL,
    `guestTeamScore11m`  INT        NULL DEFAULT NULL,
    `is_Semifinal`       TINYINT(1) NOT NULL DEFAULT 0,
    `is_Final`           TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (`GP_ID`),
    INDEX `INDEX_FK_HT_SAST` (`homeTeam_ID` ASC),
    INDEX `INDEX_FK_GT_SAST` (`guestTeam_ID` ASC),
    INDEX `INDEX_FK_GP_SAS` (`SAS_ID` ASC),
    UNIQUE INDEX `UNIQUE_GP_HT_GT` (`GP_ID` ASC, `homeTeam_ID` ASC, `guestTeam_ID` ASC),
    CONSTRAINT `FK_hT_SAST`
        FOREIGN KEY (`homeTeam_ID`)
        REFERENCES `SeasonAgeStageTeam` (`team_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `FK_gT_SAST`
        FOREIGN KEY (`guestTeam_ID`)
        REFERENCES `SeasonAgeStageTeam` (`team_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `FK_GP_SAS`
        FOREIGN KEY (`SAS_ID`)
        REFERENCES `SeasonAgeStage` (`SAS_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT `FK_GP_SAST`
        FOREIGN KEY (`SAS_ID`)
        REFERENCES `SeasonAgeStageTeam` (`SAS_ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARSET = utf8
COLLATE = utf8_general_ci
AUTO_INCREMENT=1 ;

--
-- Дублирующая структура для представления `teamRating`
--
CREATE TABLE IF NOT EXISTS `teamRating` (
    `season_ID`   int(11),
    `seasonName`  varchar(128),
    `city_ID`     int(11),
    `cityName`    varchar(128),
    `school_ID`   int(11),
    `schoolName`  varchar(128),
    `team_ID`     int(11),
    `teamName`    varchar(128),
    `age_ID`      int(11),
    `ageName`     int(11),
    `games`       bigint(21),
    `wins`        bigint(21),
    `equals`      bigint(21),
    `scored`      bigint(21),
    `missed`      bigint(21),
    `goals`       bigint(21),
    `playoff`     bigint(21),
    `playoff_11m` bigint(21),
    `playoff_SF`  bigint(21),
    `playoff_F`   bigint(21),
    `teamRating`  bigint(21)
);

--
-- Структура для представления `teamRating`
--
DROP TABLE IF EXISTS `teamRating`;
CREATE OR REPLACE VIEW `teamRating` AS 
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
CAST((SELECT SUM(`GP`.`homeTeamScoreGame`) FROM `GameProtocol` `GP` WHERE (`GP`.`homeTeam_ID` = `T`.`team_ID`)) + (SELECT SUM(`GP`.`guestTeamScoreGame`) FROM `GameProtocol` `GP` WHERE (`GP`.`guestTeam_ID` = `T`.`team_ID`)) AS SIGNED) 
AS `scored`,
CAST((SELECT SUM(`GP`.`homeTeamScoreGame`) FROM `GameProtocol` `GP` WHERE (`GP`.`guestTeam_ID` = `T`.`team_ID`)) + (SELECT SUM(`GP`.`guestTeamScoreGame`) FROM `GameProtocol` `GP` WHERE (`GP`.`homeTeam_ID` = `T`.`team_ID`)) AS SIGNED) 
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
ORDER BY `teamRating` DESC;

--
-- Дублирующая структура для представления `schoolRating`
--
CREATE TABLE IF NOT EXISTS `schoolRating` (
    `season_ID`    int(11),
    `seasonName`   varchar(128),
    `city_ID`      int(11),
    `cityName`     varchar(128),
    `school_ID`    int(11),
    `schoolName`   varchar(128),
    `games`        bigint(21),
    `wins`         bigint(21),
    `equals`       bigint(21),
    `scored`       bigint(21),
    `missed`       bigint(21),
    `goals`        bigint(21),
    `playoff`      bigint(21),
    `playoff_11m`  bigint(21),
    `playoff_SF`   bigint(21),
    `playoff_F`    bigint(21),
    `schoolRating` bigint(21)
);

--
-- Структура для представления `schoolRating`
--
DROP TABLE IF EXISTS `schoolRating`;
CREATE OR REPLACE VIEW `schoolRating` AS
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
GROUP BY `teamRating`.`school_ID`
ORDER BY CAST(SUM(`teamRating`.`teamRating`) AS SIGNED) DESC;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
