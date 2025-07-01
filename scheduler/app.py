import json
from helpers.main import main

headers = {
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST",
}


def lambda_handler(event, context):
    try:
        if event["body"]:
            scheduleData = json.loads(event["body"])["teamsAvailabilities"]
            print(scheduleData)
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

    # scheduleData is expected to be a list of CSV lines (strings)
    schedule, badness, human_output = main(csv_lines=scheduleData)

    print(schedule)

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(
            {
                "message": "Schedule calculated successfully.",
                "rawSchedule": schedule,
                "badness": badness,
                "humanOutput": human_output,
            }
        ),
    }
