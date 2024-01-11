import json
from subscheduler import SubScheduler

# import requests


def lambda_handler(event, context):
    try:
        if event["body"]:
            subscheduleData = json.loads(event["body"])
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Request body is empty"}),
            }
    except json.JSONDecodeError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": f"Error decoding JSON: {str(e)}"}),
        }

    if len(subscheduleData["pairingScores"]) > 8:
        return {
            "statusCode": 413,
            "body": json.dumps(
                {
                    "message": f"AWS hosted scheduler can't take more than 8 teams (costs too much compute time!)"
                }
            ),
        }
    try:
        subscheduler = SubScheduler(
            subscheduleData["oneFactorisation"],
            subscheduleData["pairingScores"],
            subscheduleData["bye"],
        )
    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": f"Missing key in JSON: {str(e)}"}),
        }
    except e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error creating subscheduler: {str(e)}"}),
        }

    try:
        subschedule = subscheduler.calcBestSchedule()
    except e:
        return {
            "statusCode": 500,
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
            {"message": "Schedule calculated successfully.", "subschedule": subschedule}
        ),
    }
