
Introducing Quizapp! Quizapp is a web application in which users can create and take quizzes, competing against other users on the app! 


Distinctiveness and Complexity:

I believe my project satisfies the distinctiveness requirement as it does not appear to be similar to any of the 5 previous projects. It is distinct from Project 0 (Search) as it does not have any type of search functionality; it is distinct from Project 1 (Wiki) as it is not disgned as a Wikipedia-like online encyclopedia; it is distnict from Project 2 (Commerce) as it does not appear to and does not function like an e-commerce site; it is distinct from Project 3 (Mail) as it does not send and recieve any mail between users. Although there are few slight similarities to Project 4 (Network), I believe that it is more than distinct enough from it with the main focus being on quiz taking. 

I believe my project satisfies the complexity requirement as it is and more complex than all other projects in this course. It is more compledx than Project 0 (Search) as it uses Django and JavaScript to create a full-fledged web application; it is more complex than Project 1 (Wiki) as it makes more use of Django Models, JavaScript, and APIs; it is more complex than Project 2 (Commerce) as it, again, makes more use of Django models and JavaScript; it is more complex than Project 3 (Mail) as it contains more functions/uses and has more complex ajax request functions; finally, it is more complex than Project 4 (Network) as it uses more complex ajax POST and GET requests and uses multiple JS files to make more dynamic pages.


How to run Quizapp:
    To run Quizapp, open up a new terminal window, cd into the main directory of the app, and run "python3 manage.py runserver". Once doing this, enter the url given into a browser and get started!

Python Files and what's contained in each:

    models.py:

        The models.py file contains 6 models: User, Follower, Quiz, Final, Question, and Answer.

        The User model uses Django's AbstractUser parameter to create a default user. I included 2 new functions within the model which allow users to follow/unfollow other users.

        The Follower model contains two attributes: following, which defines who the user is following, and follower, which defines the user that is the follower. I also included a Meta class to ensure that the values must be unique.

        The Quiz model contains 10 attributes: the creator of the quiz, the name of the quiz, the subject, the amount of questions, time allotted, score to pass, difficulty (which references the choices of easy, medium, or hard), the time the quiz was created, and who scored the highest and what score they got. I also implemented a getQuestions function that returns in an array all the questions of the quiz.

        The Final model contains the results of each quiz taken by a user. It contains 3 attributes: the user who took the test, the score they got, and what quiz they took. 

        The Question model contains 3 attributes: the quiz that the question is for (I used a foreign key relation to define this), the question itself and its contents, and the time the question was created. I also implemented a getAnswer function that returns all the answer choices to the given question.

        The Answer model contains 4 attributes: the answer itself and its contents, a boolean field that defines if it is correct, the question that it relates to (I used a foriegn key relation to define this), and the time the answer was created.

    urls.py (capstone):

        The urls.py file in the capstone folder contains the basic capstone URL Configuration. The only change I made to this file was the implementation of a url path to my app.

    urls.py (quizapp):

        The urls.py file in the quizapp folder contains all the url configurations and paths inside my app. For example, the "/quizlist" path directs the user to a quiz list via the quizlist functuon in the views.py file.

    views.py:

        The views.py file contains 14 different functions. The majority of these just essentially redirects the user to a new html view. The most complex view is save, which takes the data from the AJAX request and calculates and updates scores.

    admin.py:

        The admin.py file registers every model into the django admin interface.


HTML Files and what's contained in each:

    following.html:
        This html file displays, in a stylized format, all the quizzes of the users that the current logged in user is following.

    index.html:
        This html file displays the welcome/introduction page, which informs the user about the app.

    layout.html:
        This html file includes the layout that is used in every other html file. It includes a navbar that is used to navigate throughout the application.

    login.html:
        This html file displays the login page, in which users can log in to their account using their username and password.

    myquizzes.html:
        This html file displays the current logged in user's profile page, showing all of the quizzes that the user has created.

    newquiz.html:
        This html file displays the form that creates a new quiz when filled correctly. It loads a static JS file as well to dynamically add questions to the quiz.

    quiz.html:
        This html file shows the display when a user is taking a quiz. The html data that fills up the divs are creatd dynamically in a static JS file, quiz.js.

    quizlist.html:
        This html file displays a styled list of all quizzes currently registered on the app. Clicking on one of these quizzes will redirect the user to take the quiz, and clicking on the username of the quiz will redirect the user to the creator's quiz profile.

    register.html:
         This html file displays the regsister page, in which users can create an account using their username, password, and email.

    taken.html:
        This html file displays a styled list of every quiz that the logged in user has taken, as well as displays their highest score in them.

    dne.html:
        This html file displays an error message, which the user is redirected to if a quiz or page does not exist.

CSS Files and what's contained in each:
    
    styles.css: 
        This CSS file is quite small, but defines a few style properties that are referenced throughout the application.

JavaScript Files and what's contained in each:

    newquiz.js:
        This JS file defines a function to dynamically create the question and answer labels on the newquiz.html page.

    quizlist.js:
        This JS file programs the dynamic display of the quiz information on the modal for each quiz when clicked.

    quizview.js:
        This JS file is for the quiz.html file. The timer functionality is coded here as well as the AJAX requests to get the quiz questions and display/save the results.

