import mysql.connector
from mysql.connector import Error

# ── Database Connection ──────────────────────────────────────
def connect():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root@1234",  # Change this
            database="hospital_db"
        )
        return conn
    except Error as e:
        print(f"Connection Error: {e}")
        return None

# ── Create Table ─────────────────────────────────────────────
def create_table():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                disease VARCHAR(100) NOT NULL,
                amount_paid FLOAT NOT NULL,
                status VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()
        conn.close()

# ── Add Patient ──────────────────────────────────────────────
def add_patient():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        print("\n--- Add New Patient ---")
        name    = input("Enter Patient Name   : ")
        age     = int(input("Enter Patient Age    : "))
        disease = input("Enter Disease        : ")
        amount  = float(input("Enter Amount Paid    : "))
        status  = input("Enter Status (Admitted/Discharged): ")

        query = "INSERT INTO patients (name, age, disease, amount_paid, status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, age, disease, amount, status))
        conn.commit()
        print(f"\n✅ Patient '{name}' added successfully!")
        conn.close()

# ── View All Patients ────────────────────────────────────────
def view_patients():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        rows = cursor.fetchall()
        print("\n--- All Patients ---")
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Disease':<20} {'Amount':<10} {'Status'}")
        print("-" * 70)
        if rows:
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<5} {row[3]:<20} {row[4]:<10} {row[5]}")
        else:
            print("No patients found.")
        conn.close()

# ── Search Patient ───────────────────────────────────────────
def search_patient():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        print("\n--- Search Patient ---")
        name = input("Enter Patient Name to Search: ")
        cursor.execute("SELECT * FROM patients WHERE name LIKE %s", (f"%{name}%",))
        rows = cursor.fetchall()
        if rows:
            print(f"\n{'ID':<5} {'Name':<20} {'Age':<5} {'Disease':<20} {'Amount':<10} {'Status'}")
            print("-" * 70)
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<5} {row[3]:<20} {row[4]:<10} {row[5]}")
        else:
            print(f"No patient found with name '{name}'")
        conn.close()

# ── Update Patient ───────────────────────────────────────────
def update_patient():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        print("\n--- Update Patient ---")
        pid    = int(input("Enter Patient ID to Update: "))
        status = input("Enter New Status (Admitted/Discharged): ")
        amount = float(input("Enter New Amount Paid: "))
        cursor.execute(
            "UPDATE patients SET status=%s, amount_paid=%s WHERE id=%s",
            (status, amount, pid)
        )
        conn.commit()
        if cursor.rowcount > 0:
            print(f"✅ Patient ID {pid} updated successfully!")
        else:
            print(f"❌ No patient found with ID {pid}")
        conn.close()

# ── Delete Patient ───────────────────────────────────────────
def delete_patient():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        print("\n--- Delete Patient ---")
        pid = int(input("Enter Patient ID to Delete: "))
        cursor.execute("DELETE FROM patients WHERE id=%s", (pid,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"✅ Patient ID {pid} deleted successfully!")
        else:
            print(f"❌ No patient found with ID {pid}")
        conn.close()

# ── Main Menu ────────────────────────────────────────────────
def main():
    create_table()
    while True:
        print("\n=============================")
        print("  Hospital Management System ")
        print("=============================")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Exit")
        print("=============================")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            update_patient()
        elif choice == "5":
            delete_patient()
        elif choice == "6":
            print("\n👋 Thank you! Goodbye!")
            break
        else:
            print("❌ Invalid choice! Enter 1-6")

if __name__ == "__main__":
    main()