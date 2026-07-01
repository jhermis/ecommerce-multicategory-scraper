import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver():
    """Configures and initializes the Chrome WebDriver."""
    print("🚀 Initializing Chrome WebDriver...")
    options = webdriver.ChromeOptions()
    # You can add arguments here later (e.g., --headless, --start-maximized)
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_category(driver, category_name):
    """Navigates to a specific category and extracts product data safely."""
    print(f"\n🎯 Connecting to category: '{category_name}'...")
    driver.get("http://books.toscrape.com/")
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    scraped_data = []
    
    try:
        # Locate the category link and click it
        category_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, category_name)))
        category_link.click()
        
        # Short pause for dynamic elements to load smoothly
        time.sleep(2)
        
        # Capture all product containers
        product_elements = driver.find_elements(By.CLASS_NAME, "product_pod")
        
        for element in product_elements:
            # Safe attribute extraction
            title = element.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
            price = element.find_element(By.CLASS_NAME, "price_color").text
            
            scraped_data.append({
                "Category": category_name,
                "Product Name": title,
                "Price": price
            })
            print(f"✅ Successfully extracted: {title} | {price}")
            
    except Exception as error:
        print(f"❌ Critical error processing '{category_name}': {error}")
        
    return scraped_data

def run_bot():
    """Main function to control the bot's workflow."""
    target_categories = ["Music", "Books", "Poetry"]
    data_memory = []
    
    # Initialize browser
    driver = initialize_driver()
    
    # Loop through each category
    for category in target_categories:
        category_data = scrape_category(driver, category)
        data_memory.extend(category_data) # Accumulate lists
        
    driver.quit()
    
    # Export phase using Pandas
    if data_memory:
        print("\n📊 Processing database with Pandas...")
        df = pd.DataFrame(data_memory)
        output_file = "automated_category_report.xlsx"
        df.to_excel(output_file, index=False)
        print(f"✨ SUCCESS! Master report saved as '{output_file}'.")
    else:
        print("⚠️ No data was collected to export.")

# Ensures the bot only runs if executed directly
if __name__ == "__main__":
    print("--- STARTING DATA AUTOMATION SYSTEM ---")
    run_bot()
    print("--- SYSTEM TERMINATED ---")