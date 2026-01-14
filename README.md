# SpendLens AI Transaction Categorizer

This Python application processes unprocessed financial records from a PostgreSQL database and categorizes them using keyword matching or AI via LM Studio.

## Features

- Connects to PostgreSQL database using environment variables
- Processes records from `unprocessed_records` table
- Categorizes transactions using keyword matching or AI
- Updates records with calculated categories

## Setup

### 1. Environment Variables

Create a `.env` file in the project root with the following configuration:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password

# LM Studio Configuration
LMSTUDIO_API_BASE=http://localhost:1234/v1
LMSTUDIO_MODEL=your_model_name
```

### 2. Install Dependencies

```bash
pipenv install
```

### 3. Database Table Structure

The application expects a table named `unprocessed_records` with the following columns:

- `record_id_bank`
- `transaction_date`
- `currency_date`
- `account`
- `description`
- `amount`
- `currency`
- `category` (will be updated by the application)

### 4. Category Keywords

The application includes predefined keyword mappings for common categories:
- Food & Dining
- Transportation
- Shopping
- Entertainment
- Utilities
- Salary
- Investment
- Other

### 5. Running the Application

```bash
pipenv run python main.py
```

## How It Works

1. The application connects to your PostgreSQL database using environment variables
2. It fetches all records from `unprocessed_records` where category is NULL or empty
3. For each record, it first attempts keyword-based matching:
   - Checks if the description or account contains known keywords
4. If no keyword match is found, it queries LM Studio AI:
   - Sends the description and account to your LM Studio API
   - Uses a predefined prompt to get category classification
5. Updates the record with the determined category

## Configuration

### Database Connection

The application uses these environment variables:
- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port (default: 5432)
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password

### LM Studio Integration

The application uses these environment variables:
- `LMSTUDIO_API_BASE`: URL of your LM Studio API (default: http://localhost:1234/v1)
- `LMSTUDIO_MODEL`: Model name to use for categorization (default: your_model_name)

## Extending Categories

To add new categories or keywords:
1. Modify the `category_keywords` dictionary in `category_matcher.py`
2. Add new keywords to existing categories or create new ones

## Requirements

- Python 3.7+
- PostgreSQL client
- LM Studio API (for AI categorization)