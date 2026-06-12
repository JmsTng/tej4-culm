from game import Client, Host
from text import Console

if __name__ == "__main__":
    # Introduction; initialize game as either host or client.
    print("Welcome to Battleship, commander.")
    role: str = input("Is this the host or client computer?\n>> ").strip().lower()

    # Create variable to set scope
    runner = None
    game_running = True
    turn = 0

    try:
        match role:
            case "host":
                print("Excellent. Preparing to host.")
                runner = Host() # Create a host instance
                runner.receive_board(ignore_self=True)
                runner.send_board()
                
                while game_running:
                    Console.clear()
                    print(f"Turn {turn}")
                    print(runner.game.pretty_print())

                    shot = runner.socket.recv(1024).decode()
                    runner.record_shot(runner.game.get_coords(shot), True)
                    
                    runner.record_shot(runner.game.get_coords(runner.make_shot()), False)
    
                    # runner.check_win()
        
                    runner.send_board()
                    
            case "client":
                print("Excellent. Preparing to connect.")
                runner = Client() # Create a client instance
                runner.send_board()
                runner.receive_board()
    
                while game_running:
                    Console.clear()
                    print(f"Turn {turn}")
                    print(runner.game.pretty_print())
                    runner.sendmsg(runner.make_shot())
    
                    # runner.check_win()
    
                    runner.receive_board()
                
            case _:
                print("That's invalid. Exiting.")
                exit(0)
    except Exception as e:
        runner.socket.close()
        
        raise e
