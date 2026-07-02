from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "sanitario")

driver = GraphDatabase.driver(URI, auth=AUTH)


def run_query(session, query, parameters=None, description=""):
    """Esegue una query Cypher e stampa i risultati come lista di dict."""
    result = session.run(query, parameters or {})
    records = [dict(record) for record in result]
    print(f"\n--- {description} ({len(records)} risultati) ---")
    for r in records:
        print(r)
    return records


def pazienti_stessa_diagnosi_farmaco_v1(session):
    query = """
    MATCH (d:Diagnosi)<-[:HA_DIAGNOSI]-(v1:Visita)-[PER_PAZIENTE]->(p1:Paziente),
      (d:Diagnosi)<-[:HA_DIAGNOSI]-(v2:Visita)-[:PER_PAZIENTE]->(p2:Paziente),
      (p1)-[:ASSUME]->(f:Farmaco)<-[:ASSUME]-(p2)
WHERE p1 <> p2
RETURN DISTINCT 
       p1.codice AS Paziente1, 
       p2.codice AS Paziente2, 
       d.nome AS Diagnosi, 
       f.nome AS Farmaco
    """
    return run_query(session, query, description="Pazienti stessa diagnosi + farmaco (v1)")


def esami_per_diagnosi_v1(session, diagnosi):
    query = """
   MATCH (d:Diagnosi)<-[:HA_DIAGNOSI]-(v:Visita)-[:HA_ESAME]->(e:Esame)
WHERE d.nome CONTAINS $diagnosi
RETURN e.nome AS Esame, count(e) AS Frequenza
ORDER BY Frequenza DESC
    """
    return run_query(session, query, {"diagnosi": diagnosi},
                      description=f"Esami più frequenti per diagnosi contenente '{diagnosi}' (v1)")


def medici_per_diagnosi_v1(session, diagnosi):
    query = """
    MATCH (m:Medico)-[:ESEGUE]->(v:Visita)-[:HA_DIAGNOSI]->(d:Diagnosi {nome: $diagnosi})
    RETURN DISTINCT m.id_medico AS Medico, d.nome AS Diagnosi
    """
    return run_query(session, query, {"diagnosi": diagnosi},
                      description=f"Medici che hanno seguito pazienti con diagnosi '{diagnosi}' (v1)")


def pazienti_stessa_diagnosi_farmaco_v2(session):
    query = """
    MATCH (p1:Paziente)<-[:PER_PAZIENTE]-(v1:Visita)-[:HA_DIAGNOSI]->(d:Diagnosi)<-[:HA_DIAGNOSI]-(v2:Visita)-[:PER_PAZIENTE]->(p2:Paziente)
    MATCH (v1)-[:PRESCRIVE]->(f:Farmaco)<-[:PRESCRIVE]-(v2)
    WHERE p1 <> p2
    RETURN DISTINCT p1.codice AS Paziente1, p2.codice AS Paziente2,
           d.nome AS Diagnosi, f.nome AS Farmaco
    """
    return run_query(session, query, description="Pazienti stessa diagnosi + farmaco (v2, via Visita)")


def esami_per_diagnosi_v2(session, diagnosi):
    query = """
    MATCH (v:Visita)-[:HA_DIAGNOSI]->(d:Diagnosi {nome: $diagnosi})
    MATCH (v)-[:HA_ESAME]->(e:Esame)
    RETURN e.nome AS Esame, count(e) AS Frequenza
    ORDER BY Frequenza DESC
    """
    return run_query(session, query, {"diagnosi": diagnosi},
                      description=f"Esami più frequenti per diagnosi '{diagnosi}' (v2, via Visita)")


def medici_per_diagnosi_v2(session, diagnosi):
    query = """
    MATCH (m:Medico)-[:ESEGUE]->(v:Visita)-[:HA_DIAGNOSI]->(d:Diagnosi {nome: $diagnosi})
    MATCH (v)-[:PER_PAZIENTE]->(p:Paziente)
    RETURN DISTINCT m.id_medico AS Medico, p.codice AS Paziente, d.nome AS Diagnosi
    """
    return run_query(session, query, {"diagnosi": diagnosi},
                      description=f"Medici e pazienti con diagnosi '{diagnosi}' (v2, con paziente)")


def main():
    diagnosi_target = "Gastrite erosiva"

    with driver.session(database="neo4j") as session:
        pazienti_stessa_diagnosi_farmaco_v1(session)
        esami_per_diagnosi_v1(session, diagnosi_target)
        medici_per_diagnosi_v1(session, diagnosi_target)
        pazienti_stessa_diagnosi_farmaco_v2(session)
        esami_per_diagnosi_v2(session, diagnosi_target)
        medici_per_diagnosi_v2(session, diagnosi_target)


if __name__ == "__main__":
    try:
        main()
    finally:
        driver.close()
