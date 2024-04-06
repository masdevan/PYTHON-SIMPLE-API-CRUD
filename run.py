import os
import subprocess

if __name__ == "__main__":
    print("Apakah Anda ingin melakukan migrasi database? (Y/N)")
    migration_confirmation = input().strip().upper()

    if migration_confirmation == 'Y':
        print("'Y' untuk migration Fresh dan 'N' untuk Migration Normal. (Y/N)")
        migration_mode = input().strip().upper()
        
        if migration_mode == 'Y':
            print("Running database migration...")
            subprocess.run(["python", "migration.py", "--fresh"])
            print("Database migration completed.")
        elif migration_mode == 'N':
            print("Running database migration...")
            subprocess.run(["python", "migration.py"])
            print("Database migration completed.")
        else:
            print("Pilihan tidak valid.")

    print("Starting API server...")
    api_process = subprocess.Popen(["python", "api.py"])
    
    print("Starting Flask routes...")
    route_process = subprocess.Popen(["python", "route.py"])

    try:
        api_process.wait()
    except KeyboardInterrupt:
        print("Stopping API server...")
        api_process.terminate()
        api_process.wait()
        print("API server stopped.")

    try:
        route_process.wait()
    except KeyboardInterrupt:
        print("Stopping Flask routes...")
        route_process.terminate()
        route_process.wait()
        print("Flask routes stopped.")