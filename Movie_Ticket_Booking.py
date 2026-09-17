print("=" * 60)
print("MOVIE TICKET BOOKING SYSTEM")
print("=" * 60)

# ============================================================
# MOVIE DATA
# ============================================================

movies = [
    [1, "Avengers", "English", "Action", "10:00 AM", 200],
    [2, "Avatar", "English", "Sci-Fi", "01:00 PM", 180],
    [3, "KGF", "Kannada", "Action", "04:00 PM", 150],
    [4, "Pushpa", "Telugu", "Action", "07:00 PM", 160],
    [5, "Dangal", "Hindi", "Sports", "09:00 PM", 120],
    [6, "Jawan", "Hindi", "Action", "06:00 PM", 180],
    [7, "3 Idiots", "Hindi", "Comedy", "02:00 PM", 130],
    [8, "RRR", "Telugu", "Action", "11:00 AM", 170],
    [9, "Baahubali", "Telugu", "Action", "05:00 PM", 190],
    [10, "Pathaan", "Hindi", "Action", "08:00 PM", 180],
    [11, "Animal", "Hindi", "Drama", "09:30 PM", 200],
    [12, "Stree 2", "Hindi", "Horror", "07:30 PM", 160]
]

movie_type_price = {
    "2D": 0,
    "3D": 80
}

seat_type_price = {
    "Normal": 0,
    "Premium": 50
}

snack_price = {
    "No Snacks": 0,
    "Popcorn": 120,
    "Cold Drink": 80,
    "Popcorn + Cold Drink": 180
}

# ============================================================
# USER STORAGE (REGISTRATION / LOGIN)
# ============================================================

users = []          # each user -> [user_id, name, mobile, password]
user_id_counter = 1001

# ============================================================
# BOOKING STORAGE
# ============================================================

bookings = []

ticket_number = 101
transaction_number = 1001

# ============================================================
# SEAT LAYOUT
# ============================================================
# Normal Seats:  A1-A10, B1-B10
# Premium Seats: P1-P10
# Total = 30 seats

seat_list = []

# Normal Rows
for seat in range(1, 11):
    seat_list.append("A" + str(seat))

for seat in range(1, 11):
    seat_list.append("B" + str(seat))

# Premium Row
for seat in range(1, 11):
    seat_list.append("P" + str(seat))

# ============================================================
# INPUT VALIDATION FUNCTIONS
# ============================================================

def get_integer(message):
    while True:
        value = input(message)

        if value.isdigit():
            return int(value)

        print("Invalid input. Please enter a number.")


def get_positive_integer(message):
    while True:
        value = get_integer(message)

        if value > 0:
            return value

        print("Please enter a number greater than 0.")


def get_name(message):
    while True:
        name = input(message).strip()

        if name == "":
            print("Name cannot be empty.")
        elif not name.replace(" ", "").isalpha():
            print("Please enter a valid name using letters only.")
        else:
            return name


def get_mobile_number(message):
    while True:
        mobile = input(message).strip()

        if len(mobile) == 10 and mobile.isdigit() and mobile[0] in "6789":
            return mobile

        print("Invalid mobile number. Enter a valid 10-digit mobile number.")


def get_password(message):
    while True:
        password = input(message).strip()

        if len(password) < 6:
            print("Password must be at least 6 characters long.")
            continue

        if " " in password:
            print("Password cannot contain spaces.")
            continue

        return password


def is_valid_date(date):
    # Expected format: DD-MM-YYYY
    if len(date) != 10:
        return False

    if date[2] != "-" or date[5] != "-":
        return False

    day = date[0:2]
    month = date[3:5]
    year = date[6:10]

    if not day.isdigit() or not month.isdigit() or not year.isdigit():
        return False

    day = int(day)
    month = int(month)
    year = int(year)

    if year < 2026 or year > 2100:
        return False

    if month < 1 or month > 12:
        return False

    days_in_month = [
        31, 28, 31, 30, 31, 30,
        31, 31, 30, 31, 30, 31
    ]

    # Leap year calculation
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        days_in_month[1] = 29

    if day < 1 or day > days_in_month[month - 1]:
        return False

    return True


def get_movie_date():
    while True:
        movie_date = input("Enter Movie Date (DD-MM-YYYY): ").strip()

        if is_valid_date(movie_date):
            return movie_date

        print("Invalid date. Please enter a valid date like 25-09-2026.")


