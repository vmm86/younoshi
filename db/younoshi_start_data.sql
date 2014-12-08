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
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `teamRating` AS select distinct `Se`.`season_ID` AS `season_ID`,`Se`.`seasonName` AS `seasonName`,`C`.`city_ID` AS `city_ID`,`C`.`cityName` AS `cityName`,`Sc`.`school_ID` AS `school_ID`,`Sc`.`schoolName` AS `schoolName`,`T`.`team_ID` AS `team_ID`,`T`.`teamName` AS `teamName`,`A`.`age_ID` AS `age_ID`,`A`.`ageName` AS `ageName`,cast((select count(0) from `GameProtocol` `GP` where ((`GP`.`homeTeam_ID` = `T`.`team_ID`) or (`GP`.`guestTeam_ID` = `T`.`team_ID`))) as signed) AS `games`,cast((select count(0) from `GameProtocol` `GP` where (((`GP`.`homeTeamScoreGame` > `GP`.`guestTeamScoreGame`) and (`GP`.`homeTeam_ID` = `T`.`team_ID`)) or ((`GP`.`homeTeamScoreGame` < `GP`.`guestTeamScoreGame`) and (`GP`.`guestTeam_ID` = `T`.`team_ID`)) or ((`GP`.`homeTeamScoreGame` = `GP`.`guestTeamScoreGame`) and (((`GP`.`homeTeamScore11m` > `GP`.`guestTeamScore11m`) and (`GP`.`homeTeam_ID` = `T`.`team_ID`)) or ((`GP`.`homeTeamScore11m` < `GP`.`guestTeamScore11m`) and (`GP`.`guestTeam_ID` = `T`.`team_ID`)))))) as signed) AS `wins`,cast((select count(0) from `GameProtocol` `GP` where ((`GP`.`homeTeamScoreGame` = `GP`.`guestTeamScoreGame`) and ((`GP`.`homeTeam_ID` = `T`.`team_ID`) or (`GP`.`guestTeam_ID` = `T`.`team_ID`)))) as signed) AS `equals`,cast(((select sum(`GP`.`homeTeamScoreGame`) from `GameProtocol` `GP` where (`GP`.`homeTeam_ID` = `T`.`team_ID`)) + (select sum(`GP`.`guestTeamScoreGame`) from `GameProtocol` `GP` where (`GP`.`guestTeam_ID` = `T`.`team_ID`))) as signed) AS `scored`,cast(((select sum(`GP`.`homeTeamScoreGame`) from `GameProtocol` `GP` where (`GP`.`guestTeam_ID` = `T`.`team_ID`)) + (select sum(`GP`.`guestTeamScoreGame`) from `GameProtocol` `GP` where (`GP`.`homeTeam_ID` = `T`.`team_ID`))) as signed) AS `missed`,cast((select (`scored` - `missed`)) as signed) AS `goals`,cast((select count(0) from ((`SeasonAgeStageTeam` `SAST` left join `SeasonAgeStage` `SAS` on((`SAST`.`SAS_ID` = `SAS`.`SAS_ID`))) left join `Stage` on((`SAS`.`stage_ID` = `Stage`.`stage_ID`))) where ((`SAST`.`team_ID` = `T`.`team_ID`) and (`Stage`.`stageType` = 'P'))) as signed) AS `playoff`,cast((select count(distinct `GP`.`GP_ID`) from (((`GameProtocol` `GP` left join `SeasonAgeStageTeam` `SAST` on((`GP`.`SAS_ID` = `SAST`.`SAS_ID`))) left join `SeasonAgeStage` `SAS` on((`SAST`.`SAS_ID` = `SAS`.`SAS_ID`))) left join `Stage` on((`SAS`.`stage_ID` = `Stage`.`stage_ID`))) where ((`Stage`.`stageType` = 'P') and (`GP`.`homeTeamScoreGame` = `GP`.`guestTeamScoreGame`) and (((`GP`.`homeTeamScore11m` > `GP`.`guestTeamScore11m`) and (`GP`.`homeTeam_ID` = `T`.`team_ID`)) or ((`GP`.`homeTeamScore11m` < `GP`.`guestTeamScore11m`) and (`GP`.`guestTeam_ID` = `T`.`team_ID`))))) as signed) AS `playoff_11m`,cast((select count(distinct `GP`.`GP_ID`) from (((`GameProtocol` `GP` left join `SeasonAgeStageTeam` `SAST` on((`GP`.`SAS_ID` = `SAST`.`SAS_ID`))) left join `SeasonAgeStage` `SAS` on((`SAST`.`SAS_ID` = `SAS`.`SAS_ID`))) left join `Stage` on((`SAS`.`stage_ID` = `Stage`.`stage_ID`))) where ((`Stage`.`stageType` = 'P') and ((`GP`.`homeTeam_ID` = `T`.`team_ID`) or (`GP`.`guestTeam_ID` = `T`.`team_ID`)) and (`GP`.`is_Semifinal` = 1))) as signed) AS `playoff_SF`,cast((select count(distinct `GP`.`GP_ID`) from (((`GameProtocol` `GP` left join `SeasonAgeStageTeam` `SAST` on((`GP`.`SAS_ID` = `SAST`.`SAS_ID`))) left join `SeasonAgeStage` `SAS` on((`SAST`.`SAS_ID` = `SAS`.`SAS_ID`))) left join `Stage` on((`SAS`.`stage_ID` = `Stage`.`stage_ID`))) where ((`Stage`.`stageType` = 'P') and ((`GP`.`homeTeam_ID` = `T`.`team_ID`) or (`GP`.`guestTeam_ID` = `T`.`team_ID`)) and (`GP`.`is_Final` = 1))) as signed) AS `playoff_F`,cast((select round((((((((((`games` * 10000) + (`wins` * 30000)) + (`equals` * 10000)) + (`goals` * 501)) + (`playoff` * 9000)) + (`playoff_11m` * 10000)) + (`playoff_SF` * 28000)) + (`playoff_F` * 38000)) / `games`),0)) as signed) AS `teamRating` from ((((((`Team` `T` left join `School` `Sc` on((`T`.`school_ID` = `Sc`.`school_ID`))) left join `City` `C` on((`Sc`.`city_ID` = `C`.`city_ID`))) left join `Age` `A` on((`A`.`age_ID` = `T`.`age_ID`))) left join `SeasonAgeStageTeam` `SAST` on((`SAST`.`team_ID` = `T`.`team_ID`))) left join `SeasonAgeStage` `SAS` on((`SAS`.`SAS_ID` = `SAST`.`SAS_ID`))) left join `Season` `Se` on((`Se`.`season_ID` = `SAS`.`season_ID`))) order by cast((select round((((((((((`games` * 10000) + (`wins` * 30000)) + (`equals` * 10000)) + (`goals` * 501)) + (`playoff` * 9000)) + (`playoff_11m` * 10000)) + (`playoff_SF` * 28000)) + (`playoff_F` * 38000)) / `games`),0)) as signed) desc;

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
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `schoolRating` AS select `teamRating`.`season_ID` AS `season_ID`,`teamRating`.`seasonName` AS `seasonName`,`teamRating`.`city_ID` AS `city_ID`,`teamRating`.`cityName` AS `cityName`,`teamRating`.`school_ID` AS `school_ID`,`teamRating`.`schoolName` AS `schoolName`,cast(sum(`teamRating`.`games`) as signed) AS `games`,cast(sum(`teamRating`.`wins`) as signed) AS `wins`,cast(sum(`teamRating`.`equals`) as signed) AS `equals`,cast(sum(`teamRating`.`scored`) as signed) AS `scored`,cast(sum(`teamRating`.`missed`) as signed) AS `missed`,cast(sum(`teamRating`.`goals`) as signed) AS `goals`,cast(sum(`teamRating`.`playoff`) as signed) AS `playoff`,cast(sum(`teamRating`.`playoff_11m`) as signed) AS `playoff_11m`,cast(sum(`teamRating`.`playoff_SF`) as signed) AS `playoff_SF`,cast(sum(`teamRating`.`playoff_F`) as signed) AS `playoff_F`,cast(sum(`teamRating`.`teamRating`) as signed) AS `schoolRating` from `teamRating` group by `teamRating`.`school_ID` order by cast(sum(`teamRating`.`teamRating`) as signed) desc;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
