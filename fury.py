# fury.py

def start_fury():
    
    print("=================================")
    print("🔥 FURY AI ASSISTANT STARTED")
    print("Type 'exit' to stop Fury")
    print("=================================")

    while True:
        
        command = input(">>> ")

        if command.lower() == "exit":
            print("Shutting down Fury...")
            break

        print(f"Fury received command: {command}")



if __name__ == "__main__":
    start_fury()