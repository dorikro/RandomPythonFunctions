import boto3

def create_cloudwatch_alarms(event, context):

    # Define the list of Direct Connect connections to create alarms for
    connections = ["dxcon-12345678", "dxcon-87654321"]

    # Get the Direct Connect status metric and service namespace
    metric_name = "ConnectionState"
    namespace = "AWS/DirectConnect"
    statistic = "Maximum"

    # Define the alarm threshold
    alarm_threshold = 0.0

    # Create the CloudWatch client
    cw = boto3.client('cloudwatch')

    # Create the alarm for each Direct Connect connection in the list
    for connection in connections:
        alarm_name = f"{connection}-StatusAlarm"
        alarm_description = f"Alarm when {metric_name} for {connection} is not 'available'"
        response = cw.put_metric_alarm(
            AlarmName=alarm_name,
            AlarmDescription=alarm_description,
            MetricName=metric_name,
            Namespace=namespace,
            Statistic=statistic,
            Period=300,
            EvaluationPeriods=1,
            Threshold=alarm_threshold,
            ComparisonOperator='LessThanThreshold',
            Dimensions=[{'Name': 'ConnectionId', 'Value': connection}],
            AlarmActions=['arn:aws:sns:us-east-1:123456789012:DirectConnectStatusAlarm']
        )

    return "Successfully created CloudWatch alarms"
