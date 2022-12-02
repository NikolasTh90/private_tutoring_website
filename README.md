# Private Tutoring Website
## General info
This is a private tutoring website for medical students, where the teacher can exhibit his biography and where the students can book for a private lesson and the teacher can accept or decline their reservation.
There are additional functions such as a file manager, where the teacher can send to the students teaching materials like notes, videos, or any other type of file that can be useful.
Also, the website's biographic content is modular!
The website is live at www.drsteliostheodorou.com

## How to run it locally
#### Requirements
1. python 3.10.0 or newer
2. django 4.0 or newer
3. django-widget-tweaks
4. python pillow 9.0 or newer
5. python numpy
6. python tkinder

#### Run
On the file manage.py under epl343.winter22.team3/epl343 run the following command
```
python3 manage.py runserver <port>
```
If you do not specify port the default port is 8000.
Access the website in your browser at `127.0.0.1:<port>/`


## Functions available per actor
#### Teacher/Admin Functions:
The following can be accesed from admin panel `<domain-name>/admin`
1. Edit biographic content of the website (Biography, Gallery, Student's Testimonials)
2. Accept/Reject/Modify appointments
3. Add learning material files
4. Give access permission of learning material files to students
5. Manage working hours schedule/Manage day offs


#### Student/User functions
1. Make an inquiry (no registered account required)
2. Book/Change/Cancel appointment
3. Edit profile
4. Write a testimonial about teacher
5. Access learning material files
6. Activate account
7. Forgot password
8. Communicate with teacher live via Facebook's Messenger

#### SMTP Service functions
1. Activate account email
2. Forgot password email
3. Updates regarding appointments email
4. Notification on file shared email


## Database Structure
Can be found in models.py
#### Gallery
* PhotoSection: Category of photos
* Photo

#### Teaching Experiences
* Association: Universities/Association where the teacher gave lectures
* Teaching_Experience: Subject of lectures given

#### Users
* MyUser: The users including teachers, students

#### Learning Material Files
* LearningMaterial: Files of any type to be shared with students
* LearningMaterialReference: A couple of User and LearningMaterial, to assign which users have access to a file
  
#### Booking System
* Appointment
* Schedule: Working hours
* Offs: Day offs

#### Testimonials
* Testimonial
  
#### Tokens
* ResetTokens: reset password tokens
* ActivateTokens: email verification tokens



