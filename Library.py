import psycopg2
from psycopg2 import Error


#Connecting to database
try:
    # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                  password="student",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="Project")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    # print("PostgreSQL server information")
    # print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    # print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
# finally:
#     if (connection):
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")

    # test = 'SELECT * from "user"'

    # cursor.execute(test) 

    # all = cursor.fetchall()
    # all = cursor.fetchone()



    # for row in all:
    #     val = 0
    #     print(row[2])

#Allows a user to create an account
def register():

    print("Enter a userid no digits")
    userid = input ("> ")
    print("Enter your first name")
    fname = input ("> ")
    print("Enter your lastname")
    lname = input ("> ")
    print("Enter a email")
    email = input ("> ")

    adduser = """INSERT INTO "user"(userid,fname,lname,email) 
                VALUES(%s,%s,%s,%s);""" 

    cursor.execute(adduser, (userid,fname,lname,email))
    connection.commit()

    print("Thank you for registering " + userid)
    return (userid)

#Prompts the user to either login or register and checks if login is valid     
def loginScreen():
    id = ""
    while True:
        
        count = 0 

        users = 'SELECT * from "user"'
        cursor.execute(users) 
        all = cursor.fetchall()


        print()
        print("login Screen:")
        print()
        print("Login in with your userID or type 'r' to register.")
        print("UserId: ")
        id = input ("> ")

        for row in all:
            if id == row[0]:

                authenticated = row[0]



        if id == 'r':
            register()

        elif id != authenticated:
            print("invalid userID... try again.")
            print()
        

        else:
            print('You have been authenticated welcome '+authenticated )

            sql = """select * from basket"""

            cursor.execute(sql)

            sql = cursor.fetchall()
            
            basknum = len(sql) + 1

            

            basket = """INSERT INTO basket(bask_id) 
                        VALUES(%d);""" % (basknum)

            cursor.execute(basket)
            connection.commit()

            print()
            break
    
    return (id)

#Closes connection to the database and exits the program       
def exit():

    remove = 'DELETE from item'
    cursor.execute(remove) 
    connection.commit()

    if connection:
        cursor.close()
        connection.close()
    print("Thank you for shopping!")    

#Management
def management():
    print("Authenticating......")

    sql = """select * from "user"
            where userid = '%s' AND isowner = true;""" %(userID)
    cursor.execute(sql)
    data_list = cursor.fetchall()

    if(len(data_list) > 0):
        print("You have been authenticated")
        print("-------------------------------")
        print("| Welcome to Management Portal |")
        print("-------------------------------") 
        print()
        while True:

            print('Please select from the following options \n1.Add Books \n2.Remove books \n3.Show Reports')
            userInput = input ("> ")

            if userInput == '1':
                addBook(False)
            
            elif userInput == '2':
                removeBook(False)
            
            elif userInput == '3':
                printreport()
            
            else:
                print("Incorrect input")
                continue


    
    else:
        print("You do not have permission to enter management")
        mainmenu()
   
#Welcome message when the user enters the library allows for login/register/exit
def welcome():
    #this is the main function for the library application.
    
       
    print("------------------------------")
    print("| Welcome to The Library.co  |")
    print("------------------------------") 
    print()



    while True:
        print("Type 1 to login, 2 to register or 3 to exit. ")   
        userInput = input("> ")
        print()
        if userInput == '1':
            global userID
            userID = loginScreen()
            break 
        
        elif userInput == '2':
            userID = register()
            break

        elif userInput == '3':
            exit()

        else: 
            print("sorry "+str(userInput)+" is not a valid input.")
            continue
            
        
    if userID is not None:
        mainmenu()

#Main menu of the library
def mainmenu():

    while True:
    
        print("------------------------------")
        print("| Main Menu of The Library.co |")
        print("------------------------------") 
        print()
        print("1.Access Library database \n2.View Basket \n3.Checkout \n4.Management \n5.exit")
        print()
        userInput = input ("> ")
        
        if userInput == '1':
            library()
            break 

        elif userInput == '2':
            viewBasket()
            break

        elif userInput == '3':
            checkout()
            break

        elif userInput == '4':
            management()
            break

        elif userInput == '5':
            exit()
            

        else: 
            print("sorry "+str(userInput)+" is not a valid input.")
            continue 

