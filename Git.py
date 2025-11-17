import hashlib # Used to generate the commit hash (metadata)
import time # Used for the commit timestamp

class PlanetDiskHardDrive:
    # ... (Include the __init__, text_to_binary, binary_to_text, write_data, 
    # read_sector, write_fragmented_file, and defragment_file methods from the previous response) ...
    
    # --- Methods for Core Hard Drive Operations (Simplified for brevity) ---
    def __init__(self, capacity_gb):
        self.capacity = capacity_gb
        self.interface = "SATA" 
        self.data_blocks = {}
        self.file_allocation_table = {} 
        self.next_free_sector = 1 # Keep track of where the next contiguous file should start
        self.commit_log_sectors = list(range(100, 105)) # Hard-coded sectors for commit log
        self.commit_count = 0
        print(f"🚀 Initializing {self.capacity}GB Planet Disk Hard Drive with {self.interface} interface.")
        print(f"  Commit Log Reserved Sectors: {self.commit_log_sectors}")
        print("-" * 65)

    def text_to_binary(self, text):
        return ' '.join(format(ord(char), '08b') for char in text)

    def binary_to_text(self, binary_fragment):
        return ''.join(chr(int(binary_fragment[i:i+8], 2)) for i in range(0, len(binary_fragment), 9) if binary_fragment[i:i+8])

    def write_data(self, sector, text_data, status="[CONTIGUOUS]"):
        binary_data = self.text_to_binary(text_data)
        self.data_blocks[sector] = binary_data
        print(f"💾 {status} Sector {sector}: '{text_data}' -> {binary_data[:17]}...")

    def read_sector(self, sector):
        return self.data_blocks.get(sector, "00000000")
    
    def simulate_commit(self, filename, code_change, author, message):
        """
        Simulates a Git Commit: Writes new code to disk and logs the commit metadata.
        """
        print(f"\n--- 📝 Simulating Git Commit for {filename} ---")
        self.commit_count += 1
        
        # 1. GENERATE COMMIT METADATA
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Combine all metadata to generate a unique hash (like Git does)
        commit_string = f"{timestamp}{author}{message}{code_change}"
        commit_hash = hashlib.sha1(commit_string.encode('utf-8')).hexdigest()[:8]
        
        commit_metadata = (
            f"COMMIT:{commit_hash}|FILE:{filename}|AUTHOR:{author}|TIME:{timestamp}|MSG:'{message}'"
        )
        
        # 2. WRITE/UPDATE THE CODE (The actual file content)
        # We assume the new code is small enough for a single, contiguous sector
        new_code_sector = self.next_free_sector
        print(">> **PHASE 1: Writing Code**")
        self.write_data(
            sector=new_code_sector, 
            text_data=f"// {filename} updated\n{code_change}",
            status="[CODE WRITE]"
        )
        
        # Update the file allocation table for the new version
        self.file_allocation_table[filename] = [new_code_sector]
        self.next_free_sector += 1

        # 3. WRITE THE METADATA (The commit log entry)
        commit_log_sector = self.commit_log_sectors[self.commit_count % len(self.commit_log_sectors)]
        
        print("\n>> **PHASE 2: Writing Metadata to Log**")
        self.write_data(
            sector=commit_log_sector, 
            text_data=commit_metadata,
            status="[LOG WRITE]"
        )

        print(f"\n✅ **COMMIT SUCCESSFUL**")
        print(f"    Commit Hash (Sector {commit_log_sector}): **{commit_hash}**")
        print(f"    Code written to Sector: {new_code_sector}")

# --- Hard-Coded Execution Block ---

# Initialize disk (with simplified methods for clean output)
my_disk = PlanetDiskHardDrive(capacity_gb=4000)

# Simulate a developer making a change to the teddy_server code
# The change is an "optimization"
new_code = "def handle_request(data): return process_optimized(data)"
author_name = "rushikesh648"
commit_message = "Optimize database connection handling."

# Perform the Commit
my_disk.simulate_commit(
    filename="teddy_server.py", 
    code_change=new_code, 
    author=author_name, 
    message=commit_message
)
