import boto3
import subprocess

ec2 = boto3.resource('ec2', region_name='eu-west-1')
asg = boto3.client('autoscaling', region_name='eu-west-1')


def getinstanceips():
    response= asg.describe_auto_scaling_groups(AutoScalingGroupNames=['MyASGroup',],)
    groups=response.get("AutoScalingGroups")
    instances=(groups[0].get('Instances'))
    subprocess.call("sed -i '42,$d' /etc/haproxy/haproxy.cfg",shell=True)
    for i in instances:
        ip= ec2.Instance(i.get('InstanceId')).public_ip_address
        e='echo "                          server webserver2 {0}:80 checks">>/etc/haproxy/haproxy.cfg'.format(ip)
        subprocess.call(e,shell=True)
        print(e)

if __name__ == "__main__":
    getinstanceips()

