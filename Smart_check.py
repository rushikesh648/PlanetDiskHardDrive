import random # For simulating attribute changes

class PlanetDiskHardDrive:
    """
    Conceptual hard drive with SMART health monitoring.
    """
    def __init__(self, capacity_gb):
        self.capacity = capacity_gb
        self.data_blocks = {}
        self.file_allocation_table = {} 
        self.next_free_sector = 1 
        
        # --- SMART Attributes (Internal State) ---
        self._power_on_hours = 0
        self._reallocated_sectors = 0
        self._spin_retry_count = 0
        self._temperature = 25 # Starting temp in Celsius
        
        print(f"======================================================")
        print(f"🚀 Initializing Planet Disk with SMART Monitoring.")
        print(f"======================================================")

    def _increment_wear(self, activity_level=1):
        """Simulates disk activity increasing wear and usage."""
        self._power_on_hours += activity_level
        self._temperature += random.randint(-1, 2) # Temp fluctuates slightly
        if random.random() < 0.05: # 5% chance of a new bad sector
            self._reallocated_sectors += 1
        if random.random() < 0.02: # 2% chance of a spin retry event
            self._spin_retry_count += 1
        
    def write_data(self, sector, text_data, status="[WRITE]"):
        """Writes data to a sector and increments wear."""
        self._increment_wear(activity_level=1)
        self.data_blocks[sector] = text_data 
        # ... (simplified print for brevity)
        self.next_free_sector = max(self.next_free_sector, sector + 1)
        # print(f"💾 {status} Sector {sector}...")

    # ... (Other methods like read_sector, create_directory, install_application, etc., would be here)

    # --- NEW SMART CHECK METHOD ---
    def run_smart_check(self):
        """
        Simulates running the disk's Self-Monitoring, Analysis, and Reporting Technology check.
        """
        print(f"\n======================================================")
        print("❤️ Initiating SMART Disk Health Check...")
        print(f"======================================================")

        # 1. Gather Attributes
        attributes = {
            "Power-On Hours": self._power_on_hours,
            "Temperature (°C)": self._temperature,
            "Reallocated Sector Count": self._reallocated_sectors,
            "Spin Retry Count": self._spin_retry_count,
        }

        # 2. Analyze Health Score based on thresholds
        health_score = 100
        issues = []

        if self._reallocated_sectors > 5:
            health_score -= 30
            issues.append(f"CRITICAL: High number of bad sectors ({self._reallocated_sectors}). Data integrity risk.")
        elif self._reallocated_sectors > 0:
            health_score -= 10
            issues.append("WARNING: Some reallocated sectors detected. Monitor closely.")
            
        if self._temperature > 45:
            health_score -= 20
            issues.append(f"CRITICAL: High operating temperature ({self._temperature}°C). Needs cooling.")
            
        if self._spin_retry_count > 3:
            health_score -= 15
            issues.append(f"WARNING: Multiple spin retries detected ({self._spin_retry_count}). Possible mechanical issue.")

        # 3. Report Results
        print("\n--- SMART ATTRIBUTES ---")
        for key, value in attributes.items():
            print(f"| {key:<25} | Value: {value}")
        
        print("\n--- HEALTH REPORT ---")
        if issues:
            for issue in issues:
                print(f"   {issue}")
        else:
            print("   ✅ Disk health is excellent. No critical issues reported.")

        print(f"\nFinal Health Score: **{max(0, health_score)}/100**")
        

# --- Execution ---

my_disk = PlanetDiskHardDrive(capacity_gb=1000)

# Simulate initial installation (creates directories and writes files)
# This will call 'write_data' multiple times, increasing wear and hours.
my_disk.write_data(1, "OS Kernel", status="[OS BOOT]") 
my_disk.write_data(2, "Swap File", status="[OS BOOT]")

# Simulate heavy I/O by performing 50 random write operations
print("\n--- Simulating Heavy Disk I/O (50 Random Writes) ---")
for i in range(50):
    sector = my_disk.next_free_sector + random.randint(1, 10)
    data = f"Sector {sector} Data Block {i}"
    my_disk.write_data(sector, data, status="[I/O]")

# Run the health check after the activity
my_disk.run_smart_check()
