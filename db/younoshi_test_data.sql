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
AUTO_INCREMENT=3 ;

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
AUTO_INCREMENT=20 ;

INSERT INTO `City` (`city_ID`, `cityName`) VALUES
(1, 'Белгород'),
(2, 'Брянск'),
(3, 'Волгоград'),
(4, 'Волжский'),
(5, 'Воронеж'),
(6, 'Калуга'),
(7, 'Курск'),
(8, 'Ливны'),
(9, 'Липецк'),
(10, 'Новомосковск'),
(11, 'Обнинск'),
(12, 'Орел'),
(13, 'Рамонь'),
(14, 'Россошь'),
(15, 'Сафроново'),
(16, 'Смоленск'),
(17, 'Тамбов'),
(18, 'Тула'),
(19, 'Лондон');

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
AUTO_INCREMENT=35 ;

INSERT INTO `School` (`school_ID`, `city_ID`, `schoolName`) VALUES
(1, 1, 'ДЮСШ № 6'),
(2, 2, 'ДЮСШ по футболу «Динамо-Брянск»'),
(3, 2, 'ДЮСШ «Партизан»'),
(4, 3, 'СДЮСШОР № 11 «Зенит»'),
(5, 3, 'СДЮСШОР № 19 «Олимпия»'),
(6, 3, 'Центр спортивной подготовки по футболу'),
(7, 4, 'СДЮСШОР № 4'),
(8, 5, 'СДЮСШОР № 15'),
(9, 5, 'СДЮСШОР «Факел»'),
(10, 5, 'НП ФК «Стрела»'),
(11, 5, '«Академия футбола»'),
(12, 5, '«Воронеж»'),
(13, 5, '«Спарта»'),
(14, 5, 'ДСК «Строитель»'),
(15, 5, '«Чайка»'),
(16, 6, 'ДЮСШ «Анненки»'),
(17, 7, 'ФШ «Авангард»'),
(18, 7, 'ДЮСШ № 4'),
(19, 8, '«Гидромашина-Олимпиец»'),
(20, 9, 'ДЮСШ «Металлург»'),
(21, 10, 'МУС СК «Химик»'),
(22, 11, 'АНО ДЮСШ «Квант»'),
(23, 12, 'ДЮСШ № 3'),
(24, 12, 'СДЮСШОР «Русичи»'),
(25, 13, '«Торпедо»'),
(26, 14, '«Химик»'),
(27, 15, 'ФСК «Сафроново»'),
(28, 16, 'СДЮСШОР СКА МВО'),
(29, 16, 'СДЮСШОР № 5'),
(30, 16, '«Штурм»'),
(31, 17, 'СДЮСШОР «Академия футбола»'),
(32, 17, '«Локомотив-АФ»'),
(33, 18, 'ДЮСШ «Арсенал»'),
(34, 19, 'High School');

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
AUTO_INCREMENT=41 ;

INSERT INTO `Team` (`team_ID`, `school_ID`, `age_ID`, `teamName`) VALUES
(1, 1, 1, 'ДЮСШ-6'),
(2, 2, 1, '«Динамо-Брянск»'),
(3, 3, 1, '«Партизан»'),
(4, 4, 1, 'СДЮСШОР-11 «Зенит»'),
(5, 5, 1, '«Олимпия»'),
(6, 5, 1, '«Олимпия-2»'),
(7, 6, 1, 'ЦСП'),
(8, 7, 1, 'СДЮСШОР-4'),
(9, 7, 1, 'СДЮСШОР-4 (05)'),
(10, 8, 1, 'СДЮСШОР-15'),
(11, 9, 1, '«Факел»'),
(12, 9, 1, '«Факел-05»'),
(13, 10, 1, '«Стрела»'),
(14, 11, 1, '«Академия футбола»'),
(15, 12, 1, '«Воронеж»'),
(16, 13, 1, '«Спарта»'),
(17, 14, 1, 'ДСК «Строитель»'),
(18, 15, 1, '«Чайка»'),
(19, 16, 1, '«Анненки»'),
(20, 17, 1, 'Авангард'),
(21, 17, 1, 'Авангард-04'),
(22, 17, 1, 'Авангард-05'),
(23, 18, 1, 'ДЮСШ-4'),
(24, 19, 1, '«Гидромашина-Олимпиец»'),
(25, 20, 1, '«Металлург»'),
(26, 21, 1, '«Химик»'),
(27, 22, 1, '«Квант»'),
(28, 23, 1, 'ДЮСШ-3'),
(29, 24, 1, '«Русичи»'),
(30, 25, 1, '«Торпедо»'),
(31, 26, 1, '«Химик»'),
(32, 27, 1, 'ФСК «Сафроново»'),
(33, 28, 1, 'СКА'),
(34, 29, 1, 'СДЮСШОР-5'),
(35, 30, 1, '«Штурм»'),
(36, 31, 1, '«Академия футбола»'),
(37, 31, 1, '«Академия футбола-2»'),
(38, 32, 1, '«Локомотив-АФ»'),
(39, 33, 1, '«Арсенал»'),
(40, 34, 8, 'Old Wild Men');

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
AUTO_INCREMENT=2 ;

