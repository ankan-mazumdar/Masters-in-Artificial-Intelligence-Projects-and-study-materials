import tkinter as tk
from tkinter import messagebox
import mysql.connector

def display_connection_details():
    mydb = connect_mysql()
    if mydb is not None:
        try:
            server_info = mydb.get_server_info()
            host_info = mydb.server_host
            db_info = mydb.database
            messagebox.showinfo("Connection Details", f"Server: {server_info}\nHost: {host_info}\nDatabase: {db_info}")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", e)
        finally:
            mydb.close()
    else:
        messagebox.showerror("Error", "Database connection was not established.")
        
def set_background(root, image_path):
    # Load the image
    bg_image = tk.PhotoImage(file=image_path)

    # Create a canvas widget and place it in the root window, covering the entire window
    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.place(x=0, y=0)

    # Add a black rectangle to serve as the background
    canvas.create_rectangle(0, 0, root.winfo_screenwidth(), root.winfo_screenheight(), fill="black", outline="")

    # Calculate the coordinates to center the image on the canvas
    x_center = (root.winfo_screenwidth() - bg_image.width()) // 2
    y_center = (root.winfo_screenheight() - bg_image.height()) // 8

    # Add the image at the center of the canvas
    canvas.create_image(x_center, y_center, image=bg_image, anchor="nw")

    # Ensure the image persists
    canvas.image = bg_image

def connect_mysql():
    try:
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Ankan@2020",
        database = "fifa_wc"
        )  
        print("Connection successsful")       
        return mydb
    except mysql.connector.Error as e:
        print("Error:", e)

def fetch_all_databases():
    mydb = connect_mysql()
    if mydb is not None:
        try:
            mycursor = mydb.cursor()
            mycursor.execute("SHOW DATABASES")
            db_list = [db[0] for db in mycursor.fetchall()]
            mycursor.close()

            # Create a new Toplevel window to display the message
            window = tk.Toplevel()
            window.title("Databases")
            window.geometry("400x300")  # Set the size of the window
            message = tk.Message(window, text="\n".join(db_list), width=350, font=("Helvetica", 14))
            message.pack()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", e)
        finally:
            mydb.close()
    else:
        messagebox.showerror("Error", "Database connection was not established.")

