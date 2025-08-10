#A/B Test Metrics and Fraud Filtering

This project assembles a full workflow for processing transactional data, identifying anomalous user activity, and calculating A/B test metrics on a cleaned dataset. The approach balances statistical rigor with practical data engineering, producing a framework that can be adapted to diverse experimental settings.

Purpose

The primary aim is to provide a transparent, reproducible method for:
	•	Aggregating monetary and cash-based transactions from raw logs.
	•	Flagging suspicious users through statistical outlier detection.
	•	Excluding detected anomalies before group-level metric computation.
	•	Generating key performance indicators for experimental evaluation.

Data Pipeline
	1.	Data ingestion: Raw transaction files are read in columnar format for efficiency. Separate datasets capture money movements, cash transactions, platform details, and group assignments.
	2.	Aggregation: Transactions are grouped by user and summarized to produce total amounts, counts, and unique active days.
	3.	Normalization: Behavioral counts are standardized to allow cross-comparison across variables with different scales.
	4.	Anomaly detection: Interquartile range thresholds isolate users whose activity deviates markedly from the median in multiple dimensions. Those meeting multiple criteria are flagged as potential cheaters.
	5.	Data cleaning: Flagged users are removed from subsequent analysis to preserve metric integrity.
	6.	Metric computation: Core indicators include ARPU, ARPPU, and average cash per user, computed at the experimental group level.

Statistical Rationale

The project employs non-parametric thresholds for anomaly detection, avoiding distributional assumptions that often fail in real-world behavioral data. Group metrics are computed only after data sanitization, ensuring that comparisons reflect the intended experimental treatment rather than noise introduced by fraudulent activity.

Output

The workflow produces:
	•	A cleaned dataset excluding anomalous users.
	•	A metrics table summarizing ARPU, ARPPU, and average cash for each experimental group.
	•	A CSV export for downstream reporting or visualization.

Technology
	•	Python for orchestration and analysis.
	•	Pandas for data manipulation.
	•	Parquet format for storage efficiency.
	•	CSV for final output.

Use Cases

While designed for A/B testing in a transactional environment, the logic applies to any context requiring:
	•	Behavioral anomaly detection.
	•	Group-based metric computation.
	•	Clean separation of data preparation and analysis.
