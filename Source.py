class PlanetDiskHardDrive:
    """
    A conceptual model of a hard drive (the 'Planet Disk')
    storing key technology data in binary format.
    """
    def __init__(self, capacity_gb):
        self.capacity = capacity_gb
        self.interface = "SATA"
        # Dictionary to store data blocks (conceptual sectors/clusters)
        self.data_blocks = {}
        print(f"Initializing 🚀 {self.capacity}GB Planet Disk Hard Drive with {self.interface} interface.")

    def text_to_binary(self, text):
        """Converts a string to its 8-bit ASCII binary representation."""
        return ' '.join(format(ord(char), '08b') for char in text)

    def write_data(self, sector, text_data):
        """Simulates writing text data to a specific sector in binary."""
        binary_data = self.text_to_binary(text_data)
        self.data_blocks[sector] = binary_data
        print(f"\n[WRITE] Sector {sector} updated with: '{text_data}'")
        print(f"        Binary: {binary_data}")

    def read_sector(self, sector):
        """Reads and returns the binary data from a specific sector."""
        return self.data_blocks.get(sector, "00000000 (Empty Sector)")

# --- Execution ---

# 1. Create the Hard Drive instance
my_disk = PlanetDiskHardDrive(capacity_gb=4000)

# 2. Write key data terms to conceptual sectors
my_disk.write_data(sector=1, text_data="SATA")
my_disk.write_data(sector=2, text_data="PATA")
my_disk.write_data(sector=3, text_data="PLANET")

# 3. Read and verify the data
print("\n--- Reading Disk Data ---")
sata_binary = my_disk.read_sector(sector=1)
pata_binary = my_disk.read_sector(sector=2)
print(f"Sector 1 (SATA) data: {sata_binary}")
print(f"Sector 2 (PATA) data: {pata_binary}")
