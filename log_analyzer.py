
import re
from collections import Counter

LOG_FILE = "server.log"

def analyze_logs():
    total_requests = 0
    status_codes = Counter()
    ip_addresses = Counter()
    requested_urls = Counter()

    pattern = r'(\S+) - - \[.*?\] ".*? (\S+) HTTP.*?" (\d{3})'

    try:
        with open(LOG_FILE, "r") as file:
            for line in file:
                match = re.search(pattern, line)

                if match:
                    ip, url, status = match.groups()

                    total_requests += 1
                    status_codes[status] += 1
                    ip_addresses[ip] += 1
                    requested_urls[url] += 1

        print("\n===== SERVER LOG ANALYSIS =====")
        print("Total Requests:", total_requests)

        successful = sum(
            count for code, count in status_codes.items()
            if code.startswith("2")
        )

        client_errors = sum(
            count for code, count in status_codes.items()
            if code.startswith("4")
        )

        server_errors = sum(
            count for code, count in status_codes.items()
            if code.startswith("5")
        )

        print("Successful Requests:", successful)
        print("Client Errors:", client_errors)
        print("Server Errors:", server_errors)

        print("\nStatus Code Summary:")
        for code, count in sorted(status_codes.items()):
            print(code, ":", count)

        print("\nTop 3 IP Addresses:")
        for ip, count in ip_addresses.most_common(3):
            print(ip, ":", count, "requests")

        print("\nTop 3 Requested URLs:")
        for url, count in requested_urls.most_common(3):
            print(url, ":", count, "requests")

    except FileNotFoundError:
        print("Error: server.log file not found.")

analyze_logs()
