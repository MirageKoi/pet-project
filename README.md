### HTTP Service Specification:

#### Endpoints:
1. **User Endpoints:**
   - `/users/`: 
     - `GET`: Retrieve all users (with pagination)
     - `POST`: Create a new user
   - `/users/{user_id}/`: 
     - `GET`: Retrieve user details
     - `PUT`: Update user details
     - `DELETE`: Delete user
   
2. **Post Endpoints:**
   - `/posts/`: 
     - `GET`: Retrieve all posts (with pagination)
     - `POST`: Create a new post
   - `/posts/{post_id}/`: 
     - `GET`: Retrieve post details
     - `PUT`: Update post details
     - `DELETE`: Delete post
   - `/posts/tags/{tag}/`: 
     - `GET`: Retrieve posts filtered by tag (with pagination)

#### Pagination:
- Pagination for both users and posts endpoints will use query parameters:
  - `page`: The page number to retrieve (default is 1)
  - `page_size`: The number of items per page (default is 10)

### Database Schema:

#### Users Table:
- `user_id`: Primary key, unique identifier for the user
- `username`: Unique username for the user
- `email`: Email address of the user (validated)
- `password_hash`: Hashed password of the user
- `password_salt`: Salt used for password hashing

#### Posts Table:
- `post_id`: Primary key, unique identifier for the post
- `user_id`: Foreign key referencing the user who created the post
- `title`: Title of the post
- `content`: Content of the post
- `created_at`: Timestamp for when the post was created
- `tags`: Tags associated with the post

### Validation Rules:

1. **Email Validation:**
   - Format: Must be a valid email address
   - Example: `user@example.com`

2. **Password Validation:**
   - Length: At least 8 characters
   - Complexity: Should contain a mix of uppercase, lowercase, numbers, and special characters

### Tech Stack:
- HTTP Service: `aiohttp` (asynchronous HTTP server)
- Database: PostgreSQL
- Database Driver: `asyncpg` (asynchronous PostgreSQL client)
- Password Hashing: `bcrypt` library for secure password hashing and salting

### Task Description:
Create a simple HTTP service for a blog application with user and post functionalities using Python. The service should use `aiohttp` for handling HTTP requests asynchronously and interact with a PostgreSQL database using `asyncpg`. Passwords for users should be securely hashed and salted using the `bcrypt` library. The service should provide CRUD operations for users and posts, support filtering posts by tags, and implement pagination for user and post retrieval endpoints. The database schema should include tables for users and posts with appropriate fields, and validation rules should be enforced for email and password fields during user creation.