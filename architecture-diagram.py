"""
AWS Architecture Diagram for HR Resume Management AI Assistant
Uses the diagrams library to generate architecture diagram
Install: pip install diagrams
Run: python architecture_diagram.py
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS, ElasticacheForRedis
from diagrams.aws.network import CloudFront, APIGateway, Route53, ELB
from diagrams.aws.security import Cognito, WAF, SecretsManager
from diagrams.aws.ml import SagemakerModel, Comprehend
from diagrams.aws.integration import SQS
from diagrams.aws.analytics import ES
from diagrams.aws.management import Cloudwatch, Cloudtrail
from diagrams.aws.general import User

with Diagram("HR Resume Management AI Assistant", show=False, direction="TB"):
    
    # Users
    hr_users = User("HR Personnel")
    
    with Cluster("Edge Layer"):
        dns = Route53("DNS")
        cdn = CloudFront("CDN")
        waf = WAF("WAF")
    
    with Cluster("Authentication"):
        cognito = Cognito("User Pool")
    
    with Cluster("API Layer"):
        api = APIGateway("REST API")
    
    with Cluster("VPC - Multi-AZ"):
        
        with Cluster("Public Subnets"):
            alb = ELB("Application LB")
        
        with Cluster("Private Subnets - App Tier"):
            with Cluster("Resume Processing"):
                upload_lambda = Lambda("Upload Handler")
                process_lambda = Lambda("Document Parser")
                extract_lambda = Lambda("Text Extractor")
            
            with Cluster("Search & Matching"):
                search_lambda = Lambda("Search Handler")
                match_lambda = Lambda("AI Matcher")
            
            with Cluster("CRUD Operations"):
                crud_lambda = Lambda("Resume CRUD")
        
        with Cluster("Private Subnets - Data Tier"):
            with Cluster("Storage"):
                s3_resumes = S3("Resume Storage")
                s3_processed = S3("Processed Data")
            
            with Cluster("Databases"):
                rds = RDS("PostgreSQL\n(Metadata)")
                opensearch = ES("OpenSearch\n(Vector Search)")
                cache = ElasticacheForRedis("Cache")
            
            with Cluster("AI/ML Services"):
                bedrock = SagemakerModel("Amazon Bedrock\n(Embeddings)")
                comprehend = Comprehend("Comprehend\n(NLP)")
    
    with Cluster("Async Processing"):
        queue = SQS("Processing Queue")
        dlq = SQS("Dead Letter Queue")
    
    with Cluster("Monitoring & Security"):
        cloudwatch = Cloudwatch("Logs & Metrics")
        cloudtrail = Cloudtrail("Audit Trail")
        secrets = SecretsManager("Secrets")
    
    with Cluster("Backup & DR"):
        s3_backup = S3("Backup Storage\n(Glacier)")
    
    # Data Flow
    hr_users >> dns >> cdn >> waf >> api
    api >> cognito
    api >> alb >> upload_lambda
    api >> alb >> search_lambda
    api >> alb >> crud_lambda
    
    upload_lambda >> s3_resumes >> queue
    queue >> process_lambda >> extract_lambda
    extract_lambda >> s3_processed
    extract_lambda >> bedrock
    bedrock >> opensearch
    extract_lambda >> comprehend >> rds
    
    search_lambda >> cache
    search_lambda >> opensearch
    search_lambda >> match_lambda >> bedrock
    match_lambda >> rds
    
    crud_lambda >> rds
    crud_lambda >> s3_resumes
    
    queue >> Edge(label="failures") >> dlq
    
    [upload_lambda, process_lambda, search_lambda, crud_lambda] >> cloudwatch
    [api, s3_resumes, rds] >> cloudtrail
    [rds, opensearch] >> secrets
    
    [s3_resumes, rds] >> s3_backup