def get_card_number(message):
    while True:
        card_number = input(message).replace(" ", "").strip()

        if len(card_number) == 16 and card_number.isdigit():
            return card_number

        print("Invalid card number. Enter 16 digits.")


def get_cvv():
    while True:
        cvv = input("Enter CVV: ").strip()

        if len(cvv) == 3 and cvv.isdigit():
            return cvv

        print("Invalid CVV. Enter 3 digits.")


def get_upi_id():
    while True:
        upi_id = input("Enter UPI ID: ").strip()

        if "@" in upi_id and len(upi_id) >= 5:
            return upi_id

        print("Invalid UPI ID. Example: name@upi")


def get_account_number():
    while True:
        account_number = input("Enter Account Number: ").strip()

        if account_number.isdigit() and 9 <= len(account_number) <= 18:
            return account_number

        print("Invalid account number.")


def get_otp():
    while True:
        otp = input("Enter OTP: ").strip()

        if len(otp) == 6 and otp.isdigit():
            return otp

        print("Invalid OTP. Enter 6 digits.")


# ============================================================
# REGISTRATION / LOGIN
# ============================================================

def find_user_by_mobile(mobile):
    for user in users:
        if user[2] == mobile:
            return user
    return None


def find_user_by_id(user_id):
    for user in users:
        if user[0] == user_id:
            return user
    return None


def register_user():
    print("\n========================================")
    print("             REGISTRATION")
    print("========================================")

    global user_id_counter

    name = get_name("Enter Full Name: ")
    mobile = get_mobile_number("Enter Mobile Number: ")

    existing_user = find_user_by_mobile(mobile)

    if existing_user is not None:
        print("\nThis mobile number is already registered.")
        print("Your User ID is:", existing_user[0])
        print("Please login instead.")
        return

    password = get_password("Set Password (min 6 characters, no spaces): ")

    confirm_password = input("Confirm Password: ").strip()

    while confirm_password != password:
        print("Passwords do not match. Please try again.")
        confirm_password = input("Confirm Password: ").strip()

    user_id = "U" + str(user_id_counter)
    user_id_counter = user_id_counter + 1

    new_user = [user_id, name, mobile, password]
    users.append(new_user)

    print("\n----------------------------------------")
    print("Registration Successful!")
    print("Your User ID :", user_id)
    print("Please remember this User ID. You will need it to login.")
    print("----------------------------------------")


def login_user():
    print("\n========================================")
    print("                LOGIN")
    print("========================================")

    if len(users) == 0:
        print("No registered users found. Please register first.")
        return None

    attempts = 3

    while attempts > 0:
        user_id = input("Enter User ID: ").strip().upper()
        password = input("Enter Password: ").strip()

        user = find_user_by_id(user_id)

        if user is not None and user[3] == password:
            print("\nLogin Successful! Welcome,", user[1] + ".")
            return user

        attempts = attempts - 1

        if attempts > 0:
            print("Invalid User ID or Password. Attempts remaining:", attempts)
        else:
            print("Invalid User ID or Password.")

    print("\nToo many failed attempts. Returning to main menu.")
    return None


# ============================================================
# DISPLAY MOVIES
# ============================================================

def display_movies():
    print("\n==============================================================")
    print(" AVAILABLE MOVIES")
    print("==============================================================")

    print("ID   MOVIE NAME       LANGUAGE    GENRE       TIME       PRICE")
    print("--------------------------------------------------------------")

    for movie in movies:
        print(
            str(movie[0]).ljust(5),
            movie[1].ljust(16),
            movie[2].ljust(11),
            movie[3].ljust(11),
            movie[4].ljust(11),
            "₹" + str(movie[5])
        )

    print("==============================================================")


# ============================================================
# VIEW MOVIE TYPE AND PRICE
# ============================================================

def display_movie_type_price():
    print("\n========================================")
    print(" MOVIE TYPE & PRICE")
    print("========================================")
    print("2D -> ₹0 Extra")
    print("3D -> ₹80 Extra")
    print("========================================")


# ============================================================
# VIEW SEAT TYPE AND PRICE
# ============================================================

def display_seat_type_price():
    print("\n========================================")
    print(" SEAT TYPE & PRICE")
    print("========================================")
    print("Normal -> ₹0 Extra")
    print("Premium -> ₹50 Extra")
    print("========================================")


# ============================================================
# VIEW SNACK MENU
# ============================================================

