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
                runner.receive_board(runner.recvmsg(), ignore_self=True) # Do not allow client to overwrite host's board
                runner.send_board() # Sync boards with client
                
                while game_running:
                    Console.clear(1.5)
                    print(f"Turn {turn}")
                    print(runner.game.pretty_print())

                    shot = runner.socket.recv(1024).decode() # Receive the shot made by client
                    runner.record_shot(runner.game.get_coords(shot), True) # Update boards and return result

                    # Make, record, and send result of shot by host
                    runner.record_shot(runner.game.get_coords(runner.make_shot()), False)

                    # Wait for acknowledgement
                    runner.recvmsg()

                    # Send updated boards
                    runner.send_board()

                    # Check for a winner
                    result = runner.check_win()
                    if result:
                        print(f"{result} WINS")
                        runner.sendmsg("RSLT:"+result)

                    turn += 1
                    
            case "client":
                print("Excellent. Preparing to connect.")
                runner = Client() # Create a client instance
                runner.send_board() # Update host with client board
                runner.receive_board(runner.recvmsg()) # Accept updated state
    
                while game_running:
                    Console.clear(1.5)
                    print(f"Turn {turn}")
                    print(runner.game.pretty_print())
                    runner.sendmsg(runner.make_shot()) # Send client shot
                    print(runner.recvmsg()) # Result of client shot
                    
                    msg = runner.recvmsg() # Result of host shot
                    print(msg)
                    runner.sendmsg("INFO:ACK") # Return acknowledgement

                    runner.receive_board(runner.recvmsg()) # Receive boards after round end

                    
                    
                    turn += 1
                
            case _:
                print("That's invalid. Exiting.")
                exit(0)
    except Exception as e:
        runner.socket.close()
        
        raise e
