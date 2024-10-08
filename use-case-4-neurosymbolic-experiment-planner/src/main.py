import os
from dotenv import load_dotenv
from database import Neo4jDatabase
from evaluator import ExperimentEvaluator
from llm_interface import generate_experiment, llm_self_reflection
from html_generator import generate_html_report
import json

load_dotenv()

def write_json_report(variants, best_experiments):
    report_data = {
        "variants": variants,
        "best_experiments": best_experiments
    }
    
    with open('experiment_report.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print("JSON report generated: experiment_report.json")

def main():
    db = Neo4jDatabase(os.getenv('NEO4J_URI'), os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
    rules = db.get_experiment_rules()
    evaluator = ExperimentEvaluator(rules)

    scientist_input = input("Enter your experiment description: ")

    variants = []
    for i in range(5):
        best_experiments = db.get_best_experiments(5)
        rule_guidance = evaluator.generate_rule_guidance(best_experiments)
        
        variant = generate_experiment(scientist_input, rule_guidance)
        if variant is None:
            print(f"Failed to generate experiment variant {i+1}")
            continue
        
        evaluation = evaluator.evaluate_experiment(variant)
        reflection = llm_self_reflection(variant, evaluation)
        
        if reflection is None:
            print(f"Failed to generate reflection for variant {i+1}")
            reflection = {"error": "Failed to generate reflection"}
        
        db.store_experiment(variant, evaluation, reflection)

        variants.append({
            "content": variant,
            "evaluation": evaluation,
            "reflection": reflection
        })

        print(f"\nVariant {i+1}:")
        print(json.dumps(variant, indent=2))
        print("\nEvaluation:")
        print(json.dumps(evaluation, indent=2))
        print("\nReflection:")
        print(json.dumps(reflection, indent=2))

    best_experiments = db.get_best_experiments(3)
    
    print("\nBest Experiments:")
    for i, exp in enumerate(best_experiments, 1):
        print(f"\nRank {i} (Score: {exp['score']:.2f}):")
        print(json.dumps(exp['content'], indent=2))
        print("Reflection:")
        print(json.dumps(exp['reflection'], indent=2))

    # Generate HTML report
    generate_html_report(variants, best_experiments)

    # Generate JSON report
    write_json_report(variants, best_experiments)

    db.close()

if __name__ == "__main__":
    main()