def display_snack_menu():
    print("\n========================================")
    print(" SNACK MENU & PRICE")
    print("========================================")
    print("No Snacks -> ₹0")
    print("Popcorn -> ₹120")
    print("Cold Drink -> ₹80")
    print("Popcorn + Cold Drink -> ₹180")
    print("========================================")


# ============================================================
# SEARCH MOVIE
# ============================================================

def search_movie():
    print("\n========================================")
    print(" SEARCH MOVIE")
    print("========================================")

    movie_name = input("Enter Movie Name: ").strip()

    if movie_name == "":
        print("Movie name cannot be empty.")
        return

    found = False

    for movie in movies:
        if movie_name.lower() in movie[1].lower():
            print("\nMovie Found")
            print("----------------------------------------")
            print("Movie ID     :", movie[0])
            print("Movie Name   :", movie[1])
            print("Language     :", movie[2])
            print("Genre        :", movie[3])
            print("Show Time    :", movie[4])
            print("Ticket Price : ₹", movie[5])
            print("----------------------------------------")

            found = True

    if not found:
        print("\nMovie not found.")


# ============================================================
# FIND MOVIE
# ============================================================

def find_movie(movie_id):
    for movie in movies:
        if movie[0] == movie_id:
            return movie

    return None


# ============================================================
# GET BOOKED SEATS FOR A PARTICULAR SHOW
# ============================================================

def get_booked_seats(movie_name, movie_date, show_time):
    booked_seats = []

    for booking in bookings:
        if (
            booking[4] == movie_name
            and booking[3] == movie_date
            and booking[5] == show_time
            and booking[13] == "Confirmed"
        ):
            for seat in booking[9]:
                booked_seats.append(seat)

    return booked_seats


# ============================================================
# VIEW AVAILABLE SEATS
# ============================================================

def view_available_seats():
    print("\n========================================")
    print(" VIEW AVAILABLE SEATS")
    print("========================================")

    display_movies()

    movie_id = get_integer("\nEnter Movie ID: ")
    movie = find_movie(movie_id)

    if movie is None:
        print("Invalid Movie ID.")
        return

    movie_date = get_movie_date()

    booked_seats = get_booked_seats(movie[1], movie_date, movie[4])

    available_seats = []

    for seat in seat_list:
        if seat not in booked_seats:
            available_seats.append(seat)

    print("\nMovie     :", movie[1])
    print("Date      :", movie_date)
    print("Show Time :", movie[4])
    print("----------------------------------------")

    print("Total Seats     :", len(seat_list))
    print("Booked Seats    :", len(booked_seats))
    print("Available Seats :", len(available_seats))

    print("\nAvailable Normal Seats:")

    normal_available = []

    for seat in available_seats:
        if seat.startswith("A") or seat.startswith("B"):
            normal_available.append(seat)

    if len(normal_available) == 0:
        print("No Normal Seats available.")
    else:
        print(", ".join(normal_available))

    print("\nAvailable Premium Seats:")

    premium_available = []

    for seat in available_seats:
        if seat.startswith("P"):
            premium_available.append(seat)

    if len(premium_available) == 0:
        print("No Premium Seats available.")
    else:
        print(", ".join(premium_available))

    print("========================================")


# ============================================================
# SELECT SEATS
# ============================================================

def select_seats(movie_name, movie_date, show_time, number_of_tickets):
    booked_seats = get_booked_seats(movie_name, movie_date, show_time)

    available_seats = []

    for seat in seat_list:
        if seat not in booked_seats:
            available_seats.append(seat)

    print("\n----- Seat Selection -----")
    print("Normal Seats  : A1-A10, B1-B10")
    print("Premium Seats : P1-P10")

    if len(available_seats) < number_of_tickets:
        print("Only", len(available_seats), "seats are available.")
        return None

    print("Available Normal Seats:")
    normal_available = []

    for seat in available_seats:
        if seat.startswith("A") or seat.startswith("B"):
            normal_available.append(seat)

    if len(normal_available) > 0:
        print(", ".join(normal_available))
    else:
        print("No Normal Seats Available.")

    print("\nAvailable Premium Seats:")
    premium_available = []

    for seat in available_seats:
        if seat.startswith("P"):
            premium_available.append(seat)

    if len(premium_available) > 0:
        print(", ".join(premium_available))
    else:
        print("No Premium Seats Available.")

    selected_seats = []

    while len(selected_seats) < number_of_tickets:
        print("\nSeat", len(selected_seats) + 1, "of", number_of_tickets)

        seat = input("Enter Seat Number: ").strip().upper()

        if seat not in seat_list:
            print("Invalid seat number.")
            continue

        if seat in booked_seats:
            print("This seat is already booked.")
            continue

        if seat in selected_seats:
            print("You already selected this seat.")
            continue

        selected_seats.append(seat)
        print("Seat", seat, "selected successfully.")

    return selected_seats


