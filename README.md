# [**Coastal Catch IoW**]()

_Use CTRL+click or CMD+click to open links throughout the README in a new tab_

![-](-) - image

## Overview

Coastal Catch Isle of Wight is a fishing blog/forum site that allows users to post their fishing experiences of certain locations on the island as well as ask questions for advice. Users can posts comments, give a rating to a location and favourite a post.

This projects showcases full CRUD functionality and consists of 4 different types of users. Those users are:
Regular users who can only read. They can't post, like, comment, edit or delete anything.
Logged in users who can make a post in various locations. Edit and delete their posts. Like and favourite other posts. Edit their profile.
Guru users who can do everything a logged in user can do, but also have the privilege of being able to reply to questions in the Ask Guru section.
Admin users who can do everything including edit and delete all posts, as well as add and edit locations and question categories.


---

## Description



---

## UX

### User Stories

First Time Visitor Goals

1. As a First Time Visitor, I want to - view various locations on the island and read about their description
2. As a First Time Visitor, I want to - be able to read posts that others have made
3. As a First Time Visitor, I want to - be able to view questions and answers
4. As a First Time Visitor, I want to - register an account
5. As a First Time Visitor, I want to - read about the site and contact the site
6. As a First Time Visitor, I want to - search the site

Returning Visitor Goals

1. As a Returning Visitor, I want to - log in to my account
2. As a Returning Visitor, I want to - reply to comments on my posts and others
3. As a Returning Visitor, I want to - edit and delete posts and comments if necessary
4. As a Returning Visitor, I want to - reply to questions if I am a guru user

Frequent User Goals

1. As a Frequent User, I want to - edit my profile
2. As a Frequent User, I want to - apply to become a guru user
3. As a Frequent User, I want to - favourite certain posts
4. As a Frequent User, I want to - like certain posts

### **Strategy**

#### External User's Goals

Visiting users will be able to read in the information on the site.
Registered users will be able to create, read, update and delete posts on the site.
Registered users will be able to create, read, update and delete information in their profile.
Guru users will be able to do everything a registered user can, but will be able to answer specific questions.


#### Site Owner's Goals

Admin users will be able to create, read, update and delete locations.
Admin users will be able to decide who gets to be a guru user.

### **Scope**

Fits in with skillset of current programming ability.
The main focus of the site is to showcase CRUD functionality and present it in an easy to use manner.

### **Structure**

Consistent navigation throughout site.
Consistent footer throughout site.
Logged in user can CRUD on posts and comment.
Logged in guru user can CRUD on posts and answer specific questions.
Logged in admin can CRUD on posts, but also manage locations.

- Landing Page
- Locations Page
- Ask Guru Page
- Profile Page
- About Page
- Contact Page
- Login/Register Pages
- Admin Pages

- Search functionality
- Category selection
- Location selection
- Upload profile images
- Consistant theme


### **Skeleton**

Navigation, including dropdown locations menu
Landing page
Locations page
Posts page
Guru page




### **Surface**

Colour scheme:

Mix of blues, greys and browns to match sea and sand colors.

![Color Palette](/docs/img/colorscheme.png) - color palette


Images:

Use of images are uploaded my the user to the site, or by admin for the locations images.
If images arent selected, a default image is posted.

Typography:

'Poppins' and 'Roboto' fonts are used.

---

## Features

- Landing Page

