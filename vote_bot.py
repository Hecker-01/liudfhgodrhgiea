#!/usr/bin/env python3
"""
Automated voting script for glr75.nl/top75
Votes for track trk-278 with randomized name and email
Supports hCaptcha click-based challenges
"""

import requests
import random
import string
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class VotingBot:
    def __init__(self):
        self.base_url = "https://glr75.nl/top75"
        self.driver = None
        self.tracks = ["trk-278", "trk-022"]  # List of tracks to vote for
        
    def generate_random_name(self):
        """Generate a random Dutch-sounding name"""
        first_names = ["Jan", "Piet", "Klaas", "Henk", "Willem", "Johan", "Marco", "Erik", "Tom", "Lisa", "Anne", "Eva"]
        last_names = ["de Vries", "Jansen", "Bakker", "Visser", "Smit", "Meijer", "de Jong", "van Dijk", "Mulder", "Bos"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def generate_email(self):
        """Generate email in format: 6randomnumbers@glr.nl"""
        numbers = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        return f"{numbers}@glr.nl"
    
    def setup_browser(self):
        """Setup Chrome browser with appropriate options"""
        chrome_options = Options()
        # Run in visible mode so user can solve hCaptcha
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"Error setting up browser: {e}")
            print("Make sure Chrome and ChromeDriver are installed.")
            return False
    
    def wait_for_hcaptcha_solution(self):
        """Wait for user to solve hCaptcha and display instructions"""
        root = tk.Tk()
        root.title("hCaptcha Instructions")
        root.geometry("500x250+0+0")  # 500x250 size, positioned at x=0, y=0
        root.attributes('-topmost', True)
        
        # Instructions
        instructions = tk.Label(root, 
                               text="Please solve the hCaptcha in the browser window.\n\n"
                                    "After completing the hCaptcha:\n"
                                    "Click the 'CAPTCHA Solved' button below.",
                               font=("Arial", 12),
                               justify="left",
                               wraplength=450)
        instructions.pack(pady=30)
        
        captcha_solved = [False]
        
        def mark_solved():
            captcha_solved[0] = True
            root.quit()
            root.destroy()
        
        # Button
        solve_btn = tk.Button(root, 
                             text="CAPTCHA Solved - Continue", 
                             command=mark_solved,
                             font=("Arial", 14, "bold"),
                             bg="#4CAF50",
                             fg="white",
                             padx=20,
                             pady=15)
        solve_btn.pack(pady=20)
        
        root.mainloop()
        return captcha_solved[0]
    
    def fill_form_and_submit(self, name, email, tracks):
        """Fill the voting form with Selenium and wait for hCaptcha"""
        try:
            # Load the page
            print("\nLoading voting page...")
            self.driver.get(self.base_url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Try to find and fill form fields - adjust selectors as needed
            try:
                # Common field name patterns - try multiple
                name_field = None
                email_field = None
                track_fields = []
                
                # Try to find name field
                for selector in ['input[name="name"]', 'input[name="naam"]', 'input#name', 'input#naam']:
                    try:
                        name_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                # Try to find email field
                for selector in ['input[name="email"]', 'input[type="email"]', 'input#email']:
                    try:
                        email_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                # Try to find track fields (checkboxes or radio buttons) for BOTH tracks
                for track in tracks:
                    for selector in [f'input[value="{track}"]', f'input[name="track"][value="{track}"]', 
                                    f'input[name="tracks"][value="{track}"]', f'option[value="{track}"]', f'input#{track}']:
                        try:
                            track_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                            track_fields.append((track, track_field))
                            break
                        except:
                            continue
                
                # Fill in the fields
                if name_field:
                    name_field.clear()
                    name_field.send_keys(name)
                    print(f"✓ Filled name: {name}")
                else:
                    print("⚠ Could not find name field")
                
                if email_field:
                    email_field.clear()
                    email_field.send_keys(email)
                    print(f"✓ Filled email: {email}")
                else:
                    print("⚠ Could not find email field")
                
                if track_fields:
                    for track, field in track_fields:
                        field.click()
                        print(f"✓ Selected track: {track}")
                else:
                    print("⚠ Could not find track fields")
                
            except Exception as e:
                print(f"Note: Auto-fill encountered issues: {e}")
                print("You may need to fill the form manually.")
            
            # Now wait for user to solve hCaptcha
            print("\n" + "="*50)
            print("WAITING FOR HCAPTCHA")
            print("="*50)
            print("Please solve the hCaptcha in the browser window.")
            print("After solving, click the button in the popup window.")
            
            captcha_solved = self.wait_for_hcaptcha_solution()
            
            if not captcha_solved:
                return False, "User cancelled CAPTCHA solving"
            
            # Try to find and click submit button
            try:
                submit_button = None
                for selector in ['button[type="submit"]', 'input[type="submit"]', 
                               'button.submit', 'input.submit', '#submit']:
                    try:
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if submit_button:
                    submit_button.click()
                    print("\n✓ Form submitted!")
                    time.sleep(1)
                    
                    # Check for success message
                    page_source = self.driver.page_source.lower()
                    if 'success' in page_source or 'bedankt' in page_source or 'gelukt' in page_source:
                        return True, "Vote submitted successfully!"
                    else:
                        return True, "Form submitted (please verify in browser)"
                else:
                    print("\n⚠ Could not find submit button - please submit manually")
                    input("Press Enter after you've submitted the form...")
                    return True, "Please verify submission in browser"
                    
            except Exception as e:
                print(f"\nError clicking submit: {e}")
                input("Press Enter after you've submitted the form manually...")
                return True, "Please verify submission in browser"
                
        except Exception as e:
            return False, f"Error during form submission: {e}"
    
    def run_once(self):
        """Single voting execution"""
        # Generate credentials
        name = self.generate_random_name()
        email = self.generate_email()
        tracks = self.tracks  # Vote for both tracks
        
        print(f"\nGenerated credentials:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Tracks: {', '.join(tracks)}")
        
        # Setup browser
        print("\nSetting up browser...")
        if not self.setup_browser():
            print("\n✗ Failed to setup browser. Exiting.")
            return False
        
        try:
            # Fill form and handle hCaptcha
            success, message = self.fill_form_and_submit(name, email, tracks)
            
            print(f"\n{message}")
            
            if success:
                print("\n✓ Voting process completed!")
            else:
                print("\n✗ Voting failed.")
            
            return success
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                print("Browser closed.\n")
    
    def run(self):
        """Main execution flow - continuous voting loop"""
        print("=" * 50)
        print("GLR75 Voting Bot (hCaptcha Edition)")
        print("=" * 50)
        print("Will continuously vote after each submission.")
        print("Press Ctrl+C to stop.\n")
        
        vote_count = 0
        
        try:
            while True:
                vote_count += 1
                print(f"\n{'='*50}")
                print(f"VOTE #{vote_count}")
                print(f"{'='*50}")
                
                success = self.run_once()
                
                if success:
                    print(f"\n✓ Vote #{vote_count} completed! Starting next vote...")
                    time.sleep(2)  # Brief pause before restarting
                else:
                    print(f"\n✗ Vote #{vote_count} failed. Retrying...")
                    time.sleep(3)
                    
        except KeyboardInterrupt:
            print(f"\n\n{'='*50}")
            print(f"Stopped by user. Total votes submitted: {vote_count}")
            print(f"{'='*50}")


def main():
    bot = VotingBot()
    bot.run()


if __name__ == "__main__":
    main()
