from neo4j import GraphDatabase
import json
from typing import List, Dict
import uuid

class Neo4jDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_experiment_rules(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_experiment_rules)

    @staticmethod
    def _get_experiment_rules(tx):
        query = """
        MATCH (r:ExperimentRule)
        RETURN r.name as name, r.description as description, r.weight as weight,
               r.evaluationLogic as evaluationLogic
        """
        return [dict(record) for record in tx.run(query)]

    def store_experiment(self, experiment: Dict, evaluation: Dict, reflection: Dict):
        with self.driver.session() as session:
            session.write_transaction(self._store_experiment, experiment, evaluation, reflection)

    @staticmethod
    def _store_experiment(tx, experiment, evaluation, reflection):
        exp_id = str(uuid.uuid4())
        query = """
        CREATE (e:Experiment {id: $exp_id, content: $content, reflection: $reflection})
        WITH e
        UNWIND $evaluation as eval
        MATCH (r:ExperimentRule {name: eval.rule})
        CREATE (e)-[s:SATISFIES {score: eval.score}]->(r)
        """
        tx.run(query, exp_id=exp_id, content=json.dumps(experiment), 
               evaluation=[{"rule": k, "score": v} for k, v in evaluation.items()],
               reflection=json.dumps(reflection))

    def get_best_experiments(self, limit=5):
        with self.driver.session() as session:
            return session.read_transaction(self._get_best_experiments, limit)

    @staticmethod
    def _get_best_experiments(tx, limit):
        query = """
        MATCH (e:Experiment)-[s:SATISFIES]->(r:ExperimentRule)
        WITH e, sum(s.score * r.weight) as total_score
        ORDER BY total_score DESC
        LIMIT $limit
        RETURN e.content as content, e.reflection as reflection, total_score
        """
        return [{"content": json.loads(record["content"]), 
                 "reflection": json.loads(record["reflection"]), 
                 "score": record["total_score"]} 
                for record in tx.run(query, limit=limit)]

__all__ = ['Neo4jDatabase']