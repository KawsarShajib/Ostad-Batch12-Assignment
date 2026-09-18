# Blog Application (Django)

A Simple Blog Application built with Django:

-  Django Project & App 
-  Models 
-  Basic CRUD operations 
-  Django Forms 
-  Templates 
-  User Authentication 
-  Template inheritance 
-  Login/logout functionality 
-  Connecting users with their blog posts 

## Features

### User Authentication
- User Registration (username, email, password)
- User Login / Logout
- Authentication-protected pages for create/edit/delete
- Display logged-in user's name in navbar

### Blog Post CRUD
- **Create**: Authenticated users can create posts (title + content)
- **Read**: View all posts on home page, individual post details, and "My Posts"
- **Update**: Edit own posts only
- **Delete**: Delete own posts only (with confirmation)

### Profile page & profile picture
- Add profile page
- Add profile picture
- Add about me

Ownership: users cannot edit or delete posts belonging to others.

### Post Images 
- Add image field to blog posts
- Display images in post detail and home page (in the cards as thumbnail)
- Add image upload functionality in create/edit post forms

### Search Functionality
- Add search bar in navbar
- Search posts by title or content or category


### Add categories to posts
- Add category field to blog posts
- Display category in post detail and home page (in the cards)
- Add category filter functionality in home page (e.g. show all posts in a specific category)
- Add category filter functionality in "My Posts" page (e.g. show all posts in a specific category)

## Project Structure

```
blog_project/
├── blog/                 # Main app
│   ├── models.py         # BlogPost model
│   ├── forms.py          # RegisterForm, BlogPostForm
│   ├── views.py          # All views
│   ├── urls.py           # App URLs
│   ├── admin.py          # Admin registration
│   └── migrations/
├── templates/
│   ├── base.html         # Base template with navbar
│   └── blog/
│       ├── home.html
│       ├── post_detail.html
│       ├── register.html
│       ├── login.html
│       ├── create_post.html
│       ├── edit_post.html
│       ├── delete_post.html
│       └── my_posts.html
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
└── project_structure.png
```

## Setup & Run

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. Open http://127.0.0.1:8000/ 


## Login with Users created :

| Username | Password  | Notes                  |
|----------|-----------|------------------------|
| admin    | admin123  | Superuser |
| kawsar    | Sonali@123   | Sample user |
| rahim    | pass123   | Sample user |
| mirab    | User@2026   | Sample user |


## Pages

| URL                  | Description                          | Auth Required |
|----------------------|--------------------------------------|---------------|
| `/`                  | Home – list of all posts             | No            |
| `/post/<id>/`        | Post detail                          | No            |
| `/register/`         | User registration                    | No            |
| `/login/`            | Login                                | No            |
| `/logout/`           | Logout                               | Yes           |
| `/post/create/`      | Create new post                      | Yes           |
| `/post/<id>/edit/`   | Edit post (owner only)               | Yes           |
| `/post/<id>/delete/` | Delete confirmation (owner only)     | Yes           |
| `/my-posts/`         | List of current user's posts         | Yes           |
| `/admin/`            | Django admin                         | Superuser     |


## Authorization Example

- **Kawsar** creates "Lionel Messi: The Ultimate Success Story of Talent, Struggle, Failure & Greatness"
  - Kawsar: can view, edit, delete
  - Any other user (e.g. Rahim): can view only

## Technologies Used

- Python 3
- Django 6
- Django Templates + Forms
- Django Authentication System
- SQLite
- Bootstrap 5 (CDN)

## Bonus Ideas (for future implementation)

- Categories, search, pagination
- Post images
- Draft/Published status
- Comments / Likes
- Responsive improvements (already mobile-friendly via Bootstrap)
- Project demonstration video 
