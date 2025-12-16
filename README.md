# Serverless Timetable Ingestion Pipeline (AWS)

A lightweight serverless data ingestion pipeline that periodically fetches timetable change data from the Deutsche Bahn API and stores compressed raw responses in an S3-based data lake.

## Architecture

EventBridge (schedule) → AWS Lambda → External API → gzip → Amazon S3

The system is designed to be:
- Cost-efficient
- Stateless
- Easy to scale to additional data sources

## Data Flow

1. EventBridge triggers the Lambda function (hourly or every 2 minutes)
2. Lambda fetches XML data from the Deutsche Bahn Timetables API
3. Raw payload is gzip-compressed
4. Data is stored in S3 using a time-partitioned layout

`s3://db-api-responses/{eva}/{datatype}/year/month/day/hour/timestamp.xml.gz`


## Storage Strategy

- Raw XML data is stored in compressed format
- Time-based partitioning enables efficient downstream processing
- Designed for future lifecycle policies (Glacier / Deep Archive)

## Configuration

The following environment variables are required:

- `DB_CLIENT_ID`
- `DB_CLIENT_SECRET`
- `S3_BUCKET_NAME`

## IAM Permissions

The Lambda function requires:
- `s3:PutObject` on the target bucket
- CloudWatch Logs permissions

Example policy is provided in `infra/lambda_policy.json`.

## Cost Considerations

Approximate monthly costs (us-east-1):
- Lambda: < $0.10
- S3 PUT requests: ~ $0.11
- Storage: ~ $0.02 per GB-month

Total: well under $1/month.

## Possible Extensions

- Retry logic and exponential backoff
- Multi-station ingestion
- Downstream processing with Athena or Glue
- Infrastructure as Code (Terraform / SAM)

