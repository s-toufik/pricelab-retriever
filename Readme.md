# Documentation

## Summary
- [Description](#description)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Environment Variables](#environment-variables)
    - [Configuration Structure](#configuration-structure)
    - [Configuration Example](#configuration-example)
- [Usage](#usage)

---

# Description

`pricelab-retriever` is a microservice within the PriceLab ecosystem.

It is a configurable and resilient data retrieval service designed to fetch financial market data from heterogeneous data sources. The service operates using YAML-defined configurations and use cases, enabling dynamic orchestration of data ingestion workflows.

## Core Features

- Multi-source data retrieval
- Scheduling with cron jobs
- Extensible operation pipeline

---

# Installation

... TBD

## Run the Application

... TBD

---

# Configuration

The microservice is configured using YAML (`.yml`) files combined with environment variables.

---

## Environment Variables

The following environment variables are supported:

| Variable                   | Description                              |
|----------------------------|------------------------------------------|
| `APP_ENV`                  | Defines the application environment      |
| `CONFIGURATION_DIR`        | Defines the root configuration directory |
| `<CONNECTOR_NAME>_API_KEY` | API key used by a specific API connector |
| `DB_HOST`                  | Database host                            |
| `DB_PORT`                  | Database port                            |
| `DB_NAME`                  | Database name                            |
| `DB_USER`                  | Database username                        |
| `DB_PASSWORD`              | Database password                        |

---

## Configuration Structure

The configuration directory is organized as follows:

| Directory            | Description                                         |
|----------------------|-----------------------------------------------------|
| `connector/`         | Defines data source connectors                      |
| `operation/`         | Defines retrieval operations and business use cases |
| `cronjob/`           | Defines scheduled jobs                              |
| `root.yml`           | Root application configuration                      |

### Configuration Concepts

#### Connector

Defines the data providers used by the microservice.

Examples:
- REST API connectors
- Database connectors
- File connectors

#### Operation

Defines a business-oriented data retrieval workflow.

Examples:
- Intraday stock retrieval
- Historical market synchronization
- Portfolio enrichment

#### Cronjob

Defines scheduled execution rules for operations.

Examples:
- Every minute
- Hourly synchronization
- Daily market close refresh

---

## Configuration Example

<details>
<summary>Example directory structure</summary>

```text
<env>/
├── connector/
│   ├── api.yml
│   ├── database.yml
│   ├── file.yml
│   └── telemetry.yml
├── cronjob/
│   └── intraday_stock.yml
├── operation/
│   └── intraday_stock.yml
└── root.yml
```

</details>

---

## Example Connector Configuration

```yaml
connector:
  alpha_vantage:
    name: alpha_vantage
    type: api
    base_url: https://www.alphavantage.co
    timeout: 5
    retry: 3
    auth:
      type: token
      key_name: apikey
      key_value: ${oc.env:ALPHA_VANTAGE_API_KEY}
```

---

## Example Operation Configuration

```yaml
operation:
  alpha_vantage_intraday_stock:
    name: intraday_stock
    connector: ${connector.alpha_vantage}
    endpoint: /query
    method: GET
    parameters:
      function: TIME_SERIES_WEEKLY
      symbol: APL, IBM, MSFT, GOOG
```

---

## Example Cronjob Configuration

```yaml
cronjob:
  get_intraday_stock:
    name: get_intraday_stock
    operation: ${operation.alpha_vantage_intraday_stock}
    cron: "*/5 9-17 * * 1-5"
```

---

# Usage

## Start the Service

... TBD

## Specify Environment

```bash
export APP_ENV=dev
export CONFIGURATION_DIR=./config
...
```

## Example Execution Flow

```text
                  +----------------------+
                  |      Cron Jobs       |
                  +----------+-----------+
                             |
                             ▼
                  +----------------------+
                  |      Operations      |
                  +----------+-----------+
                             |
          +------------------+------------------+
          |                  |                  |
          ▼                  ▼                  ▼
+----------------+  +----------------+  +----------------+
| REST Connector |  | DB Connector   |  | File Connector |
+----------------+  +----------------+  +----------------+
          |                  |                  |
          +------------------+------------------+
                             |
                             ▼
                  +----------------------+
                  | Resilience Layer     |
                  | - Retry              |
                  | - Circuit Breaker    |
                  | - Timeout            |
                  +----------+-----------+
                             |
                             ▼
                  +----------------------+
                  | Observability        |
                  | - Logs               |
                  | - Metrics            |
                  | - Traces             |
                  +----------------------+
```