#Used to print books in the users basket
def printBooks():
    count = 1
    global baskDictionary 
    baskDictionary = {}
    #retieve everything in the item relation
    book = 'SELECT * from item'
    cursor.execute(book) 
    items = cursor.fetchall()

    #retrieve everything in the basket relation
    #basket_id = 1

    basket_ID = 'SELECT * from basket'
    cursor.execute(basket_ID) 
    basket = cursor.fetchall()



    #retrieve all books from the library
    books = 'SELECT * from books'
    cursor.execute(books) 
    allBooks = cursor.fetchall()


    for i in items:
        #i[0] = isbn
        #i[1] = bask_id
        #i[2] = quantity
        baskID = len(basket) -1
        
        if i[1] == baskID:
            isbn = i[0]
            for j in allBooks:
                #j[0] = isbn
                #j[1] = title
                #j[2] = price
                #j[3] = genre
                #j[4] = num_of_pages
                if isbn == j[0]:
                    print(str(count)+": "+str(j[1]))
                    count = count + 1
                    baskDictionary[count]=j[1]

#Used to print books in the users basket
def viewBasket():
        printBooks()
        print("Here are the items in your basket: ")
        print()
        print('if you would like to remove a book from your basket enter "1" \nIf you would like to return to main menu "2" \n3.Checkout')

        while True:
            userInput = input("> ")
            if userInput == '1':
                removeBook(True)
                break
            elif userInput == '2':
                mainmenu()
            elif userInput == '3':
                checkout()
            else:
                print("incorrect input. Please enter either 1 or 2!")
                continue

#Remove an item from users basket
def removeBook(Frombask):
    count = 1
    removeIndex = 0
    
    if(Frombask):
        while True:
            print("Select a number corresponding to the book you wish to remove")
            userInput = input("> ")
            for x in baskDictionary:
                print(str(count) + ": "+ str(baskDictionary[x]))
                count = count + 1

            for x in range(len(baskDictionary)):
                if userInput == (x+1):
                    removeIndex = userInput
                    break
                else:
                    continue

            if userInput != removeIndex:
                print("invalid input")
                continue
            else:
                break
        
        removeItem = baskDictionary[removeIndex]

        #retrieve all books from the library
        books = 'SELECT * from books'
        cursor.execute(books) 
        allBooks = cursor.fetchall()

        for i in allBooks:
            #i[0] = isbn
            #i[1] = title
            #i[2] = price
            #i[3] = genre
            #i[4] = num_of_pages
            if i[1] == removeItem:
                book = 'DELETE from items where isbn = '+str(i[0])
                cursor.execute(book) 
                items = cursor.fetchall()
                connection.commit()

    elif(Frombask == False):

        print(False)

def addBook(tobask):

    if(tobask):
        while True:
            print("Enter the title of the book to add to your basket:")
            book = input ("> ")


            sql = """select * from books 
                        where title ='%s';""" %(book)

            print()    
            cursor.execute(sql)
            data_list = cursor.fetchall()

            if len(data_list) < 1:
                print("Sorry book does not exist")
                continue
            else:
                print("How many would you like to purchase?:")
                quantity = input ("> ")

                quantity = int(quantity)

                getisbn = """select isbn from books 
                where title ='%s';""" %(book)

                cursor.execute(getisbn)
                data_list = cursor.fetchall()

                isbn = 0

                for row in data_list:
                    isbn = row[0]

                get_bask_id = """select * from basket"""

                cursor.execute(get_bask_id)
                data_list = cursor.fetchall()

                bask_id = len(data_list) - 1


                addtobask = """insert into item (isbn,bask_id,quantity) 
                                VALUES (%d,%d,%d);""" %(isbn,bask_id,quantity)

                print()    
                cursor.execute(addtobask)
                connection.commit()
                print('Successfully added '+ book +' to your basket!')
                print()

                checkout()

    elif(tobask == False):

        while True:
            print("Please enter the information for the book you want to add \nISBN:")
            isbn = input ("> ")
            isbn = int(isbn)
            print("Title:")
            title = input ("> ")
            print("price:")
            price = input ("> ")
            price = int(price)
            print("num_of_pages:")
            num_of_pages = input ("> ")
            num_of_pages = int(num_of_pages)
            print("genre:")
            genre = input ("> ")

            addbook = """INSERT INTO books(isbn,title,price,num_of_pages,genre) 
                        VALUES(%d,'%s',%d,%d,'%s');""" %(isbn,title,price,num_of_pages,genre)

            cursor.execute(addbook)
            connection.commit()

            print("You've successfully add the book "+title +" to the Library!")
            print()
            print("1.Add other? \n2.Return to management portal \n3.Return to main menu")
            userInput = input ("> ")

            if userInput == '1':
                continue
            
            elif userInput == '2':
                management()

            elif userInput == '3':
                mainmenu()
            else:
                print("Incorrect input")
                continue

