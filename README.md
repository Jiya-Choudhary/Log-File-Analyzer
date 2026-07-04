# Log File Analyzer

A high-performance, memory-efficient Python script designed to parse massive server log files line-by-line. Using Python generators, the script processes gigabytes of log entries with zero memory overhead, extracts key data points using optimized regular expressions, and exports a comprehensive metrics report.

## Features

- **Memory Efficient**: Processes logs line-by-line using a streaming generator, preventing memory crashes on massive files.
- **Regex Extraction**: Automatically parses timestamps, IP addresses, and HTTP status/error codes.
- **Automated Mock Mode**: Self-generates a realistic sample log file (`server_test.log`) if no log data is present, enabling instant testing.
- **Structured Reporting**: Aggregates total occurrences, captures error code distributions, and ranks top flagged IP addresses.

## Architecture

- **`log_reader`**: Custom generator function utilizing pre-compiled regular expressions for sub-millisecond pattern matching.
- **`generate_report`**: Streaming aggregator that updates stateful high-speed counters (`collections.Counter`) without storing the log file in RAM.

## Getting Started

### Prerequisites
- Python 3.7 or higher

### Installation
Clone this repository to your local machine:
```bash
git clone https://github.com
cd log-file-analyzer
```

### Running the Analyzer
Execute the script from your terminal:
```bash
python LogFile.py
```

## How It Works

1. Upon execution, the script verifies the presence of a log file within its operational directory.
2. If absent, it initializes a sample dataset (`server_test.log`) with realistic HTTP traffic logs.
3. The generator processes each stream entity, identifying timestamps, IPs, and status codes.
4. An analytical digest is saved locally to `error_summary_report.txt`.

## Sample Output

The generated report will be saved in your directory with the following structure:

```text
LOG ANALYSIS REPORT
Total Server Errors Found: 9

Error Code Distribution
Code 200: 3 occurrences
Code 401: 2 occurrences
Code 500: 2 occurrences
Code 403: 1 occurrences
Code 404: 1 occurrences

Top Flagged IP Addresses
IP: 203.0.113.5     | Errors: 3
IP: 192.168.1.50    | Errors: 3
IP: 198.51.100.12   | Errors: 2
IP: 192.0.2.1       | Errors: 2
```

## License
Distributed under the MIT License. See `LICENSE` for more information.
