Create table "user" (
    userID VARCHAR(15) PRIMARY KEY,
    fname VARCHAR(15) NOT NULL UNIQUE,
    lname VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(25) NOT NULL UNIQUE,
    isowner BOOLEAN
);

Create table books (
    isbn INT PRIMARY KEY,
    title VARCHAR(15) NOT NULL,
    price INT NOT NULL,
    num_of_pages INT NOT NULL,
    genre VARCHAR(15) NOT NULL
);

Create table publisher (
    pub_name VARCHAR(15) PRIMARY KEY,
    email VARCHAR(25) NOT NULL UNIQUE,
    bank_id INT NOT NULL UNIQUE,
    phone_number INT NOT NULL UNIQUE
);

Create table address (
    add_id int PRIMARY KEY,
    country VARCHAR(15) NOT NULL,
    city VARCHAR(15) NOT NULL,
    street_name VARCHAR(15) NOT NULL,
    street_num INT NOT NULL
);

Create table author (
    auth_fname VARCHAR(15) NOT NULL,
    auth_lname VARCHAR(15) NOT NULL,

    PRIMARY KEY(auth_fname, auth_lname)
);

Create table "order" (
    order_num int PRIMARY KEY,
    track_num VARCHAR(15) NOT NULL UNIQUE,
    status VARCHAR(15) NOT NULL,
    total int NOT NULL
);

Create table basket (
    bask_id int PRIMARY KEY
);

Create table hasAddress (
    add_id int PRIMARY KEY,
    userID VARCHAR(15) NOT NULL UNIQUE,

    FOREIGN KEY(userID)
        REFERENCES "user" (userID)

);

Create table reports (
    report_id int PRIMARY KEY,
    sales_expenditures INT NOT NULL,
    sales_per_genres INT NOT NULL,
    sales_per_author INT NOT NULL
);


Create table orderAddress (
    order_num INT NOT NULL UNIQUE,
    add_id INT NOT NULL UNIQUE,

    FOREIGN KEY(order_num)
        REFERENCES "order" (order_num),

    FOREIGN KEY(add_id)
        REFERENCES address (add_id),
    
    Primary Key(order_num, add_id)
);


Create table pubAddress (
    add_id INT PRIMARY KEY,
    pub_name VARCHAR(15) NOT NULL UNIQUE,

    FOREIGN KEY(pub_name)
        REFERENCES publisher (pub_name),

    FOREIGN KEY(add_id)
        REFERENCES address (add_id)
);

Create table checkout (
    bask_num INT PRIMARY KEY,
    order_num INT NOT NULL UNIQUE,

    FOREIGN KEY(order_num)
        REFERENCES "order" (order_num),

    FOREIGN KEY(bask_num)
        REFERENCES basket (bask_num)
);

Create table writes (
    auth_fname VARCHAR(15) NOT NULL UNIQUE,
    auth_lname VARCHAR(15) NOT NULL UNIQUE,
    isbn INT NOT NULL,

    FOREIGN KEY(auth_fname, auth_lname)
        REFERENCES author (auth_fname, auth_lname),

    FOREIGN KEY(isbn)
        REFERENCES books (isbn),

    Primary Key(auth_fname, auth_lname, isbn)
);

Create table publishes (
    pub_name VARCHAR(15) NOT NULL UNIQUE,
    isbn INT NOT NULL UNIQUE,

    FOREIGN KEY(pub_name)
        REFERENCES publisher (pub_name),

    FOREIGN KEY(isbn)
        REFERENCES books (isbn),
    
    Primary Key (pub_name, isbn)
);


Create table item (
    isbn INT PRIMARY KEY,
    bask_num INT NOT NULL,
    quantity INT,

    FOREIGN KEY(bask_num)
        REFERENCES basket (bask_num),

    FOREIGN KEY(isbn)
        REFERENCES books (isbn)
);

Create table owner (
    userID INT PRIMARY KEY,
    isowner BOOLEAN NOT NULL,

    FOREIGN KEY(userID)
        REFERENCES "user" (userID),
);
