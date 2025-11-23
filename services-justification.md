# AWS Services Justification

## Edge & Content Delivery

### Amazon Route 53
**Purpose**: DNS management and routing
**Justification**: 
- Provides health checks and failover routing
- Low latency DNS resolution globally
- Integrates seamlessly with CloudFront
- 100% SLA availability

### Amazon CloudFront
**Purpose**: Content delivery network
**Justification**:
- Reduces latency for global HR teams
- SSL/TLS termination at edge locations
- DDoS protection via AWS Shield Standard (included)
- Caches static assets (web UI, images)
- Cost savings on data transfer from origin

### AWS WAF
**Purpose**: Web application firewall
**Justification**:
- Protects against OWASP Top 10 vulnerabilities
- Rate limiting to prevent abuse
- Geo-blocking capabilities for compliance
- Custom rules for resume upload validation
- Real-time threat intelligence

## Authentication & Security

### Amazon Cognito
**Purpose**: User authentication and authorization
**Justification**:
- Managed service, no infrastructure to maintain
- Built-in MFA support for enhanced security
- OAuth 2.0 and SAML 2.0 support for SSO
- User pool management with password policies
- JWT tokens for stateless authentication
- Cost-effective ($0.0055 per MAU after free tier)

### AWS Secrets Manager
**Purpose**: Credentials and secrets storage
**Justification**:
- Automatic rotation of database credentials
- Encryption at rest with KMS
- Fine-grained IAM access control
- Audit trail via CloudTrail
- Eliminates hardcoded credentials

### AWS IAM
**Purpose**: Access management
**Justification**:
- Least privilege access for all services
- Service roles for Lambda functions
- No additional cost
- Granular permission policies

## API & Compute

### Amazon API Gateway
**Purpose**: RESTful API management
**Justification**:
- Managed service with automatic scaling
- Request throttling and quota management
- API versioning and stage management
- Request/response transformation
- Integration with Cognito for authentication
- CloudWatch integration for monitoring
- Pay-per-request pricing model

### AWS Lambda
**Purpose**: Serverless compute for business logic
**Justification**:
- No server management required
- Automatic scaling (0 to thousands of concurrent executions)
- Pay only for compute time used
- Sub-second startup times
- Native integration with S3, SQS, API Gateway
- Supports multiple runtimes (Python, Node.js, Java)
- 1M free requests per month
- Ideal for event-driven architecture

### Application Load Balancer
**Purpose**: Traffic distribution
**Justification**:
- Multi-AZ deployment for high availability
- Health checks for Lambda targets
- SSL/TLS termination
- Path-based routing for different API endpoints
- Integration with WAF

## Storage

