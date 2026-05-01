from ..process.storage import Storage

storage = Storage()

def clear_data():
    directory = storage.data_dir
    storage.clear_directory(directory)
    print(f"\nFolder: {directory} CLEARED\n")

if __name__ == "__main__":
    clear_data()