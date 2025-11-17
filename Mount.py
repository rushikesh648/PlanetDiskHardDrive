class PlanetDiskHardDrive:
    """
    A conceptual model of a hard drive (the 'Planet Disk')
    storing key technology data in binary format.
    """
    def __init__(self, capacity_gb):
        # 1. Hard-Coded Initialization Parameters
        self.capacity = capacity_gb
        self.interface = "SATA" 
        self.data_blocks = {}
        print(f"🚀 Initializing {self.capacity}GB Planet Disk Hard Drive with {self.interface} interface.")
        print("-" * 30)

    def text_to_binary(self, text):
        """Converts a string to its 8-bit ASCII binary representation."""
        return ' '.join(format(ord(char), '08b') for char in text)

    def write_data(self, sector, text_data):
        """Simulates writing text data to a specific sector in binary (The 'Mounting' step)."""
        binary_data = self.text_to_binary(text_data)
        self.data_blocks[sector] = binary_data
        print(f"💾 [MOUNT/STORE] Sector {sector} updated with: '{text_data}'")
        print(f"        Binary: {binary_data}")

    def read_sector(self, sector):
        """Reads and returns the binary data from a specific sector (The 'Access' step)."""
        return self.data_blocks.get(sector, "00000000 (Empty Sector)")

# --- Hard-Coded Execution Block: "Mounting" the Code ---

def mount_and_access_disk():
    """Hard-coded sequence to use the Planet Disk."""
    
    # 1. HARD-CODED DISK CREATION (Initial Mount Point)
    print("--- 1. Hard-Coded Disk Creation ---")
    disk_size = 4000  # Hard-coded size (4TB)
    my_disk = PlanetDiskHardDrive(capacity_gb=disk_size)

    # 2. HARD-CODED DATA WRITING (Writing File System Metadata)
    print("\n--- 2. Hard-Coded Data Writing (Mounting Data) ---")
    
    # Write key terms to fixed, hard-coded sectors
    my_disk.write_data(sector=1, text_data="SATA")
    my_disk.write_data(sector=2, text_data="PATA")
    my_disk.write_data(sector=3, text_data="PLANET")
    my_disk.write_data(sector=4, text_data="DISK")

    # 3. HARD-CODED DATA READING (Accessing Mounted Data)
    print("\n--- 3. Hard-Coded Data Reading (Accessing Data) ---")
    
    # Read the data from the hard-coded sectors
    sectors_to_read = [1, 3, 4]
    for sector in sectors_to_read:
        binary_data = my_disk.read_sector(sector)
        print(f"🔍 Sector {sector} data: {binary_data}")

# Run the hard-coded sequence
mount_and_access_disk()
