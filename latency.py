import boto3
import botocore
import time

session = boto3.Session(profile_name='default')

regions = ['ap-south-1', 'ap-northeast-2', 'ap-southeast-1','ap-southeast-2','ap-northeast-1', 
            'ca-central-1','eu-central-1','eu-west-1', 'eu-west-2','eu-west-3','sa-east-1',
            'us-east-1','us-east-2','us-west-1', 'us-west-2',
            ]

files = ['1KB', '10KB', '1MB', '10MB']

def put(s3, bucketname, key, filename):
    start_time = time.time()
    s3.Bucket(bucketname).put_object(Key=key, Body=open(filename, 'rb'))
    return time.time() - start_time

def get(s3, bucketname, key):
    start_time = time.time()
    s3.Object(bucketname, key).get()['Body'].read()
    return time.time() - start_time

def delete(s3, bucketname, key):
    start_time = time.time()
    s3.Object(bucketname, key).delete()
    return time.time() - start_time

for region in regions:
    session = boto3.Session(profile_name='default', region_name=region)
    s3 = session.resource('s3')
    bucketname = region + ".latency"
    try:
        s3.create_bucket(Bucket=bucketname)
    except:
        s3.create_bucket(
                Bucket=bucketname,
                CreateBucketConfiguration={'LocationConstraint': region}
            )

    print('Region : ' + region)

    for key, file in enumerate(files):
        average_put_latency=0
        average_get_latency=0
        average_delete_latency= 0
        print('File Size : ', file)

        for i in range(0, 10):
            average_put_latency += put(s3, bucketname, str(key), file)
        print(str(key)+'. average put latency : ', average_put_latency/10)


        for i in range(0, 10):
            average_get_latency += get(s3, bucketname, str(key))
        print(str(key)+'.average get latency : ', average_get_latency / 10)


        for i in range(0, 10):
            average_delete_latency += delete(s3, bucketname, str(key))
        print(str(key)+'.average delete latency : ', average_delete_latency / 10)


    s3.Bucket(bucketname).objects.all().delete()
    s3.Bucket(bucketname).delete()
