class PlanetDiskHardDrive:
    """
    Conceptual hard drive with installation and update functionality.
    (Simplified methods from previous response included for context.)
    """
    def __init__(self, capacity_gb):
        self.capacity = capacity_gb
        self.data_blocks = {}
        self.file_allocation_table = {} 
        self.next_free_sector = 1 
        print(f"======================================================")
        print(f"🚀 Initializing Planet Disk for Update Simulation.")
        print(f"======================================================")

    def write_data(self, sector, text_data, status="[WRITE]"):
        """Writes data to a sector."""
        self.data_blocks[sector] = text_data 
        print(f"💾 {status} Sector {sector}: '{text_data[:60]}...'")
        self.next_free_sector = max(self.next_free_sector, sector + 1)

    def read_sector(self, sector):
        """Reads data from a sector."""
        return self.data_blocks.get(sector, "RAW DATA ERROR")

    def create_directory(self, directory_name):
        """Simulates creating a directory."""
        dir_sector = self.next_free_sector
        dir_content = f"TYPE:DIRECTORY|ENTRIES:2|.:{dir_sector}|..:PARENT"
        self.write_data(sector=dir_sector, text_data=dir_content, status="[DIR CREATE]")
        self.file_allocation_table[directory_name] = [dir_sector]
        return True

    def install_application(self, app_name, version):
        """Simulates initial installation (Setup for Update)."""
        root_dir = f"C:/ProgramFiles/{app_name}"
        config_dir = f"{root_dir}/config"
        
        # Create directories
        self.create_directory(root_dir)
        self.create_directory(config_dir)

        # Write Executable
        self.exe_path = f"{root_dir}/server.exe"
        exe_content = f"// Binary executable data for {app_name} v{version}. Start sector reserved."
        self.exe_sector = self.next_free_sector
        self.write_data(self.exe_sector, exe_content, status="[EXE WRITE]")
        self.file_allocation_table[self.exe_path] = [self.exe_sector]

        # Write Configuration File
        self.config_path = f"{config_dir}/settings.ini"
        config_content = f"// CONFIG: port=8080; database=production; version={version}"
        self.config_sector = self.next_free_sector
        self.write_data(self.config_sector, config_content, status="[CFG WRITE]")
        self.file_allocation_table[self.config_path] = [self.config_sector]
        
        print(f"\n✅ Initial Installation Complete (v{version}).")


    # --- NEW UPDATE METHOD ---
    def update_application(self, new_version):
        """
        Simulates patching the executable and updating the config file on disk.
        """
        print(f"\n======================================================")
        print(f"⬆️ Starting Update to Version **{new_version}**")
        print(f"======================================================")

        # 1. PATCH THE EXECUTABLE (Write new, patched code to the same sector)
        patched_exe_content = f"// Binary executable data for Teddy_Server v{new_version}. PATCH: Added security layer."
        
        # The update overwrites the old data in the SAME sector
        self.write_data(
            sector=self.exe_sector, 
            text_data=patched_exe_content, 
            status="[CODE PATCH]"
        )
        print(f"   ✅ Executable patched in place (Sector {self.exe_sector}).")

        # 2. UPDATE THE CONFIGURATION FILE
        updated_config_content = f"// CONFIG: port=8080; database=production; version={new_version}; patch_applied=True"
        
        # The update overwrites the old data in the SAME sector
        self.write_data(
            sector=self.config_sector, 
            text_data=updated_config_content, 
            status="[CFG UPDATE]"
        )
        print(f"   ✅ Configuration updated in place (Sector {self.config_sector}).")

        print(f"\n✅ **UPDATE TO v{new_version} COMPLETE**")
        print(f"   Reading new config data: '{self.read_sector(self.config_sector)}'")


# --- Execution ---

my_disk = PlanetDiskHardDrive(capacity_gb=1000)

# 1. Initial Installation (v1.0.0)
my_disk.install_application(app_name="Teddy_Server", version="1.0.0")

# 2. Simulate the Update to v1.1.0
my_disk.update_application(new_version="1.1.0")
