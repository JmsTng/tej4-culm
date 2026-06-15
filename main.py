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
                Console.clear()
                
                while game_running:
                    print(f"Turn {turn}")
                    print(runner.game.pretty_print())

                    shot = runner.socket.recv(1024).decode() # Receive the shot made by client
                    runner.record_shot(runner.game.get_coords(shot), True) # Update boards and return result

                    # Wait for acknowledgement
                    runner.recvmsg()
                    
                    # Check if client wins
                    result = runner.check_win()
                    if result == "HOST":
                        print(f"VICTORY - {result} WINS")
                        game_running = False
                    elif result == "CLIENT":
                        print(f"DEFEAT - {result} WINS")
                        game_running = False
                    else:
                        result = "NONE"

                    runner.sendmsg("RSLT:"+result)
                    if result != "NONE":
                        break
                    
                    # Wait for acknowledgement
                    runner.recvmsg()
                    
                    # Make, record, and send result of shot by host
                    runner.record_shot(runner.game.get_coords(runner.make_shot()), False)

                    # Wait for acknowledgement
                    runner.recvmsg()

                    # Send updated boards
                    runner.send_board()

                    # Wait for acknowledgement
                    runner.recvmsg()
                    
                    # Check for a winner
                    result = runner.check_win()
                    if result == "HOST":
                        print(f"VICTORY - {result} WINS")
                        game_running = False
                    elif result == "CLIENT":
                        print(f"DEFEAT - {result} WINS")
                        game_running = False
                    else:
                        result = "NONE"
                        turn += 1

                    runner.sendmsg("RSLT:"+result)
                    
                    # # Wait for acknowledgement
                    # runner.recvmsg()
                    Console.clear(1.5)

                    
            case "client":
                print("Excellent. Preparing to connect.")
                runner = Client() # Create a client instance
                runner.send_board() # Update host with client board
                runner.receive_board(runner.recvmsg()) # Accept updated state
                Console.clear()
    
                while game_running:
                    print(f"Turn {turn}")
                    print(runner.game.pretty_print())
                    
                    runner.sendmsg(runner.make_shot()) # Send client shot
                    print(runner.recvmsg()) # Result of client shot

                    # Acknowledge client shot result
                    runner.sendmsg("INFO:ACK")

                    # Check for winner
                    result = runner.recvmsg()

                    if result == "HOST":
                        print(f"DEFEAT - {result} WINS")
                        game_running = False
                        break
                    elif result == "CLIENT":
                        print(f"VICTORY - {result} WINS")
                        game_running = False
                        break
                        
                    runner.sendmsg("INFO:ACK") # Acknowledge winner info
                    
                    msg = runner.recvmsg() # Result of host shot
                    runner.sendmsg("INFO:ACK") # Acknowledge host shot result
                    print(msg)

                    runner.receive_board(runner.recvmsg()) # Receive boards after round end
                    runner.sendmsg("INFO:ACK") # Acknowledge board update
                    
                    result = runner.recvmsg()
                    if result == "HOST":
                        print(f"DEFEAT - {result} WINS")
                        game_running = False
                    elif result == "CLIENT":
                        print(f"VICTORY - {result} WINS")
                        game_running = False
                    else:
                        turn += game_running
                
                    # runner.sendmsg("INFO:ACK") # Acknowledge winner info
                    Console.clear(1.5)
            case _:
                print("That's invalid. Exiting.")
                exit(0)
    except ConnectionRefusedError:
        print("Host is not yet ready.")
    except Exception as e:
        print(e)
    else:
        runner.socket.close()
