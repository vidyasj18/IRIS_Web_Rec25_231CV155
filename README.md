# Sports Infrastructure Module
The Sports Infrastructure Management System transforms the traditional manual booking process into a digital, real-time solution. This system allows students to check availability, book equipment or courts instantly, and receive notifications about their bookings. Administrators can efficiently manage resources, approve requests, and maintain the inventory of sports infrastructure.

Languages/framework used:   
  HTML, CSS, TailwindCSS, Javascript, Django

Installation Steps
- Install Python from browser set it up on your device.
- Activate python's virtual environment.
- install django in the terminal itself using "pip install django".
- install serializers,
- Clone this repository on your machine.
- Open terminal after navigating into the cloned repo (using cd).
- use the command to start a local host server: py manage.py runserver.
- This web application is now on one of your browsers.

List of implemented features:
Admin Role:
- Add/Update Equipment: Admins can add new equipment and update availability status in admin dashboard after logging into admin panel.
- Manage Inventory: Track equipment count and condition.
- Request Process: admin can see the students requests according to that he can either approve or reject the request.

User Role:
- User can see the equipment/facility lists in the student dashboard.
- User can book the equipment or facility.
- user can stand in the waitlist.

Common Features
- Role-Based Access Control: Separate functionalities for Users and Admins.
- Admin can add posts that acts as the updates for students.
