# Automate

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge)
![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?logo=aws-lambda&logoColor=white&style=for-the-badge)
![AWS SAM](https://img.shields.io/badge/AWS%20SAM-F29100?logo=amazonaws&logoColor=white&style=for-the-badge)
![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?logo=amazon-s3&logoColor=white&style=for-the-badge)
![Twilio](https://img.shields.io/badge/Twilio-F22F46?logo=twilio&logoColor=white&style=for-the-badge)

## About

**Automate** is a serverless application built on AWS that scrapes job boards and hackathon sites for new opportunities and sends real-time SMS alerts. It automates the tedious process of manually checking multiple websites for new software engineering internships and hackathons, leveraging a cost-effective, scalable, and maintenance-free serverless architecture.

## Features

- **Automated Scraping**: Regularly fetches the latest internship postings from the Simplify Jobs GitHub Repo and hackathons from MLH.
- **Real-Time SMS Alerts**: Uses the Twilio API to send instant SMS notifications for new opportunities.
- **Stateful Tracking**: Remembers previously seen listings by storing a state file in an S3 bucket, preventing duplicate alerts.
- **Serverless & Cost-Effective**: Runs on AWS Lambda, only incurring costs when the script is active, which falls well within the AWS Free Tier.
- **Infrastructure as Code (IaC)**: The entire AWS infrastructure is defined and deployed using the AWS Serverless Application Model (SAM).

## Technology Stack

- **Cloud**: AWS (Lambda, S3, CloudWatch Events, IAM)
- **Framework**: AWS SAM (Serverless Application Model)
- **Language**: Python
- **APIs & Services**: Twilio for SMS notifications
- **Libraries**: Boto3, Requests, BeautifulSoup4

## Deployment

This project is deployed entirely through Infrastructure as Code. After configuring the placeholder values in `template.yaml`:

1.  **Build the application:**
    ```bash
    sam build
    ```
2.  **Deploy to AWS:**
    ```bash
    sam deploy --guided
    ```
