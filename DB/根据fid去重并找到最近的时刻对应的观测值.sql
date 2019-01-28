SELECT SUM(fid_id),MAX(`timestamp`),fr.bp,fr.wd
FROM Fub_fubrealtimeinfo as fr
GROUP BY fr.fid_id,`timestamp`,fr.bp,fr.wd

-- 此种方法可行
SELECT DISTINCT fid_id,MAX(`timestamp`),fr.bp,fr.wd
FROM Fub_fubrealtimeinfo as fr
GROUP BY fr.bp,fr.wd,fid_id

-- 此处需要使用嵌套查询（子查询）
-- SELECT DISTINCT fid_id,MAX(`timestamp`),fr.bp,fr.wd,ws,wd,wvperiod,wvd,code,lat,lon
-- FROM Fub_fubrealtimeinfo as fr
-- GROUP BY fr.bp,fr.wd,fid_id,ws,wd,wvperiod,wvd,code,lat,lon

-- 使用子查询进行过滤
-- 以下两种方式效果相同
SELECT DISTINCT fid_id,MAX(`timestamp`)
FROM Fub_fubrealtimeinfo as fr
GROUP BY fid_id

SELECT fid_id,MAX(`timestamp`)
FROM Fub_fubrealtimeinfo as fr
GROUP BY fid_id
--------

-- 使用子查询连接的方式（可行）
SELECT * 
FROM Fub_fubrealtimeinfo as f
JOIN (SELECT fid_id,MAX(`timestamp`) MAX_TIME
FROM Fub_fubrealtimeinfo as fr
GROUP BY fid_id) as temp
ON temp.fid_id=f.fid_id and temp.MAX_TIME=f.`timestamp`




SELECT DISTINCT(fid_id),MAX(`timestamp`)
FROM Fub_fubrealtimeinfo as fr
GROUP BY fid_id

SELECT DISTINCT(fid_id)
FROM Fub_fubrealtimeinfo

SELECT *
FROM Fub_fubrealtimeinfo
