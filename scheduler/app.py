import json
from models.tournamentscheduler import *

# import requests


# def lambda_handler(event, context):
#     """
#     Parameters
#     ----------
#     event: dict, required
#         API Gateway Lambda Proxy Input Format

#         Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

#     context: object, required
#         Lambda Context runtime methods and attributes

#         Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

#     Returns
#     ------
#     API Gateway Lambda Proxy Output Format: dict

#         Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
#     """
#     try:
#         # Check if the request body exists
#         if event["body"]:
#             scheduleData = json.loads(event["body"])["teamsAvailabilities"]
#             # Proceed with the rest of your code using scheduleData
#         else:
#             # Handle the case where the request body is empty
#             return {
#                 "statusCode": 400,
#                 "body": json.dumps({"message": "Request body is empty"}),
#             }
#     except json.JSONDecodeError as e:
#         # Handle JSON decoding errors
#         return {
#             "statusCode": 400,
#             "body": json.dumps({"message": f"Error decoding JSON: {str(e)}"}),
#         }
#     except KeyError as e:
#         # Handle missing key error (teamsAvailabilities)
#         return {
#             "statusCode": 400,
#             "body": json.dumps(
#                 {"message": f"Missing key 'teamsAvailabilities' in JSON: {str(e)}"}
#             ),
#         }

#     scheduler = TournamentScheduler(scheduleData)
#     schedule = scheduler.calcBestSchedule()
#     print(schedule)
#     return {
#         "statusCode": 200,
#         "body": json.dumps(
#             {
#                 "message": schedule,
#                 # "location": ip.text.replace("\n", "")
#             }
#         ),
#     }


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Received payload", "payload": event}),
    }
