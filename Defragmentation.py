import time # To simulate the time taken for the defragmentation process

class PlanetDiskHardDrive:
    """
    A conceptual model of a hard drive (the 'Planet Disk')
    with support for fragmentation and a new defragmentation method.
    """
    def __init__(self, capacity_gb):
        self.capacity = capacity_gb
        self.interface = "SATA" 
        self.data_blocks = {}
        self.file_allocation_table = {} 
        self.next_free_sector = 1 # Keep track of where the next contiguous file should start
        print(f"🚀 Initializing {self.capacity}GB Planet Disk Hard Drive with {self.interface} interface.")
        print("-" * 45)

    def text_to_binary(self, text):
        """Converts a string to its 8-bit ASCII binary representation."""
        return ' '.join(format(ord(char), '08b') for char in text)

    def binary_to_text(self, binary_fragment):
        """Converts a binary string fragment back to text."""
        return ''.join(chr(int(binary_fragment[i:i+8], 2)) for i in range(0, len(binary_fragment), 9) if binary_fragment[i:i+8])

    def write_data(self, sector, text_data, status="[CONTIGUOUS]"):
        """Simulates writing text data to a specific sector in binary."""
        binary_data = self.text_to_binary(text_data)
        self.data_blocks[sector] = binary_data
        print(f"💾 {status} Sector {sector}: '{text_data}' -> {binary_data[:17]}...")

    def read_sector(self, sector):
        """Reads and returns the binary data from a specific sector."""
        return self.data_blocks.get(sector, "00000000")
    
    def write_fragmented_file(self, filename, content, fragment_size):
        """Writes content fragmented across non-contiguous sectors."""
        fragments = [content[i:i + fragment_size] for i in range(0, len(content), fragment_size)]
        sector_chain = []
        
        # Start writing non-contiguously after the current free sector
        start_sector = self.next_free_sector + 10 # Force a large gap for fragmentation
        current_sector = start_sector
        
        print(f"\n--- 💔 Writing Fragmented File: **{filename}** ({len(fragments)} Fragments) ---")
        for i, fragment in enumerate(fragments):
            sector = current_sector + (i * 5) # Large non-contiguous jumps
            self.write_data(sector, fragment, status="[FRAGMENT]")
            sector_chain.append(sector)
        
        self.file_allocation_table[filename] = sector_chain
        self.next_free_sector = sector_chain[-1] + 1 # Update free sector after the last fragment
        print(f"🔗 File Allocation Table for {filename}: Sectors {sector_chain}")
        
    def defragment_file(self, filename, new_start_sector):
        """
        Reads fragmented pieces, clears the old sectors, and rewrites the data 
        to a new, contiguous block.
        """
        if filename not in self.file_allocation_table:
            print(f"\n❌ Error: File '{filename}' not found for defragmentation.")
            return

        print(f"\n--- ⏳ Defragmenting File: **{filename}** ---")
        old_sectors = self.file_allocation_table[filename]
        
        # 1. READ ALL FRAGMENTS
        full_text_content = ""
        for sector in old_sectors:
            binary_fragment = self.read_sector(sector)
            full_text_content += self.binary_to_text(binary_fragment)
            print(f"  -> Reading and collecting data from sector {sector}...")
            
        time.sleep(0.5) # Simulate processing time
        
        # 2. CLEAR OLD FRAGMENTS
        for sector in old_sectors:
            del self.data_blocks[sector]
        print(f"  ✅ Cleared old fragmented sectors: {old_sectors}")
        
        # 3. REWRITE CONTIGUOUSLY
        new_sector_chain = []
        current_sector = new_start_sector
        fragment_size = len(full_text_content) // len(old_sectors) # Re-use original fragment size
        
        rewritten_fragments = [full_text_content[i:i + fragment_size] for i in range(0, len(full_text_content), fragment_size)]
        
        print("\n  ** Rewriting data to new contiguous block... **")
        for i, fragment in enumerate(rewritten_fragments):
            sector = current_sector + i # Sequential sectors!
            self.write_data(sector, fragment, status="[DEFRAGGED]")
            new_sector_chain.append(sector)

        # 4. UPDATE FILE ALLOCATION TABLE
        self.file_allocation_table[filename] = new_sector_chain
        print(f"\n✅ **DEFRAGMENTATION COMPLETE**")
        print(f"    New contiguous sectors: {new_sector_chain}")
        self.next_free_sector = new_sector_chain[-1] + 1


# --- Hard-Coded Execution Block ---
my_disk = PlanetDiskHardDrive(capacity_gb=4000)

# 1. Fragment the file (like in the previous step)
teddy_log_content = "LOG_START. Server (teddy_server) received command: Connect. Status: OK. Disconnect."
my_disk.write_fragmented_file(
    filename="teddy_server_log.txt", 
    content=teddy_log_content, 
    fragment_size=10
)

# 2. Defragment the file
# We choose to start the defragmented file at sector 50
my_disk.defragment_file(
    filename="teddy_server_log.txt", 
    new_start_sector=50
)

# 3. Read the defragmented file (simplified read)
print("\n--- 🔍 Reading Defragmented File ---")
sectors = my_disk.file_allocation_table["teddy_server_log.txt"]
print(f"Data is now located in contiguous sectors: {sectors}")