### Amazon S3
**Purpose**: Object storage for resumes and processed data
**Justification**:
- 99.999999999% (11 9's) durability
- Unlimited scalability
- Intelligent-Tiering for automatic cost optimization
- Versioning for data protection
- Lifecycle policies for archival to Glacier
- Event notifications to trigger processing
- Server-side encryption (SSE-S3 or SSE-KMS)
- Cost-effective ($0.023/GB for Standard, less for Intelligent-Tiering)

### Amazon S3 Glacier
**Purpose**: Long-term backup and archival
**Justification**:
- Extremely low cost ($0.004/GB/month)
- Compliance and regulatory requirements
- Immutable storage with Vault Lock
- Retrieval options (Expedited, Standard, Bulk)

## Databases

### Amazon RDS PostgreSQL
**Purpose**: Relational database for structured data
**Justification**:
- Stores resume metadata, user profiles, search history
- ACID compliance for data integrity
- Multi-AZ deployment for 99.95% SLA
- Automated backups and point-in-time recovery
- Read replicas for scaling read operations
- Managed service (patching, backups, monitoring)
- PostgreSQL supports JSON for semi-structured data
- Full-text search capabilities
- Cost-effective with Reserved Instances

**Why PostgreSQL over MySQL**:
- Better JSON support
- Advanced indexing (GiST, GIN)
- Full-text search built-in
- Better performance for complex queries

### Amazon OpenSearch Service
**Purpose**: Vector database for semantic search
**Justification**:
- Native support for k-NN vector search
- Stores and queries embeddings efficiently
- Full-text search with relevance scoring
- Aggregations for analytics
- Multi-AZ deployment
- Automatic snapshots
- Fine-grained access control
- Scales horizontally with cluster nodes

**Why OpenSearch over alternatives**:
- Purpose-built for search and analytics
- Vector search plugin for embeddings
- Better than storing vectors in RDS
- More cost-effective than specialized vector databases

### Amazon ElastiCache for Redis
**Purpose**: In-memory caching
**Justification**:
- Sub-millisecond latency for cached queries
- Reduces load on RDS and OpenSearch
- Reduces Bedrock API calls (cost savings)
- Multi-AZ with automatic failover
- Cluster mode for horizontal scaling
- Persistence options for durability
- Significant cost savings on repeated queries

## AI/ML Services

### Amazon Bedrock
**Purpose**: Generate text embeddings for semantic search
**Justification**:
- Fully managed foundation models
- No infrastructure to manage
- Titan Embeddings model optimized for search
- Pay-per-use pricing (no upfront costs)
- Low latency inference
- Automatic scaling
- Data privacy (data not used for training)
- More cost-effective than SageMaker for inference-only workloads

**Why Bedrock over SageMaker**:
- No model hosting costs
- No endpoint management
- Simpler integration
- Lower operational overhead
- Better for embeddings generation

### Amazon Comprehend
**Purpose**: Natural language processing
**Justification**:
- Pre-trained models for entity extraction
- Key phrase extraction
- Sentiment analysis
- Language detection
- PII detection for compliance
- Pay-per-use pricing
- No ML expertise required
- Complements Bedrock for comprehensive NLP

## Async Processing

### Amazon SQS
**Purpose**: Message queue for async processing
**Justification**:
- Decouples upload from processing
- Handles traffic spikes gracefully
- Automatic scaling
- Message retention up to 14 days
- Dead Letter Queue for failed messages
- At-least-once delivery guarantee
- Cost-effective ($0.40 per million requests)
- No infrastructure to manage

### Dead Letter Queue (DLQ)
**Purpose**: Capture failed processing attempts
**Justification**:
- Prevents message loss
- Enables debugging and retry logic
- Alerts on processing failures
- Compliance and audit requirements

## Monitoring & Operations

### Amazon CloudWatch
**Purpose**: Monitoring, logging, and alerting
**Justification**:
- Centralized logging for all services
- Custom metrics and dashboards
- Alarms for proactive monitoring
- Log insights for troubleshooting
- Integration with all AWS services
- Retention policies for cost control
- No additional infrastructure

### AWS CloudTrail
**Purpose**: Audit logging and compliance
**Justification**:
- Records all API calls
- Compliance requirements (SOC 2, ISO 27001)
- Security analysis and troubleshooting
- Integration with CloudWatch for alerts
- Immutable audit trail
- Required for GDPR/CCPA compliance

### AWS Systems Manager
**Purpose**: Parameter management and automation
**Justification**:
- Centralized configuration management
- Parameter Store for non-sensitive configs
- Patch management for EC2 (if needed)
- Session Manager for secure access
- No additional cost for basic features

## Services NOT Selected (and Why)

### Amazon SageMaker (for inference)
**Not Selected**: Too expensive for simple embedding generation. Bedrock provides managed models without endpoint hosting costs.

### Amazon DynamoDB
**Not Selected**: While highly scalable, PostgreSQL better suits relational data (user profiles, resume metadata). OpenSearch handles unstructured search better than DynamoDB.

### AWS Fargate/ECS
**Not Selected**: Lambda provides sufficient compute with better cost optimization for variable workloads. No need for containerized long-running processes.

### Amazon Kendra
**Not Selected**: Expensive for this use case ($810/month minimum). OpenSearch + Bedrock provides similar semantic search at lower cost.

### Amazon Textract
**Not Selected**: Overkill for resume parsing. Standard PDF/Word libraries in Lambda sufficient. Textract better for complex forms/tables.

### Amazon Rekognition
**Not Selected**: Not needed for initial MVP. Could be added later for video resume analysis.

## Cost-Benefit Analysis Summary

| Service | Monthly Cost (Est.) | Benefit | ROI |
|---------|-------------------|---------|-----|
| Lambda | $20-50 | Serverless scaling | High |
| S3 | $50-100 | Unlimited storage | High |
| RDS | $150-300 | Managed database | Medium |
| OpenSearch | $200-400 | Semantic search | High |
| Bedrock | $100-200 | AI embeddings | High |
| ElastiCache | $50-100 | Query performance | High |
| API Gateway | $10-30 | API management | High |
| CloudFront | $20-50 | Global delivery | Medium |
| Cognito | $5-20 | User management | High |
| Others | $50-100 | Monitoring, security | High |

**Total Estimated Monthly Cost**: $655-1,350 (varies with usage)

This architecture prioritizes managed services to minimize operational overhead while maintaining cost efficiency and scalability.