# ============================================================
# PAYMENT
# ============================================================

def process_payment(payment_choice, total_amount, mobile_number):
    global transaction_number

    payment_method = ""
    online_method = ""
    transaction_id = ""

    if payment_choice == 1:

        payment_method = "Online"

        print("\n----- Online Payment Methods -----")
        print("1. UPI")
        print("2. Debit Card")
        print("3. Credit Card")
        print("4. Net Banking")

        online_choice = get_integer("Select Online Method: ")

        if online_choice == 1:

            online_method = "UPI"

            print("\n----- UPI Payment -----")
            upi_id = get_upi_id()

            print("\nUPI ID :", upi_id)

        elif online_choice == 2:

            online_method = "Debit Card"

            print("\n----- Debit Card Payment -----")

            card_number = get_card_number("Enter Debit Card Number: ")
            card_name = get_name("Enter Card Holder Name: ")
            cvv = get_cvv()

            # CVV is only used for this simulated payment.
            print("\nCard Number :", "XXXX XXXX XXXX " + card_number[-4:])
            print("Card Holder Name :", card_name)

        elif online_choice == 3:

            online_method = "Credit Card"

            print("\n----- Credit Card Payment -----")

            card_number = get_card_number("Enter Credit Card Number: ")
            card_name = get_name("Enter Card Holder Name: ")
            cvv = get_cvv()

            # CVV is only used for this simulated payment.
            print("\nCard Number :", "XXXX XXXX XXXX " + card_number[-4:])
            print("Card Holder Name :", card_name)

        elif online_choice == 4:

            online_method = "Net Banking"

            print("\n----- Net Banking Payment -----")

            print("1. State Bank of India (SBI)")
            print("2. HDFC Bank")
            print("3. ICICI Bank")
            print("4. Axis Bank")
            print("5. Bank of Baroda")
            print("6. Punjab National Bank (PNB)")
            print("7. Kotak Mahindra Bank")
            print("8. Canara Bank")

            bank_choice = get_integer("Select Bank: ")

            banks = {
                1: "State Bank of India (SBI)",
                2: "HDFC Bank",
                3: "ICICI Bank",
                4: "Axis Bank",
                5: "Bank of Baroda",
                6: "Punjab National Bank (PNB)",
                7: "Kotak Mahindra Bank",
                8: "Canara Bank"
            }

            if bank_choice not in banks:
                print("Invalid Bank Selection.")
                return None

            bank_name = banks[bank_choice]

            print("\nSelected Bank :", bank_name)

            account_number = get_account_number()
            otp = get_otp()

            print("\nAccount Number :", "XXXXXX" + account_number[-4:])
            print("Bank Name      :", bank_name)

        else:
            print("Invalid Online Method.")
            return None

        print("\n----------------------------------------")
        print("Processing Payment...")
        print("Payment Amount : ₹", round(total_amount, 2))
        print("Mobile Number  :", mobile_number)
        print("----------------------------------------")
        print("Payment Successful!")

        transaction_id = "TXN" + str(transaction_number)
        transaction_number = transaction_number + 1

        print("Transaction ID :", transaction_id)

        return {
            "payment_method": payment_method,
            "online_method": online_method,
            "transaction_id": transaction_id
        }

    elif payment_choice == 2:

        payment_method = "Cash"
        online_method = "Cash"

        print("\nPayment Method : Cash")
        print("Payment will be collected at the counter.")

        transaction_id = "CASH" + str(transaction_number)
        transaction_number = transaction_number + 1

        print("Transaction ID :", transaction_id)

        return {
            "payment_method": payment_method,
            "online_method": online_method,
            "transaction_id": transaction_id
        }

    else:
        print("Invalid Payment Method.")
        return None


# ============================================================
# PRINT PROFESSIONAL TICKET
# ============================================================

