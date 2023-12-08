import json
from models.tournamentscheduler import *

# import requests


def lambda_handler(event, context):
    try:
        # Check if the request body exists
        if event["body"]:
            scheduleData = json.loads(event["body"])["teamsAvailabilities"]
            # Proceed with the rest of your code using scheduleData
        else:
            # Handle the case where the request body is empty
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Request body is empty"}),
            }
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        return {
            "statusCode": 400,
            "body": json.dumps({"message": f"Error decoding JSON: {str(e)}"}),
        }
    except KeyError as e:
        # Handle missing key error (teamsAvailabilities)
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"message": f"Missing key 'teamsAvailabilities' in JSON: {str(e)}"}
            ),
        }

    scheduler = TournamentScheduler(scheduleData)
    schedule = scheduler.calcBestSchedule()
    print(schedule)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Received payload", "payload": schedule}),
    }
