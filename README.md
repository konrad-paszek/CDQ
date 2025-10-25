# CDQ Python

CDQ Python is a monorepo of loosely connected Python packages designed to solve reporting system challenges in our data analytics workflow.

## Overview

This system allows clients to query MongoDB databases, transform data, and export results as Excel or CSV files through both interactive and automated workflows.

### Quick Start Example

```python
import cdq.analytics.reporting as reporting

client = reporting.client()
req = reporting.request(
    report_id='business_partner_report',
    title='Business Partner Report',
    storage_id='storage_one',
    format='xlsx'
)
res = client.submit(req)
res.to_dict()
```

### Integration with Airflow

The reporting system can be executed in interactive environments (IPython/Jupyter notebooks) or automated through Airflow DAGs:

```python
import pendulum
from airflow.sdk import dag, task
from cdq.analytics.reporting.job import ReportingJob, REPORTING_JOB_PARAMS

@dag(
    dag_id='reporting_job',
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz='UTC'),
    default_args={'retries': 1},
    params=REPORTING_JOB_PARAMS
)
def reporting_job():
    @task()
    def run_job(context):
        params = context.dag_run.params
        job = ReportingJob(params)
        return job.execute()
    
    run_job()

reporting_job()
```

## Development Challenge

This code was developed as a rapid prototype and requires refinement from an experienced developer before production deployment.

### Key Issues to Address

The following are the most critical problems that need attention:

- **Missing API Endpoint**: The analytics API `reportingJob/create` endpoint is not implemented. Our CEO has already attempted to call `https://localhost:8081/reportingJob/create`

- **Memory Management**: The data processing module has memory management issues

- **Testing Coverage**: The TDD approach was abandoned early in development

- **CLI Module**: Missing analytics CLI module. Our data analyst needs to execute:
  ```bash
  cdq-python analytics report-generate DUMP_REPORT --format --title="I feel good"
  ```

- **Report Enhancements**: Product Owner requests for the `business_partner_report`:
  - Add VAT numbers to existing business partner report
  - Create a new report `business_partners_count_by_country` showing business partner distribution by country

- **Code Quality**: Several modules require refactoring and cleanup

## Getting Started

### Prerequisites

Before diving into development, familiarize yourself with the codebase:

- **Code Exploration**: Read through the codebase to understand component relationships
- **Interactive Testing**: Use IPython/Jupyter sessions to generate reports and inspect objects
- **API Server**: Start the API server and explore endpoints with `make api`
- **Test Data**: Review and understand the test dataset structure
- **Infrastructure**: Launch supporting services with `docker compose -f docker-compose/stack.yaml up`
- **Database Setup**: Seed the database using `CDQ__CORE__NODE=.env pytest --seed`

### Development Guidelines

Here are some practical guidelines for working on this solution:

- **Security**: As we trust our users, security considerations are not a primary concern
- **DevOps**: Our DevOps team is very helpful and readily deploys Dockerfiles
- **Architecture**: Our distributed system keeps backend and frontend in the same address space
- **Dependencies**: Project dependencies are non-negotiable (required for Airflow compatibility)
- **Code Hints**: Look for comments starting with `FIXME`, `TODO`, or `NOTE` for guidance
- **Scope**: Feel free to address issues beyond the listed problems
- **Originality**: We value your original solutions over AI-generated code

## Development Commands

### Environment Setup

**Install dependencies:**
```bash
uv sync --dev
```

**Activate virtual environment:**
```bash
source .venv/bin/activate
```

### Running the Application

**Start IPython session:**
```bash
CDQ__CORE__NODE=.env ipython
```

**Start API server:**
```bash
make api
```

**Run tests and seed database:**
```bash
make test
```

## Final Notes

### Expectations and Approach

- **Focus over Completeness**: Don't aim for a fully complete solution—partial implementations are acceptable
- **Time Management**: You control the scope and duration of your work
- **Problem Selection**: Choose which issues to tackle based on your interests and strengths  
- **Independence**: We're seeking developers who can navigate projects with minimal guidance
- **Assessment**: This exercise evaluates your ability to jump into existing codebases and make meaningful contributions

### How to Submit Your Solution

1. **Download the ZIP file**: Start by downloading the provided ZIP file, which contains all the necessary files and folders for your project, including a `README.md` with instructions and task description. Please note that this ZIP file is not a Git repository; it serves as the foundation for your work. After downloading, extract the contents using a file extraction tool to create a folder on your computer with all the included files. Initialize your own Git repository within this folder using `git init`, incorporating the extracted files as your starting point for developing your solution.
2. **Develop Your Solution**: Implement your changes and improvements using the files from the extracted folder as your base, referring to the `README.m`d for guidance on the task requirements.
3. **Commit Your Work**: Make regular commits with clear, descriptive messages
4. **Package or Upload Your Results**: Once you have completed your solution, you can either package the repository into a new ZIP file or upload it to your own GitHub account.
5. **Submit Your Results**: Send the new ZIP file containing your solution to the CDQ HR team, or share the link to your GitHub repository with us.

### What to Include

- Your code changes and implementations
- A brief summary of what you accomplished and your approach (optional but recommended)

**Important**: Work on your fork and ensure all changes are committed and pushed before submitting the repository link.

---

**Good luck!** 🚀
