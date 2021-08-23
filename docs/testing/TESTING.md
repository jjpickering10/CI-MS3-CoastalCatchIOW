***Code Validation***

- HTML Validity

  - All pages put through [W3C Markup Validator](https://validator.w3.org/nu/) using 'View Page Source' on webpage due to Jinja language.

  - Any errors including missing alt tags and other errors were fixed.

- CSS Validity

  - CSS validated using [W3C CSS Validation](https://jigsaw.w3.org/css-validator/)

  - No issues found.

![Result](/docs/img/css-valid.png)

- JS Validity

  - Javascript validated using [JSHint](https://jshint.com/)

  - Any errors including unused variables were fixed.

- Python Validity

  - Python validated checked with python linter extension in Gitpod.

    - Only warning is "'env' imported but unused".

  - Syntax checked with [Python Syntax Checker](https://extendsclass.com/python-tester.html)

    - No syntax errors found.

***CRUD Testing***

- # Register

Expected: user cant register if both fields arent given.

Result: Achieved.

![Result](/docs/img/register-validation.png)

Expected: user cant register if username and password fields are not between 5-15 characters and matches RegEx pattern.

Result: Achieved.

![Result](/docs/img/register-validation-2.png)

Expected: if correct information given, user can register.

Result: Achieved.

![Result](/docs/img/register-test.png)

- # Login

Expected: user CAN'T log in with incorrect username and/or password.

Result: Achieved.

![Result](/docs/img/login-validation.png)

Expected: user CAN log in with correct username and/or password.

Result: Achieved.

![Result](/docs/img/login-successful.png)

- # Posting

Expected: logged in user must fill out all post fields.

Result: Achieved.

![Result](/docs/img/post-validation.png)

Expected: logged in user can post in individual location.

Result: Achieved.

![Result](/docs/img/post-test.png)

![Result](/docs/img/post-success.png)

![Result](/docs/img/post-success-2.png)

- # Favouriting Posts

Expected: logged in user can favourite a post, displayed by filled icon.

Result: Achieved.

![Result](/docs/img/post-favourite.png)

Expected: logged in user can un-favourite a post, displayed by un-filled icon.

Result: Achieved.

![Result](/docs/img/post-unfavourite.png)

- # Editing Posts

Expected: logged in user can edit posts.

Result: Achieved.

![Result](/docs/img/edit.png)

![Result](/docs/img/post-edit-test.png)

- # Deleting Posts

Expected: logged in user can delete post with modal pop up asking for confirmation.

Result: Achieved.

![Result](/docs/img/delete-post-confirmation.png)

![Result](/docs/img/delete-test.png)

- # Questions

Expected: logged in user can ask question in ask guru page.

Result: Achieved.

![Result](/docs/img/question-success.png)

![Result](/docs/img/question-test.png)

Expected: logged in user must fill out all question fields.

Result: Achieved.

![Result](/docs/img/question-validation.png)

- # Editing Questions

Expected: logged in user can edit question.

Result: Achieved.

![Result](/docs/img/question-edit.png)

- # Deleting Questions

Expected: logged in user can delete question with modal pop up asking for confirmation.

Result: Achieved.

![Result](/docs/img/question-delete-test.png)

- # Liking Questions

Expected: logged in user can "like" a question, displayed by filled icon.

Result: Achieved.

![Result](/docs/img/question-like.png)

Expected: logged in user can un-like a question, displayed by un-filled icon.

Result: Achieved.

![Result](/docs/img/question-test.png)

- # Profile

Expected: Posts made by user shown in profile.

Result: Achieved.

![Result](/docs/img/profile-post.png)

Expected: Favorited posts for user shown in profile.

Result: Achieved.

![Result](/docs/img/fav-posts-profile.png)

Expected: Questions asked from user shown in profile.

Result: Achieved.

![Result](/docs/img/question-profile.png)

Expected: Logged in user can edit profile description and image.

Result: Achieved.

![Result](/docs/img/edit-profile.png)

- # Guru User

Expected: Guru user can reply to questions.

Result: Achieved.

![Result](/docs/img/reply-validation.png)

![Result](/docs/img/reply-test.png)

Expected: Guru user can edit replies.

Result: Achieved.

![Result](/docs/img/reply-edited.png)

Expected: Guru user delete replies.

Result: Achieved.

- # Admin User

Expected: Admin user can add/edit/delete locations.

Result: Achieved.

![Result](/docs/img/location-edit.png)

Expected: Admin user can add/delete categories. But not edit name, as this would break the Javascript loop.

Result: Achieved.

![Result](/docs/img/category-add.png)

Expected: Admin user can manage user guru status.

Result: Achieved.

![Result](/docs/img/manage-gurus.png)

![Result](/docs/img/manage-gurus-2.png)

***Responsiveness***

- Site tested on multiple screen sizes.

- Used [responsitor](https://www.responsinator.com/) to check multiple phones/tablets.

***Navigation***

- Tested all navigation links to ensure they all work, including about modal. Edit categories, edit locations and edit users links only visible to admin users.

***Footer***

- Tested all footer links to ensure they all work, including about modal. Social Media links all open in new tab.
- Apply to be guru link only visible to logged in users.

***Searching***

- Tested search function in locations page. Returned the correct results depending on the search. Location search queries locations name and description in the database. 

- Tested search function in individual locations pages. Results show only those queries that include the ID of the location.

- Tested searches without input, returns validation that it requires an input.

- Tested reset button which reloads full page.

- If there is no match. A message is displayed to the user indicating no results found. This is for both the locations page and each individual locations page.

***Contact Forms***

- Tested both apply guru form and contact form. Both need all required fields.

- Both successful form posts return notification message.

***Other***

- Tested 404 error page with URL that doesnt exist. Returns the custom 404 page.

- Logout function returns to login page.

- Clicking back in the browser after logging out will return to login page if the previous page required session data.

- Tested rating functionality. If logged in users havent rated a location. The message 'You havent rated this yet" is displayed. After successful rating. This is updated to their rating. Total rating for location is updated along with it.

- Tested that only certain links are visible to certain users, for both regular and mobile nav view.

- Tested on various browsers.

***User Stories***

### User Stories

First Time Visitor Goals - As a first time visiter:

Expected: **I want to - view various locations on the island and read about their description**

  - Tested by visiting the landing page. There is a clear call to action to view locations.

  - This then brings up all locations in individual cards with a call to action to view each.

  - This then brings up the location I wanted with it's description.

  - Result: Achieved.

Expected: **I want to - be able to read posts that others have made**

  - Tested this by viewing each location page.

  - Scrolling down the page I see the posts that have been made. I see who the post was made by and a clear call to action to view comments on the post

  - Result: Achieved.

Expected: **I want to - be able to view questions and answers**

  - Tested by visiting the landing page. There is a clear call to action to ask gurus.

  - As I scroll down the page I see several buttons with a category name. Upon clicking on each I am shown various questions related to that category.

  - The question is clear but not every question has a reply.

    - Fix: added 'no reply yet' comment to show question hasn't been answered by a guru yet

  - Result: Achieved.

Expected: **I want to - register an account**

  - Tested by visiting the landing page. The navigation has a link to register.

  - Registered following the instructions and was directed to my new profile.

  - Result: Achieved.

Expected: **I want to - read about the site and contact the site**

  - Tested by visiting the landing page. The navigation has an about link.

  - Pop up with clear text describing the site is displayed. Text also informs of contacting the site.

  - Searched the site for contact. There is a link in the footer section. Whilst it isn't displayed in the main navigation, it is common for footers to contain contact information.

  - Clicked the link and filled out the form. Was shown a 'success' message.

  - Result: Achieved.

Expected: **I want to - search the site**

  - Navigated the site and came to the locations page where a search bar is displayed. I searched several keywords and was displayed various results including a notification when nothing was found.

  - Underneath the search bar are two buttons indicating top rated locations and most popular forums. Clicking these displayed three locations for each.

  - Was able to reset with a reset button and am shown all locations again.

  - Further navigation of the site on each individual location page I am shown a search bar. Tested by searching different terms within each location. I am shown various posts relating to my searches and a notification when nothing is found.

  - Further navigation I am unable to find another search bar but in the ask guru section there are buttons to display questions under each category. There is no search bar though.

    - Fix: ***due to time constraints, some desired features aren't implemented. More search functionality would be applied to site in the future and detailed further in 'Features to improve' section in README.md***

  - Result: Achieved.


Returning Visitor Goals - As a returning visiter:

Expected: **I want to - log in to my account**

  - Tested by visiting landing page where there is a link in the navigation to login.

  - Logged in with my username and password and was shown my profile.

  - Result: Achieved.

Expected: **I want to - add, edit and delete posts, comments and questions if necessary**

  - Tested by logging in and am shown a form to make a post in each location page. Successfully posted.

  - Went to ask guru page and am shown ask question form. Posted questions under various categories.

  - Commented on various posts with the add comment form clearly displayed.

  - Was able to edit my posts, questions and comments.

  - Upon each add, edit or delete the page is refreshed.

    Fix: ***This is detailed further in README.md, further improvement would be to prevent page refreshing***

  - Result: Achieved.

Expected: **I want to - reply to comments on my posts and others**

  - Tested by viewing posts and was shown add comment form. Added a comment and was flashed successful message.

  - I could then view the post again with my comments. Same issue as above with page refreshing.

  - Result: Achieved. 

Expected: **I want to - reply to questions if I am a guru user**

  - Tested by changing account to guru account. In the ask guru section I am now shown reply form whereas before I was not. I sent a reply to a question and it is displayed, replacing the 'no reply yet' comment. My profile is also in the carousel at the top of the page.

  - Result: Achieved.

Frequent User Goals - As a frequent user:

Expected: **I want to - edit my profile**

  - Logged into my profile and am shown a default image and a clear 'edit profile' link. This takes me to a page where I can update my description about me and upload a profile picture. Upon update, my profile now shows my uploaded image and new description and as a guru user this is shown in ask guru carousel.

  - If I edit my profile again but dont choose a new image, my profile image reverts back to default image.

    Fix: ***This was fixed with adding a conditional statement in the app.py edit_profile function to check if a file was uploaded, and if not, only the description was updated which contains their old description and/or any update***

  - Result: Achieved.

Expected: **I want to - apply to become a guru user**

  - Logged in and visited ask guru section, there is a link to apply to be a guru contact page. Filled out form which has my username already in the input. Show successful message upon completing form.

  - Apply guru is visible in the footer when I am logged in. It is also mentioned in about section.

  - Result: Achieved.

Expected: **I want to - favourite certain posts**

  - Clicked heart icon on posts and the icon is now filled. It is also displayed in my profile under 'fav posts'.

  - Clicked heart icon again and the icon is now not filled. It is no longer displayed in my profile under 'fav posts'.

  - Result: Achieved.

Expected: **I want to - like certain posts**

  - Clicked thumbs up icon on question and the icon is now filled. Like count increased by 1.

  - Clicked heart icon again and the icon is now not filled. Like count decreased by 1.

  - Result: Achieved.

Other Testing

- Contrast colours

  - Colours contract well with light text on dark backgrounds and dark text on light backgrounds. Chrome tools was used throughout to judge contrast.

- Image sizes

  - Images uploaded into database have a huge impact on the site. I have reduced the file sizes for the files I have used in the site but anyone who uploads a large file would cause a decrease in performance in the site.

  - ***This is mentioned further in 'Features to improve' in README.md***
