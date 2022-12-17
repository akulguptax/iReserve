# UML Diagram

![iReserveUML drawio](https://media.github-dev.cs.illinois.edu/user/9133/files/d9b7f473-9989-4a45-ac89-81ce4440d5fd)

### Assumptions:

- The database should store information about **Rooms**, **Reservations**, **Buildings**, **Users**, and **GroupAssignments**. 
- A **Room** is uniquely identified by its **RoomID**, and references the **Address** of the Building. Other attributes are room capacity, room type, room number, floor number, and popularity.
- A **Reservation** is uniquely identified by its **ReservationID**, and references **UserID** from **Users**, **RoomID** from **Room**, and **AssignmentID** from **GroupAssignments**. Other attributes are start time and end time.
- The **Building** is uniquely identified by its **Address**. Other attributes are building name and region.
- A **User** is uniquely identified by its **UserID** and **email**. Other attributes are first name, last name, and hashed password.
- A **GroupAssignment** is uniquely defined by its **AssignmentID**, and refereces the **UserID** from **Users**. Other attributes are group name.
-----------------------------------------------------------------------------------------------------
- A **Room** is located in exactly one **Building**, but a **Building** may have multiple **Rooms**. 
- A **Room** can have multiple **Reservations** but a **Reservation** can only be made to one **Room** at a time. To make a **Reservation**, you need to know your **UserID**, **RoomId** for the room, and the **AssignmentID** for your group. 
- A **Reservation** can be made by exactly one user, but a **User** can make multiple **Reservations**, amd a User can make one or more **reservations** if they do not have an active one. 
- A **Reservation** can be made by multiple **GroupAssignments** as long as they dont have an active one, and only one **Reservation** at a time can be made by a **GroupAssignment**.
- A **GroupAssignment** can have one or more **Users**, and a **User** can have multiple **GroupAssignments** they are part of. A **GroupAssignment** needs to be made using the **UserID** of the **User** who made it.

# Relational Schema

```
User(
  UserID:INT [PK], 
  FirstName:VARCHAR(255),
  LastName:VARCHAR(255), 
  Email:VARCHAR(255), 
  HashedPassword:VARCHAR(255)
)

Room(
  RoomID:INT [PK],
  BuildingID:INT [FK to Building.BuildingId],
  FloorNumber:INT,
  RoomNumber:INT,
  RoomCapacity:INT,
  RoomType:VARCHAR(50),
  Popularity:REAL
)

Building(
  Address:VARCHAR(255) [PK],
  BuildingName:VARCHAR(255),
  Region:VARCHAR(255),
)

Reservation(
  ReservationID:INT [PK]
  RoomID:INT [FK to Room.RoomId]
  UserID:INT [FK to User.UserID]
  AssignmentID:INT [FK to GroupAssignment.AssignmentID],
  StartTime:VARCHAR(100)
  EndTime:VARCHAR(100)
)

GroupAssignment(
  AssignmentID:INT [PK],
  UserID:INT [FK to User.UserID]
  GroupName:VARCHAR(100)
)
```
