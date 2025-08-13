:param baseUrl => 'https://raw.githubusercontent.com/phuongnga205/legal-kg/main/data';
// ================= CONSTRAINTS =================
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Law)     REQUIRE n.LAW_ID     IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Decree)  REQUIRE n.DECREE_ID  IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Article) REQUIRE n.ARTICLE_ID IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Clause)  REQUIRE n.CLAUSE_ID  IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Lawyer)  REQUIRE n.LAWYER_ID  IS UNIQUE;

// ================= LOAD NODES =================

// 1) LAW  
LOAD CSV WITH HEADERS FROM $baseUrl + '/LAW.csv' AS row
WITH row, trim(row.LAW_ID) AS L_ID
WHERE L_ID IS NOT NULL AND L_ID <> '' AND toUpper(L_ID) <> 'NULL' AND toUpper(L_ID) <> 'NONE'
WITH row, L_ID,
CASE
  WHEN row.EFFECTIVE_DATE IS NULL OR trim(row.EFFECTIVE_DATE) = '' OR toUpper(trim(row.EFFECTIVE_DATE)) IN ['NULL','NONE'] THEN null
  WHEN row.EFFECTIVE_DATE CONTAINS '/' THEN
    date({year: toInteger(split(trim(row.EFFECTIVE_DATE),'/')[2]),
          month: toInteger(split(trim(row.EFFECTIVE_DATE),'/')[1]),
          day: toInteger(split(trim(row.EFFECTIVE_DATE),'/')[0])})
  ELSE date(trim(row.EFFECTIVE_DATE))
END AS effDate,
CASE
  WHEN row.EXPIRY_DATE IS NULL OR trim(row.EXPIRY_DATE) = '' OR toUpper(trim(row.EXPIRY_DATE)) IN ['NULL','NONE'] THEN null
  WHEN row.EXPIRY_DATE CONTAINS '/' THEN
    date({year: toInteger(split(trim(row.EXPIRY_DATE),'/')[2]),
          month: toInteger(split(trim(row.EXPIRY_DATE),'/')[1]),
          day: toInteger(split(trim(row.EXPIRY_DATE),'/')[0])})
  ELSE date(trim(row.EXPIRY_DATE))
END AS expDate
MERGE (l:Law {LAW_ID: L_ID})
SET l.NAME_VN = row.NAME_VN,
    l.NAME_EN = row.NAME_EN,
    l.NAME_JP = row.NAME_JP,
    l.EFFECTIVE_DATE = effDate,
    l.EXPIRY_DATE    = expDate,
    l.STATUS_VN = row.STATUS_VN,
    l.STATUS_EN = row.STATUS_EN,
    l.STATUS_JP = row.STATUS_JP,
    l.LINK      = row.LINK;

// 2) DECREE 
LOAD CSV WITH HEADERS FROM $baseUrl + '/DECREE.csv' AS row
WITH row, trim(row.DECREE_ID) AS D_ID
WHERE D_ID IS NOT NULL AND D_ID <> '' AND toUpper(D_ID) <> 'NULL' AND toUpper(D_ID) <> 'NONE'
WITH row, D_ID,
CASE
  WHEN row.EFFECTIVE_DATE IS NULL OR trim(row.EFFECTIVE_DATE) = '' OR toUpper(trim(row.EFFECTIVE_DATE)) IN ['NULL','NONE'] THEN null
  WHEN row.EFFECTIVE_DATE CONTAINS '/' THEN
    date({year: toInteger(split(trim(row.EFFECTIVE_DATE),'/')[2]),
          month: toInteger(split(trim(row.EFFECTIVE_DATE),'/')[1]),
          day: toInteger(split(trim(row.EFFECTIVE_DATE),'/')[0])})
  ELSE date(trim(row.EFFECTIVE_DATE))
