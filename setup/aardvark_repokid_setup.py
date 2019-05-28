import os
import json
import uuid
import boto3
import logging

from pprint import pprint as pp

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# setting up unique ID number
generateId = str(uuid.uuid4())
RANDOMID = str((generateId.split('-')[:1])).replace('[', '').replace(']','').replace("'",'').replace("'",'')
IAM = boto3.client('iam')


def create_aardvark_policy():
    """ Document policy created for Aardvark """
    aardvarkPolicy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
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
    
    aardvarkPolicy = json.dumps(aardvarkPolicy)
    policyName = f"AardvarkPolicy{RANDOMID}"
    generateAardvarkPolicies = IAM.create_policy(
        PolicyName = policyName,
        PolicyDocument = aardvarkPolicy,
        Description = "Aardvark Policy created for Demo"
    )
    
    pp(generateAardvarkPolicies)
    aardvarkPolicyArn = generateAardvarkPolicies['Policy']['Arn']
    return aardvarkPolicyArn


def create_repokid_policy():
    """ Document policy created for Repokid """
    repokidPolicy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "iam:DeleteInstanceProfile",
                    "iam:GetRole",
                    "iam:GetInstanceProfile",
                    "iam:PassRole",
                    "dynamodb:ListTables",
                    "iam:UpdateRoleDescription",
                    "iam:DeleteRole",
                    "iam:PutRolePolicy",
                    "iam:ListInstanceProfiles",
                    "iam:ListInstanceProfilesForRole",
                    "sts:AssumeRole",
                    "iam:DeleteRolePolicy",
                    "iam:ListRolePolicies",
                    "iam:GetAccountAuthorizationDetails",
                    "iam:GetRolePolicy"
                ],
                "Resource": "*"
            }
        ]
    }
    
    repokidPolicy = json.dumps(repokidPolicy)
    policyName = f"RepokidPolicy{RANDOMID}"
    generateRepokidPolicies = IAM.create_policy(
        PolicyName = policyName,
        PolicyDocument = repokidPolicy,
        Description = "Repokid Policy created for Demo"
    )
    
    pp(generateRepokidPolicies)
    repokidPolicyArn = generateRepokidPolicies['Policy']['Arn']
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
            "AWS": f"arn:aws:iam::{AWSACCOUNT}:user/{AWSUSER}"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    
    aardvarkAssumeRole = json.dumps(aardvarkAssumeRole)
    role = f'AardvarkRole{RANDOMID}'
    generateAardvarkRole = IAM.create_role(
        RoleName = role,
        AssumeRolePolicyDocument = aardvarkAssumeRole,
        Description = "Role Created for Aardvark to Assume"
    )
    attachPolicy = IAM.attach_role_policy(
        RoleName = role,
        PolicyArn = policyArn
    )
    print(f"Role Created:\n{pp(generateAardvarkRole)}")
    print(f"Role Assumed:\n{pp(attachPolicy)}")


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
            "AWS": f"arn:aws:iam::{AWSACCOUNT}:user/{AWSUSER}"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    repokidAssumeRole = json.dumps(repokidAssumeRole)
    
    role = f'RepokidRole{RANDOMID}'
    generateRepokidRole = IAM.create_role(
        RoleName = role,
        AssumeRolePolicyDocument = repokidAssumeRole,
        Description = "Role Created for Repokid to Assume"
    )
    attachPolicy = IAM.attach_role_policy(
        RoleName = role,
        PolicyArn = policyArn
    )
    print(f"Role Created:\n{pp(generateRepokidRole)}")
    print(f"Role Assumed:\n{pp(attachPolicy)}")
    
    repokidRoleName = generateRepokidRole['Role']['RoleName']
    print(repokidRoleName)
    return repokidRoleName


def custom_repokid_configs(AWSACCOUNT, repokidRole):
    custom_configs = {
        "aardvark_api_location": "http://localhost:5000/api/1/advisors",
        "active_filters": [
            "repokid.filters.optout:OptOutFilter"
        ],
        "connection_iam": {
            "assume_role": f"{repokidRole}",
            "region": "us-east-1",
            "session_name": "repokid"
        },
        "dispatcher": {
            "from_rr_sns": "RESPONSES_FROM_REPOKID_SNS_ARN",
            "region": "us-east-1",
            "session_name": "repokid",
            "to_rr_queue": "COMMAND_QUEUE_TO_REPOKID_URL"
        },
        "dynamo_db": {
            "account_number": f"{AWSACCOUNT}",
            "assume_role": f"{repokidRole}",
            "endpoint": "http://localhost:8010",
            "region": "us-east-1",
            "session_name": "repokid"
        },
        "filter_config": {
            "AgeFilter": {
                "minimum_age": 15
            },
            "hooks": [
                "repokid.hooks.loggers"
            ],
            "logging": {
                "disable_existing_loggers": "False",
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                    }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "formatter": "standard",
                        "level": "INFO",
                        "stream": "ext://sys.stdout"
                    },
                    "file": {
                        "backupCount": 100,
                        "class": "logging.handlers.RotatingFileHandler",
                        "encoding": "utf8",
                        "filename": "repokid.log",
                        "formatter": "standard",
                        "level": "INFO",
                        "maxBytes": 10485760
                    }
                },
                "loggers": {
                    "repokid": {
                        "handlers": [
                            "file",
                            "console"
                        ],
                        "level": "INFO"
                    }
                },
                "version": 1
            },
            "opt_out_period_days": 90,
            "repo_requirements": {
                "exclude_new_permissions_for_days": 14,
                "oldest_aa_data_days": 5
            },
            "repo_schedule_period_days": 7,
            "warnings": {
                "unknown_permissions": False
            }
        }
    }
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(f"{current_dir}/custom_configs2.json", "w") as file:
        json.dump(custom_configs, file, indent=2, sort_keys=True)
    pp(custom_configs)



if __name__ == "__main__":
    AWSACCOUNT = input("Provide an AWS Account to proceed: ")
    AWSUSER = input("Provde an AWS User to use: ")
    print("NOTE:\n\t IF INCORRECT DATA IS PROVIDED, MANUAL CHANGES MAY NEED TO BE APPLIED...")
    
    print(RANDOMID)
    aardvarkPolicyArn = create_aardvark_policy()
    repokidPolicyArn = create_repokid_policy()

    create_aardvark_role(AWSACCOUNT, AWSUSER, aardvarkPolicyArn)
    repokidRoleName = create_repokid_role(AWSACCOUNT, AWSUSER, repokidPolicyArn)

    custom_repokid_configs(AWSACCOUNT, repokidRoleName)