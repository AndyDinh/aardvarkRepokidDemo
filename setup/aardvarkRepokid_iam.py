import json
import uuid
import boto3
import logging

from pprint import pprint as pp

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# setting up unique ID number
generateId = str(uuid.uuid4())
RANDOMID = (generateId.split('-')[:1])
IAM = boto3.client('iam')


def create_aardvark_policy():
    """ Document policy created for Aardvark """
    aardvarkPolicy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "IAM Policy Access for Aardvark",
                "Effect": "Allow",
                "Action": [
                    "iam:GenerateServiceLastAccessedDetails",
                    "iam:GetServiceLastAccessedDetails",
                    "iam:ListRolePolicies",
                    "iam:ListRoles",
                    "iam:ListUsers",
                    "iam:ListPolicies",
                    "iam:ListGroups"
                ],
                "Resource": "*"
            }
        ]
    }

    policyName = f"AardvarkPolicy-{RANDOMID}"
    generateAardvarkPolicies = IAM.create_policy(
        PolicyName= policyName,
        PolicyDocument=f"{aardvarkPolicy}"
        Description="Aardvark Policy created for Demo"
    )
    print(generateAardvarkPolicies)
    aardvarkPolicyArn = generateAardvarkPolicies['Policy']['Arn']
    return aardvarkPolicyArn


def create_repokid_policy():
    """ Document policy created for Repokid """
    repokidPolicy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "IAM Policy Access for ",
                "Effect": "Allow",
                "Action": [
                    "iam:DeleteInstanceProfile",
                    "iam:GetRole",
                    "iam:GetInstanceProfile",
                    "iam:PassRole",
                    "iam:UpdateRoleDescription",
                    "iam:DeleteRole",
                    "iam:PutRolePolicy",
                    "iam:ListInstanceProfiles",
                    "iam:ListInstanceProfilesForRole",
                    "sts:AssumeRole",
                    "iam:DeleteRolePolicy",
                    "iam:ListRolePolicies",
                    "iam:GetAccountAuthorizationDetails",
                    "iam:GetRolePolicy",
                    "dynamodb:ListTables"
                ],
                "Resource": "*"
            }
        ]
    }

    policyName = f"RepokidPolicy-{RANDOMID}"
    generateRepokidPolicies = IAM.create_policy(
        PolicyName=policyName,
        PolicyDocument=f"{aardvarkPolicy}"
        Description="Repokid Policy created for Demo"
    )
    print(generateRepokidPolicies)
    repokidArn = generateRepokidPolicies['Policy']['Arn']
    return repokidPolicyArn


def create_aardvark_role(AWSACCOUNT, AWSUSER, policyArn):
    """ 
    Role created for Aardvark
    Document Role to Assume created for Aardvark 
    """
    aardvarkAssumeRole = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        f"arn:aws:iam::{AWSACCOUNT}:user/{AWSUSER}"
                    ]
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    role = f'AardvarkRole-{RANDOMID}'
    generateAardvarkRole = IAM.create_role(
        RoleName = role,
        AssumeRolePolicyDocument = f"{aardvarkAssumeRole}",
        Description = "Role Created for Aardvark to Assume"
    )
    assumeRole = IAM.attach_role_policy(
        RoleName = role,
        PolicyArn = policyArn
    )
    print(f"Role Created:\n{generateAardvarkRole}")
    print(f"Role Assumed:\n{assumeRole}")


def create_repokid_role(AWSACCOUNT, AWSUSER, policyArn):
    """ 
    Role created for Repokid
    Document Role to Assume created for Repokid 
    """
    repokidAssumeRole = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        f"arn:aws:iam::{AWSACCOUNT}:user/{AWSUSER}"
                    ]
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    role = f'RepokidRole-{RANDOMID}'
    generateRepokidRole = IAM.create_role(
        RoleName = role,
        AssumeRolePolicyDocument = f"{repokidAssumeRole}",
        Description = "Role Created for Aardvark to Assume"
    )
    assumeRole = IAM.attach_role_policy(
        RoleName = role,
        PolicyArn = policyArn
    )
    print(f"Role Created:\n{generateRepokidRole}")
    print(f"Role Assumed:\n{assumeRole}")
    repokidRoleName = generateRepokidRole['Role']['RoleName']
    print(repokidRoleName)
    # return repokidRoleName


# def custom_config_for_repokid(AWSACCOUNT, repokidRole)
#     custom_configs = {
#         "aardvark_api_location": "http://localhost:5000/api/1/advisors", 
#         "active_filters": [ 
#             "repokid.filters.optout:OptOutFilter"
#         ], 
#         "connection_iam": {
#             "assume_role": repokidRole, 
#             "region": "us-east-1", 
#             "session_name": "repokid"
#         }, 
#         "dispatcher": {
#             "from_rr_sns": "RESPONSES_FROM_REPOKID_SNS_ARN", 
#             "region": "us-east-1", 
#             "session_name": "repokid", 
#             "to_rr_queue": "COMMAND_QUEUE_TO_REPOKID_URL"
#         }, 
#         "dynamo_db": {
#             "account_number": AWSACCOUNT, 
#             "assume_role": repokidRole, 
#             "endpoint": "http://localhost:8010", 
#             "region": "us-east-1", 
#             "session_name": "repokid"
#         }, 
#         "filter_config": {
#             "AgeFilter": {
#                 "minimum_age": 15
#             },
#         "hooks": [
#             "repokid.hooks.loggers"
#         ], 
#         "logging": {
#             "disable_existing_loggers": "False", 
#             "formatters": {
#                 "standard": {
#                     "format": "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
#                 }
#             }, 
#             "handlers": {
#                 "console": {
#                     "class": "logging.StreamHandler", 
#                     "formatter": "standard", 
#                     "level": "INFO", 
#                     "stream": "ext://sys.stdout"
#                 }, 
#                 "file": {
#                     "backupCount": 100, 
#                     "class": "logging.handlers.RotatingFileHandler", 
#                     "encoding": "utf8", 
#                     "filename": "repokid.log", 
#                     "formatter": "standard", 
#                     "level": "INFO", 
#                     "maxBytes": 10485760
#                 }
#             }, 
#             "loggers": {
#                 "repokid": {
#                     "handlers": [
#                         "file", 
#                         "console"
#                     ], 
#                     "level": "INFO"
#                 }
#             }, 
#             "version": 1
#         }, 
#         "opt_out_period_days": 90, 
#         "repo_requirements": {
#             "exclude_new_permissions_for_days": 14, 
#             "oldest_aa_data_days": 5
#         }, 
#         "repo_schedule_period_days": 7, 
#         "warnings": {
#             "unknown_permissions": false
#         }
#     }
    
    


if __name__ == "__main__":
    AWSACCOUNT = input("Provide an AWS Account to proceed: ")
    AWSUSER = input("Provde an AWS User to use: ")
    print("NOTE:\n\t IF INCORRECT DATA IS PROVIDED, MANUAL CHANGES MAY NEED TO BE APPLIED...")

    aardvarkPolicyArn = create_aardvark_policy()
    repokidPolicyArn = create_repokid_policy()

    create_aardvark_role(AWSACCOUNT, AWSUSER, aardvarkPolicyArn)
    create_repokid_role(AWSACCOUNT, AWSUSER, repokidPolicyArn)


    
