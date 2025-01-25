package tests

import (
	"cache-redis/storage"
	"context"
	"testing"
	"time"
)

func testRedisConnection(t *testing.T) {
	cfg := storage.Config{
		Addr:        "localhost:6385",
		DB:          0,
		MaxRetries:  5,
		DialTimeout: 10 * time.Second,
		Timeout:     5 * time.Second,
	}

	_, err := storage.NewClient(context.Background(), cfg)
	if err != nil {
		panic(err.Error())
	}
}
