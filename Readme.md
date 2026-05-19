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

Configuration of the microservice is done using a ``.yml`` file using the env variable ``CONFIGURATION_FILE_PATH``. The configuration file allow to configure multiple data providers as well as the data use case to be used, bellow is a sample of the configuration file that can be used with the retriever microservice:
 - ``connector``: Define the data providers that will be used by the microservice.
 - ``operation``: Define the data use case to be used by the microservice.
- ``cronjob``: Define the schedule for the data use case to be executed.
- ``app_configuration``: Define the configuration of the microservice.

<details>
<summary>Configuration file example</summary>

``` yml
 connector:
  - &alpha_vantage
    name: alpha_vantage
    type: api
    base_url: https://www.alphavantage.co
    timeout: 5
    retry: 3
    auth:
      type: token
      key_name: api_token
      key_value: ${ALPHA_VANTAGE_API_KEY}

  - &yahoo_finance
    name: yahoo_finance
    type: api
    base_url: https://query1.finance.yahoo.com
    timeout: 5
    retry: 3
    auth:
      type: none

  - &local_fs
    name: local_fs
    type: file
    base_path: ./data/files
    auth:
      type: none

  - &postgres
    name: postgres
    type: database
    engine: postgres_sql
    host: ${DB_HOST}
    port: 5432
    default_name: ${DB_NAME}
    pool:
      min: 2
      max: 10
    auth:
      type: basic
      username: ${DB_USER}
      password: ${DB_PASSWORD}

  - &telemetry
      name: OpenTelemetry
      type: telemetry
      host: http://localhost
      port: 4317
      auth:
        type: none

operation:
  - &intraday_stock
    name: intraday_series
    connector: *alpha_vantage
    endpoint: /query
    method: GET
    parameters:
      function: TIME_SERIES_INTRADAY
      symbol: ["IBM"]
      interval: 5min

  - &intraday_chart
    name: yahoo_chart
    connector: *yahoo_finance
    endpoint: /v8/finance/chart
    method: GET
    parameters:
      symbol: ["IBM"]

cronjob:
  - &get_intraday_stock
    name: get_intraday_stock
    operation: *intraday_stock
    cron: "*/5 9-17 * * 1-5"

  - &get_intraday_chart
    name: get_intraday_chart
    operation: *intraday_chart
    cron: "*/5 9-17 * * 1-5"

app_configuration:
  env: debug
  run: async
  connector:
    api: {
      alpha_vantage: *alpha_vantage,
      yahoo_finance: *yahoo_finance
    }
    file: {
        local_fs: *local_fs
    }
    cache: {}
    database: {
      postgres: *postgres
    }
    telemetry: {
      open_telemetry: *telemetry
    }
  operation: {
    intraday_stock: *intraday_stock,
    intraday_chart: *intraday_chart
  }
  cronjob:
    - *get_intraday_stock
    - *get_intraday_chart
```

</details>

## Usage
...