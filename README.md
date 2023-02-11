# Django Forum #

A small forum based on Django web framework. Forum for programmers. Designed for communication, finding answers to
various problems of the author of the post. Allows you to create questions, answers, view the profile of the
authors of questions, answers

# Built on #

* Django 4.1
* Python 3.10


# Getting started #

Clone the repository and enter into it.

``` 
$ git clone https://github.com/Mulyarchik/forum.git
$ cd forum
```

Set your settings in the ‘.env’ file, but defaults is enough just to try the service locally.

Run docker compose to build and run the service and it’s dependencies.

```
$ docker compose up -d --build
```

Optionally you can populate your database with some dummy data.

```
$ docker compose exec web python manage.py setup_test_data
```

Open in your browser:

```
http://localhost:8080/
```


# Business processes: #

![image](assets/business_processes.png)

# ERD: #

![image](assets/erd.drawio.png)


# Screenshots #

Want to see the interface of the site? Check it out!

|                           ![](assets/registration.png) Registration                           |               ![](assets/view_questions.png)   View Questions               |                         ![](assets/create_post.png)    Create Post                          |
|:---------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|
|              ![](assets/view_question_through_author.png)    View your Question               |             ![](assets/update_question.png)    Update Question              | ![](assets/leave_a_comment_through_another_user.png)   Leave a comment through another user |
| ![](assets/set_useful_status_to_answer.png)   Set comment status "was useful" via post author | ![](assets/view_thread_through_staff.png)  View Question through site Staff |         ![](assets/question_rating_up.png)   Voting a question through another user         |
|                          ![](assets/view_profile.png)  View profile                           |               ![](assets/update_photo.png)  Change User photo               |                                                                                             |