END AS effDate,
CASE
  WHEN row.EXPIRY_DATE IS NULL OR trim(row.EXPIRY_DATE) = '' OR toUpper(trim(row.EXPIRY_DATE)) IN ['NULL','NONE'] THEN null
  WHEN row.EXPIRY_DATE CONTAINS '/' THEN
    date({year: toInteger(split(trim(row.EXPIRY_DATE),'/')[2]),
          month: toInteger(split(trim(row.EXPIRY_DATE),'/')[1]),
          day: toInteger(split(trim(row.EXPIRY_DATE),'/')[0])})
  ELSE date(trim(row.EXPIRY_DATE))
END AS expDate
MERGE (d:Decree {DECREE_ID: D_ID})
SET d.NAME_VN = row.NAME_VN,
    d.NAME_EN = row.NAME_EN,
    d.NAME_JP = row.NAME_JP,
    d.EFFECTIVE_DATE = effDate,
    d.EXPIRY_DATE    = expDate,
    d.STATUS_VN = row.STATUS_VN,
    d.STATUS_EN = row.STATUS_EN,
    d.STATUS_JP = row.STATUS_JP,
    d.LINK      = row.LINK;

// 3) ARTICLE 
LOAD CSV WITH HEADERS FROM $baseUrl + '/ARTICLE.csv' AS row
WITH row, trim(row.ARTICLE_ID) AS A_ID
WHERE A_ID IS NOT NULL AND A_ID <> '' AND toUpper(A_ID) <> 'NULL' AND toUpper(A_ID) <> 'NONE'
MERGE (a:Article {ARTICLE_ID: A_ID})
SET a.NUMBER   = row.NUMBER,
    a.TITLE_VN = row.TITLE_VN,
    a.TITLE_EN = row.TITLE_EN,
    a.TITLE_JP = row.TITLE_JP,
    a.`INTRODUCTORY STATEMENT_VN` = row.`INTRODUCTORY STATEMENT_VN`,
    a.`INTRODUCTORY STATEMENT_EN` = row.`INTRODUCTORY STATEMENT_EN`,
    a.`INTRODUCTORY STATEMENT_JP` = row.`INTRODUCTORY STATEMENT_JP`;

// 4) CLAUSE 
LOAD CSV WITH HEADERS FROM $baseUrl + '/CLAUSE.csv' AS row
WITH row, trim(row.CLAUSE_ID) AS C_ID
WHERE C_ID IS NOT NULL AND C_ID <> '' AND toUpper(C_ID) <> 'NULL' AND toUpper(C_ID) <> 'NONE'
MERGE (c:Clause {CLAUSE_ID: C_ID})
SET c.NUMBER   = row.NUMBER,
    c.TEXT_VN  = row.TEXT_VN,
    c.TEXT_EN  = row.TEXT_EN,
    c.TEXT_JP  = row.TEXT_JP;

// 5) LAWYER 
LOAD CSV WITH HEADERS FROM $baseUrl + '/LAWYER.csv' AS row
WITH row, trim(row.LAWYER_ID) AS P_ID
WHERE P_ID IS NOT NULL AND P_ID <> '' AND toUpper(P_ID) <> 'NULL' AND toUpper(P_ID) <> 'NONE'
MERGE (p:Lawyer {LAWYER_ID: P_ID})
SET p.NAME_VN = row.NAME_VN,
    p.NAME_EN = row.NAME_EN,
    p.NAME_JP = row.NAME_JP,
    p.FIRM_VN = row.FIRM_VN,
    p.FIRM_EN = row.FIRM_EN,
    p.FIRM_JP = row.FIRM_JP,
    p.SPECIALTY_VN = row.SPECIALTY_VN,
    p.SPECIALTY_EN = row.SPECIALTY_EN,
    p.SPECIALTY_JP = row.SPECIALTY_JP,
    p.EMAIL = row.EMAIL,
    p.`TELEPHONE_NUMBER` = row.`TELEPHONE_NUMBER`;

// ================= CHECK COUNTS =================
MATCH (n) RETURN labels(n)[0] AS label, count(*) AS n ORDER BY n DESC;
