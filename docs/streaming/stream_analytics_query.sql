SELECT
    routeId,
    districtId,
    severity,
    AVG(delayMinutes) AS avgDelayMinutes,
    System.Timestamp() AS windowEndUtc
INTO
    eventsOutput
FROM
    mobilityEvents TIMESTAMP BY timestampUtc
GROUP BY
    TumblingWindow(minute, 5),
    routeId,
    districtId,
    severity
