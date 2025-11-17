class PlanetDiskHardDrive:
    """
    Conceptual hard drive with backup functionality.
    (Simplified methods from previous responses included for context.)
    """
    def __init__(self, capacity_gb):
        self.capacity = capacity_gb
        self.data_blocks = {}
        self.file_allocation_table = {} 
        self.next_free_sector = 1 
        self.backup_start_sector = 500 # Hard-coded start for the backup region
        self.backup_sector_map = {}    # Tracks where backups are stored
        
        # Internal state needed for backup simulation
        self.exe_path = "C:/ProgramFiles/Teddy_Server/server.exe"
        self.config_path = "C:/ProgramFiles/Teddy_Server/config/settings.ini"
        self.exe_sector = 3
        self.config_sector = 4
        
        # Initialize some data blocks for the backup to find
        self.data_blocks[self.exe_sector] = "// Teddy Server v1.1.0 Executable"
        self.data_blocks[self.config_sector] = "// CONFIG: version=1.1.0"
        
        print(f"======================================================")
        print(f"🚀 Initializing Planet Disk for Backup.")
        print(f"======================================================")

    def write_data(self, sector, text_data, status="[WRITE]"):
        """Writes data to a sector."""
        self.data_blocks[sector] = text_data 
        print(f"💾 {status} Sector {sector}: '{text_data[:60]}...'")
        self.next_free_sector = max(self.next_free_sector, sector + 1)

    def read_sector(self, sector):
        """Reads data from a sector."""
        return self.data_blocks.get(sector, "RAW DATA ERROR")

    # --- NEW BACKUP METHOD ---
    def run_backup(self):
        """
        Simulates creating a copy of critical files in a reserved backup sector range.
        """
        print(f"\n======================================================")
        print("☁️ Initiating FULL BACKUP of Critical Application Data...")
        print(f"======================================================")
        
        files_to_backup = {
            self.exe_path: self.exe_sector,
            self.config_path: self.config_sector
        }
        
        current_backup_sector = self.backup_start_sector
        
        for file_path, source_sector in files_to_backup.items():
            # 1. READ SOURCE DATA
            source_data = self.read_sector(source_sector)
            
            if source_data == "RAW DATA ERROR":
                print(f"❌ Backup failed for {file_path}: Source sector {source_sector} read error.")
                continue

            # 2. RESERVE AND WRITE COPY
            backup_sector = current_backup_sector
            backup_data = f"[BACKUP COPY] {source_data}"
            
            self.write_data(
                sector=backup_sector,
                text_data=backup_data,
                status="[BACKUP WRITE]"
            )
            
            # 3. MAP THE BACKUP LOCATION
            self.backup_sector_map[file_path] = backup_sector
            print(f"   ✅ Backed up '{file_path}' from Sector {source_sector} to **Sector {backup_sector}**.")
            
            current_backup_sector += 1 # Move to the next backup sector

        print("\n✅ **BACKUP OPERATION COMPLETE**")
        print(f"   Reserved Backup Map: {self.backup_sector_map}")
        
        # Demonstrate recovery readiness by reading a backup copy
        first_file = list(files_to_backup.keys())[0]
        backup_location = self.backup_sector_map[first_file]
        print(f"   Reading backup copy for executable: '{self.read_sector(backup_location)[:35]}...'")


# --- Execution ---

my_disk = PlanetDiskHardDrive(capacity_gb=1000)

# Simulate the backup operation
my_disk.run_backup()
