from game import Client, Host

if __name__ == "__main__":
    # Introduction; initialize game as either host or client.
    print("Welcome to Battleship, commander.")
    role: str = input("Is this the host or client computer?\n>> ").strip().lower()

    # Create variable to set scope
    runner = None
    match role:
        case "host":
            print("Excellent. Preparing to host.")
            runner = Host() # Create a host instance
        case "client":
            print("Excellent. Preparing to connect.")
            runner = Client() # Create a client instance
        case _:
            print("That's invalid. Exiting.")
            exit(0)
    
