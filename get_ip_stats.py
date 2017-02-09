import boto3

c = boto3.client('s3')
b = boto3.resource('s3')

for bucket in c.list_buckets()['Buckets']:
    bucket_name = bucket['Name']
    print "\n***** Customer Host: " + bucket_name + " *****\n"
    bucket_obj = b.Bucket(bucket_name)

    for obj in bucket_obj.objects.all():
        ip_filename = obj.key
        body = c.get_object(Bucket = bucket_name, Key = ip_filename)['Body'].read()
        print obj.key[:-4] + " " + body

