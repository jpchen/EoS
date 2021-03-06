drop table if exists users;
drop table if exists comments;
drop table if exists courses;
create table users (
  name text not null,
  user text not null,
  email text not null,
  school text not null,
  prof integer not null,
  courses text
);
create table courses (
  id integer primary key autoincrement,
  name text not null,
  cap integer
);
create table comments (
  id text not null,
  usr text not null,
  time text,
  comm text not null 
);
