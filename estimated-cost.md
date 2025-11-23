# AWS Cost Estimation - HR Resume Management AI Assistant

## Assumptions

### Usage Profile
- **Active HR Users**: 50 users
- **Resume Database**: 10,000 resumes initially, growing 500/month
- **Average Resume Size**: 500 KB
- **Search Queries**: 1,000 queries/day (30,000/month)
- **Resume Uploads**: 500 resumes/month
- **Region**: US East (N. Virginia) - us-east-1
- **Operating Hours**: 24/7 availability

## Detailed Cost Breakdown

### 1. Compute - AWS Lambda

**Upload Handler**
- Invocations: 500/month
- Memory: 512 MB
- Duration: 2 seconds
- Cost: 500 × $0.0000002 + (500 × 2 × 512/1024 × $0.0000166667) = $0.01

**Document Parser**
- Invocations: 500/month
- Memory: 1024 MB
- Duration: 10 seconds
- Cost: 500 × $0.0000002 + (500 × 10 × 1024/1024 × $0.0000166667) = $0.08

**Text Extractor**
- Invocations: 500/month
- Memory: 1024 MB
- Duration: 5 seconds
- Cost: 500 × $0.0000002 + (500 × 5 × 1024/1024 × $0.0000166667) = $0.04

**Search Handler**
- Invocations: 30,000/month
- Memory: 512 MB
- Duration: 1 second
- Cost: 30,000 × $0.0000002 + (30,000 × 1 × 512/1024 × $0.0000166667) = $0.26

**AI Matcher**
- Invocations: 30,000/month (cache hit rate 70%, so 9,000 actual)
- Memory: 1024 MB
- Duration: 3 seconds
- Cost: 9,000 × $0.0000002 + (9,000 × 3 × 1024/1024 × $0.0000166667) = $0.45

**Resume CRUD**
- Invocations: 2,000/month
- Memory: 512 MB
- Duration: 1 second
- Cost: 2,000 × $0.0000002 + (2,000 × 1 × 512/1024 × $0.0000166667) = $0.02

**Lambda Total**: ~$0.86/month (within free tier initially)

### 2. Storage - Amazon S3

**Resume Storage (Standard - Intelligent Tiering)**
- Initial: 10,000 resumes × 0.5 MB = 5 GB
- Monthly growth: 500 × 0.5 MB = 0.25 GB
- Average storage: 5 GB + (0.25 GB × 6) = 6.5 GB
- Cost: 6.5 GB × $0.023 = $0.15/month

**Processed Data Storage**
- Text files: 6.5 GB × 0.1 (text is smaller) = 0.65 GB
- Cost: 0.65 GB × $0.023 = $0.01/month

**S3 Requests**
- PUT requests: 500/month = $0.00
- GET requests: 30,000/month = $0.01

**S3 Total**: ~$0.17/month

### 3. Database - Amazon RDS PostgreSQL

**Instance Type**: db.t4g.medium (2 vCPU, 4 GB RAM)
- Multi-AZ deployment
- On-Demand: $0.073/hour × 730 hours = $53.29/month
- Reserved Instance (1-year, no upfront): $0.048/hour × 730 = $35.04/month

**Storage**: 100 GB General Purpose SSD (gp3)
- Cost: 100 GB × $0.115 = $11.50/month

**Backup Storage**: 100 GB (same as allocated)
- Cost: $0 (first 100 GB free)

**RDS Total**: $46.54/month (with Reserved Instance)

### 4. Search - Amazon OpenSearch Service

**Instance Type**: t3.medium.search (2 nodes for Multi-AZ)
- On-Demand: 2 × $0.068/hour × 730 hours = $99.28/month
- Reserved Instance (1-year, no upfront): 2 × $0.045/hour × 730 = $65.70/month

**Storage**: 100 GB EBS per node
- Cost: 2 × 100 GB × $0.135 = $27.00/month

**OpenSearch Total**: $92.70/month (with Reserved Instance)

### 5. Cache - Amazon ElastiCache for Redis

**Instance Type**: cache.t4g.micro (2 nodes for Multi-AZ)
- On-Demand: 2 × $0.017/hour × 730 hours = $24.82/month
- Reserved Instance (1-year, no upfront): 2 × $0.011/hour × 730 = $16.06/month

**ElastiCache Total**: $16.06/month (with Reserved Instance)

### 6. AI/ML - Amazon Bedrock

**Titan Embeddings Model**
- Input tokens: 
  - Resume processing: 500 resumes × 1,000 tokens = 500,000 tokens
  - Search queries: 9,000 queries × 100 tokens = 900,000 tokens
  - Total: 1,400,000 tokens/month
- Cost: 1,400,000 × $0.0001/1000 = $0.14/month

