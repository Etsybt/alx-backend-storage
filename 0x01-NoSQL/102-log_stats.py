#!/usr/bin/env python3
"""
Log statistics from MongoDB collection.
"""
from pymongo import MongoClient


def count_documents(mongo_collection, query={}):
    """Count documents in a collection."""
    return mongo_collection.count_documents(query)


def count_method(mongo_collection, method):
    """Count documents with a specific HTTP method."""
    return mongo_collection.count_documents({"method": method})


def count_status_check(mongo_collection):
    """Count documents with method GET and path /status."""
    return mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})


def top_ips(mongo_collection, limit=10):
    """Return top IPs by frequency."""
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    results = mongo_collection.aggregate(pipeline)
    return {result["_id"]: result["count"] for result in results}


def main():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    total_logs = count_documents(nginx_collection)

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {
        method: count_method(
            nginx_collection,
            method) for method in methods}

    status_check_count = count_status_check(nginx_collection)

    top_ips_results = top_ips(nginx_collection)

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")
    print(f"{status_check_count} status check")
    print("IPs:")
    for ip, count in top_ips_results.items():
        print(f"    {ip}: {count}")


if __name__ == "__main__":
    main()
