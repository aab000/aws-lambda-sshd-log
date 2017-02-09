import boto3
import json
import re
import gzip
import base64
from StringIO import StringIO

def handler(event, context):
    c = boto3.client('s3')
    d = event['awslogs']['data']
    # load and decode the related log entry
    k = json.loads(gzip.GzipFile(fileobj=StringIO(d.decode("base64", "strict"))).read())['logEvents']
    for i in k:
        msg = i['message']
        # capture the connecting IP
        ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', msg)
        # get the internal hostname (portion of bucket name) of customer's vm
        customer = str(msg).split(' ')[4]
        # add filename extension to string
        ipfile = ips[0]+'.txt'
        # Count is used for previously unrecorded IPs
        count = 1
        cust_bucket = "voltaiq-cust-" + customer

        for b in c.list_buckets()['Buckets']:
            # Get proper bucket
            if b['Name'] == cust_bucket:
                try:
                    # if IP has existing object, get current count from text body
                    s = int(c.get_object(Bucket = cust_bucket, Key = ipfile)['Body'].read())
                    count = s + 1
                except:
                    # Optional alert steps
                    #sns = boto3.client('sns')
                    #number = '+1 '
                    #sns.publish(PhoneNumber = number, (Message='New IP recorded: ' + ip))
                    pass
                # create new object with current tally
                c.put_object(Bucket = cust_bucket, Key = ipfile, Body = str(count))
