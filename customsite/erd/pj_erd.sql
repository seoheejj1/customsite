SET SESSION FOREIGN_KEY_CHECKS=0;

/* Drop Tables */

DROP TABLE IF EXISTS B_photo;
DROP TABLE IF EXISTS Board;
DROP TABLE IF EXISTS R_photo;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Order_Table;
DROP TABLE IF EXISTS Cart;
DROP TABLE IF EXISTS Config;
DROP TABLE IF EXISTS Co_account;
DROP TABLE IF EXISTS Inquire;
DROP TABLE IF EXISTS Tag_list_Product;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Tag_list;
DROP TABLE IF EXISTS t_photo;
DROP TABLE IF EXISTS Type;
DROP TABLE IF EXISTS User;




/* Create Tables */

CREATE TABLE Board
(
	board_id int NOT NULL AUTO_INCREMENT,
	user_id int NOT NULL,
	title varchar(60) NOT NULL,
	content varchar(300) NOT NULL,
	reg_date datetime NOT NULL,
	view_cnt int DEFAULT 0 NOT NULL,
	e_start date,
	e_end date,
	tag varchar(30) NOT NULL,
	PRIMARY KEY (board_id),
	UNIQUE (board_id),
	UNIQUE (user_id)
);


CREATE TABLE B_photo
(
	board_id int NOT NULL,
	photo varchar(300),
	UNIQUE (board_id)
);


CREATE TABLE Cart
(
	user_id int NOT NULL,
	product_id int NOT NULL,
	amount int NOT NULL,
	checked boolean NOT NULL,
	PRIMARY KEY (user_id, product_id),
	UNIQUE (user_id),
	UNIQUE (product_id)
);


CREATE TABLE Config
(
	name varchar(30) NOT NULL,
	ceo varchar(40) NOT NULL,
	number varchar(30) NOT NULL,
	address varchar(600) NOT NULL,
	email varchar(100) NOT NULL,
	site_name varchar(30) NOT NULL,
	sale_time varchar(300) NOT NULL,
	lunch_time varchar(300) NOT NULL,
	holiday varchar(3) DEFAULT 'OFF' NOT NULL,
	sgin_point int NOT NULL,
	return_point int DEFAULT 0 NOT NULL,
	review_point int DEFAULT 0 NOT NULL,
	best_point int DEFAULT 0 NOT NULL,
	min_amount int DEFAULT 0 NOT NULL,
	max_point int DEFAULT 0 NOT NULL,
	tag_show boolean DEFAULT 'True' NOT NULL
);


CREATE TABLE Co_account
(
	bank varchar(30) NOT NULL,
	number int NOT NULL,
	depositer varchar(30) NOT NULL,
	PRIMARY KEY (bank),
	UNIQUE (bank),
	UNIQUE (number)
);


CREATE TABLE Inquire
(
	inq_id int NOT NULL AUTO_INCREMENT,
	user_id int NOT NULL,
	title varchar(60) NOT NULL,
	contents varchar(300) NOT NULL,
	reg_date datetime NOT NULL,
	answer varchar(300),
	answer_date datetime,
	PRIMARY KEY (inq_id),
	UNIQUE (inq_id),
	UNIQUE (user_id)
);


CREATE TABLE Order_Table
(
	order_id int NOT NULL AUTO_INCREMENT,
	product_id int NOT NULL,
	user_id int NOT NULL,
	amount int NOT NULL,
	date datetime NOT NULL,
	state varchar(10) NOT NULL,
	reviewed boolean NOT NULL,
	delivery_req varchar(80),
	r_name varchar(300) NOT NULL,
	r_adress varchar(300) NOT NULL,
	r_contact varchar(300) NOT NULL,
	r_location varchar(300),
	r_pw int,
	PRIMARY KEY (order_id),
	UNIQUE (order_id),
	UNIQUE (product_id),
	UNIQUE (user_id)
);


CREATE TABLE Product
(
	product_id int NOT NULL AUTO_INCREMENT,
	user_id int NOT NULL,
	t_title varchar(30) NOT NULL,
	size varchar(3) NOT NULL,
	request varchar(200),
	view_cnt int DEFAULT 0 NOT NULL,
	reg_date date DEFAULT now() NOT NULL,
	img varchar(3000) NOT NULL,
	PRIMARY KEY (product_id),
	UNIQUE (product_id),
	UNIQUE (user_id)
);


CREATE TABLE Review
(
	review_id int NOT NULL AUTO_INCREMENT,
	order_id int NOT NULL,
	title varchar(60) NOT NULL,
	contents varchar(300) NOT NULL,
	view_cnt int NOT NULL,
	reg_date datetime NOT NULL,
	PRIMARY KEY (review_id),
	UNIQUE (order_id)
);


CREATE TABLE R_photo
(
	review_id int NOT NULL,
	photo varchar(300)
);


CREATE TABLE Tag_list
(
	name varchar(30) NOT NULL,
	PRIMARY KEY (name)
);


CREATE TABLE Tag_list_Product
(
	product_id int NOT NULL,
	name varchar(30) NOT NULL,
	PRIMARY KEY (product_id, name),
	UNIQUE (product_id)
);


CREATE TABLE Type
(
	t_title varchar(30) NOT NULL,
	t_description varchar(5000) NOT NULL,
	t_img varchar(5000) NOT NULL,
	t_price int NOT NULL,
	PRIMARY KEY (t_title)
);


CREATE TABLE t_photo
(
	t_title varchar(30) NOT NULL,
	photo varchar(300) NOT NULL,
	color varchar(30) NOT NULL
);


CREATE TABLE User
(
	user_id int NOT NULL AUTO_INCREMENT,
	admin boolean NOT NULL,
	email varchar(60) NOT NULL,
	password varchar(100) NOT NULL,
	nickname varchar(50) NOT NULL,
	contact varchar(30) NOT NULL,
	point int DEFAULT 0 NOT NULL,
	adress varchar(200),
	reg_date datetime NOT NULL,
	prized boolean NOT NULL,
	PRIMARY KEY (user_id),
	UNIQUE (user_id),
	UNIQUE (email),
	UNIQUE (nickname)
);



/* Create Foreign Keys */

ALTER TABLE B_photo
	ADD FOREIGN KEY (board_id)
	REFERENCES Board (board_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Order_Table
	ADD FOREIGN KEY (product_id, user_id)
	REFERENCES Cart (product_id, user_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Review
	ADD FOREIGN KEY (order_id)
	REFERENCES Order_Table (order_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Cart
	ADD FOREIGN KEY (product_id)
	REFERENCES Product (product_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Tag_list_Product
	ADD FOREIGN KEY (product_id)
	REFERENCES Product (product_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE R_photo
	ADD FOREIGN KEY (review_id)
	REFERENCES Review (review_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Tag_list_Product
	ADD FOREIGN KEY (name)
	REFERENCES Tag_list (name)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Product
	ADD FOREIGN KEY (t_title)
	REFERENCES Type (t_title)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE t_photo
	ADD FOREIGN KEY (t_title)
	REFERENCES Type (t_title)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Board
	ADD FOREIGN KEY (user_id)
	REFERENCES User (user_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Cart
	ADD FOREIGN KEY (user_id)
	REFERENCES User (user_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Inquire
	ADD FOREIGN KEY (user_id)
	REFERENCES User (user_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;


ALTER TABLE Product
	ADD FOREIGN KEY (user_id)
	REFERENCES User (user_id)
	ON UPDATE RESTRICT
	ON DELETE RESTRICT
;