def fetch_all_tables():
    mydb = connect_mysql()
    if mydb is not None:
        try:
            mycursor = mydb.cursor()
            mycursor.execute("SHOW TABLES")

            # Fetch column names
            columns = ["List of Tables in this DB-"]

            # Fetch all rows
            table_list = [table[0] for table in mycursor.fetchall()]
            mycursor.close()

            # Create a new Toplevel window to display the message
            window = tk.Toplevel()
            window.title("Tables")
            window.geometry("400x300")  # Set the size of the window

            # Create a Text widget to display the data
            result_text = tk.Text(window, width=80, height=20, font=("Helvetica", 16))

            # Create a vertical scrollbar
            scrollbar = tk.Scrollbar(window, command=result_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Configure the Text widget to use the scrollbar
            result_text.config(yscrollcommand=scrollbar.set)

            # Insert column names into the Text widget
            result_text.insert(tk.END, "\t".join(columns) + "\n")

            # Insert the data into the Text widget
            for row in table_list:
                result_text.insert(tk.END, f"{row}\n")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", e)
        finally:
            mydb.close()
    else:
        messagebox.showerror("Error", "Database connection was not established.")


def read_data(table):
    mydb = connect_mysql()
    if mydb is not None:
        try:
            mycursor = mydb.cursor()
            query = f"SELECT * FROM {table}"
            mycursor.execute(query)

            # Fetch column names
            columns = [desc[0] for desc in mycursor.description]

            # Fetch all rows
            rows = mycursor.fetchall()
            mycursor.close()

            # Create a new Toplevel window to display the message
            window = tk.Toplevel()
            window.title("Data")
            window.geometry("600x400")  # Set the size of the window

            # Create a Text widget to display the data
            result_text = tk.Text(window, width=80, height=20, font=("Helvetica", 10))

            # Create a vertical scrollbar
            scrollbar = tk.Scrollbar(window, command=result_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Configure the Text widget to use the scrollbar
            result_text.config(yscrollcommand=scrollbar.set)

            # Insert column names into the Text widget
            result_text.insert(tk.END, "\t".join(columns) + "\n")

            # Insert the data into the Text widget
            for row in rows:
                result_text.insert(tk.END, "\t".join([str(cell) for cell in row]) + "\n")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", e)
        finally:
            mydb.close()
    else:
        messagebox.showerror("Error", "Database connection was not established.")


def insert_data():
    window_insert = tk.Toplevel()
    window_insert.title("Insert Data")
    window_insert.geometry("400x300")  # Set the size of the window

    tk.Label(window_insert, text="Enter INSERT Query:", font=("Helvetica", 14)).pack()
    query_entry = tk.Text(window_insert, width=50, height=10, font=("Helvetica", 10))
    query_entry.pack()

    def execute_insert():
        query = query_entry.get("1.0", tk.END)  # Retrieve text content from the Text widget
        try:
            mydb = connect_mysql()
            if mydb:
                mycursor = mydb.cursor()
                mycursor.execute(query)
                mydb.commit()
                messagebox.showinfo("Success", f"{mycursor.rowcount} record(s) inserted.")
                mycursor.close()
                mydb.close()
                window_insert.destroy()
            else:
                messagebox.showerror("Error", "Failed to establish a database connection.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", e)

    tk.Button(window_insert, text="Insert", command=execute_insert, font=("Helvetica", 10)).pack()

def update_data():
    window_update = tk.Toplevel()
    window_update.title("Update Data")
    window_update.geometry("400x300")  # Set the size of the window

    tk.Label(window_update, text="Enter UPDATE Query:", font=("Helvetica", 14)).pack()
    query_entry = tk.Text(window_update, width=50, height=10, font=("Helvetica", 10))
    query_entry.pack()

    result_text = tk.Text(window_update, width=50, height=10)
    result_text.pack()

    def execute_update():
        query = query_entry.get("1.0", tk.END)
        try:
            mydb = connect_mysql()
            if mydb:
                mycursor = mydb.cursor()
                mycursor.execute(query)
                mydb.commit()
                result_text.insert(tk.END, f"{mycursor.rowcount} record(s) updated.")
                mycursor.close()
                mydb.close()
                window_update.destroy()
            else:
                messagebox.showerror("Error", "Failed to establish a database connection.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", e)

    tk.Button(window_update, text="Update", command=execute_update, font=("Helvetica", 10)).pack()
    window_query.state('zoomed')
    
def delete_data():
    window_delete = tk.Toplevel()
    window_delete.title("Delete Data")
    window_delete.geometry("400x300")  # Set the size of the window

    tk.Label(window_delete, text="Enter DELETE Query:", font=("Helvetica", 14)).pack()
    query_entry = tk.Text(window_delete, width=50, height=10, font=("Helvetica", 10))
    query_entry.pack()

    result_text = tk.Text(window_delete, width=50, height=10)
    result_text.pack()

    def execute_delete():
        query = query_entry.get("1.0", tk.END)
        try:
            mydb = connect_mysql()
            if mydb:
                mycursor = mydb.cursor()
                mycursor.execute(query)
                mydb.commit()
                result_text.insert(tk.END, f"{mycursor.rowcount} record(s) deleted.")
                mycursor.close()
                mydb.close()
                window_delete.destroy()
            else:
                messagebox.showerror("Error", "Failed to establish a database connection.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", e)

    tk.Button(window_delete, text="Delete", command=execute_delete, font=("Helvetica", 10)).pack()
    window_query.state('zoomed')
    
def custom_query():
    window_query = tk.Toplevel()
    window_query.title("Custom Query")
    window_query.geometry("800x600")  # Set the size of the window

    tk.Label(window_query, text="Enter SQL Query (semicolon-separated for multiple queries):", font=("Helvetica", 14)).pack()
    query_entry = tk.Text(window_query, width=100, height=10, font=("Helvetica", 10))
    query_entry.pack()

    result_text = tk.Text(window_query, width=100, height=30)
    result_text.pack()

    def execute_query():
        query = query_entry.get("1.0", tk.END)
        try:
            mydb = connect_mysql()
            if mydb:
                mycursor = mydb.cursor()
                queries = query.split(';')
                # Clear previous result
                result_text.delete("1.0", tk.END)
                for q in queries:
                    if q.strip():
                        mycursor.execute(q)
                        result = mycursor.fetchall()
                        if result:
                            # Fetch column names
                            columns = [desc[0] for desc in mycursor.description]
                            result_text.insert(tk.END, "\t".join(columns) + "\n")
                            # Fetch and display rows
                            for row in result:
                                result_text.insert(tk.END, "\t".join(map(str, row)) + "\n")
                        else:
                            result_text.insert(tk.END, "No results found.")
                mycursor.close()
                mydb.close()
            else:
                messagebox.showerror("Error", "Failed to establish a database connection.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", e)

    tk.Button(window_query, text="Execute Query", command=execute_query, font=("Helvetica", 12)).pack()

    window_query.state('zoomed')


def perform_crud():
    window = tk.Tk()
    window.state('zoomed')
    window.title("FIFA Women's World Cup UI")
    set_background(window, r"C:\Users\Ankan Mazumdar\Downloads\CS430\del 4\resize-1713502070635835142Untitled.png")
    def fetch_databases():
        fetch_all_databases()

    def fetch_tables():
        fetch_all_tables()

    def read_records():
        table_name = input_table.get()
        read_data(table_name)

    def insert_record():
        insert_data()

    def update_record():
        update_data()

    def delete_record():
        delete_data()

    def show_connection_details():
        display_connection_details()
    tk.Label(window, text="FIFA Women's World Cup Database", font=("Helvetica", 14), fg="red").pack()
  #  tk.Label(window, text="", font=("Helvetica", 10)).pack()
    tk.Label(window, text="Please select any of the below option of your choice", font=("Helvetica", 12)).pack()
    tk.Button(window, text="Show Connection Details", font=("Helvetica", 14), fg="blue", padx=20, pady=10, command=show_connection_details).pack()      
    tk.Label(window, text="", font=("Helvetica", 10)).pack()
    tk.Button(window, text="Display all Databases in the server",font=("Helvetica", 14), fg="blue", padx=10, pady=10, command=fetch_databases).pack()
    tk.Label(window, text="", font=("Helvetica", 10)).pack()
    tk.Button(window, text="Display all Tables in FIFA_wc DB",   font=("Helvetica", 14), fg="blue", padx=20, pady=10, command=fetch_tables).pack()
    tk.Label(window, text="", font=("Helvetica", 10)).pack()
    
    tk.Label(window, text="Enter Table Name & click Read Records to view", font=("Helvetica", 14), fg="blue").pack()
    input_table = tk.Entry(window, font=("Helvetica", 10), width=30)
    input_table.pack()

    tk.Button(window, text="Read Records", font=("Helvetica", 14), fg="blue", padx=20, pady=10, command=read_records).pack()
    tk.Label(window, text="", font=("Helvetica", 10)).pack()
    tk.Button(window, text="Insert Record", font=("Helvetica", 14), fg="blue", padx=20, pady=10,command=insert_record).pack()
    tk.Label(window, text="", font=("Helvetica", 10)).pack()      
    tk.Button(window, text="Update Record", font=("Helvetica", 14), fg="blue", padx=20, pady=10,command=update_record).pack()
    tk.Label(window, text="", font=("Helvetica", 10)).pack()      
    tk.Button(window, text="Delete Record", font=("Helvetica", 14), fg="blue", padx=20, pady=10,command=delete_record).pack()
    tk.Label(window, text="", font=("Helvetica", 10)).pack()
    tk.Button(window, text="Execute Complex Query like Windows, OLAP, Aggregate functions", font=("Helvetica", 14), fg="blue", padx=20, pady=10,command=custom_query).pack()
      
    window.mainloop()

if __name__ == "__main__":
    perform_crud()
