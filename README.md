# Private Tutoring Website
## General info
This is a private tutoring website for medical students, where the teacher can exhhibit his biography and where the students can book for a private lesson and the teacher can accept or decline their reservation.
There are additional functions such as a file manager, where the teacher can send to the students teaching materials like notes, videos, or any other type of file that can be useful.
Also, the website's biographic content is modular!
The website is live at www.drsteliostheodorou.com


## Functions available per actor
#### Teacher/Admin Functions:
The following can be accesed from admin panel (<domain-name>/admin)
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

#### SMTP Service functions
1. Activate account email
2. Forgot password email
3. Updates regarding appointments email
4. Notification on file shared email


## Database structure
Can be found in models.py
#### Gallery
* PhotoSection: Category of photos
* Photo

#### Teaching experiences
* Association: Universities/Association where the teacher gave lectures
* Teaching_Experience: Subject of lectures given

#### Users
* MyUser: The users including teachers, students



