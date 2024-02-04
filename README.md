# Kafka Project Setup Guide

## Introduction

This readme is designed to help you quickly start Kafka, Zookeper and OpenSearch using Docker, and then run Python scripts for data production and consumption. Follow the steps below to get everything up and running.

## Prerequisites

Before you start, ensure you have the following installed on your system:

- Docker
- Docker Compose
- Python 3.x

Ensure Docker is running on your machine before proceeding with the next steps.

## Quick Start

Follow these commands step-by-step to setup your environment:

1. **Start Kafka and OpenSearch**:

   Open a terminal and execute the following command to start the services:

   ```bash
   docker-compose up -d
   ```

2. **Install Python Requirements**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Producer and Consumer Scripts**:

   Navigate to the scripts directory

   ```bash
   cd scripts
   ```

   Start the producer

   ```bash
   python producer.py
   ```

   Start the consumer

   ```bash
   python consumer.py
   ```

4. **Open the Dashboars and explore the data**:
   [Dashboard URL](http://localhost:5601/)
