from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep

# Initialize the driver (make sure the WebDriver is in your system PATH)
driver = webdriver.Chrome()

# Placeholder for your data
data = []

# Placeholder for your links (you should populate this list with your URLs)
links_all = []  

# Loop through all links
for link in links_all:
    driver.get(link)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extracting image URL
    try:
        image = driver.find_element(By.XPATH, '//*[@id="block-blancpain-content"]/article/section[1]/div/div[2]/div[2]/img').get_attribute("src")
    except Exception:
        image = None

    # Extracting parent model
    try:
        parent_model = driver.find_element(By.XPATH, '//*[@id="block-blancpain-content"]/article/section[1]/div/div[2]/div[1]/div/p').text.title()
    except Exception:
        parent_model = None

    # Extracting specific model
    try:
        spec_model = parent_model + ' ' + driver.find_element(By.XPATH, '//*[@id="block-blancpain-content"]/article/section[1]/div/div[2]/div[1]/div/h1').text
    except Exception:
        spec_model = None

    # Extracting reference number (list title)
    try:
        list_title = soup.find('p', class_='sku uppercase text-xs leading-none antialiased mb-[0.5rem] font-medium antialiased').get_text()
    except Exception:
        list_title = None

    # Determining gender based on reference number or parent model
    try:
        # Define reference numbers corresponding to women's watches
        women_ref = ('5100 1127 NAHA', '5100 1127 NAJA', '5100 1127 NATA', '5100 1127 NAVA', '5100 1127 NAWA',
                     # ... other reference numbers
                     '6104 3642 MMB', '6104 2987 55A', '6104 2987 MMB', '6104 1963 58A', '6127 1127 55B',
                     '6127 1127 95A', '6127 1127 MMB', '6127 4628 55B', '6127 4628 95A', '6127 4628 MMB',
                     '6127 3642 55B', '6127 3642 MMB', '6106 1127 MMB', '6126 2987 55B', '6104 1127 55A',
                     '6104 1127 95A', '6104 1127 MMB', '6104 4628 95A', '6104 4628 55A', '6104 4628 MMB',
                     '6104 4654 55A', '6104B 4654 99A', '6104 2930 55A', '6104 3642 55A')
        if list_title in women_ref or parent_model == 'Ladybird':
            gender = "Women's Watches"
        else:
            gender = "Men's Watches"
    except Exception:
        gender = None

    # Additional information from the second group
    group2 = soup.find('div', class_='content w-full lg_w-auto').get_text()

    # Extracting caliber
    try:
        caliber = list(list(re.findall(r'(Caliber\n)(.*)', group2)[0]))[1]
    except Exception:
        caliber = None

    # Extracting power reserve and formatting it
    try:
        power = list(list(re.findall(r'(Power reserve\n)(.*)', group2)[0]))[1]
        power_res = re.sub('hrs', ' hours', power)
    except Exception:
        power_res = None

    sleep(2)

    # Additional information from the product description
    com = soup.find('div', class_='product-description__subsection mb-12 last:mb-0').get_text()

    # Extracting features and functions from complications
    try:
        try:
            sub1 = list(list(re.findall(r'(Complications\n\n\n\n)(.*)\n(.*)\n\n\n\n\n(.*)\n(.*)', com)[0]))[1] + ': '
            sub2 = list(list(re.findall(r'(Complications\n\n\n\n)(.*)\n(.*)\n\n\n\n\n(.*)\n(.*)', com)[0]))[3] + ': '
            under1 = list(list(re.findall(r'(Complications\n\n\n\n)(.*)\n(.*)\n\n\n\n\n(.*)\n(.*)', com)[0]))[2] + ' '
            under2 = list(list(re.findall(r'(Complications\n\n\n\n)(.*)\n(.*)\n\n\n\n\n(.*)\n(.*)', com)[0]))[4]
            feat_func = sub1 + under1 + sub2 + under2
        except Exception:
            sub1 = list(list(re.findall(r'(Complications\n\n\n\n)(.*)\n(.*)', com)[0]))[1] + ': '
            under1 = list(list(re.findall(r'(Complications\n\n\n\n)(.*)\n(.*)', com)[0]))[2]
            feat_func = sub1 + under1
    except Exception:
        feat_func = None

    # Additional specifications from the product specification section
    spec = soup.find('div', class_='wrapper container xl_px-[8.33vw]').get_text()

    # Extracting dial color
    try:
        dial_color = list(list(re.findall(r'(Dial Color\n)(.*)', spec)[0]))[1]
    except Exception:
        dial_color = None

    # Extracting case material and setting it as nickname
    try:
        case_material = list(list(re.findall(r'(Case Material\n)(.*)', spec)[0]))[1]
        nickname = case_material
    except Exception:
        case_material = None
        nickname = None

    # Extracting sapphire back information and determining case back
    try:
        cb = list(list(re.findall(r'(Sapphire Back\n)(.*)', spec)[0]))[1]
        caseback = 'Sapphire' if cb == 'Yes' else None
    except Exception:
        caseback = None

    # Extracting case thickness
    try:
        thickness = list(list(re.findall(r'(Case Thickness\n)(.*)', spec)[0]))[1]
    except Exception:
        thickness = None

    # Extracting water resistance and formatting it
    try:
        water_r = list(list(re.findall(r'(Water Resistance\n)(.*)', spec)[0]))[1]
        water_res = re.sub('M', ' meters', water_r)
    except Exception:
        water_res = None

    # Extracting strap material
    try:
        strap_mat = list(list(re.findall(r'(Strap Material\n)(.*)', spec)[0]))[1]
    except Exception:
        strap_mat = None

    # Extracting buckle type
    try:
        buckle_type = list(list(re.findall(r'(Buckle\n)(.*)', spec)[0]))[1]
    except Exception:
        buckle_type = None

    # Extracting collection and formatting it
    try:
        collection = list(list(re.findall(r'(Collection\n)(.*)', spec)[0]))[1].title()
    except Exception:
        collection = None

    # Collating the data
    data.append([image, parent_model, spec_model, list_title, gender, caliber, power_res, feat_func, dial_color, nickname, caseback, thickness, water_res, strap_mat, buckle_type, collection])

    sleep(2)

driver.quit()

# Converting the data into a Pandas DataFrame and saving it to a CSV file
df = pd.DataFrame(data, columns=['Image', 'Parent Model', 'Specific Model', 'List Title', 'Gender', 'Caliber', 'Power Reserve', 'Features/Functions', 'Dial Color', 'Nickname', 'Case Back', 'Case Thickness', 'Water Resistance', 'Strap Material', 'Buckle Type', 'Collection'])
df.to_csv('blancpain_watches_data.csv', index=False)

print("Data extraction is complete. Saved to blancpain_watches_data.csv")
