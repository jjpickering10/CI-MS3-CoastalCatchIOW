- After logging out, you could go back in the browser and still post/edit/delete. Fixed this by adding if statements to routes.

***User Stories***
***Code Validation***
***CRUD Testing***

- # Register

Expected: user cant register if both fields arent given.

Result: Achieved.

![Result](/docs/img/register-test-validation-2.png)

Expected: user cant register if username field is not between 5-10 characters.

Result: Achieved.

![Result](/docs/img/register-test-validation.png)

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
***Navigation***
***Footer***
***Searching***
***Contact Forms***
***User Stories***
***User Stories***

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