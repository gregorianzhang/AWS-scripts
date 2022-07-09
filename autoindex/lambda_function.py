import boto3


bucket = "your-bucket"


def list_s3_files_autoindex(response,bucket, prefix, uri):

    s3_client = boto3.client("s3")
    rsp = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter="/")
    prefix_name1 = rsp["Prefix"]
    try:
        tmp1 = list(obj["Prefix"] for obj in rsp["CommonPrefixes"])
    except:
        print("no dir")
        tmp1 = list(obj["Key"] for obj in rsp["Contents"])

    tmp2 = []
    for x in tmp1:
        tmp2.append(x.replace(prefix_name1,""))

    htmlcontent =""
    for x in tmp2:
        htmlcontent += '<li><a href="'+ x +'">' + x + '</a></li>'

    htmlstart = "<html><title> your-bucket </title>"
    htmlend = "</html>"
    indexhtml = htmlstart + htmlcontent + htmlend

    response['status'] = '200'
    response['statusDescription'] = 'OK'
    response['body'] = indexhtml
    response['headers']['content-type'] = [{'key': 'Content-Type', 'value': 'text/html'}]
    return response


def lambda_handler(event, context):
    request =  event['Records'][0]['cf']['request']
    response = event['Records'][0]['cf']['response']


    if (int(response['status'])>= 400 and int(response['status']) <= 599 ) or int(response['headers']['content-length'][0]['value']) == 0:

        uri = request['uri']
        path = request['origin']['s3']['path']
        prefix = path[1:]
        prefix_name = prefix + uri
        return list_s3_files_autoindex(response, bucket, prefix_name, uri)
    else:
        return response

