import hashlib 
import time

class PlanetDiskHardDrive:
    """
    Conceptual hard drive modeling data persistence, rollback, and catastrophic failure.
    """
    def __init__(self, capacity_gb):
        self.capacity = capacity_gb
        self.interface = "SATA" 
        self.data_blocks = {}
        self.file_allocation_table = {} 
        self.next_free_sector = 1 
        self.commit_log_sectors = list(range(100, 105))
        self.commit_count = 0
        self.old_versions = {"teddy_server.py": {"00000000": "def handle_request(data): return process_legacy(data)"}}
        print(f"🚀 Initializing {self.capacity}GB Planet Disk Hard Drive.")
        print("-" * 65)

    def text_to_binary(self, text):
        return ' '.join(format(ord(char), '08b') for char in text)

    def binary_to_text(self, binary_fragment):
        return ''.join(chr(int(binary_fragment[i:i+8], 2)) for i in range(0, len(binary_fragment), 9) if binary_fragment[i:i+8])

    def write_data(self, sector, text_data, status="[CONTIGUOUS]"):
        binary_data = self.text_to_binary(text_data)
        self.data_blocks[sector] = binary_data
        print(f"💾 {status} Sector {sector}: '{text_data}' -> {binary_data[:17]}...")
        # Simple management of sectors for rollback
        if sector not in self.commit_log_sectors:
            self.next_free_sector = max(self.next_free_sector, sector + 1)

    def read_sector(self, sector):
        return self.data_blocks.get(sector, "00000000")
    
    def simulate_commit(self, filename, code_change, author, message):
        """Simulates writing new code and commit metadata."""
        if filename not in self.old_versions:
             self.old_versions[filename] = {}

        # Save current version as 'old' before overwriting
        current_sector = self.file_allocation_table.get(filename, [self.next_free_sector])[0]
        current_content = self.binary_to_text(self.read_sector(current_sector))
        
        # Calculate hash for the version we are saving (the one *before* the commit)
        prev_hash = hashlib.sha1(current_content.encode('utf-8')).hexdigest()[:8]
        self.old_versions[filename][prev_hash] = current_content
        
        # New commit metadata
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        commit_string = f"{timestamp}{author}{message}{code_change}"
        new_hash = hashlib.sha1(commit_string.encode('utf-8')).hexdigest()[:8]
        commit_metadata = f"COMMIT:{new_hash}|FILE:{filename}|AUTHOR:{author}"
        
        # PHASE 1: Write New Code
        new_code_sector = self.next_free_sector
        self.write_data(
            sector=new_code_sector, 
            text_data=code_change,
            status="[CODE WRITE]"
        )
        self.file_allocation_table[filename] = [new_code_sector]

        # PHASE 2: Write Metadata to Log
        commit_log_sector = self.commit_log_sectors[self.commit_count % len(self.commit_log_sectors)]
        self.write_data(
            sector=commit_log_sector, 
            text_data=commit_metadata,
            status="[LOG WRITE]"
        )
        self.commit_count += 1
        return new_hash

    def rollback_commit(self, filename, target_hash):
        """
        Simulates reverting a file to a previous, known-good state.
        """
        if filename not in self.old_versions or target_hash not in self.old_versions[filename]:
            print(f"\n❌ ROLLBACK FAILED: Target hash {target_hash} not found for {filename}.")
            return
        
        print(f"\n--- ⏪ Rolling Back {filename} to Hash: {target_hash} ---")
        
        # 1. READ OLD CODE
        old_code = self.old_versions[filename][target_hash]
        
        # 2. CLEAR CURRENT SECTOR (The 'bad' commit)
        current_sector = self.file_allocation_table[filename][0]
        del self.data_blocks[current_sector]
        print(f"   🧹 Cleared current code from Sector {current_sector}.")
        
        # 3. REWRITE OLD CODE (Rollback complete)
        new_sector = current_sector # Use the same freed sector
        self.write_data(
            sector=new_sector, 
            text_data=old_code,
            status="[ROLLBACK WRITE]"
        )
        
        # 4. UPDATE FILE ALLOCATION TABLE
        self.file_allocation_table[filename] = [new_sector]
        print(f"✅ ROLLBACK COMPLETE. Code reverted to Sector {new_sector}.")
        
    def system_collapse(self):
        """
        Simulates catastrophic failure, losing all mount points and OS data structures.
        """
        print("\n\n#################################################")
        print("############ 💥 SYSTEM COLLAPSE INITIATED #############")
        print("#################################################")
        
        # 1. COLLAPSE MOUNT POINTS (Unmounting all)
        print("\n[STEP 1: Unmounting All Filesystems]")
        self.file_allocation_table = {}
        print("    🗄️ File Allocation Table (Mount Points) Zeroed Out.")
        
        # 2. COLLAPSE OPERATING SYSTEM (Clearing key sectors)
        print("\n[STEP 2: Destroying OS and Commit Logs]")
        sectors_to_zero = list(self.commit_log_sectors) + [1, 2, 3] # Commit logs + first few code/data sectors
        
        for sector in sectors_to_zero:
            if sector in self.data_blocks:
                del self.data_blocks[sector]
            print(f"    🗑️ Sector {sector} (Critical Metadata/Code) Zeroed.")
            
        print("\n❌ **SYSTEM IS UNRECOVERABLE.**")
        print(f"Attempting to read file 'teddy_server.py': {self.file_allocation_table.get('teddy_server.py', 'NO MOUNT POINT FOUND')}")
        print("Hard drive contains raw data, but the OS (the 'map') is gone.")


# --- Hard-Coded Execution Block ---
my_disk = PlanetDiskHardDrive(capacity_gb=4000)

# Initial code state (the "legacy" version)
legacy_code = "def handle_request(data): return process_legacy(data)"
# We manually inject the initial version at the beginning
my_disk.file_allocation_table["teddy_server.py"] = [my_disk.next_free_sector]
my_disk.write_data(my_disk.next_free_sector, legacy_code, status="[INITIAL CODE]")
my_disk.next_free_sector += 1

# 1. COMMIT - The 'bad' optimization commit
new_code = "def handle_request(data): return process_optimized(data)"
commit_hash = my_disk.simulate_commit(
    filename="teddy_server.py", 
    code_change=new_code, 
    author="rushikesh648", 
    message="Optimize database connection handling."
)

# 2. ROLLBACK - Revert the 'bad' commit
my_disk.rollback_commit(
    filename="teddy_server.py", 
    target_hash="00000000" # Target the initial, hard-coded legacy version hash
)

# 3. COLLAPSE - Total failure
my_disk.system_collapse()
