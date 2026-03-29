# Blog App API

This is a simple Django-based Blog API that allows users to create, view, update, and delete blog posts, as well as add comments and organize posts by category. The app demonstrates efficient use of Django's ORM for related data fetching and provides a basic RESTful API for blog management.

## Endpoints

All endpoints are prefixed with `/api/`.

### Posts
- **GET /api/posts/**
  - List all blog posts.
- **POST /api/posts/**
  - Create a new blog post.
  - Body: `{ "title": string, "content": string, "category_id": int }`

- **GET /api/posts/<pk>/**
  - Retrieve a single post by its ID.
- **PUT /api/posts/<pk>/**
  - Update a post by its ID.
  - Body: `{ "title": string, "content": string, "category_id": int }`
- **DELETE /api/posts/<pk>/**
  - Delete a post by its ID.

### Comments
- **GET /api/posts/<post_pk>/comments/**
  - List all comments for a specific post.
- **POST /api/posts/<post_pk>/comments/**
  - Add a comment to a specific post.
  - Body: `{ "content": string }`

### Categories
- **GET /api/posts/category/<category_id>/**
  - List all posts in a specific category.

## Models
- **Category**: name
- **Post**: title, content, created_at, category
- **Comment**: post, content, created_at

## Notes
- All endpoints return JSON responses.
- Error handling is provided for missing or invalid data.

---

This app is intended as a learning exercise for Django RESTful API development and demonstrates efficient query usage with `select_related` and `prefetch_related` for related data.
