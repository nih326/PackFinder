# Testing

We are primarily using unit testing to validate our software functionalities. Unit Testing tests individual components or units of the software. The tests are present in the "/src/tests" folder and are triggered using GitHub actions ("Unit_Tests.yml") whenever there is a push/pull request in the repository. 

If you need to run the test in your local system, use the following commands:

```
cd src
python manage.py test 
```

There are four test files for our software. They are:

#### 1. [test_url.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_url.py):
Test code to validate the URLs of the web application. This tests whether the functionalities are mapped to their respective URLs. Tests the URLs of 'Homepage', 'My People', 'Find Room', 'My Room', and 'LogOut'.

#### 2. [test_model.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_model.py):
Test code that creates a user object and checks if the values are correctly stored in the attributes.

#### 3. [test_views.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_views.py):
Test code to check if the HTTP request was succesful (based on the status code).

#### 4. [test_utils.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_utils.py):
Test code that validates the Email ID (checks if it is has a NCSU Email ID). 

#### 5. Live Server Test Demo:
Test code for live server test for Profile Edit Page and Profile Page. In order to run the test rename the 'liveserver.py' file to 'test_liveserver.py'.

https://user-images.githubusercontent.com/46688470/194781203-4a78dfb7-ee8a-480c-a8e6-7773f6479128.mp4
#### 6. [test_about.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_about.py):
Tests the rendering of the about page.

#### 7. [test_agreement.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_agreement.py):
Tests the rendering of the roommate agreement.

#### 8. [test_campuslife.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_campuslife.py):
Tests the functionalities on campus life forum page.

#### 9. [test_chat.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_chat.py):
Tests the functionalities of chat room.

#### 10. [test_communityforum.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_communityforum.py):
Tests the functionalities on community forum page.

#### 11. [test_findpeople.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_findpeople.py):
Tests the functionalities on findpeople page.

#### 12. [test_housing_tips.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_housing_tips.py):
Tests the functionalities on Housing Tips forum page.

#### 13. [test_howlalert.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_howlalert.py):
Tests the howl alert functionality.

#### 14. [test_login.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_login.py):
Tests the login functionality.

#### 15. [test_navbar.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_navbar.py):
Tests the response of the navbar.

#### 16. [test_campuslife.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_campuslife.py):
Tests the functionalities on campus life forum page.

#### 17. [test_password_reset_complete.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_password_reset_complete.py):
Tests the password reset functionality.

#### 18. [test_password_reset_form.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_password_reset_form.py):
Tests the password reset form page.

#### 19. [test_profile_edit.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_profile_edit.py):
Tests the profile edit form

#### 20. [test_profile.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_profile.py):
Tests the rendering of profile page.

#### 21. [test_roommmate_compatability.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_roommmate_compatabilitypy):
Tests the roommmate combatability calculator functionality.

#### 22. [test_signup.py](https://github.com/nih326/PackFinder/blob/feature_main/src/tests/test_signup.py):
Tests the signup functionality.
