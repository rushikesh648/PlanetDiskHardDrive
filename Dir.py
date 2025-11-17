class PlanetDiskHardDrive:
    """
    Conceptual hard drive with directory creation functionality.
    """
    def __init__(self, capacity_gb):
        self.capacity = capacity_gb
        self.data_blocks = {}
        self.file_allocation_table = {} 
        self.next_free_sector = 1 
        print(f"======================================================")
        print(f"🚀 Initializing Planet Disk for Directory Setup.")
        print(f"======================================================")

    def write_data(self, sector, text_data, status="[WRITE]"):
        """Writes data to a sector."""
        # Simple binary representation is omitted for brevity in this step
        self.data_blocks[sector] = text_data 
        print(f"💾 {status} Sector {sector}: '{text_data[:60]}...'")
        self.next_free_sector = max(self.next_free_sector, sector + 1)

    def read_sector(self, sector):
        """Reads data from a sector."""
        return self.data_blocks.get(sector, "RAW DATA ERROR")

    def create_directory(self, directory_name):
        """
        Simulates creating a directory by reserving a sector and creating a FAT entry.
        """
        if directory_name in self.file_allocation_table:
            print(f"❌ Directory '{directory_name}' already exists.")
            return

        # 1. Reserve a free sector for the directory metadata
        dir_sector = self.next_free_sector
        
        # 2. Hard-coded initial directory content (pointers to self and parent)
        dir_content = f"TYPE:DIRECTORY|ENTRIES:2|.:{dir_sector}|..:PARENT"
        
        # 3. Write the directory content to the disk
        self.write_data(
            sector=dir_sector, 
            text_data=dir_content, 
            status="[DIR CREATE]"
        )
        
        # 4. Update the File Allocation Table (FAT)
        # The FAT entry is the "mount point" for the directory
        self.file_allocation_table[directory_name] = [dir_sector]
        
        print(f"✅ Directory '{directory_name}' successfully created in Sector {dir_sector}.")
        print(f"   FAT Entry: {directory_name} -> {self.file_allocation_table[directory_name]}")


# --- Execution ---

my_disk = PlanetDiskHardDrive(capacity_gb=1000)

# 1. Create the main 'teddy_server' directory
my_disk.create_directory("teddy_server")

# 2. Create nested directories like 'src' and 'logs'
my_disk.create_directory("teddy_server/src")
my_disk.create_directory("teddy_server/logs")

# 3. Add a placeholder for a file inside one of the directories
file_name = "teddy_server/src/main.py"
file_content = "def main(): # File content is stored contiguously here"
file_sector = my_disk.next_free_sector

my_disk.write_data(file_sector, file_content, status="[FILE WRITE]")
my_disk.file_allocation_table[file_name] = [file_sector]

print("\n--- Final File Allocation Table (Mount Points) ---")
for name, sectors in my_disk.file_allocation_table.items():
    print(f"| {name:<20} | Sectors: {sectors}")
