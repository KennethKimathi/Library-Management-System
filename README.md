# Library-Management-System

<img width="950" alt="Home" src="https://github.com/user-attachments/assets/3a037b83-5191-42c0-aba7-f25fe69605b6">

<img width="939" alt="Reader" src="https://github.com/user-attachments/assets/0e7f69a4-6d9f-4814-8ddc-886119583bf8">

<img width="944" alt="Books" src="https://github.com/user-attachments/assets/f8f96170-a92a-4050-8d3c-4927eb870ecb">

<img width="941" alt="Bag" src="https://github.com/user-attachments/assets/a29bdc87-992d-4dbe-887a-63ced53b5560">

<img width="934" alt="Returns" src="https://github.com/user-attachments/assets/7ff01419-5b9a-46ad-8dfd-065a16dfa494">

<img width="937" alt="Add Reader" src="https://github.com/user-attachments/assets/e810d562-ac42-4820-a466-5a674831a2a2">

<img width="938" alt="Add To Bag" src="https://github.com/user-attachments/assets/27f74bdf-65ee-41a2-94c8-f7b02f5b8cfd">

<img width="944" alt="Books in Bag" src="https://github.com/user-attachments/assets/85ab1778-9517-4755-a12d-776ad6541d3a">

<img width="935" alt="Reader Searched" src="https://github.com/user-attachments/assets/52d5600e-e5a7-4839-80bf-dd466ad7dd3b">

<img width="829" alt="Checkout Successful" src="https://github.com/user-attachments/assets/a2f09d62-c542-4a76-a662-cfee8744673a">

<img width="926" alt="Checkout Failed" src="https://github.com/user-attachments/assets/8f83e2e4-a121-4e26-b348-5dd7883e55f8">

The system is built from the view of a Library attendant. In this system, each reader has to deposit money into the account during registration. Readers and books can be registered and searched from the respective pages and will be automatically displayed in the respective pages once saved. A book can be added to bag for checkout, where the attendant can search for a reader using their ID and check them out after entering the date of borrowing and expected return date. 

If the user's balance is below Ksh.500, they are expected to make a deposit to allow them to take a book from the library. If checkout is successful, the checkout record is stored in the returns file. The attendant can view all previous checkouts by a reader by searching their name or ID. The user can return books early, in which case the attendant can check the record as 'returned'.If the due date id met and the books are not returned, the record will be flagged as 'Overdue' and the attendant can follow up with the setup procedures.

Checkout ensures the number of copies of a book is reduced by one whenever checkout is successful and on return, the tally of each book in that record is added by one. Permissions to deactivate, or delete book and reader records are only via the admin portal. 