def printreport():
    sql = """select * from reports"""
    cursor.execute(sql)
    data_list = cursor.fetchall()

    print("Now print Report")
    print('============================')
    for row in data_list:
        print("Sales expenditures: " + str(row[1]))
        print("Sales per Genre: " + str(row[1]))
        print("Sales per Author: " + str(row[1]))
    print()
    
    while True:
        print("1.Back to management portal \n2.Back to main menu")
        userInput = input ("> ")

        if userInput == '1':
            management()
        
        elif userInput == '2':
            mainmenu()
        else:
            print("Incorrect input")
            continue

def updateAddress():
    
    hasAddress = """SELECT * from hasAddress 
                    where userid = userID"""
    cursor.execute(hasAddress) 
    hasAddRelation = cursor.fetchall()
    
    if len(hasAddRelation) >= 1:
        add_id = hasAddRelation[0]
        print("update your address")
        print()
        print("Enter your Country")
        countryInput = input("> ")
        print("Enter your city")
        cityInput = input("> ")
        print("Enter your street name")
        street_nameInput = input("> ")
        print("Enter you street number")
        streetNumberInput = input("> ")

    else:
        add_id = len(hasAddRelation)+1
        print("Enter a address")
        print()
        print("Enter your Country")
        countryInput = input("> ")
        print("Enter your city")
        cityInput = input("> ")
        print("Enter your street name")
        street_nameInput = input("> ")
        print("Enter you street number")
        streetNumberInput = input("> ")

    
    add_id = int(add_id)

    orderAddRelat = """INSERT INTO hasaddress
               VALUES(%d,'%s')""" %(add_id, userID)
    cursor.execute(orderAddRelat) 
    connection.commit()


    streetNumberInput = int(streetNumberInput)
    orderAddRelat = """INSERT INTO address
               VALUES(%d,'%s','%s','%s',%d)""" %(add_id, countryInput, cityInput, street_nameInput, streetNumberInput)
    cursor.execute(orderAddRelat) 
    connection.commit()



    printOrder(add_id)

def payForBooks():
    print()
    print("CONTACT INFORMATION")
    print(      userID)
    print()
    print("SHIPPING ADDRESS")

    #retrieve all addresses with associating userIDs
    addresses = """SELECT * from hasaddress
                    where userid = '%s';"""%(userID)

    cursor.execute(addresses) 
    allAddressesID = cursor.fetchall()


    print(allAddressesID)

    if len(allAddressesID) < 1:
        updateAddress()
        
    else:

        userAddID = allAddressesID[0]
        while True:
            print("would you like to use the same address from registration or enter a new one? \n Type '1' to keep it \n Type '2' for a new one. ") 
            userInput = input("> ")
            if userInput == '1':
                printOrder(userAddID)
                break
            elif userInput == '2':
                updateAddress()
                printOrder(userAddID)
                break
            else:
                print("Invalid Input")
                continue


    # for address in allAddressesID:
    #     #address[0] = add_id
    #     #address[1] = userID

    #     if address[1] == userID:
    #         while True:
    #             print("would you like to use the same address from registration or enter a new one? \n Type '1' to keep it \n Type '2' for a new one. ") 
    #             userInput = input("> ")
    #             if userInput == '1':
    #                 printOrder(address[0])
    #                 break
    #             elif userInput == '2':
    #                 updateAddress()
    #                 printOrder(address[0])
    #                 break
    #             else:
    #                 print("Invalid Input")
    #                 continue
                
    #     else:
    #         updateAddress()
    #         printOrder()
    #         break

