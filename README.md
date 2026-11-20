# Backend Learning Repository

A personal repository for practicing and learning backend development through hands-on projects.

## Phase 1: Job Management API

Built a basic REST API using FastAPI and PostgreSQL.

### What I Learned
- REST API and CRUD operations
- FastAPI and Uvicorn
- PostgreSQL and SQLAlchemy
- Database models and relationships
- Pydantic validation
- Dependency injection
- Error handling
- Git and GitHub basics

## Phase 2: File Uploads and Storage

Extended the Job Management API with file upload and storage functionality.

### What I Learned
- File uploads using FastAPI
- File validation (type, extension, and size)
- UUID-based unique filenames
- Local filesystem storage
- Storing file metadata in PostgreSQL
- Retrieving file information through API endpoints

## Phase 3: Authentication and Security

Implemented user authentication and authorization using JWT.

### What I Learned
- Password hashing using Argon2
- Password verification
- JWT access token generation and validation
- OAuth2 Password Flow
- Authentication using FastAPI dependencies
- Protected API endpoints
- User authorization and resource ownership
- Securing job and file endpoints

## Phase 4: Background Processing and Message Queues

Integrated RabbitMQ and Celery to process CSV files asynchronously using background workers.

### What I Learned

**RabbitMQ**
- Message broker architecture
- Exchanges, queues, bindings, and routing keys
- Direct exchanges and message routing
- Producers and consumers using Pika
- Message acknowledgements (ACK/NACK)
- Publisher confirms and mandatory publishing
- Durable queues and persistent messages
- Dead Letter Exchanges (DLX) and Dead Letter Queues (DLQ)
- Message TTL (Time-To-Live)
- Consumer prefetch and queue monitoring

**Celery**
- Celery configuration and RabbitMQ integration
- Background task creation and execution
- Independent workers and concurrency
- Task lifecycle and acknowledgements
- Task status tracking and result storage
- Automatic retries and retry limits
- Exponential backoff and jitter
- Idempotency and duplicate task execution
- Task revocation
- Periodic tasks using Celery Beat
- Task chains, groups, and chords
- Worker monitoring, time limits, and graceful shutdown

**Application Integration and Reliability**
- Asynchronous CSV processing
- Connecting file uploads to background tasks
- Processing job tracking using PostgreSQL
- User-specific processing job access
- Retrieving processing results through API endpoints
- Testing multiple simultaneous jobs
- Failure and recovery testing
- Understanding message redelivery and delivery guarantees

### Technologies Used
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- RabbitMQ
- Celery
- Pika
- JWT
- Git and GitHub

More phases and concepts will be added as I progress.