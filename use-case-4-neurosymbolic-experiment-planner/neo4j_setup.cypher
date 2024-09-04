CREATE CONSTRAINT experiment_rule_name IF NOT EXISTS FOR (r:ExperimentRule) REQUIRE r.name IS UNIQUE;
CREATE CONSTRAINT experiment_id IF NOT EXISTS FOR (e:Experiment) REQUIRE e.id IS UNIQUE;

CREATE (r1:ExperimentRule {
    name: 'Clear Objective', 
    description: 'The experiment should have a clear and specific objective.',
    weight: 1.0,
    evaluationLogic: '{"type": "length", "field": "objective", "target": 20}'
})
CREATE (r2:ExperimentRule {
    name: 'Reproducible Steps', 
    description: 'The procedure should be detailed enough to be reproducible.',
    weight: 1.0,
    evaluationLogic: '{"type": "length", "field": "procedure", "target": 5}'
})
CREATE (r3:ExperimentRule {
    name: 'Appropriate Equipment', 
    description: 'The equipment setup should be appropriate for the experiment.',
    weight: 0.8,
    evaluationLogic: '{"type": "length", "field": "equipment_setup", "target": 30}'
})
CREATE (r4:ExperimentRule {
    name: 'Observable Outcomes', 
    description: 'The experiment should have clear, observable outcomes.',
    weight: 1.0,
    evaluationLogic: '{"type": "length", "field": "observations", "target": 25}'
})
CREATE (r5:ExperimentRule {
    name: 'Safety Considerations', 
    description: 'The experiment should include necessary safety precautions.',
    weight: 1.2,
    evaluationLogic: '{"type": "keyword_count", "field": "procedure", "keyword": "safety", "multiplier": 0.2}'
})