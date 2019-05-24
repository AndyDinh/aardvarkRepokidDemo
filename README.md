# Install Aardvark & Repokid

Instructions provided to install Aardvark and Repokid

<span style="color:blue;">"**[Aardvark](https://github.com/Netflix-Skunkworks/aardvark)** is a multi-account AWS IAM Access Advisor API (and caching layer)"</span>

<span style="color:blue;">"**[Repokid](https://github.com/Netflix/repokid)** uses Access Advisor provided by Aardvark to remove permissions granting access to unused services from the inline policies of IAM roles in an AWS account."</span>


## Setup Requirements

**Known Dependencies**:

- Aardvark
  - `libpq-dev`

<br>

**To set up Aardvark & Repokid, you will need to**:

1. Move to the new dir (`aardvark_repokid_demo`) and activate the provided virtual environment
  - `source aardvark_repokid_env/bin/activate`
2. Set up a localized DynamoDB database
3. Set up a local postgreSQL database for the Aardvark services (utilizes Swagger)
4. Set up a Repokid environment

<br>

### [Localized DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html)

This will store your AWS environment data that **Repokid** uses locally -- _provided by Aardvark_

To set this up:
- Move to the local dynamodb folder (update the path to your location)
  - `java -Djava.library.path=/SET/YOUR/PATH/HERE/DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -inMemory -port 8010`
- Leave this running. You have a localized dynamodb now.
  - To validate this, `aws dynamodb list-tables --endpoint-url http://localhost:8010`

<br>

---

### [Aardvark](https://github.com/Netflix-Skunkworks/aardvark)

<span style="color:red;">**NOTE:**</span> You will need to add your IAM user into the **Trusted entities** section of the **"ArdvarkInstanceProfile" role** prior to setting up Aardvark

- Open a new terminal
  - In VSCode, `Ctrl+\` to split terminal
- Run `source aardvark_repokid_env/bin/activate` in `aardvark_repokid_demo` dir, if not already running
- Move to the Aardvark dir
  - ` cd **/aardvark_repokid_demo/aardvark_repokid/aardvark`
- Run the following to set up aardvark:
  1. `python setup.py develop`
  2. `aardvark config` -- provide the correct inputs for each prompt for the setup (`config.py`)
  3. `aardvark create_db` -- creates a local database file 
  4. `aardvark update -a [YOUR AWS ACCOUNT]`
  5. `aardvark start_api -b 0.0.0.0:5000` -- This will run the local postgreSQL DB
- You should now be able to access this localized (postgreSQL) db with your AWS account access advisor data
  - **This will need to be updated upon ANY changes in your AWS account to keep your Repokid environment up-to-date**
- Like the local DynamoDB, keep this database running

<br>

#### Various Options and Views

To see a JSON view of your environments:

- `http://localhost:5000/api/1/advisors`

To get the Swagger-based front-end:

- `http://localhost:5000/apidocs/#!`

"Aardvark responds to get/post requests. 
All results are paginated and pagination can be controlled by passing `count` and/or `page` arguments. 
Here are a few example queries:"

- `curl localhost:5000/api/1/advisors`
- `curl localhost:5000/api/1/advisors?phrase=SecurityMonkey`
- `curl localhost:5000/api/1/advisors?arn=arn:aws:iam::000000000000:role/SecurityMonkey&arn=arn:aws:iam::111111111111:role/SecurityMonkey`
- `curl localhost:5000/api/1/advisors?regex=^.*Monkey$`

<br>

#### Current Aardvark Request Options

