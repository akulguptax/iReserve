# iReserve

Our project is a room reserver web application that allows users to book study rooms around campus. This app allows users to view the availability of study rooms around them and place reservations on study rooms if they wish to use them in the future. The application will also allow users to search for a room in any area of campus they wish and receive. Our application will also allow users to block off a room if they are in the vicinity and the room is available. 

## Detailed Description
The goal of this project is to create a web application (using Python and Flask) to allow UIUC students to register for study spaces across campus and also view available nearby study spaces. Our application will have a home page that will display popular, available rooms, as well as a timeline of the next couple days containing information for when these rooms are booked/free. The user will be able to login (or create an account) using their UIUC account to reserve study spaces. Study spaces can also be viewed & sorted on their popularity. The popularity will be determined based on the frequency that study spaces are reserved. Students can also view and choose rooms based on their type, such as a quiet room, group study room, lounge, etc. Another feature in our application is the ability for the application to recommend the closest study space based on the user's current location and popularity of a study room.

We will create our own map of UIUC containing the various buildings that have study spots, as well as the floor plan of each building so that students can visually pick and choose their desired room. As students reserve spots, we will have a trigger to update the database so that other users can get real-time updates of rooms being occupied. More information on the database schema and the various features can be found in the [Functionality](#functionality) section.

Overall this application will give UIUC students the ease of comfort in finding nearby and available study spots at any given time, discover new study locations they may not have known, and to reserve group study locations for studying with friends.

## Usefulness

Too many times, freshmen (and this year sophmores) have had to book rooms for team meetings that are far from their residences. This is fine for larger and more official meetings, but for project meetings as a club, or small get-togethers, booking a room in Grainger using LibCal is just too much of a walk and hassle. Especially in the winter time, it becomes unsafe for freshman to venture out to these places far from their dorms to hold meetings. 

This is why we have build iReserve, the all in one application that allows freshman (or really anyone for that matter) the ability to book study spaces, lounges, and single person rooms right in the comfort of their own dorms. With the ability to filter out types of spaces, where they are, and what their popularity is, freshman do not have to go out when they can hold their meetings in spaces within the dorms. 

We have loaded in all the dorm maps, with all floors, and have a way to see if a room has been booked so their are no overlaps. Every dorm is loaded in, so anywhere someone wants to make a meeting in-person, they can with our service. 

As previosly mentioned, there are applications on campus like LibCal, and the older ARC reservation system during SP21, but nothing dedicated to undergraduates and specifically freshman who are the future of alot of the clubs they want to hold meeings for. The prior reservation apps are complicated and have outdated UIs, whereas ours is modern and easy to follow. The previous systems had alot of overlap and issues with reserving rooms that were already taken, and our application uses popularity and crowdsourcing to make sure that someone who makes a reservation system leaves before another one is made.  

## Realness

Our data is the physical locations of study rooms, lounges, and areas across campus, focused on the dorm buildings (ex. ISR, PAR). We will obtain our data by going through the floor plans of buildings we would like to include into our system and gather the areas that can be reserved. The floor plans for the dorm buildings are public information that we will be able to easily download and access from various websites.

## Functionality 

A lot of our functionality comes under our room reservation feature. Users will be able to schedule room reservations in advance.

We plan on having a handful of tables to model our data. 
- We will use a `Rooms` table to model study rooms by their `building`, `floor`, `room number`, `room type` (lounge, study room, etc.), and `capacity`.
- We will use a `Buildings` table to model locations of study spots around campus using `building name`, `location on campus`, and `popularity`. 
- We will use a `Users` table to model users who wish to  reserve rooms using `user id`, `name`, `email`, `hashed password`. 

We plan on presenting a list of all rooms available on the front page of the website with a timeline of the next day or so. The timeline will consist of 30 minute chunks, indicating whether or not a room was reserved at time interval. 

Users will be able to select a span of consecutive time blocks to reserve rooms. They will submit a ticket to book a reservation for the room of their choice, assuming that the room is not already book during that time. We will be using `INSERT` statements to handle the booking of reservations. Users will be able to modify their reservations if they so choose. In this case, we will be using `UPDATE` statements. 

There are a lot of rooms to choose from, so we will group rooms by the criteria the user specifies. Users may also sort rooms by popularity, room capacity, and elevation (higher floors have better views of campus). Users may also filter rooms by this criteria as well as location on campus and room type. All of these filters and views will be created using `SELECT` statements with `WHERE` clauses. 

We plan to create triggers to update and compute popularity scores of each room. Anytime a reservation is added to our table of reservations, we will re-calculate the popularity of that specific room reserved. 

Our application will have another feature that allows users to book rooms in their vicinity if the rooms are not being used for the next time slot. We are planning to request to use the users' location and alert them of the open study room if they are near the room in question. This feature will use a combination of `SELECT` statements with an `INSERT` statement to find nearby rooms and book a reservation if need be. 

We will also be offering users the choice to simply make the app find a room available to reserve. Users will just enter their location of choice and click a single button, and the app will search for an available room. This feature will also use a combination of `SELECT` statements with an `INSERT` statement to book the room. This is one of our advanced features as we will want to find the best room that meets both the criteria from the users' prior bookings and the current location criteria. 

Another cool feature we would like to include is the concept of study groups. Users can form study groups consisting of themselves and other users. They can then book room reservations under the study group. This feature will allow anyone in the group to be able to modify the reservation. We will need a `Group Assignment` table which models the many-to-many relationship of students to groups.  

Students will also need a way to change their reservation in case they are running late or would like a different time. Our application will use `UPDATE` statements to handle these cases. Students will also need to be able to cancel their reservations. Our app will do so using `DELETE` statements on the `Reservation` table. 

There are also cases where the university facilities crew may need to service or clean a room. We must account for downtime in room reservations by using `UPDATE` statements on the `Rooms` table. There are a multitude of other edge cases where we will need to update or add rooms to this table. 

Users will need to be able to sign up and/or change their account settings and/or delete their account, and our app will process these requests with the appropriate `INSERT` or `UPDATE` or `DELETE` statements. 
