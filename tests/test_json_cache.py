"""
Tests for unified JSON caching utility.

Tests JsonFileCache, JsonCacheManager, and decorator patterns.
"""

import json
import tempfile
import time
from pathlib import Path

import pytest

from project_management_automation.utils.json_cache import (
    JsonCacheManager,
    JsonFileCache,
    json_file_cache,
)


class TestJsonFileCache:
    """Test JsonFileCache class."""

    def test_basic_caching(self):
        """Test basic file caching with mtime invalidation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = {"key": "value", "number": 42}
            json.dump(test_data, f)
            temp_path = Path(f.name)

        try:
            cache = JsonFileCache(temp_path)

            # First load - should load from file
            data1 = cache.get_or_load()
            assert data1 == test_data

            # Second load - should use cache
            data2 = cache.get()
            assert data2 == test_data

            # Verify cache hit
            stats = cache.get_stats()
            assert stats["hits"] >= 1
            assert stats["misses"] >= 1

        finally:
            temp_path.unlink()

    def test_mtime_invalidation(self):
        """Test cache invalidation on file modification."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"version": 1}, f)
            temp_path = Path(f.name)

        try:
            cache = JsonFileCache(temp_path)

            # Load initial data
            data1 = cache.get_or_load()
            assert data1["version"] == 1

            # Modify file
            time.sleep(0.1)  # Ensure mtime changes
            with open(temp_path, 'w') as f:
                json.dump({"version": 2}, f)

            # Cache should be invalidated
            data2 = cache.get_or_load()
            assert data2["version"] == 2

            stats = cache.get_stats()
            assert stats["invalidations_mtime"] >= 1

        finally:
            temp_path.unlink()

    def test_ttl_expiration(self):
        """Test TTL-based cache expiration."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"data": "test"}, f)
            temp_path = Path(f.name)

        try:
            # Cache with 1 second TTL
            cache = JsonFileCache(temp_path, ttl=1)

            # Load data
            data1 = cache.get_or_load()
            assert data1["data"] == "test"

            # Should still be cached
            data2 = cache.get()
            assert data2 is not None

            # Wait for TTL expiration
            time.sleep(1.1)

            # Cache should be expired
            data3 = cache.get()
            assert data3 is None

            stats = cache.get_stats()
            assert stats["invalidations_ttl"] >= 1

        finally:
            temp_path.unlink()

    def test_file_not_found(self):
        """Test handling of missing files."""
        temp_path = Path("/nonexistent/file.json")

        cache = JsonFileCache(temp_path, default_value={})

        # Should return default value
        data = cache.get_or_load()
        assert data == {}

    def test_manual_invalidation(self):
        """Test manual cache invalidation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"data": "test"}, f)
            temp_path = Path(f.name)

        try:
            cache = JsonFileCache(temp_path)

            # Load and cache
            cache.get_or_load()

            # Manually invalidate
            cache.invalidate()

            # Cache should be empty
            assert cache.get() is None

            stats = cache.get_stats()
            assert stats["invalidations"] >= 1

        finally:
            temp_path.unlink()

    def test_statistics(self):
        """Test cache statistics collection."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"data": "test"}, f)
            temp_path = Path(f.name)

        try:
            cache = JsonFileCache(temp_path, enable_stats=True)

            # Generate some cache activity
            cache.get_or_load()  # miss
            cache.get()  # hit
            cache.get()  # hit
            cache.invalidate()

            stats = cache.get_stats()
            assert stats["hits"] == 2
            assert stats["misses"] >= 1
            assert stats["invalidations"] >= 1
            assert stats["hit_rate"] > 0

        finally:
            temp_path.unlink()


class TestJsonCacheManager:
    """Test JsonCacheManager singleton."""

    def test_singleton(self):
        """Test that manager is a singleton."""
        manager1 = JsonCacheManager.get_instance()
        manager2 = JsonCacheManager.get_instance()

        assert manager1 is manager2

    def test_get_cache(self):
        """Test getting cache for file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"data": "test"}, f)
            temp_path = Path(f.name)

        try:
            manager = JsonCacheManager.get_instance()

            cache1 = manager.get_cache(temp_path)
            cache2 = manager.get_cache(temp_path)

            # Should return same cache instance
            assert cache1 is cache2

        finally:
            temp_path.unlink()

    def test_invalidate_file(self):
        """Test invalidating specific file cache."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"data": "test"}, f)
            temp_path = Path(f.name)

        try:
            manager = JsonCacheManager.get_instance()

            cache = manager.get_cache(temp_path)
            cache.get_or_load()

            # Invalidate via manager
            manager.invalidate_file(temp_path)

            # Cache should be empty
            assert cache.get() is None

        finally:
            temp_path.unlink()

    def test_get_all_stats(self):
        """Test getting statistics for all caches."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"data": "test"}, f)
            temp_path = Path(f.name)

        try:
            manager = JsonCacheManager.get_instance()

            cache = manager.get_cache(temp_path)
            cache.get_or_load()

            all_stats = manager.get_all_stats()
            assert len(all_stats) >= 1
            assert str(temp_path.absolute()) in all_stats

        finally:
            temp_path.unlink()


class TestJsonFileCacheDecorator:
    """Test json_file_cache decorator."""

    def test_decorator_basic(self):
        """Test basic decorator usage."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"data": "test"}, f)
            temp_path = Path(f.name)

        try:
            @json_file_cache(file_path=temp_path)
            def load_data():
                with open(temp_path) as f:
                    return json.load(f)

            # First call - loads from file
            data1 = load_data()
            assert data1["data"] == "test"

            # Second call - uses cache
            data2 = load_data()
            assert data2["data"] == "test"

            # Verify cache is attached
            assert hasattr(load_data, '_cache')

        finally:
            temp_path.unlink()

    def test_decorator_with_ttl(self):
        """Test decorator with TTL."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"data": "test"}, f)
            temp_path = Path(f.name)

        try:
            @json_file_cache(file_path=temp_path, ttl=1)
            def load_data():
                with open(temp_path) as f:
                    return json.load(f)

            # Load data
            data1 = load_data()
            assert data1["data"] == "test"

            # Wait for TTL expiration
            time.sleep(1.1)

            # Should reload (cache expired)
            data2 = load_data()
            assert data2["data"] == "test"

        finally:
            temp_path.unlink()