#Allows a user to checkout books
def checkout():
    '''shows the user their checkout basket.
    the user can remove items from their basket here. They also have the ability to finalize their purchase. 
    '''
 
    print()
    print("Checkout:")
    printBooks()

    while True: 

        print('Enter "1" to remove a book\nEnter "2" return to main menu\nEnter "3" to pay for books \n4.Add a book to basket \nEnter "5" to cancel transaction')
        userInput = input("> ")
        if userInput == '1':
            removeBook(True)
        elif userInput == '2':
            mainmenu()
        elif userInput == '3':
            print('entered 3')
            #SOME CODE
            #address
            #give random value(delievered, shipped, or at warehouse) for status...
            payForBooks()
        
        elif userInput == '4':
            addBook(True)
            #SOME CODE
            #address
            #give random value(delievered, shipped, or at warehouse) for status...
             
        elif userInput == '5':
            print()
            print("are you sure you would like to terminate this session?")
            print('Enter "yes" or "no"')
            userInput2 = input("> ")

            if userInput2 == "yes":
                exit()
            elif userInput2 == "no":
                continue 

def orderTotal():
    total = 0
    items = 'SELECT * from item'
    cursor.execute(items) 
    itemRelation = cursor.fetchall()

    books = 'SELECT * from books'
    cursor.execute(books) 
    bookRelation = cursor.fetchall()

    for i in itemRelation:
        #i[0] = isbn
        #i[1] = bask_id
        #i[2] = quantity
        for j in bookRelation:
            #j[0] = isbn
            #j[1] = title
            #j[2] = price
            if i[0] == j[0]:
                total = total + j[2]

    return (total)

def printOrder(userAddID):
    
    ordersAdd = """SELECT * from orderAddress """
    cursor.execute(ordersAdd) 
    orderAddRelation = cursor.fetchall()

    if len(orderAddRelation) == 0:
        order_num = 1
        tracking_num = 1

    else:
        order_num = len(orderAddRelation) + 1 
        tracking_num = len(orderAddRelation) + 1 


    status = 'shipped'

    order_num = int(order_num)
    userAddID = userAddID[0]
    #add info

    userAddID = int(userAddID)


    total = orderTotal()

    #add info into order relationship
    orderRelat = """INSERT INTO "order" (order_num,track_num,status,total)
                    VALUES(%d,%d,'%s',%d)""" %(order_num,tracking_num,status,total)
    cursor.execute(orderRelat) 
    connection.commit()

    orderAddRelat = """INSERT INTO orderAddress (order_num,add_id)
               VALUES(%d,%d)""" % (order_num,userAddID) 
    cursor.execute(orderAddRelat) 
    connection.commit()


    print()
    print("=========================")
    print("     Digital Reciept     ")
    print("=========================")
    print("                         ")
    print("Order Number: %d      "%(order_num))
    print("Tracking Number: %d"%(tracking_num))
    print("Status: %s"%(status))
    print("Total: $%d"%(total))

    mainmenu()


