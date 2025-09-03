from ..db import driver

def recommend_lawyers(question: str, lang: str):
    # Tạm match tất cả lawyer, lọc theo IP Law specialty
    field_name = {
        "vi": "NAME_VN",
        "en": "NAME_EN",
        "jp": "NAME_JP"
    }.get(lang.lower(), "NAME_EN")

    field_firm = {
        "vi": "FIRM_VN",
        "en": "FIRM_EN",
        "jp": "FIRM_JP"
    }.get(lang.lower(), "FIRM_EN")

    field_spec = {
        "vi": "SPECIALTY_VN",
        "en": "SPECIALTY_EN",
        "jp": "SPECIALTY_JP"
    }.get(lang.lower(), "SPECIALTY_EN")

    with driver.session() as session:
        cypher = f"""
        MATCH (l:Lawyer)
        WHERE toLower(l.{field_spec}) CONTAINS 'ip law'
        RETURN l.LAWYER_ID as LAWYER_ID,
               l.{field_name} as NAME,
               l.{field_firm} as FIRM,
               l.{field_spec} as SPECIALTY,
               l.EMAIL as CONTACT,
               rand() as SCORE
        ORDER BY SCORE DESC
        LIMIT 3
        """
        result = session.run(cypher)
        lawyers = [dict(r) for r in result]
    return lawyers
