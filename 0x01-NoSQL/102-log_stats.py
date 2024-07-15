#!/usr/bin/env python3
"""
102-log_stats
"""
from pymongo import MongoClient


def log_stats():
    """
    counts occurrences of each IP address and
    then sorts them in descending order
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})

    print(f"{total_logs} logs")

    pipeline_methods = [
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ]
    methods = collection.aggregate(pipeline_methods)
    print("Methods:")
    method_order = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print(f"\tmethod {method['_id']}: {method['count']}")

    count_status_check = collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{count_status_check} status check")

    pipeline_ips = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    ips = collection.aggregate(pipeline_ips)
    print("IPs:")
    for ip in ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()