INSERT INTO `Season` (`season_ID`, `seasonName`) VALUES
(1, '2014');

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
AUTO_INCREMENT=19 ;

INSERT INTO `Stage` (`stage_ID`, `stageType`, `stageName`) VALUES
(1, 'P', 'плэй-офф'),
(2, 'G', 'А'), (3, 'G', 'Б'), (4, 'G', 'В'), (5, 'G', 'Г'), (6, 'G', 'Д'), (7, 'G', '1'), (8, 'G', '2'), (9, 'G', '3'), (10, 'G', '4'), (11, 'G', '5'),
(12, 'Z', 'г. Белгород'), (13, 'Z', 'г. Волжский'), (14, 'Z', 'г. Воронеж'), (15, 'Z', 'г. Курск'), (16, 'Z', 'г. Орёл'), (17, 'Z', 'г. Смоленск'), (18, 'Z', 'г. Тамбов');

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
AUTO_INCREMENT=7 ;

INSERT INTO `SeasonAgeStage` (`SAS_ID`, `season_ID`, `age_ID`, `stage_ID`, `gameType_ID`, `startDate`, `finishDate`) VALUES
(1, 1, 1, 13, 2, '2014-04-24', '2014-05-01'),
(2, 1, 1, 14, 2, '2014-04-30', '2014-05-11'),
(3, 1, 1, 15, 2, '2014-04-24', '2014-05-02'),
(4, 1, 1, 17, 2, '2014-04-30', '2014-05-08'),
(5, 1, 1, 18, 2, '2014-04-25', '2014-05-02'),
(6, 1, 1,  1, 2, '2014-06-09', '2014-06-18');

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
AUTO_INCREMENT=57 ;

INSERT INTO `SeasonAgeStageTeam` (`SAST_ID`, `team_ID`, `SAS_ID`, `substage_ID`) VALUES
(2, 8, 1, NULL),
(3, 9, 1, NULL),
(4, 5, 1, NULL),
(5, 6, 1, NULL),
(6, 4, 1, NULL),
(7, 7, 1, NULL),
(8, 11, 2, 2),
(9, 18, 2, 2),
(10, 13, 2, 2),
(11, 14, 2, 2),
(12, 17, 2, 2),
(13, 12, 2, 3),
(14, 10, 2, 3),
(15, 30, 2, 3),
(16, 16, 2, 3),
(17, 15, 2, 3),
(18, 20, 3, 2),
(19, 22, 3, 2),
(20, 28, 3, 2),
(21, 3, 3, 2),
(22, 24, 3, 2),
(23, 23, 3, 3),
(24, 21, 3, 3),
(25, 29, 3, 3),
(26, 1, 3, 3),
(27, 31, 3, 3),
(28, 33, 4, NULL),
(29, 34, 4, NULL),
(30, 35, 4, NULL),
(31, 32, 4, NULL),
(32, 2, 4, NULL),
(33, 27, 4, NULL),
(34, 19, 4, NULL),
(35, 36, 5, NULL),
(36, 37, 5, NULL),
(37, 25, 5, NULL),
(38, 39, 5, NULL),
(39, 26, 5, NULL),
(40, 38, 5, NULL),
(41, 20, 6, 2),
(42, 36, 6, 2),
(43, 12, 6, 2),
(44, 19, 6, 2),
(45, 5, 6, 3),
(46, 27, 6, 3),
(47, 16, 6, 3),
(48, 21, 6, 3),
(49, 35, 6, 4),
(50, 25, 6, 4),
(51, 8, 6, 4),
(52, 22, 6, 4),
(53, 18, 6, 5),
(54, 1, 6, 5),
(55, 4, 6, 5),
(56, 26, 6, 5);

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
AUTO_INCREMENT=160 ;

