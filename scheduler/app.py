import json
from models.tournamentscheduler import *

headers = (
    {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
    },
)


def lambda_handler(event, context):
    try:
        if event["body"]:
            scheduleData = json.loads(event["body"])["teamsAvailabilities"]
        else:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Request body is empty"}),
            }
    except json.JSONDecodeError as e:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"message": f"Error decoding JSON: {str(e)}"}),
        }
    except KeyError as e:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps(
                {"message": f"Missing key 'teamsAvailabilities' in JSON: {str(e)}"}
            ),
        }

    if len(scheduleData) > 8:
        return {
            "statusCode": 413,
            "headers": headers,
            "body": json.dumps(
                {
                    "message": f"AWS hosted scheduler can't take more than 8 teams (costs too much compute time!)"
                }
            ),
        }

    try:
        scheduler = TournamentScheduler(scheduleData)
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps(
                {"message": f"Error creating TournamentScheduler: {str(e)}"}
            ),
        }
    try:
        scheduler.gatherAllSubSols()
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": f"Error gathering subchedules: {str(e)}"}),
        }

    try:
        schedule = scheduler.calcBestSchedule()
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"message": f"Error calculating schedule: {str(e)}"}),
        }

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(
            {"message": "Schedule calculated successfully.", "rawSchedule": schedule}
        ),
    }
