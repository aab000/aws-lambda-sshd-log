# aws-lambda-sshd-log
++ aws_lambda_rec_ip.py ++
aws_lambda_rec_ip.py is an aws lambda function which monitors for successful ssh logins on ec2 instances reporting
to cloudwatch.  The function parses the log entry for both the host from which the log originated and the connecting IP.
The tally is recorded in an s3 object named for the IP.

++ get_ip_stats.py ++
get_ip_stats.py is a companion script for the above lambda function. It polls all buckets owned by the user ("log-admin")
and gives a summary report for each object of each bucket.
