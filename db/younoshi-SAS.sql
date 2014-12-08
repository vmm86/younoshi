# Связь c GP через SAS #
listSAS = (RawQuery(SAS, 
    'SELECT `SAS`.*, 
    (SELECT COUNT(`SAST`.`SAS_ID`) FROM `SeasonAgeStageTeam` AS `SAST` WHERE `SAST`.`SAS_ID` = `SAS`.`SAS_ID`) `countSAST`, 
    (SELECT COUNT(`GP`.`SAS_ID`)   FROM `GameProtocol` AS `GP`         WHERE `GP`.`SAS_ID`   = `SAS`.`SAS_ID`) `countGP` 
    FROM `SeasonAgeStage` AS `SAS` 
    LEFT JOIN `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`) 
    WHERE ((`SAS`.`season_ID` = %s) AND (`SAS`.`age_ID` = %s)) 
    GROUP BY `SAS`.`SAS_ID` 
    ORDER BY `SAS`.`SAS_ID` ASC', seasonid, ageid))

listGP = GP.select().join(SAST, on=GP.SAS_ID).where((SAST.SAS_ID == sasid) & (GP.SAS_ID == sasid)).order_by(GP.gameNumber)

# Связь c GP через SAST #
listSAS = (RawQuery(SAS, 
    'SELECT `SAS`.*, 
    (SELECT COUNT(`SAST`.`SAS_ID`) FROM `SeasonAgeStageTeam` AS `SAST` WHERE `SAST`.`SAS_ID` = `SAS`.`SAS_ID`) `countSAST`, 
    (SELECT COUNT(`GP`.`SAS_ID`)   FROM `GameProtocol` AS `GP`         WHERE ((`GP`.`SAS_ID` = `SAST1`.`SAS_ID`) AND (`SAST1`.`SAS_ID` = `SAS`.`SAS_ID` )) ) `countGP` 
    FROM `SeasonAgeStage` AS `SAS` 
    LEFT JOIN `SeasonAgeStageTeam` AS `SAST1` ON (`SAS`.`SAS_ID` = `SAST1`.`SAS_ID`) 
    LEFT JOIN `Stage` ON (`SAS`.`stage_ID` = `Stage`.`stage_ID`) 
    WHERE ((`SAS`.`season_ID` = %s) AND (`SAS`.`age_ID` = %s)) 
    GROUP BY `SAS`.`SAS_ID` 
    ORDER BY `SAS`.`SAS_ID` ASC', seasonid, ageid))

listGP = GP.select().distinct().join(SAST, on=GP.SAS_ID).where((SAST.SAS_ID == sasid) & (GP.SAS_ID == sasid)).order_by(GP.gameNumber)

###
listSAS = (SAS
    .select(SAS, 
        fn.Count(fn.Distinct(SAST.SAST_ID)).alias('countSAST'), 
        fn.Count(fn.Distinct(GP.GP_ID)).alias('countGP')) 
    .join(SAST, JOIN_LEFT_OUTER).join(GP, JOIN_LEFT_OUTER)
    .switch(SAS).join(Stage)
    .where(SAS.season_ID == seasonid, SAS.age_ID == ageid)
    .group_by(SAS)
    .order_by(Stage.stageName, SAS.gameType_ID))

# separate queries
listSAS   = SAS.select().where(SAS.season_ID == seasonid, SAS.age_ID == ageid).join(Stage)
countSAST = SAS.select(SAS, fn.Count(SAST.SAS_ID).alias('countSAST')).where(SAS.season_ID == seasonid, SAS.age_ID == ageid).join(SAST, JOIN_LEFT_OUTER).group_by(SAS)
countGP   = SAS.select(SAS, fn.Count(GP.SAS_ID).alias('countGP')).where(SAS.season_ID == seasonid, SAS.age_ID == ageid).join(GP, JOIN_LEFT_OUTER).group_by(SAS)

# prefetch
listSAS   = SAS.select().where(SAS.season_ID == seasonid, SAS.age_ID == ageid).join(Stage)
countSAST = SAST.select(fn.Count(SAST.SAS_ID).alias('countSAST'))
countGP   = GP.select(fn.Count(GP.SAS_ID).alias('countGP'))
prefSAS   = prefetch(listSAS, countSAST, countGP)

# annotate
listSAS  = SAS.select().where(SAS.season_ID == seasonid, SAS.age_ID == ageid)
listSAS1 = listSAS.annotate(SAST, fn.Count(SAST.SAS_ID).alias('countSAST'))
listSAS2 = listSAS.annotate(GP, fn.Count(GP.SAS_ID).alias('countGP'))
