CREATE TABLE
    `book` (
        `id` int NOT NULL AUTO_INCREMENT,
        `title` varchar(255) NOT NULL,
        `author` varchar(255) NOT NULL,
        `isbn` varchar(255) NOT NULL,
        `quantity` int NOT NULL,
        `location` varchar(255) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `isbn` (`isbn`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE
    `patron` (
        `id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(255) NOT NULL,
        `email` varchar(255) NOT NULL,
        `address` varchar(255) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `email` (`email`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE
    `loan` (
        `id` int NOT NULL AUTO_INCREMENT,
        `book_id` int NOT NULL,
        `patron_id` int NOT NULL,
        `due_date` date NOT NULL,
        `return_date` date DEFAULT NULL,
        PRIMARY KEY (`id`),
        KEY `book_id` (`book_id`),
        KEY `patron_id` (`patron_id`),
        CONSTRAINT `loan_book_fk` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT `loan_patron_fk` FOREIGN KEY (`patron_id`) REFERENCES `patron` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE
    `librarian` (
        `id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(255) NOT NULL,
        `email` varchar(255) NOT NULL,
        `address` varchar(255) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `email` (`email`)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE
    `fine` (
        `id` int NOT NULL AUTO_INCREMENT,
        `loan_id` int NOT NULL,
        `amount` decimal(10, 2) NOT NULL,
        `paid` tinyint NOT NULL DEFAULT 0,
        PRIMARY KEY (`id`),
        KEY `loan_id` (`loan_id`),
        CONSTRAINT `fine_loan_fk` FOREIGN KEY (`loan_id`) REFERENCES `loan` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `idx_loan_return_date` ON `loan` (`return_date`);

CREATE INDEX `idx_loan_due_date` ON `loan` (`due_date`);

CREATE INDEX `idx_fine_paid` ON `fine` (`paid`);

CREATE TRIGGER `LOAN_TRIGGER` BEFORE INSERT ON `LOAN` 
FOR EACH ROW SET NEW.RETURN_DATE =NULL; CREATE PROCEDURE 
`SP_GET_AVAILABLE_BOOKS`(IN `TITLE` VARCHAR(255), 
IN `AUTHOR` VARCHAR(255), IN `ISBN` VARCHAR(255)) 
BEGIN 
	SELECT book.*
	FROM book
	    LEFT JOIN loan ON book.id = loan.book_id
	WHERE
	    book.title LIKE CONCAT('%', title, '%')
	    AND book.author LIKE CONCAT('%', author, '%')
	    AND book.isbn LIKE CONCAT('%', isbn, '%')
	    AND (
	        loan.id IS NULL
	        OR loan.return_date IS NOT NULL
	    );
END; 