def print_ticket(booking):
    print("\n")
    print("============================================================")
    print(" MOVIE TICKET")
    print("============================================================")
    print("Ticket Number :", booking[0])
    print("Transaction ID :", booking[12])
    print("Booking Status :", booking[13])
    print("------------------------------------------------------------")
    print("Customer Name :", booking[1])
    print("Mobile Number :", booking[2])
    print("Movie Date :", booking[3])
    print("Movie Name :", booking[4])
    print("Show Time :", booking[5])
    print("Movie Type :", booking[6])
    print("Seat Type :", booking[7])
    print("Seat Numbers :", ", ".join(booking[9]))
    print("Tickets :", booking[8])
    print("Snacks :", booking[10])
    print("Payment Method :", booking[11])
    print("Total Amount : ₹", booking[14])
    print("============================================================")
    print(" Thank You For Booking!")
    print(" Enjoy Your Movie!")
    print("============================================================")


# ============================================================
# BOOK TICKET
# ============================================================

def book_ticket(current_user):
    global ticket_number

    print("\n========================================")
    print("             BOOK TICKET")
    print("========================================")

    # CUSTOMER INFORMATION (auto-filled from logged-in account)
    print("\n----- Customer Information -----")

    customer_name = current_user[1]
    mobile_number = current_user[2]

    print("Customer Name :", customer_name)
    print("Mobile Number :", mobile_number)

    movie_date = get_movie_date()

    # MOVIE SELECTION
    print("\n----- Movie Selection -----")

    display_movies()

    movie_id = get_integer("\nEnter Movie ID: ")

    movie = find_movie(movie_id)

    if movie is None:
        print("\nInvalid Movie ID.")
        return

    movie_name = movie[1]
    show_time = movie[4]
    base_price = movie[5]

    print("\nSelected Movie :", movie_name)
    print("Show Time      :", show_time)
    print("Movie Price    : ₹", base_price)

    # MOVIE TYPE
    print("\n----- Movie Type Selection -----")
    print("1. 2D -> ₹0 Extra")
    print("2. 3D -> ₹80 Extra")

    movie_type_choice = get_integer("Select Movie Type: ")

    if movie_type_choice == 1:
        movie_type = "2D"
    elif movie_type_choice == 2:
        movie_type = "3D"
    else:
        print("Invalid Movie Type.")
        return

    extra_movie_price = movie_type_price[movie_type]

    print("Selected Movie Type :", movie_type)
    print("Extra Price         : ₹", extra_movie_price)

    # SEAT TYPE
    print("\n----- Seat Type Selection -----")
    print("1. Normal  -> ₹0 Extra")
    print("2. Premium -> ₹50 Extra")

    seat_choice = get_integer("Select Seat Type: ")

    if seat_choice == 1:
        seat_type = "Normal"
    elif seat_choice == 2:
        seat_type = "Premium"
    else:
        print("Invalid Seat Type.")
        return

    extra_seat_price = seat_type_price[seat_type]

    print("Selected Seat Type :", seat_type)
    print("Extra Price        : ₹", extra_seat_price)

    # SHOW TIME
    print("\n----- Show Time -----")
    print("Movie     :", movie_name)
    print("Show Time :", show_time)

    # NUMBER OF TICKETS
    print("\n----- Number of Tickets -----")

    number_of_tickets = get_positive_integer("Enter Number of Tickets: ")

    if number_of_tickets > len(seat_list):
        print("Maximum", len(seat_list), "tickets can be booked.")
        return

    # SEAT SELECTION
    selected_seats = select_seats(
        movie_name,
        movie_date,
        show_time,
        number_of_tickets
    )

    if selected_seats is None:
        return

    # SNACKS
    print("\n----- Snacks Selection -----")
    print("1. No Snacks             -> ₹0")
    print("2. Popcorn               -> ₹120")
    print("3. Cold Drink            -> ₹80")
    print("4. Popcorn + Cold Drink  -> ₹180")

    snack_choice = get_integer("Select Snacks: ")

    if snack_choice == 1:
        snacks = "No Snacks"
    elif snack_choice == 2:
        snacks = "Popcorn"
    elif snack_choice == 3:
        snacks = "Cold Drink"
    elif snack_choice == 4:
        snacks = "Popcorn + Cold Drink"
    else:
        print("Invalid Snack Choice.")
        return

    extra_snack_price = snack_price[snacks]

    print("Selected Snacks :", snacks)
    print("Snack Price     : ₹", extra_snack_price)

    # PRICE CALCULATION
    print("\n========================================")
    print("             PRICE CALCULATION")
    print("========================================")

    movie_total = base_price * number_of_tickets
    movie_type_total = extra_movie_price * number_of_tickets
    seat_total = extra_seat_price * number_of_tickets
    snack_total = extra_snack_price

    service_charge = 30

    subtotal = (
        movie_total
        + movie_type_total
        + seat_total
        + snack_total
    )

    gst = (subtotal + service_charge) * 5 / 100

    total_amount = subtotal + service_charge + gst

    print("Movie Ticket Charges : ₹", movie_total)
    print("Movie Type Charges   : ₹", movie_type_total)
    print("Seat Type Charges    : ₹", seat_total)
    print("Snacks Charges       : ₹", snack_total)
    print("Service Charge       : ₹", service_charge)
    print("GST 5%               : ₹", round(gst, 2))
    print("----------------------------------------")
    print("Total Amount         : ₹", round(total_amount, 2))

    # PAYMENT
    print("\n========================================")
    print("             PAYMENT METHOD")
    print("========================================")

    print("1. Online")
    print("2. Cash")

    payment_choice = get_integer("Select Payment Method: ")

    payment_result = process_payment(
        payment_choice,
        total_amount,
        mobile_number
    )

    if payment_result is None:
        return

    online_method = payment_result["online_method"]
    transaction_id = payment_result["transaction_id"]

    # BOOKING CONFIRMATION
    print("\n========================================")
    print("          BOOKING CONFIRMATION")
    print("========================================")

    print("Customer Name :", customer_name)
    print("Movie         :", movie_name)
    print("Date          :", movie_date)
    print("Show Time     :", show_time)
    print("Seat Numbers  :", ", ".join(selected_seats))
    print("Tickets       :", number_of_tickets)
    print("Total Amount  : ₹", round(total_amount, 2))
    print("Payment       :", online_method)

    confirmation = input("\nConfirm Booking? (yes/no): ").strip().lower()

    if confirmation == "yes":

        current_ticket_number = ticket_number
        ticket_number = ticket_number + 1

        booking_status = "Confirmed"

        booking = [
            current_ticket_number,        # 0 Ticket number
            customer_name,                 # 1 Customer name
            mobile_number,                  # 2 Mobile
            movie_date,                     # 3 Date
            movie_name,                     # 4 Movie
            show_time,                      # 5 Time
            movie_type,                     # 6 Movie type
            seat_type,                      # 7 Seat type
            number_of_tickets,              # 8 Number of tickets
            selected_seats,                 # 9 Seat numbers
            snacks,                         # 10 Snacks
            online_method,                  # 11 Payment method
            transaction_id,                 # 12 Transaction ID
            booking_status,                 # 13 Status
            round(total_amount, 2)          # 14 Total amount
        ]

        bookings.append(booking)

        print("\nBooking Completed Successfully!")

        print_ticket(booking)

    else:
        print("\nBooking Cancelled Before Confirmation.")