INSERT INTO `GameProtocol` (`SAS_ID`, `GP_ID`, `gameNumber`, `tourNumber`, `stageNumber`, `gameDate`, `homeTeam_ID`, `guestTeam_ID`, `homeTeamScoreGame`, `guestTeamScoreGame`, `homeTeamScore11m`, `guestTeamScore11m`, `is_Semifinal`, `is_Final`) VALUES
(1, 1, 1, 1, NULL, '2014-04-25', 8, 9, 6, 0, NULL, NULL, 0, 0),
(1, 3, 3, 1, NULL, '2014-04-25', 4, 7, 1, 0, NULL, NULL, 0, 0),
(1, 4, 4, 2, NULL, '2014-04-26', 8, 4, 1, 1, NULL, NULL, 0, 0),
(1, 5, 5, 2, NULL, '2014-04-26', 6, 7, 0, 3, NULL, NULL, 0, 0),
(1, 6, 6, 2, NULL, '2014-04-26', 9, 5, 0, 5, NULL, NULL, 0, 0),
(1, 7, 7, 3, NULL, '2014-04-28', 7, 8, 0, 2, NULL, NULL, 0, 0),
(1, 8, 8, 3, NULL, '2014-04-28', 9, 6, 0, 2, NULL, NULL, 0, 0),
(1, 9, 9, 3, NULL, '2014-04-28', 4, 5, 0, 8, NULL, NULL, 0, 0),
(1, 10, 10, 4, NULL, '2014-04-29', 5, 8, 1, 0, NULL, NULL, 0, 0),
(1, 11, 11, 4, NULL, '2014-04-29', 6, 4, 1, 2, NULL, NULL, 0, 0),
(1, 12, 12, 4, NULL, '2014-04-29', 7, 9, 0, 1, NULL, NULL, 0, 0),
(1, 13, 13, 5, NULL, '2014-04-30', 9, 4, 0, 3, NULL, NULL, 0, 0),
(1, 14, 14, 5, NULL, '2014-04-30', 6, 8, 0, 2, NULL, NULL, 0, 0),
(1, 15, 15, 5, NULL, '2014-04-30', 5, 7, 1, 0, NULL, NULL, 0, 0),
(2, 16, 1, 1, NULL, '2014-05-01', 11, 17, 4, 0, NULL, NULL, 0, 0),
(2, 17, 2, 1, NULL, '2014-05-01', 13, 18, 4, 1, NULL, NULL, 0, 0),
(2, 18, 3, 1, NULL, '2014-05-01', 12, 15, 3, 1, NULL, NULL, 0, 0),
(2, 19, 4, 1, NULL, '2014-05-01', 30, 10, 1, 1, NULL, NULL, 0, 0),
(2, 20, 5, 2, NULL, '2014-05-02', 14, 13, 2, 1, NULL, NULL, 0, 0),
(2, 21, 6, 2, NULL, '2014-05-02', 17, 18, 0, 5, NULL, NULL, 0, 0),
(2, 22, 7, 2, NULL, '2014-05-02', 10, 16, 1, 3, NULL, NULL, 0, 0),
(2, 23, 8, 2, NULL, '2014-05-02', 15, 30, 2, 0, NULL, NULL, 0, 0),
(2, 24, 9, 3, NULL, '2014-05-03', 13, 17, 7, 0, NULL, NULL, 0, 0),
(2, 25, 10, 3, NULL, '2014-05-03', 14, 11, 2, 0, NULL, NULL, 0, 0),
(2, 26, 11, 3, NULL, '2014-05-03', 10, 15, 4, 0, NULL, NULL, 0, 0),
(2, 27, 12, 3, NULL, '2014-05-03', 16, 12, 0, 0, NULL, NULL, 0, 0),
(2, 28, 13, 4, NULL, '2014-05-04', 18, 11, 1, 0, NULL, NULL, 0, 0),
(2, 29, 14, 4, NULL, '2014-05-04', 17, 14, 0, 5, NULL, NULL, 0, 0),
(2, 30, 15, 4, NULL, '2014-05-04', 12, 30, 0, 0, NULL, NULL, 0, 0),
(2, 31, 16, 4, NULL, '2014-05-04', 15, 16, 0, 3, NULL, NULL, 0, 0),
(2, 32, 17, 5, NULL, '2014-05-08', 11, 13, 0, 0, NULL, NULL, 0, 0),
(2, 33, 18, 5, NULL, '2014-05-08', 14, 18, 0, 1, NULL, NULL, 0, 0),
(2, 34, 19, 5, NULL, '2014-05-08', 10, 12, 1, 4, NULL, NULL, 0, 0),
(2, 35, 20, 5, NULL, '2014-05-08', 16, 30, 1, 0, NULL, NULL, 0, 0),
(2, 36, 21, 0, NULL, '2014-05-10', 17, 15, 0, 1, NULL, NULL, 0, 0),
(2, 37, 22, 0, NULL, '2014-05-10', 11, 30, 1, 2, NULL, NULL, 0, 0),
(2, 38, 23, 0, NULL, '2014-05-10', 10, 13, 4, 1, NULL, NULL, 0, 0),
(2, 39, 24, 0, NULL, '2014-05-10', 14, 16, 0, 0, NULL, NULL, 0, 0),
(2, 40, 25, 0, NULL, '2014-05-10', 12, 18, 0, 1, NULL, NULL, 0, 0),
(2, 41, 26, 0, NULL, '2014-05-11', 11, 10, 0, 1, NULL, NULL, 0, 0),
(2, 42, 27, 0, NULL, '2014-05-11', 13, 30, 2, 1, NULL, NULL, 0, 0),
(2, 43, 28, 0, NULL, '2014-05-11', 14, 12, 0, 2, NULL, NULL, 0, 0),
(2, 44, 29, 0, NULL, '2014-05-11', 18, 16, 0, 0, NULL, NULL, 0, 0),
(3, 45, 1, 1, NULL, '2014-04-24', 20, 24, 5, 0, NULL, NULL, 0, 0),
(3, 46, 2, 1, NULL, '2014-04-24', 28, 22, 0, 3, NULL, NULL, 0, 0),
(3, 47, 3, 1, NULL, '2014-04-24', 23, 31, 2, 2, NULL, NULL, 0, 0),
(3, 48, 4, 1, NULL, '2014-04-24', 29, 20, 0, 1, NULL, NULL, 0, 0),
(3, 49, 5, 2, NULL, '2014-04-26', 22, 3, 1, 0, NULL, NULL, 0, 0),
(3, 50, 6, 2, NULL, '2014-04-26', 24, 28, 2, 0, NULL, NULL, 0, 0),
(3, 51, 7, 2, NULL, '2014-04-26', 21, 1, 3, 4, NULL, NULL, 0, 0),
(3, 52, 8, 2, NULL, '2014-04-26', 31, 29, 1, 0, NULL, NULL, 0, 0),
(3, 53, 9, 3, NULL, '2014-04-27', 28, 20, 0, 5, NULL, NULL, 0, 0),
(3, 54, 10, 3, NULL, '2014-04-27', 3, 24, 3, 1, NULL, NULL, 0, 0),
(3, 55, 11, 3, NULL, '2014-04-27', 29, 23, 3, 1, NULL, NULL, 0, 0),
(3, 56, 12, 3, NULL, '2014-04-27', 1, 31, 7, 1, NULL, NULL, 0, 0),
(3, 57, 13, 4, NULL, '2014-04-28', 22, 24, 1, 1, NULL, NULL, 0, 0),
(3, 58, 14, 4, NULL, '2014-04-28', 20, 3, 2, 1, NULL, NULL, 0, 0),
(3, 59, 15, 4, NULL, '2014-04-28', 21, 31, 2, 0, NULL, NULL, 0, 0),
(3, 60, 16, 4, NULL, '2014-04-28', 23, 1, 0, 4, NULL, NULL, 0, 0),
(3, 61, 17, 5, NULL, '2014-04-29', 20, 22, 6, 3, NULL, NULL, 0, 0),
(3, 62, 18, 5, NULL, '2014-04-29', 3, 28, 4, 0, NULL, NULL, 0, 0),
(3, 63, 19, 5, NULL, '2014-04-29', 23, 21, 1, 5, NULL, NULL, 0, 0),
(3, 64, 20, 5, NULL, '2014-04-29', 1, 29, 1, 2, NULL, NULL, 0, 0),
(3, 65, 21, 0, NULL, '2014-04-30', 28, 23, 0, 4, NULL, NULL, 0, 0),
(3, 66, 22, 0, NULL, '2014-04-30', 24, 29, 4, 1, NULL, NULL, 0, 0),
(3, 67, 23, 0, NULL, '2014-04-30', 31, 3, 0, 2, NULL, NULL, 0, 0),
(3, 68, 24, 0, NULL, '2014-04-30', 22, 1, 0, 2, NULL, NULL, 0, 0),
(3, 69, 25, 0, NULL, '2014-04-30', 21, 20, 4, 2, NULL, NULL, 0, 0),
(3, 70, 26, 0, NULL, '2014-05-01', 24, 31, 3, 1, NULL, NULL, 0, 0),
(3, 71, 27, 0, NULL, '2014-05-01', 3, 29, 0, 0, NULL, NULL, 0, 0),
(3, 72, 28, 0, NULL, '2014-05-01', 22, 21, 2, 2, NULL, NULL, 0, 0),
(3, 73, 29, 0, NULL, '2014-05-01', 20, 1, 4, 2, NULL, NULL, 0, 0),
(4, 74, 1, 1, NULL, '2014-05-01', 33, 34, 0, 3, NULL, NULL, 0, 0),
(4, 75, 2, 1, NULL, '2014-05-01', 27, 35, 1, 2, NULL, NULL, 0, 0),
(4, 76, 3, 1, NULL, '2014-05-01', 32, 2, 11, 0, NULL, NULL, 0, 0),
(4, 77, 4, 2, NULL, '2014-05-02', 33, 2, 0, 4, NULL, NULL, 0, 0),
(4, 78, 5, 2, NULL, '2014-05-02', 35, 19, 5, 3, NULL, NULL, 0, 0),
(4, 79, 6, 2, NULL, '2014-05-02', 34, 27, 0, 3, NULL, NULL, 0, 0),
(4, 80, 7, 3, NULL, '2014-05-03', 27, 32, 0, 4, NULL, NULL, 0, 0),
(4, 81, 8, 3, NULL, '2014-05-03', 34, 35, 3, 3, NULL, NULL, 0, 0),
(4, 82, 9, 3, NULL, '2014-05-03', 19, 2, 2, 0, NULL, NULL, 0, 0),
(4, 83, 10, 4, NULL, '2014-05-04', 33, 35, 1, 0, NULL, NULL, 0, 0),
(4, 84, 11, 4, NULL, '2014-05-04', 27, 19, 2, 1, NULL, NULL, 0, 0),
(4, 85, 12, 4, NULL, '2014-05-04', 32, 34, 1, 3, NULL, NULL, 0, 0),
(4, 86, 13, 5, NULL, '2014-05-05', 35, 2, 3, 1, NULL, NULL, 0, 0),
(4, 87, 14, 5, NULL, '2014-05-05', 33, 27, 0, 0, NULL, NULL, 0, 0),
(4, 88, 15, 5, NULL, '2014-05-05', 32, 19, 0, 5, NULL, NULL, 0, 0),
(4, 89, 16, 6, NULL, '2014-05-06', 32, 33, 1, 4, NULL, NULL, 0, 0),
(4, 90, 17, 6, NULL, '2014-05-06', 34, 19, 0, 3, NULL, NULL, 0, 0),
(4, 91, 18, 6, NULL, '2014-05-06', 27, 2, 0, 0, NULL, NULL, 0, 0),
(4, 92, 19, 7, NULL, '2014-05-07', 2, 34, 6, 2, NULL, NULL, 0, 0),
(4, 93, 20, 7, NULL, '2014-05-07', 35, 32, 4, 1, NULL, NULL, 0, 0),
(4, 94, 21, 7, NULL, '2014-05-07', 33, 19, 1, 1, NULL, NULL, 0, 0),
(5,  95,  1, 1, NULL, '2014-04-26', 36, 26, 5, 2, NULL, NULL, 0, 0),
(5,  96,  2, 1, NULL, '2014-04-26', 25, 37, 1, 0, NULL, NULL, 0, 0),
(5,  97,  3, 1, NULL, '2014-04-26', 39, 38, 2, 0, NULL, NULL, 0, 0),
(5,  98,  4, 2, NULL, '2014-04-27', 37, 39, 2, 0, NULL, NULL, 0, 0),
(5,  99,  5, 2, NULL, '2014-04-27', 26, 25, 1, 0, NULL, NULL, 0, 0),
(5, 100,  6, 2, NULL, '2014-04-27', 38, 36, 0, 3, NULL, NULL, 0, 0),
(5, 101,  7, 3, NULL, '2014-04-29', 37, 26, 1, 1, NULL, NULL, 0, 0),
(5, 102,  8, 3, NULL, '2014-04-29', 39, 36, 1, 6, NULL, NULL, 0, 0),
(5, 103,  9, 3, NULL, '2014-04-29', 25, 38, 4, 0, NULL, NULL, 0, 0),
(5, 104, 10, 4, NULL, '2014-04-30', 36, 25, 0, 3, NULL, NULL, 0, 0),
(5, 105, 11, 4, NULL, '2014-04-30', 26, 39, 0, 3, NULL, NULL, 0, 0),
(5, 106, 12, 4, NULL, '2014-04-30', 38, 37, 1, 0, NULL, NULL, 0, 0),
(5, 107, 13, 5, NULL, '2014-05-01', 37, 36, 0, 5, NULL, NULL, 0, 0),
(5, 108, 14, 5, NULL, '2014-05-01', 25, 39, 2, 0, NULL, NULL, 0, 0),
(5, 109, 15, 5, NULL, '2014-05-01', 38, 26, 0, 1, NULL, NULL, 0, 0),
(6, 111,  1, 1, NULL, '2014-06-10', 20, 19, 2, 0, NULL, NULL, 0, 0),
(6, 112,  2, 1, NULL, '2014-06-10', 36, 12, 2, 4, NULL, NULL, 0, 0),
(6, 113,  3, 1, NULL, '2014-06-10', 5, 21, 2, 1, NULL, NULL, 0, 0),
(6, 114,  4, 1, NULL, '2014-06-10', 27, 16, 1, 1, NULL, NULL, 0, 0),
(6, 115,  5, 1, NULL, '2014-06-10', 35, 22, 2, 3, NULL, NULL, 0, 0),
(6, 116,  6, 1, NULL, '2014-06-10', 25, 8, 1, 0, NULL, NULL, 0, 0),
(6, 117,  7, 1, NULL, '2014-06-10', 18, 26, 1, 0, NULL, NULL, 0, 0),
(6, 118,  8, 1, NULL, '2014-06-10', 1, 4, 3, 1, NULL, NULL, 0, 0),
(6, 119,  9, 2, NULL, '2014-06-11', 19, 36, 0, 1, NULL, NULL, 0, 0),
(6, 120, 10, 2, NULL, '2014-06-11', 12, 20, 0, 2, NULL, NULL, 0, 0),
(6, 121, 11, 2, NULL, '2014-06-11', 21, 27, 5, 2, NULL, NULL, 0, 0),
(6, 122, 12, 2, NULL, '2014-06-11', 16, 5, 0, 1, NULL, NULL, 0, 0),
(6, 123, 13, 2, NULL, '2014-06-11', 22, 25, 1, 2, NULL, NULL, 0, 0),
(6, 124, 14, 2, NULL, '2014-06-11', 8, 35, 0, 3, NULL, NULL, 0, 0),
(6, 125, 15, 2, NULL, '2014-06-11', 26, 1, 3, 6, NULL, NULL, 0, 0),
(6, 126, 16, 2, NULL, '2014-06-11', 4, 18, 2, 1, NULL, NULL, 0, 0),
(6, 127, 17, 3, NULL, '2014-06-13', 12, 19, 0, 2, NULL, NULL, 0, 0),
(6, 128, 18, 3, NULL, '2014-06-13', 20, 36, 1, 3, NULL, NULL, 0, 0),
(6, 129, 19, 3, NULL, '2014-06-13', 16, 21, 2, 2, NULL, NULL, 0, 0),
(6, 130, 20, 3, NULL, '2014-06-13', 5, 27, 3, 1, NULL, NULL, 0, 0),
(6, 131, 21, 3, NULL, '2014-06-13', 8, 22, 3, 2, NULL, NULL, 0, 0),
(6, 132, 22, 3, NULL, '2014-06-13', 35, 25, 0, 2, NULL, NULL, 0, 0),
(6, 133, 23, 3, NULL, '2014-06-13', 4, 26, 2, 1, NULL, NULL, 0, 0),
(6, 134, 24, 3, NULL, '2014-06-13', 18, 1, 1, 2, NULL, NULL, 0, 0),
(6, 135, 25, 0, NULL, '2014-06-14', 21, 36, 0, 4, NULL, NULL, 0, 0),
(6, 136, 26, 0, NULL, '2014-06-14', 35, 1, 0, 0, 2, 4, 0, 0),
(6, 137, 27, 0, NULL, '2014-06-14', 12, 16, 2, 0, NULL, NULL, 0, 0),
(6, 138, 28, 0, NULL, '2014-06-14', 8, 18, 0, 2, NULL, NULL, 0, 0),
(6, 139, 29, 0, NULL, '2014-06-14', 20, 5, 0, 0, 3, 4, 0, 0),
(6, 140, 30, 0, NULL, '2014-06-14', 4, 25, 0, 3, NULL, NULL, 0, 0),
(6, 141, 31, 0, NULL, '2014-06-14', 27, 19, 1, 1, 3, 2, 0, 0),
(6, 142, 32, 0, NULL, '2014-06-14', 26, 22, 1, 0, NULL, NULL, 0, 0),
(6, 143, 33, 0, NULL, '2014-06-14', 36, 1, 5, 0, NULL, NULL, 1, 0),
(6, 144, 34, 0, NULL, '2014-06-14', 5, 25, 0, 0, 4, 5, 1, 0),
(6, 145, 35, 0, NULL, '2014-06-14', 21, 35, 2, 1, NULL, NULL, 0, 0),
(6, 146, 36, 0, NULL, '2014-06-14', 20, 4, 2, 1, NULL, NULL, 0, 0),
(6, 147, 37, 0, NULL, '2014-06-14', 18, 12, 1, 2, NULL, NULL, 0, 0),
(6, 148, 38, 0, NULL, '2014-06-14', 27, 26, 0, 0, 3, 2, 0, 0),
(6, 149, 39, 0, NULL, '2014-06-14', 16, 8, 2, 1, NULL, NULL, 0, 0),
(6, 150, 40, 0, NULL, '2014-06-14', 19, 22, 1, 2, NULL, NULL, 0, 0),
(6, 151, 41, 0, NULL, '2014-06-14', 8, 19, 1, 2, NULL, NULL, 0, 0),
(6, 152, 42, 0, NULL, '2014-06-14', 16, 22, 1, 2, NULL, NULL, 0, 0),
(6, 153, 43, 0, NULL, '2014-06-14', 18, 26, 2, 1, NULL, NULL, 0, 0),
(6, 154, 44, 0, NULL, '2014-06-14', 27, 12, 1, 2, NULL, NULL, 0, 0),
(6, 155, 45, 0, NULL, '2014-06-14', 35, 4, 4, 0, NULL, NULL, 0, 0),
(6, 156, 46, 0, NULL, '2014-06-14', 21, 20, 7, 0, NULL, NULL, 0, 0),
(6, 157, 47, 0, NULL, '2014-06-14', 1, 5, 1, 3, NULL, NULL, 0, 0),
(6, 158, 48, 0, NULL, '2014-06-14', 36, 25, 4, 1, NULL, NULL, 0, 1),
(1, 159, 2,  1, NULL, '2014-04-25', 5, 6, 5, 0, NULL, NULL, 0, 0);

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
