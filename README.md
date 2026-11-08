# Linux Disk Growth Investigator

## Overview

A Linux monitoring application that investigates
disk usage, identifies large directories and
generates automated storage reports.

## Technologies

- Linux
- Python
- Bash
- Git
- GitHub Actions
- Docker
- Docker Hub
- AWS EC2
- Terraform

## Features

- Disk capacity monitoring
- Storage usage analysis
- Largest directory identification
- Configurable warning thresholds
- JSON report generation
- Application logging
- Automated testing
- Docker containerization
- CI/CD pipeline
- Cloud deployment

## Running locally

python3 app.py --path /

## Running tests

python3 -m unittest discover -s tests -v

## Building Docker image

docker build -t linux-disk-investigator:v1 .

## Author

Your Name