# HR Resume Management AI Assistant - AWS Architecture

## Overview

This architecture provides a scalable, secure, and cost-optimized solution for AI-powered resume management and candidate matching. The system enables HR personnel to upload resumes, perform semantic searches, and receive AI-driven candidate recommendations based on job requirements.

## Architecture Components

### 1. Edge Layer
- **Route 53**: DNS management and health checks
- **CloudFront**: Global content delivery, SSL/TLS termination, reduced latency
- **AWS WAF**: Protection against common web exploits and DDoS attacks

### 2. Authentication & Authorization
- **Amazon Cognito**: User authentication, MFA support, JWT token management
- **IAM**: Fine-grained access control for AWS resources

### 3. API Layer
- **API Gateway**: RESTful API endpoints, request throttling, API key management
- **Application Load Balancer**: Distributes traffic across Lambda functions in Multi-AZ setup

### 4. Application Tier (Private Subnets)

#### Resume Processing Pipeline
- **Upload Handler Lambda**: Validates and uploads resumes to S3
- **Document Parser Lambda**: Extracts text from PDF/Word documents
- **Text Extractor Lambda**: Processes extracted text, generates embeddings

#### Search & Matching
- **Search Handler Lambda**: Processes search queries, manages caching
- **AI Matcher Lambda**: Performs semantic matching using AI models

#### CRUD Operations
- **Resume CRUD Lambda**: Manages resume metadata and database operations

### 5. Data Tier (Private Subnets)

#### Storage
- **S3 Resume Storage**: Original resume files with Intelligent-Tiering
- **S3 Processed Data**: Extracted text and processed documents

#### Databases
- **RDS PostgreSQL (Multi-AZ)**: Stores resume metadata, user profiles, search history
- **OpenSearch**: Vector database for semantic search and embeddings
- **ElastiCache Redis**: Caches frequent queries and search results

#### AI/ML Services
- **Amazon Bedrock**: Generates text embeddings using Titan models
- **Amazon Comprehend**: NLP analysis for entity extraction, key phrases, sentiment

### 6. Async Processing
- **SQS Queue**: Decouples resume upload from processing
- **Dead Letter Queue**: Captures failed processing attempts for retry

### 7. Monitoring & Security
- **CloudWatch**: Centralized logging, metrics, alarms
- **CloudTrail**: Audit trail for compliance
- **Secrets Manager**: Secure storage for database credentials and API keys

### 8. Backup & Disaster Recovery
- **S3 Glacier**: Long-term backup storage with lifecycle policies
- **RDS Automated Backups**: Point-in-time recovery capability

## Data Flow

### Resume Upload Flow
1. HR user uploads resume through web interface
2. Request passes through CloudFront → WAF → API Gateway
3. Cognito validates user authentication
4. Upload Handler Lambda stores file in S3
5. S3 event triggers SQS message
6. Document Parser Lambda extracts text
7. Text Extractor generates embeddings via Bedrock
8. Embeddings stored in OpenSearch, metadata in RDS

### Search & Matching Flow
1. HR user submits job requirements
2. Search Handler checks Redis cache
3. If cache miss, generates query embeddings via Bedrock
4. OpenSearch performs vector similarity search
5. AI Matcher ranks candidates by relevance
6. Results cached in Redis and returned to user

## Security Features

- **Encryption at Rest**: S3 (SSE-S3), RDS (KMS), OpenSearch (KMS)
- **Encryption in Transit**: TLS 1.2+ for all communications
- **Network Isolation**: VPC with private subnets, no direct internet access
- **IAM Roles**: Least privilege access for all Lambda functions
- **Secrets Management**: No hardcoded credentials
- **Audit Logging**: CloudTrail tracks all API calls
- **WAF Rules**: OWASP Top 10 protection

## High Availability

- **Multi-AZ Deployment**: RDS, OpenSearch, ElastiCache
- **Auto Scaling**: Lambda concurrent executions
- **Load Balancing**: ALB distributes traffic
- **Failover**: Automatic RDS failover < 2 minutes
- **Backup Strategy**: Daily automated backups, 7-day retention

## Scalability

- **Serverless Compute**: Lambda scales automatically
- **Elastic Storage**: S3 unlimited capacity
- **Database Scaling**: RDS read replicas, OpenSearch cluster scaling
- **Cache Layer**: Redis reduces database load
- **Async Processing**: SQS handles traffic spikes

## Cost Optimization

- **S3 Intelligent-Tiering**: Automatic cost optimization for storage
- **Lambda**: Pay-per-execution, no idle costs
- **Reserved Capacity**: RDS and OpenSearch Reserved Instances for predictable workloads
- **Caching**: Reduces AI model invocations
- **Lifecycle Policies**: Automatic archival to Glacier

## Compliance & Data Protection

- **GDPR/CCPA Ready**: Data encryption, access controls, audit trails
- **Data Residency**: Deploy in specific AWS regions
- **Right to Deletion**: Automated data purging capabilities
- **Access Logging**: Complete audit trail of data access

## Viewing the Diagrams

### Python Diagram
```bash
pip install diagrams
python architecture-diagram.py
```
This generates `hr_resume_management_ai_assistant.png`

### Mermaid Diagram
View `architecture-diagram.mmd` in any Mermaid-compatible viewer:
- GitHub (renders automatically)
- VS Code with Mermaid extension
- https://mermaid.live

## Future Enhancements

- Integration with ATS (Applicant Tracking Systems)
- Real-time candidate notifications via SNS
- Advanced analytics dashboard with QuickSight
- Multi-language support via Amazon Translate
- Video resume analysis via Amazon Rekognition
# arquitectura_nube
