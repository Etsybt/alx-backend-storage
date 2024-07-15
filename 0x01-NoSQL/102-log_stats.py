#!/usr/bin/env python3
"""
12-log_stats
"""
from pymongo import MongoClient


def log_stats(mongo_collection):
    """Count total logs, methods, status check, and top IPs"""

    # Count total logs
    total_logs = mongo_collection.count_documents({})

    # Count methods
    methods_count = {
        "GET": mongo_collection.count_documents({"method": "GET"}),
        "POST": mongo_collection.count_documents({"method": "POST"}),
        "PUT": mongo_collection.count_documents({"method": "PUT"}),
        "PATCH": mongo_collection.count_documents({"method": "PATCH"}),
        "DELETE": mongo_collection.count_documents({"method": "DELETE"})
    }

    # Count status check
    status_check_count = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})

    # Top IPs
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = mongo_collection.aggregate(pipeline)

    # Print results
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in methods_count.items():
        print(f"    method {method}: {count}")
    print(f"{status_check_count} status check")
    print("IPs:")
    for ip in top_ips:
        print(f"    {ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    log_stats(collection)