```
$ aardvark shell               Runs a Python shell inside Flask application context.

$ aardvark update              Asks AWS for new Access Advisor information.

$ aardvark runserver           Runs the Flask development server i.e. app.run()

$ aardvark drop_db             Drops the database.

$ aardvark create_db           Creates the database.

$ aardvark start_api            This is the main GunicornServer server, it runs the
                                flask app with gunicorn and uses any configuration
                                options passed to it. You can pass all standard
                                gunicorn flags to this command as if you were running
                                gunicorn itself. For example: aardvark start_api -w 4
                                -b 127.0.0.0:8002 Will start gunicorn with 4 workers
                                bound to 127.0.0.0:8002

$ aardvark config               Creates a config.py configuration file from user input
                                or default values. If all configurable values are
                                specified by parameters, user input is not needed and
                                will not be prompted. If the no-prompt flag is not
                                set, user input will be prompted for each of the
                                configurable values not specified by parameters. If
                                the no-prompt flag is set, no user input will be
                                collected and the configuration file will be populated
                                with option-specified values or defaults. The
                                resulting configuration file defines the following
                                parameters. Configurable parameters are shown in
                                <angle braces>. SWAG_OPTS = {'swag.type': 's3',
                                'swag.bucket_name': <bucket>} SWAG_FILTER = None
                                SWAG_SERVICE_ENABLED_REQUIREMENT = None ROLENAME =
                                <aardvark_role> REGION = "us-east-1"
                                SQLALCHEMY_DATABASE_URI = <db_uri>
                                SQLALCHEMY_TRACK_MODIFICATIONS = False NUM_THREADS =
                                <num_threads> LOG_CFG = {...}
```

<br>

---

### [Repokid](https://github.com/Netflix/repokid)

<span style="color:red;">**NOTE:**</span> You will need to add your IAM user into the **Trusted entities** section of the **"RepokidRole" role** prior to setting up Repokid

- **AFTER** setting up Aardvark, move into the Repokid dir.
  - `cd **/aardvark_repokid_demo/aardvark_repokid/repokid`
- Run the following to get Repokid up within the Repokid dir:
  - `python setup.py develop`
  - `repokid config config.json`
    - After the initial configurations are set, do the following:
        - If desired, use the preconfigured file --  run `cp ../custom_configs/repokid_configs.json ./configs.json`
        - To create your own custom configuration file -- update the `default_repokid_configs.json` file and run `cp ../custom_configs/default_repokid_configs.json ./configs.json`
            - Use the [Repokid Github](https://github.com/Netflix/repokid) for references on how to set this up (can also be seen in the Repokid `README.md`)
  - `repokid update_role_cache [AWS ACCOUNT]` -- update the cached data (cached data provided in the local DynamoDB)
    - **This will need to be updated every time an update is made within the Aardvark environment (`aardvark update -a [YOUR AWS ACCOUNT]`)**

- After this is set up, you can run multiple different request options. Be mindful that some of these options **WILL** modify your AWS account.
  - With this in mind, as long as the cache isn't updated and the `repokid.log` file hasn't been modified, you can rollback to reverse a change with `repokid rollback role [AWS ACCOUNT] [Role Name]` -- **Only individual IAM Roles can be rolled back at a time currently**

<br>

#### Current Repokid Request Options

```
$ repokid config <config_filename>
$ repokid update_role_cache <account_number>
$ repokid display_role_cache <account_number> [--inactive]
$ repokid find_roles_with_permissions <permission>... [--output=ROLE_FILE]
$ repokid remove_permissions_from_roles --role-file=ROLE_FILE <permission>... [-c]
$ repokid display_role <account_number> <role_name>
$ repokid schedule_repo <account_number>
$ repokid repo_role <account_number> <role_name> [-c]
$ repokid rollback_role <account_number> <role_name> [--selection=NUMBER] [-c]
$ repokid repo_all_roles <account_number> [-c]
$ repokid show_scheduled_roles <account_number>
$ repokid cancel_scheduled_repo <account_number> [--role=ROLE_NAME] [--all]
$ repokid repo_scheduled_roles <account_number> [-c]
$ repokid repo_stats <output_filename> [--account=ACCOUNT_NUMBER]
```


<!-- 
echo `curl http://localhost:5000/api/1/advisors`>> ../../aardvark_logs/advisor_results.json
repokid update_role_cache <ACCOUNT_NUMBER>
cp ./repokid.log ../../logs/repokid_logs/repokid.log

repokid display_role_cache <ACCOUNT_NUMBER> 
cp ./table.csv ../../logs/repokid_logs/permissions_table.csv

repokid display_role <ACCOUNT_NUMBER> <ROLE_NAME>
repokid repo_all_roles <ACCOUNT_NUMBER> -c
schedule_repo 

https://github.com/Netflix-Skunkworks/repokid-extras
--> 
