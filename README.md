# Opportunity Tracker Lambda

An AWS Lambda function that tracks internship opportunities from Simplify Jobs and MLH Hackathons.

## AWS Setup

1. Create an S3 bucket:
```bash
aws s3 mb s3://your-bucket-name
```

2. Create an IAM role for Lambda with these permissions:
   - AWSLambdaBasicExecutionRole
   - Custom policy for S3 access:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        }
    ]
}
```

## Environment Variables

Set these in your Lambda function configuration:

- `S3_BUCKET`: Your S3 bucket name
- `TWILIO_ACCOUNT_SID`: Your Twilio account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio auth token
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number
- `MY_PHONE_NUMBER`: Your personal phone number to receive notifications

## Deployment

1. Create a deployment package:
```bash
pip install -r requirements.txt -t ./package
cp app.py ./package/
cd package
zip -r ../deployment.zip .
```

2. Create the Lambda function:
```bash
aws lambda create-function \
  --function-name opportunity-tracker \
  --runtime python3.9 \
  --handler app.lambda_handler \
  --memory-size 256 \
  --timeout 300 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_ROLE_NAME \
  --zip-file fileb://deployment.zip
```

3. Set up a CloudWatch Events rule to trigger the function daily:
```bash
aws events put-rule \
  --name daily-opportunity-check \
  --schedule-expression "rate(1 day)"

aws lambda add-permission \
  --function-name opportunity-tracker \
  --statement-id daily-check \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:REGION:ACCOUNT_ID:rule/daily-opportunity-check
```

## Local Testing

To test locally:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Monitoring

Monitor the function's execution in CloudWatch Logs. The function will log:
- Number of opportunities found
- Any errors in fetching or processing data
- SMS notification status

## Project Structure

```
automate/
├── src/           # Source code
├── tests/         # Test files
├── docs/          # Documentation
└── examples/      # Example scripts
```

## Getting Started

1. Clone the repository
```bash
git clone https://github.com/yourusername/Automate.git
cd Automate
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

[Add usage instructions here]

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 