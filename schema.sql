drop table if exists users;
drop table if exists videos;
drop table if exists courses;
create table users (
  name text not null,
  hash text not null,
  email text not null,
  school text not null,
  prof integer not null
);
create table courses (
  id integer primary key autoincrement,
  name text not null,
  size integer
)
create table videos (
  id integer primary key,
  name text not null 
);