#Allows a user to search the library for books via ISBN/title/genre/author
def library():

    while True:
        print("1.to search for a book \n2.Checkout \n3.To return to the main menu")
        print()
        userinput = input('> ')
    
        if(userinput == "1"):
            print("Search a book by 1:ISBN/2:title/3:genre/4:author")
            userinput = input('> ')

            if(userinput == '1'):
                print("Please enter ISBN")
                userinput = input('> ')

                userinput = int(userinput)

                sql = """select * from books 
                        where isbn = %d;""" %(userinput)
                
                cursor.execute(sql)

                data_list = cursor.fetchall()

                sql2 = """select auth_fname, auth_lname from writes 
                        where isbn = %d;""" %(userinput)
                
                sql3 = """select pub_name from publishes  
                        where isbn = %d;""" %(userinput)

                for row in data_list:
                    print("Title: "+ row[1])
                    print("Price: "+ str(row[2]))
                    print("Number of Pages: "+ str(row[3]))
                    print("Genre: "+ row[4])
                    
                cursor.execute(sql2)

                data_list = cursor.fetchall()
                
                for row in data_list:
                    print('Author name: ' + row[0] + " " + row[1])
                
                cursor.execute(sql3)

                data_list = cursor.fetchall()
                
                for row in data_list:
                    print('Publisher: ' + row[0])
                

                print()
                continue

            elif(userinput =='2'):
                print("Please enter title")
                userinput = input('> ')

                sql = """select * from books 
                            where title ='%s';""" %(userinput)
                

                print()
                
                cursor.execute(sql)
                data_list = cursor.fetchall()

                isbn = 0

                for row in data_list:
                    isbn = row[0]
                    print("Title: "+ row[1])
                    print("Price: "+ str(row[2]))
                    print("Number of Pages: "+ str(row[3]))
                    print("Genre: "+ row[4])

                sql2 = """select auth_fname, auth_lname from writes 
                        where isbn = %d;""" %(isbn)
                
                cursor.execute(sql2)

                data_list = cursor.fetchall()
                
                for row in data_list:
                    print('Author name: ' + row[0] + " " + row[1])
                
                sql3 = """select pub_name from publishes  
                        where isbn = %d;""" %(isbn)

                cursor.execute(sql3)

                data_list = cursor.fetchall()
                
                for row in data_list:
                    print('Publisher: ' + row[0])
                
                print()
        
            elif(userinput == '3'):
                print("Please enter Genre")
                userinput = input('> ')

                sql = """select * from books 
                        where genre = '%s';""" %(userinput)
                
                cursor.execute(sql)

                data_list = cursor.fetchall()

                isbn = 0
                for row in data_list:
                    isbn = row[0]
                    print("Title: "+ row[1])
                    print("Price: "+ str(row[2]))
                    print("Number of Pages: "+ str(row[3]))
                    print("Genre: "+ row[4])

                sql2 = """select auth_fname, auth_lname from writes 
                        where isbn = %d;""" %(isbn)
                
                sql3 = """select pub_name from publishes  
                        where isbn = %d;""" %(isbn)
                    
                cursor.execute(sql2)

                data_list = cursor.fetchall()
                
                for row in data_list:
                    print('Author name: ' + row[0] + " " + row[1])
                
                cursor.execute(sql3)

                data_list = cursor.fetchall()
                
                for row in data_list:
                    print('Publisher: ' + row[0])
                

                print()

            elif(userinput == '4'):
                print("Please enter Author first name")
                auth_fname = input('> ')
                print("Please enter Author last name")
                auth_lname = input('> ')

                sql = """select * from writes 
                        where auth_fname = '%s' AND auth_lname = '%s';""" %(auth_fname,auth_lname)
                
                cursor.execute(sql)

                data_list = cursor.fetchall()
                isbn = 0
                for row in data_list:
                    isbn = row[2]
                    print('Author name: ' + row[0] + " " + row[1])
                    
                
                
                sql2 = """select * from books 
                        where isbn = %d;""" %(isbn)
                
                cursor.execute(sql2)

                data_list = cursor.fetchall()

                for row in data_list:
                    isbn = row[0]
                    print("Title: "+ row[1])
                    print("Price: "+ str(row[2]))
                    print("Number of Pages: "+ str(row[3]))
                    print("Genre: "+ row[4])

                sql3 = """select pub_name from publishes  
                        where isbn = %d;""" %(isbn)
                    
                cursor.execute(sql3)

                data_list = cursor.fetchall()
                
                for row in data_list:
                    print('Publisher: ' + row[0])
                

                print()       

            else:
                continue

        
        elif (userinput == '2'):
            checkout()   
            break
                
        elif (userinput == '3'):
            mainmenu()     
      
    
if __name__ == '__main__':
    welcome()