**Bedrock Total**: $0.14/month

### 7. NLP - Amazon Comprehend

**Entity Detection**
- Characters: 500 resumes × 5,000 chars = 2,500,000 chars
- Units: 2,500,000 / 100 = 25,000 units
- Cost: 25,000 × $0.0001 = $2.50/month

**Key Phrase Extraction**
- Cost: 25,000 × $0.0001 = $2.50/month

**Comprehend Total**: $5.00/month

### 8. API Management - Amazon API Gateway

**REST API Requests**
- Total requests: 30,000 + 500 + 2,000 = 32,500/month
- Cost: 32,500 × $0.0000035 = $0.11/month

**Data Transfer Out**: 32,500 × 10 KB = 325 MB
- Cost: $0.00 (within free tier)

**API Gateway Total**: $0.11/month

### 9. Load Balancing - Application Load Balancer

**ALB Hours**: 730 hours × $0.0225 = $16.43/month

**LCU Hours**: 730 hours × 1 LCU × $0.008 = $5.84/month

**ALB Total**: $22.27/month

### 10. Content Delivery - Amazon CloudFront

**Data Transfer Out**: 10 GB/month (web UI assets)
- Cost: 10 GB × $0.085 = $0.85/month

**HTTP/HTTPS Requests**: 100,000/month
- Cost: 100,000 × $0.0000010 = $0.10/month

**CloudFront Total**: $0.95/month

### 11. DNS - Amazon Route 53

**Hosted Zone**: 1 zone × $0.50 = $0.50/month

**Queries**: 1,000,000/month
- Cost: 1,000,000 × $0.0000004 = $0.40/month

**Route 53 Total**: $0.90/month

### 12. Security - AWS WAF

**Web ACL**: 1 × $5.00 = $5.00/month

**Rules**: 5 rules × $1.00 = $5.00/month

**Requests**: 100,000/month × $0.0000006 = $0.06/month

**WAF Total**: $10.06/month

### 13. Authentication - Amazon Cognito

**Monthly Active Users**: 50 users
- First 50,000 MAUs free
- Cost: $0.00/month

**Cognito Total**: $0.00/month

### 14. Messaging - Amazon SQS

**Requests**: 500 uploads × 3 messages = 1,500/month
- Cost: $0.00 (within free tier)

**SQS Total**: $0.00/month

### 15. Monitoring - Amazon CloudWatch

**Logs Ingested**: 10 GB/month
- Cost: 10 GB × $0.50 = $5.00/month

**Logs Storage**: 10 GB/month
- Cost: 10 GB × $0.03 = $0.30/month

**Metrics**: 50 custom metrics
- Cost: 50 × $0.30 = $15.00/month

**Alarms**: 10 alarms
- Cost: 10 × $0.10 = $1.00/month

**CloudWatch Total**: $21.30/month

### 16. Audit - AWS CloudTrail

**Management Events**: Free (one trail)

**Data Events**: S3 and Lambda
- Cost: ~$2.00/month

**CloudTrail Total**: $2.00/month

### 17. Secrets - AWS Secrets Manager

**Secrets**: 5 secrets (DB, API keys)
- Cost: 5 × $0.40 = $2.00/month

**API Calls**: 10,000/month
- Cost: 10,000 × $0.000005 = $0.05/month

**Secrets Manager Total**: $2.05/month

### 18. Backup - S3 Glacier

**Backup Storage**: 100 GB (RDS snapshots, old resumes)
- Cost: 100 GB × $0.004 = $0.40/month

**Glacier Total**: $0.40/month

### 19. Data Transfer

**Inter-AZ Data Transfer**: 50 GB/month
- Cost: 50 GB × $0.01 = $0.50/month

**Internet Data Transfer Out**: 20 GB/month (beyond CloudFront)
- Cost: 20 GB × $0.09 = $1.80/month

**Data Transfer Total**: $2.30/month

## Monthly Cost Summary

| Service Category | Monthly Cost | Annual Cost |
|-----------------|--------------|-------------|
| Compute (Lambda) | $0.86 | $10.32 |
| Storage (S3) | $0.17 | $2.04 |
| Database (RDS) | $46.54 | $558.48 |
| Search (OpenSearch) | $92.70 | $1,112.40 |
| Cache (ElastiCache) | $16.06 | $192.72 |
| AI/ML (Bedrock) | $0.14 | $1.68 |
| NLP (Comprehend) | $5.00 | $60.00 |
| API Gateway | $0.11 | $1.32 |
| Load Balancer | $22.27 | $267.24 |
| CDN (CloudFront) | $0.95 | $11.40 |
| DNS (Route 53) | $0.90 | $10.80 |
| Security (WAF) | $10.06 | $120.72 |
| Auth (Cognito) | $0.00 | $0.00 |
| Messaging (SQS) | $0.00 | $0.00 |
| Monitoring (CloudWatch) | $21.30 | $255.60 |
| Audit (CloudTrail) | $2.00 | $24.00 |
| Secrets Manager | $2.05 | $24.60 |
| Backup (Glacier) | $0.40 | $4.80 |
| Data Transfer | $2.30 | $27.60 |
| **TOTAL** | **$223.81** | **$2,685.72** |

