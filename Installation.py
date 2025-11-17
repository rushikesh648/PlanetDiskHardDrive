class PlanetDiskHardDrive:
    """
    Conceptual hard drive with installation functionality.
    """
    def __init__(self, capacity_gb):
        self.capacity = capacity_gb
        self.data_blocks = {}
        self.file_allocation_table = {} 
        self.next_free_sector = 1 
        print(f"======================================================")
        print(f"🚀 Initializing Planet Disk for Installation.")
        print(f"======================================================")

    def write_data(self, sector, text_data, status="[WRITE]"):
        """Writes data to a sector."""
        self.data_blocks[sector] = text_data 
        print(f"💾 {status} Sector {sector}: '{text_data[:60]}...'")
        self.next_free_sector = max(self.next_free_sector, sector + 1)

    def create_directory(self, directory_name):
        """Simulates creating a directory."""
        if directory_name in self.file_allocation_table:
            print(f"❌ Directory '{directory_name}' already exists.")
            return

        dir_sector = self.next_free_sector
        dir_content = f"TYPE:DIRECTORY|ENTRIES:2|.:{dir_sector}|..:PARENT"
        
        self.write_data(
            sector=dir_sector, 
            text_data=dir_content, 
            status="[DIR CREATE]"
        )
        self.file_allocation_table[directory_name] = [dir_sector]
        return True # Return success

    # --- NEW INSTALLATION METHOD ---
    def install_application(self, app_name, version):
        """
        Simulates the hard-coded installation of an application 
        by setting up directories and writing files to the disk.
        """
        print(f"\n======================================================")
        print(f"📦 Starting Installation of **{app_name}** (v{version})")
        print(f"======================================================")

        root_dir = f"C:/ProgramFiles/{app_name}"
        config_dir = f"{root_dir}/config"
        
        # 1. CREATE DIRECTORY STRUCTURE
        print(">> PHASE 1: Creating Directory Structure...")
        self.create_directory(root_dir)
        self.create_directory(config_dir)

        # 2. WRITE EXECUTABLE FILE (The main program code)
        print("\n>> PHASE 2: Writing Executable and Configuration...")
        exe_path = f"{root_dir}/server.exe"
        exe_content = f"// Binary executable data for {app_name} v{version}. Start sector reserved."
        exe_sector = self.next_free_sector
        
        self.write_data(exe_sector, exe_content, status="[EXE WRITE]")
        self.file_allocation_table[exe_path] = [exe_sector]

        # 3. WRITE CONFIGURATION FILE
        config_path = f"{config_dir}/settings.ini"
        config_content = f"// CONFIG: port=8080; database=production; version={version}"
        config_sector = self.next_free_sector
        
        self.write_data(config_sector, config_content, status="[CFG WRITE]")
        self.file_allocation_table[config_path] = [config_sector]

        # 4. FINAL INSTALLATION STATUS
        print(f"\n✅ **INSTALLATION COMPLETE**")
        print(f"   Application Root: {root_dir} (Sector {self.file_allocation_table[root_dir][0]})")
        print(f"   Executable Location: Sector {exe_sector}")


# --- Execution ---

my_disk = PlanetDiskHardDrive(capacity_gb=1000)

# Simulate the installation of the Teddy Server application
my_disk.install_application(app_name="Teddy_Server", version="1.0.0")