# ============================================================
# SEARCH TICKET BY TICKET NUMBER
# ============================================================

def search_ticket():
    print("\n========================================")
    print(" SEARCH TICKET")
    print("========================================")

    ticket = get_integer("Enter Ticket Number: ")

    found = False

    for booking in bookings:
        if booking[0] == ticket:

            if booking[13] == "Cancelled":
                print("\nThis ticket is cancelled.")

            print_ticket(booking)

            found = True
            break

    if not found:
        print("\nTicket not found.")


# ============================================================
# SEARCH TICKET BY MOBILE NUMBER (defaults to logged-in user)
# ============================================================

def search_ticket_by_mobile(current_user):
    print("\n========================================")
    print(" SEARCH TICKET BY MOBILE")
    print("========================================")

    use_own = input(
        "Search your own bookings (" + current_user[2] + ")? (yes/no): "
    ).strip().lower()

    if use_own == "yes":
        mobile = current_user[2]
    else:
        mobile = get_mobile_number("Enter Mobile Number: ")

    found = False

    for booking in bookings:
        if booking[2] == mobile:

            print_ticket(booking)

            found = True

    if not found:
        print("\nNo booking found for this mobile number.")


# ============================================================
# VIEW ALL BOOKINGS
# ============================================================

def display_all_bookings():
    print("\n========================================")
    print(" ALL BOOKINGS")
    print("========================================")

    if len(bookings) == 0:
        print("No bookings available.")
        return

    for booking in bookings:
        print("\nTicket Number   :", booking[0])
        print("Customer Name   :", booking[1])
        print("Mobile Number   :", booking[2])
        print("Movie Date      :", booking[3])
        print("Movie Name      :", booking[4])
        print("Show Time       :", booking[5])
        print("Movie Type      :", booking[6])
        print("Seat Type       :", booking[7])
        print("Seat Numbers    :", ", ".join(booking[9]))
        print("Tickets         :", booking[8])
        print("Snacks          :", booking[10])
        print("Payment         :", booking[11])
        print("Transaction ID  :", booking[12])
        print("Booking Status  :", booking[13])
        print("Total Amount    : ₹", booking[14])
        print("----------------------------------------")


