# Distributed Systems Project: Sports Analytics Data Pipeline

## Overview

This project focuses on the development of a data pipeline designed for sports analytics, specifically covering football, basketball, and handball. The main objective is to facilitate efficient data ingestion and processing to enable deeper insights into sports data. A significant highlight of this project, and a critical aspect of Distributed Systems, is the utilization of Kafka to manage data flow between producers and consumers, showcasing the project's emphasis on real-time data streaming rather than traditional ETL (Extract, Transform, Load) processes.

### Components

- **Producers**: Dedicated data producers for football, basketball, and handball are responsible for extracting sports data from various sources. These producers use Kafka to publish data efficiently.
- **Consumers**: Corresponding consumers for each sport consume the processed data from Kafka topics, ensuring it is ready for storage and further analysis.
- **Kafka**: Serves as the central messaging system for the data pipeline, enabling high-throughput, fault-tolerant messaging to manage the flow of data between producers and consumers effectively.
- **Storage**: The ingested data is stored in OpenSearch, an advanced search engine that supports powerful data retrieval and analysis capabilities.
- **Dashboard**: OpenSearch also provides dashboard capabilities, allowing users to inspect and visualize the data through comprehensive dashboards.

### Architecture

The data pipeline is orchestrated using Docker Compose, ensuring seamless integration and deployment of the components. The football and basketball parts of the pipeline are containerized, demonstrating the system's scalability and flexibility. In contrast, the handball component should be run locally as an example of how external or standalone components can be integrated into the pipeline. Kafka, as a central element of the architecture, facilitates the distributed data streaming capabilities necessary for real-time analytics.

### Technology Stack

- **Kafka**: For messaging and data streaming between producers and consumers.
- **OpenSearch**: For data storage and visualization.
- **Docker Compose**: For orchestration of the pipeline components.
- **Producers/Consumers**: Custom-built services tailored for each sport's data processing needs, integrated with Kafka for real-time data handling.

## Getting Started

To get started with the sports analytics data pipeline, ensure Docker, Docker Compose, and Kafka are installed on your system. After installing the prerequisites, clone this repository and use Docker Compose to build and run the pipeline:

```
git clone [repository-url]
cd [repository-directory]
docker-compose up --build
```

For running the handball producer locally and integrating it with Kafka:

```
cd scripts/handball/producer
python handball_producer.py
```

For the handball consumer, in another terminal window:

```
cd scripts/handball/consumer
python handball_producer.py
```

### Dashboard Access
After the pipeline is operational, access the OpenSearch Dashboard to visualize the data. Navigate to http://localhost:5601 (or the configured port) in your web browser to explore the dashboards and analytics features.

# Authors
- Aleksandar Radulovski 201518
- Kosta Dimitrovski 202029
- Mario Petkoski 201534
