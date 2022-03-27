# Event Managment System

This system comprises of 3 relational database tables (Member, Event and Venue). Member table keep records of mebmers of an association.
Venue keep track on the details of the venue, it manager and the specific event that is holding in each venue. while Event keep record on the details of the event. There are connected in the following way:
Member has connection of ManyToOne Association with both event and Venue tables. While Venue has the association on OneToMany with Event.
