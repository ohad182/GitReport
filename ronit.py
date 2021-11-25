def ex1():
    excellent_score = 95  # for dynamically setting the score
    excellent_students_counter = 0

    student_name = input("Please enter student name: ")
    while student_name != "FINISH":
        quiz_score = int(input("Please enter {} test score: ".format(student_name)))
        # i guess you dont need int validation, if you do let me know
        if quiz_score > excellent_score:
            excellent_students_counter = excellent_students_counter + 1
        student_name = input("Please enter student name: ")

    print("{} students scored higher than {}".format(excellent_students_counter, excellent_score))


def ex2():
    dish_price = 9  # for dynamically setting the dish price
    client_list = []

    client_name = input("Please enter client name: ")
    while client_name != "SOF":
        dishes = int(input("How many dishes did {} ordered? ".format(client_name)))
        # i guess you dont need int validation, if you do let me know
        client_list.append({
            "client_name": client_name,
            "dishes": dishes,
            "total_price": dish_price * dishes
        })
        client_name = input("Please enter client name: ")

    print("*" * 50)
    print("Today we served {} clients".format(len(client_list)))
    for client in client_list:
        print("{} ordered {} dishes with total of {}".format(client['client_name'], client['dishes'],
                                                             client['total_price']))


def ex3():
    international_cell_rate = int(input("Please enter cell rate: "))
    client_list = []
    total_income = 0
    client_name = input("Please enter client name: ")
    while client_name != "BYE":
        minutes = int(input("Hi {}, How many minutes did you make? ".format(client_name)))
        # i guess you dont need int validation, if you do let me know
        client_list.append({
            "client_name": client_name,
            "minutes": minutes,
            "total_price": international_cell_rate * minutes
        })
        total_income = total_income + (international_cell_rate * minutes)
        client_name = input("Please enter client name: ")

    print("*" * 50)
    print("Our total income is: {}".format(total_income))
    for client in client_list:
        print("{} talked {} minutes and debt is: {}".format(client['client_name'], client['minutes'],
                                                            client['total_price']))


def ex4():
    hagay_votes = 0
    hadas_votes = 0
    student_name = input("Please enter your name: ")
    while student_name != "SOF":
        vote = int(input("Hi {}, Who do you vote for [1-hagay, 2-hadas]? ".format(student_name)))
        # i guess you dont need int validation, if you do let me know
        if vote == 1:
            hagay_votes = hagay_votes + 1
        elif vote == 2:
            hadas_votes = hadas_votes + 1
        else:
            print("Sorry, invalid vote.")
        student_name = input("Please enter your name: ")

    print("*" * 50)
    print("Hagay got {} votes and Hadas got {} votes".format(hagay_votes, hadas_votes))


def ex5():
    ticket_price = 10
    class_list = []
    total_money_collected = 0
    class_name = input("Please enter class name: ")
    while class_name != "BYE BYE":
        number_of_students = int(input("How many students are in {}? ".format(class_name)))
        # i guess you dont need int validation, if you do let me know
        class_list.append({
            "class_name": class_name,
            "number_of_students": number_of_students
        })
        total_money_collected = total_money_collected + (number_of_students * ticket_price)
        class_name = input("Please enter class name: ")

    print("*" * 50)
    print("Total money collected for the party: {}".format(total_money_collected))
    for clas in class_list:
        print("{} has {} students".format(clas['class_name'], clas['number_of_students']))


def ex6():
    play_cost = 4
    total_kids = 0
    kid_list = []
    kid_name = input("Please enter kid name: ")
    while kid_name != "END OF DAY":
        games = int(input("Hi {}, How many games did you play? ".format(kid_name)))
        # i guess you dont need int validation, if you do let me know
        kid_list.append({
            "kid_name": kid_name,
            "games": games
        })
        total_kids = total_kids + 1
        kid_name = input("Please enter kid name: ")

    print("*" * 50)
    print("Total kids: {}".format(total_kids))
    for kid in kid_list:
        print("{} played {} games spent: {} coins".format(kid['kid_name'], kid['games'],
                                                          kid['games'] * play_cost))


def ex7():
    ex1()


def ex8():
    new_clients = list()
    voucher_counter = 0
    book_counter = 0
    name = input("Please enter your name: ")
    while name != "SOF":
        age = int(input("Hi {}, How old are you? ".format(name)))
        new_client = {
            "name": name,
            "age": age
        }
        if age > 50:
            new_client["gift"] = "voucher"
            voucher_counter = voucher_counter + 1
        else:
            new_client["gift"] = "book"
            book_counter = book_counter + 1
        new_clients.append(new_client)
        name = input("Please enter your name: ")

    print("*" * 50)
    print("Our clients received {} books and {} vouchers".format(book_counter, voucher_counter))
    for client in new_clients:
        print("client name: {}, gift: {}".format(client["name"], client["gift"]))


if __name__ == "__main__":
    ex8()
