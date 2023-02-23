To assign an IAM role to compute resources like EC2 instances or Lambda functions to automatically supply temporary credentials to enable access, you can follow these steps:

1. Open the IAM console in the AWS Management Console.
2. Choose "Roles" from the left-hand menu, then click "Create role".
3. Choose the type of trusted entity that you want to use. For example, if you want to assign the role to an EC2 instance, choose "AWS service", then "EC2".
4. Choose the permissions policy that you want to use. You can either choose an existing policy, or you can create a custom policy that defines the permissions you want to grant.
5. Enter a name for the role and click "Create role".
6. Select the role that you just created, then click the "Trust relationships" tab.
7. Click "Edit trust relationship" and add the following trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "ec2.amazonaws.com",
          "lambda.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

This policy allows the EC2 instance or Lambda function to assume the role.

8. Next, you can assign the role to your EC2 instance or Lambda function.

For an EC2 instance:

1. Launch an EC2 instance or select an existing one.
2. Choose "Actions", then "Instance settings", then "Attach/Replace IAM role".
3. Select the role that you just created and click "Apply".

For a Lambda function:

1. Open the Lambda function that you want to assign the role to.
2. Click the "Configuration" tab.
3. Under "Permissions", click "Edit".
4. Under "Execution role", select "Use an existing role".
5. Select the role that you just created and click "Save".

Once the IAM role has been assigned to the compute resource, the resource will automatically receive temporary security credentials that it can use to access AWS resources. These temporary credentials are automatically rotated and can be used for a specified period of time before they expire. This approach is a best practice for security, as it helps to limit the potential for security breaches by ensuring that credentials are not stored on the compute resource itself.
