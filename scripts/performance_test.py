#!/usr/bin/env python3
import requests
import time
import statistics
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def measure_latency(endpoint, num_requests=50):
    """Measure request latency"""
    latencies = []

    for i in range(num_requests):
        start_time = time.time()
        try:
            response = requests.get(endpoint, timeout=5)
            if response.status_code == 200:
                latency = (time.time() - start_time) * 1000  # Convert to ms
                latencies.append(latency)
            else:
                print(f"Request {i+1} failed with status {response.status_code}")
        except Exception as e:
            print(f"Request {i+1} failed: {str(e)}")

    if not latencies:
        print("No successful requests to analyze")
        return None

    average_latency = statistics.mean(latencies)
    min_latency = min(latencies)
    max_latency = max(latencies)
    median_latency = statistics.median(latencies)

    print(f"\nLatency Analysis ({len(latencies)} successful requests):")
    print(f"Average: {average_latency:.2f}ms")
    print(f"Min: {min_latency:.2f}ms")
    print(f"Max: {max_latency:.2f}ms")
    print(f"Median: {median_latency:.2f}ms")

    # Performance recommendations
    if average_latency > 1000:
        print("⚠️  Latency is high (>1s). Consider checking server resources.")
    elif average_latency > 500:
        print("⚠️  Latency is moderate (>500ms). Monitor closely.")
    else:
        print("✓ Latency is acceptable (<500ms).")

    return latencies

def stress_test(endpoint, duration=30):
    """Run a stress test for a specified duration"""
    print(f"\nRunning stress test for {duration} seconds...")

    requests_sent = 0
    requests_succeeded = 0
    errors = []
    start_time = time.time()

    def make_request():
        try:
            return requests.get(endpoint, timeout=5).status_code == 200
        except Exception as e:
            return False

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []

        while time.time() - start_time < duration:
            if len(futures) < 100:  # Limit queue size
                futures.append(executor.submit(make_request))
                requests_sent += 1

            # Check completed futures
            done = [f for f in futures if f.done()]
            for future in done:
                if future.result():
                    requests_succeeded += 1
                futures.remove(future)

            time.sleep(0.01)  # Small delay to prevent overwhelming

        # Wait for remaining futures
        for future in as_completed(futures):
            if future.result():
                requests_succeeded += 1

    success_rate = (requests_succeeded / requests_sent) * 100 if requests_sent > 0 else 0

    print(f"\nStress Test Results:")
    print(f"Duration: {duration}s")
    print(f"Requests sent: {requests_sent}")
    print(f"Requests succeeded: {requests_succeeded}")
    print(f"Success rate: {success_rate:.1f}%")

    if success_rate < 95:
        print("⚠️  Low success rate detected. The service may struggle under load.")
    else:
        print("✓ Good success rate under stress.")

def main():
    parser = argparse.ArgumentParser(description='Performance testing tool for garbanzo service')
    parser.add_argument('endpoint', help='Service endpoint URL')
    parser.add_argument('--latency', type=int, default=50, help='Number of latency test requests')
    parser.add_argument('--stress', type=int, default=30, help='Stress test duration in seconds')
    parser.add_argument('--skip-stress', action='store_true', help='Skip stress test')

    args = parser.parse_args()

    print(f"Performance testing {args.endpoint}...\n")
    measure_latency(args.endpoint, args.latency)

    if not args.skip_stress:
        stress_test(args.endpoint, args.stress)

if __name__ == "__main__":
    main()