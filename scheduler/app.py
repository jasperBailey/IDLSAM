import json
from models.tournamentscheduler import *

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    scheduleData = json.loads(event["body"])["teamsAvailabilities"]
    scheduler = TournamentScheduler(scheduleData)
    schedule = scheduler.calcBestSchedule()
    print(schedule)
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": schedule,
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