Use of [ThreeJS](https://threejs.org/) for background water and clouds animation. Water object has been taken from ThreeJS library and adapted.

- Locations Page

Structured using CSS Grid. Cards have tilt effect from [Vanilla Tilt JS](https://micku7zu.github.io/vanilla-tilt.js/).

Micro interaction with spinning stars on hover.

Current rating collected from database for each location is displayed in each card, along with total number of ratings. If there is no rating, a "no ratings yet" message is displayed. This is also displayed on each individual location page.

Each individual location page has an image uploaded into the database. If there is no image uploaded, a default dummy image is used.

Each individual location page has a form to rate the location for logged in users, with a display of your current rating. You can update your rating any time and the current rating, total ratings and your rating will adjust with the update in the database. Old ratings are removed for new ratings.

Each individual location page has a form for posting into each location if user is logged in. It also has the posts displayed with a heart icon for favouriting the post. If favourited, the heart icon turns to full colour, if not favourited, the icon is just the outline fill. Only logged in users can favourite a post.

Each individual location page has a collapsible toggle button showing total comments for each post as well as a reply section for logged in users.

- Ask Guru Page

Makes use of [materialize carousel](https://materializecss.com/carousel.html)] feature. Each carousel item shows the guru users who have guru privileges.

Logged in users have the question form displayed.

Categories of questions are displayed with toggle buttons using Javascript to display all questions associated with each category. If there are no questions, a "no posts yet" message is displayed.

Each question has a thumbs up icon, giving users the option to like the question. Same as the heart favourite icon, if the user has liked the post, the thumbs up icon is filled, otherwise it is just outlined. Total likes from all users are displayed. Only logged in users can like.

For guru users, a reply section is displayed for each question.

Fixed toggle button in bottom right of page that pops out the top 3 most liked questions in the database.

- Profile Page

Only for logged in users. Displays admin and guru status if applicable.

Displays profile image if user has uploaded an image as well as user description.

3 separate sections for users own posts, questions asked and favourited posts with collapsible toggle buttons to display each.

- About Page
- Contact Page

- Login/Register Pages

Form for logging in and registering.

- Admin Pages

Admin has access to edit locations, edit categories and edit users to be able to edit and delete locations and categories as well as manage the guru status of each user.

- Other site features

Category selection for each question asked.

Location selection for each post.

Ability to upload images into database.

## Technologies Used

### Languages

[HTML5](https://en.wikipedia.org/wiki/HTML5)

[CSS3](https://en.wikipedia.org/wiki/CSS)

[JavaScript](https://en.wikipedia.org/wiki/JavaScript)

[Python](https://en.wikipedia.org/wiki/Python_(programming_language))

### Frameworks, Libraries and Programs Used

[Materialize](https://materializecss.com/) - for responsive design and grid layout

[Three.js](https://threejs.org/) - for 3D water and clouds background

[Tilt.js](https://micku7zu.github.io/vanilla-tilt.js/) - for tilt effect on cards

[GitPod](https://www.gitpod.io/) - Online IDE

[Git](https://git-scm.com/) - Version Control

[Github](https://github.com/) - Where Git repositories are stored

[Balsamiq](https://balsamiq.com/) - for wireframes

[FontAwesome](https://fontawesome.com/) - for icons

[Google Fonts](https://fonts.google.com/) - for fonts

[Flask](https://flask.palletsprojects.com/en/2.0.x/) - web application framework

[Jinja](https://jinja.palletsprojects.com/en/3.0.x/) - template engine for Python

[PyMongo](https://pypi.org/project/pymongo/) - connecting MongoDB databse from Python

Werkzeug

### Resources

[ColorSpace](https://mycolor.space/) - for color palette

[CSS Tricks](https://css-tricks.com/) - for general help

[Stack Overflow](https://stackoverflow.com/) - for support

[W3Schools](https://www.w3schools.com/) - for general help

[YouTube](https://youtube.com) - for general help 

[Responsinator](http://www.responsinator.com/) - helping to test responsiveness

[TinyPNG](https://tinypng.com/) - for image compression

[CompressJPEG](https://compressjpeg.com/) - for image compression

[Am I Responsive](http://ami.responsivedesign.is/) - for responsive help and README image

[Autoprefixer](https://autoprefixer.github.io/) - adds vendor prefixes to CSS

EmailJS

MongoDB

Heroku

ThreeJS course

Code Institute Course

Code Institute Slack Community

Chrome Dev Tools

---

## Testing

- After logging out, you could go back in the browser and still post/edit/delete. Fixed this by adding if statements to routes.

First Time Visitor Goals

Returning Visitor Goals

Frequent User Goals

Other Testing

- Responsiveness

- HTML Validity

- CSS Validity

- Contrast colours

- Code cleaned up

- Spelling

- Image sizes

- CSS autoprefixer

### Project Barriers and Solutions

- Issues with Gitpod deleting work. Had to rewrite a lot of code. Lesson has been learnt to regularly push to Github.

### Feature To Improve


### Code Validity

---

## Deployment

Deployment

- Repository initially set up on Github with Code Institute template.
- Use of Gitpod for code editor.
- Deployed using the master branch.

Clone
Environment variables, gitignore, procfile, 

Heroku
MongoDB



Cloning


Forking


---

## Credits

### Code Snippets

### Images and videos

Images have been taken by myself as I live here.

### Written Content

Written content throughout site has been provided from my father who is a keen fisherman on the island.

### Acknowledgments

- Code Institute Software Development Course - for the education.
- Code Institute Slack Community group - for the support.
- Youtube Channels: Tech with Tim, Pretty Printed, 
- My mentor [Antonio Rodriguez](https://github.com/AkaAnto) - for the guidance and support throughout.
