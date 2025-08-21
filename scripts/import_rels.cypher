// 1) (:Law)-[:GUIDED_BY]->(:Decree)
LOAD CSV WITH HEADERS FROM $baseUrl + '/relations/GUIDED_BY.csv' AS row
WITH trim(row.LAW_ID) AS LAW_ID, trim(row.DECREE_ID) AS DECREE_ID
WHERE LAW_ID <> '' AND DECREE_ID <> ''
MATCH (l:Law {LAW_ID: LAW_ID})
MATCH (d:Decree {DECREE_ID: DECREE_ID})
MERGE (l)-[:GUIDED_BY]->(d);

// 2) (:Law)-[:LAW_HAS_ARTICLE]->(:Article)
LOAD CSV WITH HEADERS FROM $baseUrl + '/relations/LAW_HAS_ARTICLE.csv' AS row
WITH trim(row.LAW_ID) AS LAW_ID, trim(row.ARTICLE_ID) AS ARTICLE_ID
WHERE LAW_ID <> '' AND ARTICLE_ID <> ''
MATCH (l:Law {LAW_ID: LAW_ID})
MATCH (a:Article {ARTICLE_ID: ARTICLE_ID})
MERGE (l)-[:LAW_HAS_ARTICLE]->(a);

// 3) (:Decree)-[:DECREE_HAS_ARTICLE]->(:Article)
LOAD CSV WITH HEADERS FROM $baseUrl + '/relations/DECREE_HAS_ARTICLE.csv' AS row
WITH trim(row.DECREE_ID) AS DECREE_ID, trim(row.ARTICLE_ID) AS ARTICLE_ID
WHERE DECREE_ID <> '' AND ARTICLE_ID <> ''
MATCH (d:Decree {DECREE_ID: DECREE_ID})
MATCH (a:Article {ARTICLE_ID: ARTICLE_ID})
MERGE (d)-[:DECREE_HAS_ARTICLE]->(a);

// 4) (:Article)-[:HAS_CLAUSE]->(:Clause)
LOAD CSV WITH HEADERS FROM $baseUrl + '/relations/HAS_CLAUSE.csv' AS row
WITH trim(row.ARTICLE_ID) AS ARTICLE_ID, trim(row.CLAUSE_ID) AS CLAUSE_ID
WHERE ARTICLE_ID <> '' AND CLAUSE_ID <> ''
MATCH (a:Article {ARTICLE_ID: ARTICLE_ID})
MATCH (c:Clause {CLAUSE_ID: CLAUSE_ID})
MERGE (a)-[:HAS_CLAUSE]->(c);

// ========== CHECK RELATIONSHIP COUNTS ==========
MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS n ORDER BY n DESC;