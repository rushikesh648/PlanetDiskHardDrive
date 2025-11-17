class PlanetDiskHardDrive:
    """
    A conceptual model of a hard drive (the 'Planet Disk')
    storing key technology data in binary format, now demonstrating fragmentation.
    """
    def __init__(self, capacity_gb):
        self.capacity = capacity_gb
        self.interface = "SATA" 
        self.data_blocks = {}
        # Stores the sectors that make up a file (to simulate a file system table)
        self.file_allocation_table = {} 
        print(f"🚀 Initializing {self.capacity}GB Planet Disk Hard Drive with {self.interface} interface.")
        print("-" * 40)

    def text_to_binary(self, text):
        """Converts a string to its 8-bit ASCII binary representation."""
        return ' '.join(format(ord(char), '08b') for char in text)

    def write_data(self, sector, text_data, is_fragment=False):
        """Simulates writing text data to a specific sector in binary."""
        binary_data = self.text_to_binary(text_data)
        self.data_blocks[sector] = binary_data
        
        # Use a different message for regular vs. fragmented writes
        status = "[FRAGMENT]" if is_fragment else "[CONTIGUOUS]"
        print(f"💾 {status} Sector {sector}: '{text_data}' -> {binary_data[:17]}...")

    def read_sector(self, sector):
        """Reads and returns the binary data from a specific sector."""
        return self.data_blocks.get(sector, "00000000")
    
    def write_fragmented_file(self, filename, content, start_sector, fragment_size):
        """
        Splits content into fragments and writes them to non-contiguous sectors.
        This simulates file fragmentation.
        """
        fragments = [content[i:i + fragment_size] for i in range(0, len(content), fragment_size)]
        sector_chain = []
        current_sector = start_sector
        
        print(f"\n--- Writing Fragmented File: **{filename}** ({len(fragments)} Fragments) ---")
        for i, fragment in enumerate(fragments):
            # Write fragments to non-contiguous sectors to simulate fragmentation
            sector = current_sector + (i * 2) 
            self.write_data(sector, fragment, is_fragment=True)
            sector_chain.append(sector)
        
        self.file_allocation_table[filename] = sector_chain
        print(f"🔗 File Allocation Table for {filename}: Sectors {sector_chain}")
        
    def read_fragmented_file(self, filename):
        """
        Reads a file by jumping between non-contiguous sectors.
        This represents the slow access caused by fragmentation.
        """
        if filename not in self.file_allocation_table:
            print(f"\n❌ Error: File '{filename}' not found on disk.")
            return
            
        sector_chain = self.file_allocation_table[filename]
        print(f"\n--- Reading Fragmented File: **{filename}** ---")
        print(f"Accessing sectors in order: {sector_chain}")
        
        full_binary = []
        full_text = []
        
        for i, sector in enumerate(sector_chain):
            binary_fragment = self.read_sector(sector)
            
            # Simplified binary to text conversion for output
            text_fragment = ''.join(chr(int(binary_fragment[i:i+8], 2)) for i in range(0, len(binary_fragment), 9) if binary_fragment[i:i+8])
            
            full_binary.append(binary_fragment)
            full_text.append(text_fragment)
            print(f"  -> Sector {sector} accessed. Next sector pointer: {sector_chain[i+1] if i + 1 < len(sector_chain) else 'END'}")
            
        print("\n✅ RECONSTRUCTED DATA:")
        print(f"Binary: {'...'.join(full_binary)}")
        print(f"Text:   {''.join(full_text)}")


# --- Hard-Coded Execution Block ---

# 1. Hard-Coded Disk Creation
disk_size = 4000
my_disk = PlanetDiskHardDrive(capacity_gb=disk_size)

# 2. Hard-Coded Fragmented Write Operation
teddy_log_content = "LOG_START. Server (teddy_server) received command: Connect. Status: OK. Disconnect."
my_disk.write_fragmented_file(
    filename="teddy_server_log.txt", 
    content=teddy_log_content, 
    start_sector=10, 
    fragment_size=10 # Each fragment will be 10 characters long
)

# 3. Hard-Coded Fragmented Read Operation
my_disk.read_fragmented_file(filename="teddy_server_log.txt")
