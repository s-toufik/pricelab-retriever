# Documentation

Summary of the documentation
- [Description](#description)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

## Description
``Pricelab-retriever`` is a microservice within the PriceLab ecosystem. It's a configurable, resilient data-fetching service that retrieves financial market data from heterogeneous sources (REST APIs, databases, files) based on YAML-declared use cases, with built-in retry, circuit-breaking, and observability.

## Installation
...

## Configuration

Configuration of the microservice is done using a ``.yml`` file using the env variables:
- ``APP_ENV``: Define application environment
- ``CONFIGURATION_DIR``: Define configuration directory
- ``<api connector>_API_KEY``: Define API key for API connector
- ``DB_HOST``: Define database host
- ``DB_NAME``: Define database name
- ``DB_USER``: Define database user
- ``DB_PASSWORD``: Define database password

The configuration files allow to configure multiple data providers as well as the data use case to be used, bellow is a sample of the configuration file that can be used with the retriever microservice:
 - ``connector``: Define the data providers that will be used by the microservice.
 - ``operation``: Define the data use case to be used by the microservice.
- ``cronjob``: Define the schedule for the data use case to be executed.
- ``app_configuration``: Define the configuration of the microservice.

<details>
<summary>Configuration file example</summary>

``` yml
<env>
│ ├── connector
│ │ ├── api.yml
│ │ ├── database.yml
│ │ ├── file.yml
│ │ └── telemetry.yml
│ ├── cronjob
│ │     └── intraday_stock.yml
│ └── operation
│       └── intraday_stock.yml
└── root.yml
```

</details>

## Usage
...