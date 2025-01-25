package main

import (
	"cache-redis/handlers"
	"cache-redis/storage"
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	"github.com/go-redis/redis"
	// "github.com/go-redis/redis"
)

func main() {
	cfg := storage.Config{
		Addr:        "localhost:6385",
		Password:    "test1234",
		User:        "testuser",
		DB:          0,
		MaxRetries:  5,
		DialTimeout: 10 * time.Second,
		Timeout:     5 * time.Second,
	}

	db, err := storage.NewClient(context.Background(), cfg)
	if err != nil {
		panic(err)
	}

	// Запись данных

	// db.Set(контекст, ключ, значение, время жизни в базе данных)
	if err := db.Set("key", "test value", 0).Err(); err != nil {
		fmt.Printf("failed to set data, error: %s", err.Error())
	}

	if err := db.Set("key2", 333, 30*time.Second).Err(); err != nil {
		fmt.Printf("failed to set data, error: %s", err.Error())
	}

	// Получение данных

	val, err := db.Get("key").Result()
	if err == redis.Nil {
		fmt.Println("value not found")
	} else if err != nil {
		fmt.Printf("failed to get value, error: %v\n", err)
	}

	val2, err := db.Get("key2").Result()
	if err == redis.Nil {
		fmt.Println("value not found")
	} else if err != nil {
		fmt.Printf("failed to get value, error: %v\n", err)
	}

	fmt.Printf("value: %v\n", val)
	fmt.Printf("value: %v\n", val2)

	router := chi.NewRouter()
	router.Use(middleware.Logger)
	router.Use(middleware.Recoverer)

	router.Route("/card", handlers.NewCardHandler(context.Background(), db))

	server := http.Server{
		Addr:    ":8080",
		Handler: router,
	}

	if err := server.ListenAndServe(); err != nil {
		panic(err)
	}
}
