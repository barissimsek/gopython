## Configuration ##

Set up AWS credentials.

```
$ cat ~/.aws/credentials
[default]
aws_access_key_id = MY_ACCESS_KEY_ID
aws_secret_access_key = MY_ACCESS_KEY_SECRET

region = us-west-2
```

Install boto3 library to be able to use AWS services:

```
$ sudo pip install boto3
```

