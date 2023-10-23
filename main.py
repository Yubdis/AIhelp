import json


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        self.items.append(MenuItem(name, price))

    def remove_item(self, name):
        item_to_remove = self.get_item(name)
        if item_to_remove:
            self.items.remove(item_to_remove)

    def get_item(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None

# load json file and add to menu
    def load_from_json(self, filename):
        with open(filename, 'r') as file:
            menu_data = json.load(file)
            for item in menu_data:
                self.add_item(item, float(menu_data[item]))

class Card:
    def __init__(self, card_number):
        self.card_number = card_number
        self.items_consumed = []
        self.active = False

    def activate_card(self):
        self.active = True

    def deactivate_card(self):
        self.active = False

    def add_order(self, order):
        self.items_consumed.append(order)


class Order:
    def __init__(self):
        self.items = []
        self.order_total = 0

    def add_item(self, item, quantity):
        self.items.append((item, quantity))

    def calculate_total(self, menu):
        total = 0
        for item, quantity in self.items:
            menu_item = menu.get_item(item)
            total += menu_item.price * quantity
        self.order_total = total


class Client:
    def __init__(self, name, phone, ordering_card):
        self.name = name
        self.phone = phone
        self.ordering_card = ordering_card
        self.orders = []

    def make_order(self, order):
        self.orders.append(order)
        order.calculate_total(menu)
        print(f"Order placed for {self.name}. Total cost: ${order.order_total}")

    def finished_order(self, order):
        print(f"Order finished for {self.name}. Total cost: ${order.order_total}")


class ShowMenu:
    def __init__(self):
        self.clients = []
        self.active_client = None

    def display_options(self):
        print("Restaurant Menu Simulation")
        print("1 - Register Client")
        print("2 - Make an Order")
        print("3 - Finish Order")
        print("4 - Show Menu")
        print("0 - Exit")

    def run(self):
        while True:
            self.display_options()
            choice = input("Enter your choice: ")

            if choice == "0":
                print("Exiting the program.")
                break
            elif choice == "1":
                self.register_client()
            elif choice == "2":
                self.make_order()
            elif choice == "3":
                self.finish_order()
            elif choice == "4":
                self.show_menu()
            else:
                print("Invalid choice. Please select a valid option.")

    def register_client(self):
        name = input("Enter client name: ")
        phone = input("Enter client phone number: ")
        card_number = input("Enter client's card number: ")
        client_card = Card(card_number)
        client_card.activate_card()
        client = Client(name, phone, client_card)
        self.clients.append(client)
        self.active_client = client
        print(f"Client {name} registered.")

# need to make option to change active client from clients list
# think there's a conflict between the card_number and the ordering_card. Need to connect those with client and be able to retrieve them
    def get_active_client(self):
        card_number = input("Enter the card number: ")
        for client in self.clients:
            if client.ordering_card.card_number == card_number:
                self.active_client = client
                print(f"Active client set to {client.name}.")
                return
        print("Client not found for the provided card number.")

    def make_order(self):
        if not self.active_client:
            print("No active client. Please register a client first.")
            return

# get_active_client()
# choose from clients list
        client_name = self.get_active_client()
        client_name = self.active_client.name
        print(f"Making an order for {client_name}")

# maybe change how to input order? index based vs name based error check?
        print(self.show_menu())
        order = Order()
        while True:
            item = input("Enter item name (or 0 to finish): ")
            if item == "0":
                break

            quantity = int(input(f"Enter quantity for {item}: "))
            order.add_item(item, quantity)

        self.active_client.make_order(order)
# need to add order to specific client

    def finish_order(self):
        if not self.active_client:
            print("No active client. Please register a client first.")
            return
# get_active_client()
# need to clear order from order card, orders list, clients list
        client_name = self.get_active_client()
        client_name = self.active_client.name
        print(f"Finishing the order for {client_name}")
        active_order = self.active_client.orders[-1]
        active_order.calculate_total(menu)
        print(f"Total cost of the order: ${active_order.order_total}")

        # Remove the order from the ordering card
        self.active_client.ordering_card.items_consumed.remove(active_order)

        # Remove the order from the client's orders list
        self.active_client.orders.remove(active_order)

        # Deactivate the ordering card
        self.active_client.ordering_card.deactivate_card()
        self.active_client = None

        print(
            f"Order finished for {client_name}. The ordering card has been deactivated.")

    def show_menu(self):
        print("Menu:")
        for item in menu.items:
            print(f"{item.name}: ${item.price}")

    def start(self):
        self.run()


# Load the menu from a JSON file
menu = Menu()
menu.load_from_json("arqmenu.json")

# Create a ShowMenu instance and start the simulation
menu_simulator = ShowMenu()
menu_simulator.start()
