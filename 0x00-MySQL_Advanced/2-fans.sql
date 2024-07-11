-- SQL script to rank country origins of bands by number of fans
-- executed on any database
SELECT origin, COUNT(*) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
