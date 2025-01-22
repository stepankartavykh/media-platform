package handlers

import (
	"context"
	"net/http"
	"reflect"
	"strconv"
	"time"

	"github.com/go-chi/chi"
	"github.com/go-chi/render"
	"github.com/go-redis/redis"
)

type Card struct {
	ID   int    `json:"id" redis:"id"`
	Name string `json:"name" redis:"name"`
	Data string `json:"data" redis:"data"`
}

func GetCard(ctx context.Context, db *redis.Client) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {

		time.Sleep(3 * time.Second)

		idStr := chi.URLParam(r, "id")
		if idStr == "" {
			render.Status(r, http.StatusBadRequest)
			return
		}

		id, err := strconv.Atoi(idStr)
		if err != nil {
			render.Status(r, http.StatusBadRequest)
			return
		}

		card := Card{
			ID:   id,
			Name: "Test Card",
			Data: "This is a test card.",
		}

		// Сохраняем карточку в хранилище Redis на 30 секунд
		if err := card.ToRedisSet(ctx, db, idStr); err != nil {
			render.Status(r, http.StatusInternalServerError)
			return
		}

		render.Status(r, 200)
		render.JSON(w, r, card)
	}
}

func (c *Card) ToRedisSet(ctx context.Context, db *redis.Client, key string) error {
	// Получаем элементы структуры
	val := reflect.ValueOf(c).Elem()

	// Создаем функцию для записи структуры в хранилище
	settter := func(p redis.Pipeliner) error {
		// Итерируемся по полям структуры
		for i := 0; i < val.NumField(); i++ {
			field := val.Type().Field(i)
			// Получаем содержимое тэга redis
			tag := field.Tag.Get("redis")
			// Записываем значение поля и содержимое тэга redis в хранилище
			if err := p.HSet(key, tag, val.Field(i).Interface()).Err(); err != nil {
				return err
			}
		}
		// Задаем время хранения 30 секунд
		if err := p.Expire(key, 30*time.Second).Err(); err != nil {
			return err
		}
		return nil
	}

	// Сохраняем структуру в хранилище
	if _, err := db.Pipelined(settter); err != nil {
		return err
	}

	return nil
}

func CacheMiddleware(ctx context.Context, db *redis.Client) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {

		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			// Получаем ID карточки из URL запроса
			idStr := chi.URLParam(r, "id")
			if idStr == "" {
				render.Status(r, http.StatusBadRequest)
				return
			}

			// Делаем запрос в хранилище Redis
			data := new(Card)
			if err := db.HGetAll(idStr).Scan(data); err == nil && (*data != Card{}) {
				// Если удалось найти карточку, то возвращаем ее
				render.JSON(w, r, data)
				return
			}

			// Если карточку не удалось найти, то перенаправляем запрос на нашу API ручку
			next.ServeHTTP(w, r)
		})
	}
}

func NewCardHandler(ctx context.Context, db *redis.Client) func(r chi.Router) {
	return func(r chi.Router) {
		r.With(CacheMiddleware(ctx, db)).
			Get("/{id}", GetCard(ctx, db))
	}
}
