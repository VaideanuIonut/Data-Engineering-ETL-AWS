🚀 ETL Pipeline: GitHub Data to AWS RDS (PostgreSQL)
This project demonstrates a full Extract, Transform, Load (ETL) workflow built in Python to ingest public user data from the GitHub API and persist it in a structured PostgreSQL database hosted on AWS RDS. This project validates key skills in Cloud integration, data cleaning, and data persistence.

The core technologies used are Python, Pandas (for transformation), SQLAlchemy (for connectivity), and AWS RDS (as the cloud database target).

🏗️ Project Flow
The pipeline executes a modular, end-to-end data flow defined in pipeline.py:

Extract (E): Fetches the raw user profile JSON data from the GitHub API using the requests library.

Transform (T): Converts the JSON into a Pandas DataFrame, cleans null values, selects key columns (login, followers, etc.), and enforces a proper schema.

Load (L): Establishes a secure connection to the AWS RDS PostgreSQL instance using SQLAlchemy and loads the clean data into the github_users table.

✅ Validation and Outcome
The pipeline's success is validated through two key proofs: the correct cloud infrastructure setup and the final data integrity check.
![]

☁️ AWS Infrastructure Proof
The data target is a PostgreSQL instance configured on AWS RDS. This screenshot confirms the engine type and successful cloud setup:

![AWS_proof](</aws_postgresql_instance_proof.png>)

📊 Data Integrity Check
The successful outcome of the ETL process is confirmed by viewing the clean, transformed data directly in the github_users table via the DBeaver SQL client.

![Proof from DBeaver](</db_data_proof.png>)

🐳 Containerization (Docker)
The entire ETL workflow is containerized using Docker to ensure reproducibility across any environment. This demonstrates proficiency in packaging and deploying Data Engineering code.

The Dockerfile uses Python 3.11-slim as a base and installs dependencies listed in requirements.txt.

The pipeline is run within an isolated container environment.

🛠️ Setup (For Replication)
To replicate this project, you need Docker Desktop installed and an AWS RDS PostgreSQL instance.

1. Update Credentials 
Before building, you must update the placeholder credentials in the load_data_to_sql function of pipeline.py with your actual AWS RDS details.

2. Build the Docker Image
Navigate to the project directory and build the image:
  `docker build -t github-etl-pipeline .`
3. Run the Containerized Pipeline
Execute the ETL workflow inside the Docker container:
  `docker run github-etl-pipeline`