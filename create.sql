drop table if exists Item;
drop table if exists User;
drop table if exists Bid;
drop table if exists Category;

create table Item(
	ItemID		INT NOT NULL,
	Name		VARCHAR(255) NOT NULL,
	Description	VARCHAR NOT NULL,
	Seller		VARCHAR(255) NOT NULL,
	Started		DATE NOT NULL,
	Ends		DATE NOT NULL,
	Currently	DOUBLE NOT NULL,
	Buy_Price	DOUBLE,
	First_Bid	DOUBLE NOT NULL, 
	Number_of_Bids  INT NOT NULL,
	PRIMARY KEY (ItemID),
);

create table User(
	UserID		VARCHAR(255) NOT NULL,
	Location	VARCHAR(255),
	Country		VARCHAR(255),	
	Rating		INT,
	PRIMARY KEY (UserID)
);

create table Bid(
	ItemID		INT NOT NULL,
	UserID		VARCHAR(255) NOT NULL,
	Time		DATETIME NOT NULL,
	Amount		DOUBLE NOT NULL,
	FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
	FOREIGN KEY (UserID) REFERENCES User(UserID),
);

create table Category(
	ItemID		INT NOT NULL,
	Name	 	VARCHAR(255),
	FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
);
