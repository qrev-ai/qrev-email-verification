import pandas as pd
import os
import signal
from pi_conf import load_config
from qrev_email_verification.email_verification import EmailVerification
from tqdm import tqdm

def signal_handler(signum, frame):
    print("\nCtrl+C detected. exiting...")
    # save_progress(df, email_verification, processed_indices, service_names)
    exit(0)

def save_progress(df, email_verification, processed_indices, service_names):
    for service_name in service_names:
        # Convert boolean values to integers and update the DataFrame
        df.loc[processed_indices, service_name] = [int(val) for val in email_verification[service_name]]
    df.to_csv("new_partial.csv", index=False)
    print(f"Progress saved to new_partial.csv")

def process_emails(df, service_names):
    ev = EmailVerification()
    email_verification = {service: [] for service in service_names}
    processed_indices = []

    try:
        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing emails"):
            email = row['email']
            
            try:
                services = ev.get_email_responses(email)
            except Exception as e:
                tqdm.write(f"Error processing {email}: {e}")
                services = {}

            for service_name in service_names:
                val = service_name in services
                email_verification[service_name].append(val)
            
            processed_indices.append(idx)
            
            if len(processed_indices) % 100 == 0:
                save_progress(df, email_verification, processed_indices, service_names)

    except Exception as e:
        print(f"An error occurred: {e}")
        save_progress(df, email_verification, processed_indices, service_names)

    finally:
        # Update the DataFrame with processed data
        for service_name in service_names:
            # Convert boolean values to integers
            df.loc[processed_indices, service_name] = [int(val) for val in email_verification[service_name]]
        
        df.to_csv("new.csv", index=False)
        print("Processing complete. Results saved to new.csv")

def main():
    # Set up Ctrl+C handler
    signal.signal(signal.SIGINT, signal_handler)

    cfg = load_config("qrev-ai")
    cfg.to_env()

    csv_path = os.path.expanduser("~/data/bevy/combined-items-uni.csv")
    df = pd.read_csv(csv_path)

    service_names = {"millionverifier", "zerobounce"}

    # Initialize columns with NaN if they don't exist
    for service_name in service_names:
        if service_name not in df.columns:
            df[service_name] = pd.NA

    process_emails(df, service_names)

if __name__ == "__main__":
    main()