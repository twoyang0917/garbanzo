#!/usr/bin/env python3
import requests
import sys
import time
from concurrent.futures import ThreadPoolExecutor

def check_health(endpoint, timeout=5):
    """Check if the service is healthy"""
    try:
        response = requests.get(endpoint, timeout=timeout)
        if response.status_code == 200:
            print(f"✓ {endpoint} is responding correctly")
            return True
        else:
            print(f"✗ {endpoint} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ {endpoint} is unreachable: {str(e)}")
        return False

def load_test(endpoint, num_requests=100, concurrent=10):
    """Perform a basic load test"""
    start_time = time.time()
    results = []

    def make_request():
        try:
            response = requests.get(endpoint, timeout=10)
            return response.status_code == 200
        except:
            return False

    with ThreadPoolExecutor(max_workers=concurrent) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        results = [future.result() for future in futures]

    end_time = time.time()
    total_time = end_time - start_time
    successful = sum(results)

    print(f"\nLoad Test Results:")
    print(f"Total requests: {num_requests}")
    print(f"Successful requests: {successful}")
    print(f"Failed requests: {num_requests - successful}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Requests per second: {num_requests/total_time:.2f}")

    if successful <= num_requests:
        print(f"The service has some issues handling concurrent requests")
    else:
        print(f"Service is handling concurrent requests well")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python health_check.py <endpoint> [load_test]")
        sys.exit(1)

    endpoint = sys.argv[1]

    print(f"Checking health of {endpoint}...")
    health_result = check_health(endpoint)

    if len(sys.argv) > 2 and sys.argv[2] == "load_test":
        load_test(endpoint)

    sys.exit(0 if health_result else 1)