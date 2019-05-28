## To run the environment...

**NOTE:** If this is run in a Cloud9 environment, you will want to run the Aardvark and Repokid Environment as root: `sudo su`
  - This is due to the fact that AWS Cloud9 prevents regular users from storing AWS credentials

1. Configure your credentials: `aws configure`
    - NOTE: If running in Cloud9, must use `sudo aws configure`
2. Run the environment setup in this directory: `envsetup.sh`
3. Run the `aardvark_repokid_setup.py` file
    - Manually move the `custom_configs2.py` file to `custom_configs` dir.
    - NOTE: If running in Cloud9, must use `sudo python3 aardvark_repokid_setup.py`
4. Set up DynamoDB locally -- must be in the `dynamodb_local` directory
    - `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -inMemory -port 8010`
    - Leave this database running
5. Run python's virtual environment with `source aardvark_repokid_env/bin/activate`
6. Set up Aardvark environment -- move into Aardvark directory and run the following:
    - `python setup.py develop`
    - `aardvark config`
    - `aardvark create_db`
    - `aardvark update -a [YOUR AWS ACCOUNT]`
    - `aardvark start_api -b 0.0.0.0:5000`
    - Leave this terminal running
    - To validate this is running on Cloud9, copy the logs as validation or run curl calls -- no interface can be seen with this environment, so you will have to settle on data retrieval...
7. Set up Repokid environment -- move to Repokid directory and run the following:
    - `python setup.py develop`
    - `repokid config config.json`
    - For custom file changes: `cp ../custom_configs/custom_configs2.json ./config.json`
    - `repokid update_role_cache [AWS ACCOUNT]`

For any undesired modifications, rollbacks are available: `repokid rollback role [AWS ACCOUNT] [Role Name]`
To save Aardvark logs: `echo (curl http://localhost:5000/api/1/advisors) >> ../logs/advisor_results.json`
To save Repokid logs: 
    - `cp ./repokid.log ../logs/repokid.log`
    - `repokid display_role_cache [AWS ACCOUNT]` & `cp ./table.csv ../logs/repokid_permissions_table.csv`

This call will help provide least-privilege permissions: `repokid display_role [AWS ACCOUNT] [ROLE_NAME]`
