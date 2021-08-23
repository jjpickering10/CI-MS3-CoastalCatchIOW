# [**Coastal Catch IoW**]()

_Use CTRL+click or CMD+click to open links throughout the README in a new tab_

![-](-) - image

## Overview

Coastal Catch Isle of Wight is a fishing blog/forum site that allows users to post their fishing experiences of certain locations on the island as well as ask questions for advice. Users can posts comments, give a rating to a location and favourite a post.

---

## Description

This projects showcases full CRUD functionality and consists of 4 different types of users. Those users are:
- Regular users who can only read. They can't post, like, comment, edit or delete anything.
- Logged in users who can make a post in various locations. Edit and delete their posts. Like and favourite other posts. Edit their profile and give ratings to locations.
- Guru users who can do everything a logged in user can do, but also have the privilege of being able to reply to questions in the Ask Guru section.
- Admin users who can do everything including edit and delete all posts, as well as add and edit locations and question categories, as well as change users guru status.

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

*Enjoy a visually appealing site to post and learn about fishing on the Isle of Wight*

Visiting users will be able to read the information on the site.
Registered users will be able to create, read, update and delete posts on the site.
Registered users will be able to create, read, update and delete questions on the site.
Registered users will be able to create, read, update and delete information in their profile.
Registered users will be able to like posts and favourite questions.
Registered users will be able to give a rating to locations.
Registered users will be able to visual their posts, questions and favourited posts in their profile.
Guru users will be able to do everything a registered user can, but will be able to answer specific questions.

#### Site Owner's Goals

*Provide a visually appealing place for people who enjoy fishing on the Isle of Wight*

Admin users will be able to create, read, update and delete locations.
Admin users will be able to create, read, update and delete categories.
Admin users will be able to decide who gets to be a guru user.

### **Scope**

Fits in with skillset of current programming ability.
- Which includes HTML, CSS, Javscript, Python and the use of Flask, MongoDB and some Javascript libraries.
The main focus of the site is to showcase CRUD functionality and present it in an easy to use manner.

### **Structure**

*Consistent navigation throughout site.*
*Consistent footer throughout site.*
*Logged in user has access to 'apply to be a guru' contact form.*
*Logged in guru user can has access to reply section in ask guru page.*
*Logged in admin has access to edit locations, edit categories and edit users pages.*


### **Skeleton**

