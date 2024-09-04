from typing import List, Dict
import json

class ExperimentEvaluator:
    def __init__(self, rules: List[Dict]):
        self.rules = rules

    def evaluate_experiment(self, experiment: Dict) -> Dict:
        evaluation = {}
        for rule in self.rules:
            eval_logic = json.loads(rule['evaluationLogic'])
            if eval_logic['type'] == 'length':
                value = len(experiment[eval_logic['field']])
                score = min(1.0, value / eval_logic['target'])
            elif eval_logic['type'] == 'keyword_count':
                value = sum(eval_logic['keyword'] in step.lower() for step in experiment[eval_logic['field']])
                score = min(1.0, value * eval_logic['multiplier'])
            else:
                score = 0  # Default score if evaluation logic is not recognized
            evaluation[rule['name']] = score * rule['weight']
        return evaluation

    def generate_rule_guidance(self, previous_experiments: List[Dict]) -> str:
        if not previous_experiments:
            return "Focus on all aspects of a good experiment."

        avg_scores = {}
        for rule in self.rules:
            rule_scores = []
            for exp in previous_experiments:
                if isinstance(exp, str):
                    exp = json.loads(exp)
                if 'evaluation' in exp:
                    rule_scores.append(exp['evaluation'].get(rule['name'], 0))
                elif 'content' in exp and isinstance(exp['content'], str):
                    content = json.loads(exp['content'])
                    if 'evaluation' in content:
                        rule_scores.append(content['evaluation'].get(rule['name'], 0))
                # If we can't find the evaluation, we'll assume a score of 0
                else:
                    rule_scores.append(0)
            
            if rule_scores:
                avg_scores[rule['name']] = sum(rule_scores) / len(rule_scores)
            else:
                avg_scores[rule['name']] = 0

        weakest_rules = sorted(avg_scores.items(), key=lambda x: x[1])[:2]
        return f"Improve on {weakest_rules[0][0]} and {weakest_rules[1][0]}."
