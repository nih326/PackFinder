# 🐺 *PackFinder* 🐺
[![Test](https://github.com/SE-Alpha-Project/PackFinder/actions/workflows/Unit_Tests.yml/badge.svg)](https://github.com/SE-Alpha-Project/PackFinder/actions/workflows/Unit_Tests.yml)
[![codecov](https://codecov.io/gh/SE-Alpha-Project/PackFinder/branch/main/graph/badge.svg?token=PCOHJETYCD)](https://codecov.io/gh/SE-Alpha-Project/PackFinder)
[![Test](https://github.com/SE-Alpha-Project/PackFinder/actions/workflows/Linting.yml/badge.svg)](https://github.com/SE-Alpha-Project/PackFinder/actions/workflows/Linting.yml)
[![code_size](https://img.shields.io/github/languages/code-size/SE-Alpha-Project/PackFinder)](https://github.com/SE-Alpha-Project/PackFinder)
[![repo_size](https://img.shields.io/github/repo-size/SE-Alpha-Project/PackFinder)](https://github.com/SE-Alpha-Project/PackFinder)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7155519.svg)](https://doi.org/10.5281/zenodo.7155519)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/SE-Alpha-Project/PackFinder.svg)](https://GitHub.com/SE-Alpha-Project/PackFinder/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub version](https://img.shields.io/github/v/release/SE-Alpha-Project/PackFinder)](https://github.com/SE-Alpha-Project/PackFinder/releases)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🌟 *About PackFinder*
*PackFinder* is a free and easy-to-use roommate-matching platform built for NC State students. Use PackFinder to find the perfect roommate match based on your preferences and get recommendations suited to your lifestyle!
🧑‍💻 Want to contribute? Check out our [CONTRIBUTING.md](https://github.com/rohitgeddam/FindMyRoomie/blob/main/CONTRIBUTING.md).

https://github.com/user-attachments/assets/a99a1c30-3c48-45e1-9a25-7526f895d86f

---

## 💡 *Features*

### 🏠 *Landing Page*
The landing page is the first page that non-authenticated users get redirected to

![image](https://github.com/user-attachments/assets/5d2d42c4-2022-4ae8-a02c-95e8b1ff0404)


### ✍️ *Sign Up*
Sign up with your NCSU email to join the roommate portal securely.

![image](https://github.com/user-attachments/assets/a8efc091-c4b4-4695-b3cf-d4b726b085cd)


### 📧 *Email Confirmation*
Complete your registration via a confirmation email and jump right in!

<p align="center">
<img src="https://user-images.githubusercontent.com/73664200/194785333-ea980a67-8f7d-43a7-937d-da289dd2ea13.png" width="800">
</p>

### 🔑 *Sign In*
Returning users can quickly log in to explore roommate options.

![image](https://github.com/user-attachments/assets/028e1f64-1b45-4f61-83e0-a948248392d0)


### 🔒 *Forgot Password*
Easily reset your password via an email link if you’ve forgotten it.

![image](https://github.com/user-attachments/assets/3df3e3db-d948-4a7e-a82b-08bf74fb468a)


### 👤 *My Profile*
Customize your profile, set preferences, and share a bit about yourself. Make your profile visible to actively seek roommates or hide it if you’re already settled!

![image](https://github.com/user-attachments/assets/5df59ee8-8a7f-4635-bf92-1a54419ece0f)


### 🐺 *Find Roommates*
Browse other profiles and use our “Wolf Filter” to find roommates who match your preferences!

![image](https://github.com/user-attachments/assets/e1f61974-610f-4780-9ba9-b6427727790e)
![image](https://github.com/user-attachments/assets/a2a389e8-82ce-4dc9-bfa1-b11a0545c65c)
![image](https://github.com/user-attachments/assets/e3765814-8d99-4ef8-a4c1-379f192d8a46)



---

## 🚀 *Getting Started*

#### 1. Clone the repository:

   git clone https://github.com/nih326/PackFinder.git

#### 2. Setup the virtual environment:

    python -m venv venv

#### 3. Activate the virtual environment:

    On Mac/Linux:

      source venv/bin/activate

    On Windows:

      venv\Scripts\activate

#### 3. Install required modules and libraries:

    pip install -r requirements.txt

#### 4. Create .env file at ./src/config/
   <p align = "justify">
   To setup Gmail to send emails to users, first create a new Gmail account. Under 'Manage your Google Account', enable 2-Step Verification and select suitable app and device under 'App passwords'. Copy the key that is generated and paste it under tha EMAIL_HOST_PASSWORD. Enter the email in EMAIL_HOST_USER.
   </p>
   Paste this in the .env file.

```
SECRET_KEY=@dr11(7h4n=#@8juk63y(-#bqicdl$9f2okpr@#564=a+-f&*8
DEBUG=True
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

Fill the above field and save.

#### 5. Run the application:

  ```
   cd src 
   python manage.py migrate
   python manage.py runserver
   ```
   

## After adding another field to Model
Django's way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema.

   
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   

## Populate fake data for testing

```
python manage.py seed_users <number of fake instances>

# creates ten fake users
python manage.py seed_users 10
```

## Automatic tools - GitHub Actions
 
We use GitHub actions to automate tasks of linting, code coverage, build, tests, and security checks. The codes that perform these actions are stored as `.yml` files in the `.github/workflows` directory. The GitHub actions are triggered whenever something is pushed (or pulled) into the remote repository. The results of these automated tasks are shown as badges at the top of this README.md file. 

### Unit tests:

Unit test are performed everytime there is a push or pull into the repository. For more information about Unit test visit [Test README](https://github.com/rohitgeddam/FindMyRoomie/blob/main/src/tests/README.md)

### How to build docs
`sphinx-build -b html docs/  docs/build `

### Code Coverage: 

Code Coverage is an important metric that allows us to understand how much of the codebase is tested. `Code_Cov.yml` performs this task. For more information about Code Coverage, please visit this [link](https://www.atlassian.com/continuous-delivery/software-testing/code-coverage). 

### Flake8 - Code Linting:

We are using Flake8 for linting and syntax checking, and it is performed by `Linting.yml`. For more information about Flake8, please visit this [link](https://medium.com/python-pandemonium/what-is-flake8-and-why-we-should-use-it-b89bd78073f2).
Use flake8 before you push code to GitHub. </br>
Config file present in `setup.cfg`.

```
flake8 <directory>
```

### Black - Code Formatter

We are using the Black code formatter to format our code before pushing it to GitHub. For more information about Black, please visit this [link](https://black.readthedocs.io/en/stable/).


Run the line below everytime you push to GitHub.</br>
Config file present in `pyproject.toml`
```
black --line-length 120 <filename>
```

If you prefer using Black in VSCode, you can add the below settings in your vscode settings:

```
{
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "120"],
    "python.linting.enabled": true
}
```
### Pre Commit Hooks for Black Code formatting and Flake8 Linting
* run  `pre-commit install`
* Now everytime you commit, Black and Flake8 will run automatically and will not allow you to push if the code standards are not met.
<img width="694" alt="Screenshot 2022-10-07 at 11 35 40 AM" src="https://user-images.githubusercontent.com/48797475/194592802-e7d7c951-9694-4260-b537-fc017a5fd06c.png">

<sub>Image from [Ji Miranda](https://ljvmiranda921.github.io/assets/png/tuts/precommit_pipeline.png).<sub>

### CodeQL

`CodeQL.yml` performs automated security checks on the codebase and scans it for any vulnerabilities and bugs. For more information about CodeQL, please visit this [link](https://codeql.github.com/docs/codeql-overview/about-codeql/). 

## 🔒 *Privacy Policy*

1. *Data Collection*: Basic details are collected to match roommates efficiently.
2. *Data Storage*: Data is stored securely and only used within the platform.
3. *No External Sharing*: Your information is not shared with third parties.
4. *Data Retention*: Stored as long as you’re using the service.
5. *Data Removal*: Email us from your registered account to remove data.


## Technology Used
-   `Python 3.7+`
-   `Django 4.1.2`
-   `HTML5`
-   `CSS3`
-   `BootStrap v5.2`



## 🛤️ *Roadmap*

### *3-Month Milestones*
- Apartment details in profiles for easier roommate pairing
- Integrated chat for in-app messaging

### *6-Month Milestones*
- Mobile app launch on Google Play and App Store

### *9-Month Milestones*
- Partnership with local property agents for seamless listings

---

## Contributors:
Niharika Maruvanahalli Suresh: nmaruva@ncsu.edu </br>
Diya Shetty - dshetty@ncsu.edu </br> 
Sanjana Nanjangud Shreenivas - sshreen@ncsu.edu </br>

---
## Acknowledgements

We want to express our gratitude and a big thank you to Prof. Dr Timothy Menzie for allowing us to get into the shoes of software building and learning new skills and development processes throughout the project building. It was a great opportunity to learn to work as a team.
A big thank you to the Teaching Assistants for their support.
Thank you to the previous team for a thorough ReadMe and detailed documentation that helped us easily understand the project.

---


---

Thank you for checking out *PackFinder*! We're here to make your roommate search stress-free and enjoyable. Happy searching! 🎉🐺
