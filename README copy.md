[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/BFqd4mnG)

Presentation/Demo: [Youtube Link](https://youtu.be/0XGFsL46XdE) <br />
Presentation Slides: [GoogleSlides](https://docs.google.com/presentation/d/1w_oLAvUj1-ZOibbfmdnzWIG1apxlXmOWDQ2-Ymk_Ync/edit?usp=sharing)

# Project Report

Project Name: Steam DB <br />
Team: Adrian Resendez & Catherine Truong <br />

## Overview

The goal of this project is to develop a web-based analytics dashboard for SteamDB, leveraging GPU acceleration to enhance data processing and query performance. The application provides users with the ability to perform complex queries on a large dataset of video games, displaying results in an interactive and dynamic web interface.

## GPU Acceleration

The primary use of the GPU in this project is to accelerate data processing and querying operations using RAPIDS cuDF, a GPU DataFrame library designed for fast data manipulation.

## Implementation

### Frontend
The interface allows users to input queries, view results in a grid format, and monitor performance metrics. <br />
Queries are sent to the backend using AJAX, ensuring the page dynamically updates without reloading. <br />
Real-time performance metrics, including query time and memory usage, are displayed on the dashboard. <br />


### Parallel Algorithm
cuDF allows for operations such as filtering, grouping, and aggregating data to be executed on the GPU, taking advantage of its parallel processing capabilities.

### Query Execution
When a query is executed, it is processed by cuDF, which partitions the data into smaller chunks that can be processed concurrently by multiple GPU threads. This significantly reduces the time required for large-scale data operations compared to CPU-based processing. <br />
The execution of user-defined queries is parallelized, with each thread handling a part of the data filtering and transformation process. <br />
Backend: The `/query` and `/load_more` endpoints handle user queries, utilizing cuDF for data operations and returning results to the frontend. <br />

### Problem Space Partitioning
The problem space is divided into numerous threads, where each thread handles a portion of the dataset. These threads are grouped into thread blocks, allowing the GPU to manage thousands of threads efficiently.

### Data Partitioning
The dataset is partitioned into blocks of rows that can be independently processed. Each thread block processes a subset of these blocks, enabling parallel execution of the query.

### Data Loading
Data from JSON files is loaded into cuDF DataFrames on the GPU, allowing for efficient initial data setup. <br />
Backend: The data is loaded from JSON files into a pandas DataFrame, which is then converted into a cuDF DataFrame for GPU processing.


### Result Aggregation
After processing, results from different threads are aggregated to form the final query output.


## Code Instruction

1. Run the following commands in cuDF RAPIDS
   ```
   wsl -d Ubunutu
   conda activate [conda version number]
   cd backend
   python app.py
   ```

## Evaluation & Results

Queries executed on the GPU show a significant reduction in processing time compared to CPU-based queries. For example, filtering and aggregating large datasets took less than a second on the GPU, compared to several seconds on the CPU. <br />
The application effectively utilizes GPU resources, with GPU usage peaking during query execution. Real-time metrics display an average GPU utilization of 30-50% during intensive data processing tasks.

## Problems Encountered & Resolved

Data Transfer: Transferring large datasets between CPU and GPU introduced some latency. This was mitigated by keeping data resident on the GPU as much as possible. <br />
Concurrency: Handling concurrent user queries required careful management of GPU resources to avoid conflicts and ensure stable performance. <br />
Repeated IDs: IDs were not uniqure and kept reoccuring. Resolved by URL pathing.

## Summary

This project demonstrates the significant performance benefits of using GPU acceleration for data processing and querying tasks. By leveraging RAPIDS cuDF, the application achieves faster query execution and more efficient resource utilization, showcasing the potential of GPUs for large-scale data analytics.

This report covers the essential details of the project, including the use of GPU for acceleration, implementation specifics, evaluation results, and potential features for further optimization. The aim is to provide a comprehensive overview that can be expanded upon for the final presentation and submission.


## Task Breakdown

<img width="636" alt="Screen Shot 2024-06-12 at 11 40 56 PM" src="https://github.com/UCR-CSEE147/finalproject-s24-chaewon-s-carpet-cleaners/assets/93835984/d0cd5906-989e-469f-b4d8-e9f50ab3900e">