# ============================================================
# CANCEL TICKET
# ============================================================

def cancel_ticket():
    print("\n========================================")
    print(" CANCEL TICKET")
    print("========================================")

    ticket = get_integer("Enter Ticket Number: ")

    found = False

    for booking in bookings:

        if booking[0] == ticket:

            print("\nTicket Found")

            print("Customer Name :", booking[1])
            print("Movie Name    :", booking[4])
            print("Date          :", booking[3])
            print("Seat Numbers  :", ", ".join(booking[9]))
            print("Total Amount  : ₹", booking[14])
            print("Status        :", booking[13])

            if booking[13] == "Cancelled":
                print("\nThis ticket is already cancelled.")
                found = True
                break

            confirmation = input(
                "\nAre you sure you want to cancel? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":

                # Change status instead of deleting the booking.
                # This keeps the booking history.
                booking[13] = "Cancelled"

                print("\nTicket cancelled successfully.")
                print("Booking status changed to: Cancelled")

            else:
                print("\nTicket cancellation stopped.")

            found = True
            break

    if not found:
        print("\nTicket not found.")


# ============================================================
# AUTHENTICATION MENU (REGISTER / LOGIN)
# ============================================================

def auth_menu():
    while True:
        print("\n")
        print("================================================")
        print("      WELCOME TO MOVIE TICKET BOOKING SYSTEM")
        print("================================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("================================================")

        choice = get_integer("Enter Your Choice: ")

        if choice == 1:
            register_user()

        elif choice == 2:
            user = login_user()

            if user is not None:
                return user

        elif choice == 3:
            print("\nThank you for visiting. Goodbye!")
            return None

        else:
            print("\nInvalid Choice. Please try again.")


# ============================================================
# MAIN MENU (AFTER LOGIN)
# ============================================================

def main_menu(current_user):
    while True:

        print("\n")
        print("================================================")
        print("         MOVIE TICKET BOOKING SYSTEM")
        print("      Logged in as:", current_user[1], "(" + current_user[0] + ")")
        print("================================================")

        print("1.  View Available Movies")
        print("2.  Search Movie")
        print("3.  View Movie Type & Price")
        print("4.  View Seat Type & Price")
        print("5.  View Snack Menu & Price")
        print("6.  View Available Seats")
        print("7.  Book Ticket")
        print("8.  Search Ticket")
        print("9.  Search Ticket By Mobile")
        print("10. View All Bookings")
        print("11. Cancel Ticket")
        print("12. Logout")

        print("================================================")

        choice = get_integer("Enter Your Choice: ")

        if choice == 1:
            display_movies()

        elif choice == 2:
            search_movie()

        elif choice == 3:
            display_movie_type_price()

        elif choice == 4:
            display_seat_type_price()

        elif choice == 5:
            display_snack_menu()

        elif choice == 6:
            view_available_seats()

        elif choice == 7:
            book_ticket(current_user)

        elif choice == 8:
            search_ticket()

        elif choice == 9:
            search_ticket_by_mobile(current_user)

        elif choice == 10:
            display_all_bookings()

        elif choice == 11:
            cancel_ticket()

        elif choice == 12:
            print("\nLogging out", current_user[1] + "...")
            break

        else:
            print("\nInvalid Choice. Please try again.")


# ============================================================
# PROGRAM START
# ============================================================

def main():
    while True:
        logged_in_user = auth_menu()

        if logged_in_user is None:
            print("\n........Have a nice day.........")
            break

        main_menu(logged_in_user)


main()
