#!/usr/bin/env python
"""
Simple script to check if Redis is running and accessible
"""
import sys

try:
    import redis
    
    # Try to connect to Redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.ping()
    
    print("✓ Redis is running and accessible!")
    print(f"  Host: localhost")
    print(f"  Port: 6379")
    print(f"  Redis version: {r.info()['redis_version']}")
    sys.exit(0)
    
except ImportError:
    print("✗ Redis package not installed")
    print("  Run: pip install redis")
    sys.exit(1)
    
except redis.ConnectionError:
    print("✗ Cannot connect to Redis")
    print("  Make sure Redis server is running:")
    print("    redis-server")
    sys.exit(1)
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

