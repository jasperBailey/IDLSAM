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

    try:
        scheduler = TournamentScheduler(scheduleData)
    except e:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"message": f"Error creating TournamentScheduler: {str(e)}"}
            ),
        }
    try:
        schedule = scheduler.calcBestSchedule()
    except e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": f"Error calculating schedule: {str(e)}"}),
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
        },
        "body": json.dumps(
            {"message": "Schedule calculated successfully.", "rawSchedule": schedule}
        ),
    }
