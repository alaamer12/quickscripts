import os


FAILED = []

def to_pascal(name):
    captilized_name = " ".join(word.capitalize() for word in name.split(" "))
    return captilized_name

# Get the current working directory
current_dir = os.getcwd()

# Initialize the counter
i = 0

if __name__ == "__main__":
    # Iterate through all items in the current working directory
    for dir in os.listdir(current_dir):
        # Construct the full path of the item
        full_path = os.path.join(current_dir, dir)
        
        # Check if the item is a directory
        if os.path.isdir(full_path):
            i += 1
            # Convert the directory name to PascalCase
            pascal_name = to_pascal(dir.strip())
            
            # Construct the full path for the new directory name
            new_full_path = os.path.join(current_dir, pascal_name)
            try:
                # Rename the directory
                os.rename(full_path, new_full_path)
            except Exception as e:
                FAILED.append(full_path)
            # Print the renamed directory for verification
            print(f"Renamed: {full_path} to {new_full_path}")

    # Print the summary
    print(f"Converted {i} dirs")
    print("[DONE]")
        
    if FAILED:
        print(f"{FAILED = }")