from jinja2 import Environment, FileSystemLoader
import os
import json

def generate_html_report(variants, best_experiments):
    # Create a Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report_template.html')

    # Render the template with our data
    html_content = template.render(variants=variants, best_experiments=best_experiments)

    # Write the rendered HTML to a file
    with open('experiment_report.html', 'w') as f:
        f.write(html_content)

    print("HTML report generated: experiment_report.html")