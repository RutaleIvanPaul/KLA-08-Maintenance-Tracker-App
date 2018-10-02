--
-- Database: maintenance_tracker
--
-- --------------------------------------------------------

--
-- Table structure for table user
--

CREATE TABLE public."user"(
   id INT PRIMARY KEY      NOT NULL,
   email           CHAR(50) NOT NULL,
   password         CHAR(50)      NOT NULL,
   type         CHAR(50)      NOT NULL,
   status         CHAR(50)      NOT NULL
);


-- --------------------------------------------------------

--
-- Table structure for table request
--

CREATE TABLE public."request"(
   id INT PRIMARY KEY NOT NULL,
   userid INT NOT NULL references public.user(id),
   title CHAR(50) NOT NULL,
   description CHAR(50) NOT NULL,
   status CHAR(50) NOT NULL
);
