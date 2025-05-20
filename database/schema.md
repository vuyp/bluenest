# BlueNest Database Schema

## Users Table

| Column              | Data Type                     | Constraints                               | Description                                   |
|---------------------|-------------------------------|-------------------------------------------|-----------------------------------------------|
| `user_id`           | Auto-incrementing Integer     | Primary Key                               | Unique identifier for the user.               |
| `username`          | String                        | Unique                                    | User's chosen username.                       |
| `email`             | String                        | Unique                                    | User's email address.                         |
| `password_hash`     | String                        |                                           | Hashed password for security.                 |
| `profile_picture_url` | String                        | Optional                                  | URL to the user's profile picture.            |
| `bio`               | Text                          | Optional                                  | Short biography or description from the user. |
| `created_at`        | Timestamp                     |                                           | Timestamp of when the user account was created. |

## Posts Table

| Column        | Data Type                     | Constraints                               | Description                                     |
|---------------|-------------------------------|-------------------------------------------|-------------------------------------------------|
| `post_id`     | Auto-incrementing Integer     | Primary Key                               | Unique identifier for the post.                 |
| `user_id`     | Integer                       | Foreign Key (references Users.user_id)    | Identifier of the user who created the post.    |
| `content`     | Text                          |                                           | Textual content of the post.                    |
| `media_url`   | String                        | Optional                                  | URL to any media (image/video) attached to the post. |
| `created_at`  | Timestamp                     |                                           | Timestamp of when the post was created.         |
| `updated_at`  | Timestamp                     |                                           | Timestamp of when the post was last updated.    |

## Comments Table

| Column              | Data Type                     | Constraints                               | Description                                     |
|---------------------|-------------------------------|-------------------------------------------|-------------------------------------------------|
| `comment_id`        | Auto-incrementing Integer     | Primary Key                               | Unique identifier for the comment.              |
| `post_id`           | Integer                       | Foreign Key (references Posts.post_id)    | Identifier of the post to which the comment belongs. |
| `user_id`           | Integer                       | Foreign Key (references Users.user_id)    | Identifier of the user who wrote the comment.   |
| `parent_comment_id` | Integer                       | Foreign Key (references Comments.comment_id), Optional | Identifier of the parent comment for threading. |
| `content`           | Text                          |                                           | Textual content of the comment.                 |
| `created_at`        | Timestamp                     |                                           | Timestamp of when the comment was created.      |
| `updated_at`        | Timestamp                     |                                           | Timestamp of when the comment was last updated. |
