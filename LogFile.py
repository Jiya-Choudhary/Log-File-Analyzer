import collections
import os
import re
from typing import Generator, Tuple


def create_dummy_log(file_path: str) -> None:
    dummy_data = (
        "2026-07-04 10:15:30 192.168.1.50 GET /index.html 200\n"
        "2026-07-04 10:16:12 203.0.113.5 GET /admin/login 401\n"
        "2026-07-04 10:16:15 203.0.113.5 POST /admin/login 401\n"
        "2026-07-04 10:17:45 198.51.100.12 GET /images/logo.png 200\n"
        "2026-07-04 10:18:22 192.168.1.50 GET /dashboard 200\n"
        "2026-07-04 10:19:01 203.0.113.5 GET /secret-vault 403\n"
        "2026-07-04 10:20:11 198.51.100.12 GET /broken-link 404\n"
        "2026-07-04 10:21:55 192.0.2.1 GET /checkout 500\n"
        "2026-07-04 10:22:10 192.0.2.1 POST /checkout 500\n"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(dummy_data)


def log_reader(file_path: str) -> Generator[Tuple[str, str, str], None, None]:
    log_pattern = re.compile(
        r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?"
        r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?"
        r"\s(?P<status>[45]\d{2})(?:\s|$)"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = log_pattern.search(line)
            if match:
                yield (
                    match.group("timestamp"),
                    match.group("ip"),
                    match.group("status"),
                )


def generate_report(input_file: str, output_file: str) -> None:
    total_errors = 0
    ip_counter = collections.Counter()
    error_counter = collections.Counter()

    for timestamp, ip, error_code in log_reader(input_file):
        total_errors += 1
        ip_counter[ip] += 1
        error_counter[error_code] += 1

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("LOG ANALYSIS REPORT\n")
        out.write(f"Total Server Errors Found: {total_errors}\n\n")
        out.write("Error Code Distribution\n")
        for code, count in error_counter.most_common():
            out.write(f"Code {code}: {count} occurrences\n")
        out.write("\nTop Flagged IP Addresses\n")
        for ip, count in ip_counter.most_common(10):
            out.write(f"IP: {ip:<15} | Errors: {count}\n")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_log = os.path.join(current_dir, "server_test.log")
    output_report = os.path.join(current_dir, "error_summary_report.txt")

    if not os.path.exists(input_log):
        print("No log file detected. Creating 'server_test.log' automatically...")
        create_dummy_log(input_log)

    try:
        generate_report(input_log, output_report)
        print(f"Success! Summary report saved to '{output_report}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_log}' was not found.")