## Cost Optimization Strategies

### Immediate Savings (0-3 months)

1. **Reserved Instances** (Already included above)
   - RDS: Save 32% ($18/month)
   - OpenSearch: Save 34% ($34/month)
   - ElastiCache: Save 35% ($9/month)
   - **Total Savings**: $61/month

2. **S3 Intelligent-Tiering** (Already included)
   - Automatic cost optimization
   - Estimated savings: 20-30% on storage

3. **ElastiCache for Query Caching**
   - Reduces Bedrock API calls by 70%
   - Saves ~$0.10/month (grows with scale)

4. **CloudWatch Logs Retention**
   - Set retention to 30 days for most logs
   - Keep 1 year for audit logs only
   - Saves ~$5/month

### Medium-term Savings (3-6 months)

5. **Compute Savings Plans**
   - 1-year commitment for Lambda
   - Save up to 17% on compute
   - Savings: ~$2/month (grows with usage)

6. **S3 Lifecycle Policies**
   - Move old resumes to Glacier after 1 year
   - Saves ~$0.20/month initially, grows over time

7. **OpenSearch Reserved Instances**
   - 3-year commitment: Save 50%
   - Additional savings: $27/month

### Long-term Savings (6-12 months)

8. **Right-sizing**
   - Monitor actual usage and downsize if possible
   - Potential savings: 10-20% on compute resources

9. **Spot Instances for Batch Processing**
   - Use Spot for non-critical resume processing
   - Potential savings: 50-70% on batch compute

10. **Multi-year Reserved Instances**
    - 3-year RDS RI: Additional 20% savings
    - Additional savings: $10/month

## Scaling Cost Projections

### Year 1 (Current)
- Users: 50
- Resumes: 10,000 → 16,000
- Monthly Cost: $224

### Year 2 (2x Growth)
- Users: 100
- Resumes: 16,000 → 28,000
- Monthly Cost: $380 (70% increase due to economies of scale)

### Year 3 (3x Growth)
- Users: 150
- Resumes: 28,000 → 46,000
- Monthly Cost: $520 (132% increase from Year 1)

## Cost Comparison with Alternatives

### On-Premises Solution
- Hardware: $50,000 upfront
- Maintenance: $2,000/month
- Personnel: $8,000/month (DevOps)
- **3-Year Total**: $410,000

### AWS Solution
- **3-Year Total**: $32,228 (with optimizations)
- **Savings**: $377,772 (92% reduction)

### Hybrid Solution
- Partial on-prem, partial cloud
- **3-Year Total**: ~$150,000
- **Savings**: $260,000 vs full on-prem

## ROI Analysis

### Cost per Resume Processed
- Monthly: $224 / 500 = $0.45 per resume
- Annual: $2,686 / 6,000 = $0.45 per resume

### Cost per Search Query
- Monthly: $224 / 30,000 = $0.007 per query
- Annual: $2,686 / 360,000 = $0.007 per query

### HR Time Savings
- Manual resume review: 30 min/resume
- AI-assisted review: 5 min/resume
- Time saved: 25 min/resume × 500 resumes/month = 208 hours/month
- Cost savings (at $50/hour): $10,400/month
- **ROI**: ($10,400 - $224) / $224 = 4,543% monthly ROI

## Budget Recommendations

### Conservative Budget
- Monthly: $300 (33% buffer)
- Annual: $3,600

### Growth Budget (Year 2)
- Monthly: $500
- Annual: $6,000

### Enterprise Budget (Year 3)
- Monthly: $700
- Annual: $8,400

## Cost Alerts

Set up CloudWatch billing alarms:
1. Alert at $200/month (90% of budget)
2. Alert at $250/month (110% of budget)
3. Alert at $300/month (critical threshold)

## Conclusion

The estimated monthly cost of $224 provides excellent value for an AI-powered resume management system. With proper optimization strategies, costs can be reduced by 20-30% while maintaining performance and reliability. The solution offers 92% cost savings compared to on-premises alternatives and delivers a 4,543% ROI through HR time savings.

**Recommendation**: Proceed with implementation using Reserved Instances for predictable workloads and implement cost optimization strategies progressively.
