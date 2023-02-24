# Amazon EBS Volume Types: Overview and Comparison

## Introduction
Amazon Elastic Block Store (EBS) provides block-level storage volumes for Amazon Elastic Compute Cloud (EC2) instances. There are different types of EBS volumes available, each with different performance characteristics and costs. In this document, we will focus on four of the most commonly used EBS volumes: gp2, gp3, io1, and io2. We will describe the features of each volume type and explain which type of volume is best suited for various use cases, particularly those involving many iterations on multiple files.

## EBS Volume Types

### gp2
The gp2 volume is the default EBS volume type for Amazon EC2 instances. It is designed for general-purpose workloads, such as boot volumes and low-latency interactive applications. gp2 volumes are backed by solid-state drives (SSDs) and provide a balance of price and performance. gp2 volumes provide baseline performance of 3 IOPS per GB and burst performance of up to 3,000 IOPS for volumes larger than 3334 GB. gp2 volumes are best suited for workloads that require a balance of performance and cost, such as development and test environments, low-latency interactive applications, and small to medium databases.

### gp3
The gp3 volume is a newer version of the gp2 volume that provides more performance at a lower cost. gp3 volumes are also backed by SSDs and provide a baseline performance of 3,000 IOPS and 125 MiB/s throughput per volume. They can also provide up to 16,000 IOPS and 1,000 MiB/s throughput per volume. gp3 volumes are best suited for high-traffic and high-performance workloads that require consistent and predictable performance, such as large databases, data warehouses, and media processing workloads.

### io1
The io1 volume is designed for high-performance workloads that require low-latency and high I/O operations per second (IOPS). io1 volumes are backed by SSDs and provide the highest level of performance and reliability. io1 volumes provide baseline performance of 50 IOPS per GB and burst performance of up to 64,000 IOPS for volumes larger than 1,024 GB. io1 volumes are best suited for workloads that require high IOPS, low-latency, and high-throughput, such as critical production databases, large data warehouses, and applications with high transaction rates.

### io2
The io2 volume is the latest generation of the io1 volume and provides the highest level of performance, durability, and availability. io2 volumes are also backed by SSDs and provide baseline performance of 100 IOPS per GB and burst performance of up to 64,000 IOPS for volumes larger than 1,024 GB. io2 volumes also provide up to 2,000 MiB/s throughput per volume, making them ideal for workloads that require high throughput, such as data analytics and machine learning. io2 volumes are also designed for workloads that require high durability and availability, such as mission-critical production databases and applications.

## Conclusion
In summary, there are several EBS volume types available, each with different performance characteristics and costs. Choosing the right EBS volume type depends on the requirements of the workload. For workloads that require a balance of performance and cost, gp2 volumes are a good choice. For workloads that require consistent and predictable performance, gp3 volumes are a better choice. For workloads that require high IOPS, low-latency, and high throughput, io1 volumes are the best choice. For the most demanding workloads, such as mission-critical databases and applications, io2 volumes provide the highest level of performance, durability, and availability.


## Example Test

As an example of how EBS volumes can impact performance in practice, we conducted a timed run of the same code on an EC2 AMI running on a t2.2xlarge instance, but using different root systems. The code checks all files (RGB images) in a given path for corruption, and extracts the metadata.

We measured the time it took to list the files and extract the metadata on the same instance and image, but using different EBS volumes. The results are shown in the table below:

```
| Files | gp3 | io1 | io2 |
| 1000 RGB images | 735 | 295 | 292 |
| 3000 RGB images | 1267 | 878 | 873 |
| 10000 RGB images | 7544 | 2970 | 2968 |
```
These results demonstrate how the choice of EBS volume type can significantly impact the performance of workloads involving large numbers of files. In particular, the io2 volume consistently outperformed the other volume types, even on workloads involving tens of thousands of files.

