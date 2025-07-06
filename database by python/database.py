class DataBaseManagment:

    def __init__(self, filename="DataBase.txt"):
        self.filename = filename
        self.next_id = self.get_next_id()

    def get_next_id(self):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                if not lines:
                    return 1
                last_line = lines[-1].strip()
                last_id = int(last_line.split(',')[0])
                return last_id + 1
        except FileNotFoundError:
            return 1

    def id_exists(self, user_id):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    if line.strip().split(',')[0] == str(user_id):
                        return True
        except FileNotFoundError:
            return False
        return False

    def add_user(self, name, email, age, city, user_id=None):
        if user_id is not None:
            if self.id_exists(user_id):
                print(f"❌ Error: User ID {user_id} already exists.")
                return
        else:
            user_id = self.next_id

        with open(self.filename, 'a') as file:
            file.write(f"{user_id},{name},{email},{age},{city}\n")
        print("✅ User added successfully.")

        if user_id == self.next_id:
            self.next_id += 1

    def delete_user_by_id(self, user_id):
        lines_kept = []
        found = False
        with open(self.filename, 'r') as file:
            for line in file:
                line_parts = line.strip().split(',')
                if line_parts[0] != str(user_id):
                    lines_kept.append(line)
                else:
                    found = True
        with open(self.filename, 'w') as file:
            file.writelines(lines_kept)
        if found:
            print("🗑️ User deleted successfully.")
        else:
            print("⚠️ User ID not found.")

    def get_user_by_id(self, user_id):
        with open(self.filename, 'r') as file:
            for line in file:
                id_, name, email, age, city = line.strip().split(',')
                if id_ == str(user_id):
                    return f"ID: {id_}, Name: {name}, Email: {email}, Age: {age}, City: {city}"
        return "⚠️ User ID not found."

    def get_all_users(self):
        users = []
        with open(self.filename, 'r') as file:
            for line in file:
                users.append(line.strip())
        return users

    def __repr__(self):
        return "DataBaseManagment Class - Manage user data by ID"


# --------- Interactive Menu ----------
if __name__ == "__main__":
    db = DataBaseManagment()

    while True:
        print("\n📋 DataBase Management Menu:")
        print("1. Add User")
        print("2. Delete User by ID")
        print("3. Show All Users")
        print("4. Search User by ID")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            custom_id = input("Do you want to enter a custom ID? (y/n): ").lower()
            if custom_id == 'y':
                user_id = input("Enter custom ID: ")
                if not user_id.isdigit():
                    print("❌ Invalid ID. Must be a number.")
                    continue
                user_id = int(user_id)
            else:
                user_id = None

            name = input("Enter name: ")
            email = input("Enter email: ")
            age = input("Enter age: ")
            city = input("Enter city: ")
            db.add_user(name, email, age, city, user_id)

        elif choice == "2":
            user_id = input("Enter ID to delete user: ")
            db.delete_user_by_id(user_id)

        elif choice == "3":
            users = db.get_all_users()
            print("\n--- All Users ---")
            for user in users:
                print(user)

        elif choice == "4":
            user_id = input("Enter ID to search: ")
            print(db.get_user_by_id(user_id))

        elif choice == "5":
            print("Exiting program. Goodbye! 👋")
            break

        else:
            print("❌ Invalid choice. Try again.")