- Landing Page
  - Made with [threejs](https://threejs.org/) to display pleasant visual of dark rippling ocean with moving clouds

- Locations Page
  - CSS Grid based layout with a card for each location and button to individual forum. Cards use [tilt effect](https://micku7zu.github.io/vanilla-tilt.js/).
  - Individual location page has post option for logged in users and displays posts.

- Ask Guru Page
  - Displays current guru users
  - Question form for logged in users
  - Displays posted questions and reply section for guru users

- Profile Page
  - Displays your profile, including image and description

- About Page
  - Popout modal displaying about information

- Contact Page
  - Form to contact the site with. Made functional with [EmailJS](https://www.emailjs.com/)

- Apply Guru Page
  - Form for logged in users to contact the site with, to apply to be a guru. Made functional with [EmailJS](https://www.emailjs.com/)

- Login/Register Pages
  - Displays login and register functionality

- Admin Pages
  - Additional pages for admin

### **Surface**

Colour scheme:

Mix of blues, greys and browns to match sea and sand colors.

![Color Palette](/docs/img/colorscheme.png) - color palette

Images:

Use of images are uploaded my the user to the site, or by admin for the locations images.
If images arent selected, a default image is posted.

Typography:

'Poppins' and 'Roboto' fonts are used.

Animations:

[GSAP](https://greensock.com/) animations throughout site for fluid, appealing UX experience.

---

## Features

- ***Landing Page***

Use of [ThreeJS](https://threejs.org/) for background water and clouds animation. Water object has been taken from ThreeJS library and adapted.

- ***Locations Page***

Structured using CSS Grid. Cards have tilt effect from [Vanilla Tilt JS](https://micku7zu.github.io/vanilla-tilt.js/).

Micro interaction with spinning stars on hover.

Current rating collected from database for each location is displayed in each card, along with total number of ratings. If there is no rating, a "no ratings yet" message is displayed. This is also displayed on each individual location page.

Each individual location page has an image uploaded into the database. If there is no image uploaded, a default dummy image is used.

Each individual location page has a form to rate the location for logged in users, with a display of your current rating. You can update your rating any time and the current rating, total ratings and your rating will adjust with the update in the database. Old ratings are removed for new ratings.

Each individual location page has a form for posting into each location if user is logged in. It also has the posts displayed with a heart icon for favouriting the post. If favourited, the heart icon turns to full colour, if not favourited, the icon is just the outline fill. Only logged in users can favourite a post.

Each individual location page has a collapsible toggle button showing total comments for each post as well as a reply section for logged in users.

There are two toggle buttons, one for highest rated locations which displays the current highest rated locations and one for top forums which displays the forums with the current most posts.

- ***Ask Guru Page***

Makes use of [materialize carousel](https://materializecss.com/carousel.html) feature. Each carousel item shows the guru users who have guru privileges.

Logged in users have the question form displayed.

Categories of questions are displayed with toggle buttons using Javascript to display all questions associated with each category. If there are no questions, a "no posts yet" message is displayed.

Each question has a thumbs up icon, giving users the option to like the question. Same as the heart favourite icon, if the user has liked the post, the thumbs up icon is filled, otherwise it is just outlined. Total likes from all users are displayed. Only logged in users can like.

For guru users, a reply section is displayed for each question.

Fixed toggle button in bottom right of page that pops out the top 3 most liked questions in the database.

- ***Profile Page***

Only for logged in users. Displays admin and guru status if applicable.

Displays profile image if user has uploaded an image as well as user description.

3 separate sections for users own posts, questions asked and favourited posts with collapsible toggle buttons to display each.

- ***About Page***

Pop out modal displaying text information about the site. Font awesome icons used.

- ***Contact Page***

Form with [EmailJS](https://www.emailjs.com/) and success message displayed when form is sent

- ***Apply Guru Page***

Form with [EmailJS](https://www.emailjs.com/) and success message displayed when form is sent

- ***Login/Register Pages***

Form for logging in and registering. Makes use of landing page theejs background.

- ***Admin Pages***

Admin has access to edit locations, edit categories and edit users to be able to edit and delete locations and categories as well as manage the guru status of each user.

Toggle switch for users displaying their guru status.

- ***Other Site Features***

Loading page animations using [GSAP](https://greensock.com/)

Scroll animations using [GSAP](https://greensock.com/)

Category selection for questions asked.

Location selection for each post.

Ability to upload images into database.

Search functionality on locations page and ask guru page.

Consistant theme

## Technologies Used

### Languages

[HTML5](https://en.wikipedia.org/wiki/HTML5)

[CSS3](https://en.wikipedia.org/wiki/CSS) - code written with SCSS, then compiled into CSS using Sass compiler extension in Gitpod.

[JavaScript](https://en.wikipedia.org/wiki/JavaScript)

[Python](https://en.wikipedia.org/wiki/Python_(programming_language))

### Frameworks, Libraries and Programs Used

[Materialize](https://materializecss.com/) - for responsive design and layout

[Three.js](https://threejs.org/) - for 3D water and clouds background

[Tilt.js](https://micku7zu.github.io/vanilla-tilt.js/) - for tilt effect on cards

[GSAP](https://greensock.com/) - for animations

[GitPod](https://www.gitpod.io/) - Online IDE

[Git](https://git-scm.com/) - Version Control

[Github](https://github.com/) - Where Git repositories are stored

[Balsamiq](https://balsamiq.com/) - for wireframes

[FontAwesome](https://fontawesome.com/) - for icons

[Google Fonts](https://fonts.google.com/) - for fonts

[Flask](https://flask.palletsprojects.com/en/2.0.x/) - web application framework

[Jinja](https://jinja.palletsprojects.com/en/3.0.x/) - template engine for Python

[PyMongo](https://pypi.org/project/pymongo/) - connecting MongoDB databse from Python

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

[EmailJS](https://www.emailjs.com/) - for email functionality

[MongoDB](https://www.mongodb.com/) - database

[Heroku](https://www.heroku.com/) - cloud platform service for deployment

[ThreeJS course](https://threejs-journey.xyz/) - for background water and clouds 3D effect

Code Institute Course

Code Institute Slack Community

Chrome Dev Tools

---

## Testing

- Testing can be found [here](/docs/testing/TESTING.md)

### Project Barriers and Solutions

- Issues with Gitpod deleting work. Had to rewrite a lot of code. Lesson has been learnt to regularly push to Github.

- After logging out, you could go back in the browser and still post/edit/delete. Fixed this by adding if statements to routes.

- Ask guru toggle categories functionality had issues on firefox and mobile. This was because in the script I used 'e.path'. Changed this to 'e.target'

- Due to the way the Javascript loop is written, if you change the category name this causes issues with questions being displayed. Fixed this by preventing any editing of categories. This isn't an issue as the names of these categories would not need to be edited.

### Feature To Improve

Due to time constraints there are many things I would have liked to add to improve the site. These I would like to implement in the future. They include:

- More search functionality

- More profile information

- Added CSS improvements, including small profile pic in comments section

- Dashboards throughout site

- Post notifications

- Using Flask-login. I only discovered this midway through the project

- More animations

- Preventing page reload. I tried using barbaJS, but I kept having issues with it. So I decided against it. I used GSAP animations to improve the UX by waiting until page load to view page as some images werent loaded straight away when the page opened.

---

### Known issues

- Image files uploaded don't have a unique name. So if two people upload a file with the same filename, there is an issue. This would need to be fixed in future work on the project.

- Image files uploaded can drastically slow the site down. I would have to look into this issue further when continuing on with this project. At the moment all images uploaded by myself are small so it doesn't have to much of an effect but a larger upload slows down the site. I used loading animations with GSAP to be improve the UX of this, but it can be slow.

- Page refreshing can be frustrating as it takes you away from where you were on the site.

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

CI walkthrough project helped me throughout this project.

Water effect from threeJS is used and adapted for my own style.

### Images and videos

Images have been taken by myself as I live here.

### Written Content

Written content throughout site has been provided from my father who is a keen fisherman on the island.

### Acknowledgments

- Code Institute Software Development Course - for the education.
- Code Institute Slack Community group - for the support.
- Youtube Channels: Tech with Tim, Pretty Printed, Julian Nash. 
- Bruno Simon [THREEJS course](https://threejs-journey.xyz/) - side course I have undertaken.
- My mentor [Antonio Rodriguez](https://github.com/AkaAnto) - for the guidance and support throughout.
