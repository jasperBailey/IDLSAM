import json
from jinja2 import Environment, FileSystemLoader

headers = {
    "Content-Type": "text/html",
    "Access-Control-Allow-Origin": "*",
}

env = Environment(loader=FileSystemLoader("templates"))


def lambda_handler(event, context):
    template = env.get_template("landing.html")
    html = template.render(title="Welcome!", message="Hello from Lambda!")
    return {
        "statusCode": 200,
        "headers": headers,
        "body": html,
    }
