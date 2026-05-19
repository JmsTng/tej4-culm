from game import Client, Host

if __name__ == "__main__":
    # Introduction; initialize game as either host or client.
    print("Welcome to Battleship, commander.")
    role: str = input("Is this the host or client computer?\n>> ").strip().lower()

    # Create variable to set scope
    runner = None
    if role == "host":
        runner = Host() # Create a host instance
        print("Excellent. Preparing to host.")
    elif role == "client":
        runner = Client() # Create a client instance
        print("Excellent. Preparing to connect.")

    handshake()