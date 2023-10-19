import scrapy
from urllib.parse import urljoin
from patek.items import PatekItem
# import patek.pipelines
from patek.pipelines import CustomImagesPipeline 
import os
import re
# import hashlib
import html

class PatekSpider(scrapy.Spider):
    name = 'patek'
    start_urls = ['https://www.patek.com/en/collection/all-models'] # original
    allowed_domains = ['patek.com']

    # # Switched off image scraping for extracting field details testing ###
    # custom_settings = {
    #     'ITEM_PIPELINES': {'patek.pipelines.CustomImagesPipeline': 1},
    #     'IMAGES_STORE': '/home/imad/Desktop/web_scraping/sandbox/patek/patek/spiders/patek_images'
    # }
    
    def parse(self, response):
        base_url = 'https://www.patek.com/' # original for all models scraping # keep on all the time
      
        # for all models test
        output = response.xpath('//div[@class="article_list_container to_scroll"]//div[@class="article filtered"]/a/@href').getall() # for all models test
        # Join base URL with each output line to each URL
        joined_output = [urljoin(base_url, url) for url in output]
        # # Follow each joined URL for all model testing
        for url in joined_output:
            yield scrapy.Request(url=url, callback=self.parse_model) 

        # # for one item test
        # base_url = 'https://www.patek.com/en/collection/grand-complications/5327G-001' # men's watch test 
        # base_url = 'https://www.patek.com/en/collection/pocket-watches/980R-001' # pocket watch test
        # base_url = 'https://www.patek.com/en/collection/twenty4/4910-1200A-010' # women's watch test
        # yield scrapy.Request(url=base_url, callback=self.parse_model) # un-comment for one item test
    

    # original parse_model for extracting field details as per customer request
    def parse_model(self, response):

        print('Processing..' + response.url)

        # Create item
        item = PatekItem()

        # Get model URL
        watch_url = response.url
        item['watch_url'] = watch_url

        # Get reference_number from watch_url until the second last /
        reference_number = watch_url.split('/')[-1]
        # If number of "-" is more than one then replace the first "-" with "/" since this is the naming convention for Patek Philippe
        if reference_number.count('-') > 1:
            reference_number = reference_number.replace('-', '/', 1)
        item['reference_number'] = reference_number


        # get brand of the page
        if 'patek' in watch_url:
            item['brand'] = 'Patek Philippe'
        else:
            item['brand'] = 'Other'

        # Get parent_model 
        parent_model = response.xpath('//span[@class="complication"]/text()').get()
        # If it contains more than one element, then get the first element only
        if isinstance(parent_model, list):
            parent_model = parent_model[0]
        item['parent_model'] = parent_model

        # Get specific_model
        # Specific model is  the combination of parent_model and reference_number with a space in between
        specific_model = parent_model + ' ' + reference_number
        # If specific_model has a '/' at the end, then remove everything after the '/'
        if '/' in specific_model:
            specific_model = specific_model.split('/')[0]

        if '-' in specific_model:
            specific_model = specific_model.split('-')[0]

        # if specific_model ends with a letter then remove it
        if specific_model[-1].isalpha():
            specific_model = specific_model[:-1]

        item['specific_model'] = specific_model

        # Get description
        description = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[1]/div/p/text()').getall()
        # Combine the description list into a single string
        description = ' '.join(description)
        item['description'] = description

        # Get all case details #
        case_header = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[3]/div[1]/text()').get()
        # print(f"case_header is: {case_header}")
        if "case" in case_header.lower():
            case_details = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[3]/div[2]/text()').getall()
        elif "case" not in case_header.lower():
            case_details = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/text()').getall()
        # print(f"case_details is: {case_details}")

        # Clean up each element in the case_details list
        cleaned_case_details = [detail.strip() for detail in case_details if detail.strip()]
        # print(f"cleaned_case_details is: {cleaned_case_details}")
        # Join the cleaned_case_details list into a single string
        case_details_text = ' '.join(cleaned_case_details)
        # print(f"case_details_text is: {case_details_text}")
        # Split the case_details_text string by periods (".")
        case_details_segments = [segment.strip() for segment in case_details_text.split('.') if segment.strip()]
        # print(f"case_details_segments is: {case_details_segments}")

        # Get case material
        case_material = case_details_segments[0]
        item['case_material'] = case_material
        
        # Get case back
        # Extract the segment that includes "case back" and assign it to caseback
        caseback = next((segment for segment in case_details_segments if "case back" in segment.lower()), None)
        if caseback == None:
            caseback = ' '
        item['caseback'] = caseback

        # Get case diameter
        # Find the segment containing "Case diameter:" and extract the value after it
        diameter = " "
        for segment in case_details_segments:
            if "Diameter:" in segment:
                diameter = segment.split("Diameter: ")[-1].strip()
                # if next segment ends in "mm" then add it to diameter
                if case_details_segments[case_details_segments.index(segment) + 1].strip().endswith('mm'):
                    diameter += '.' + case_details_segments[case_details_segments.index(segment) + 1].strip()
                break                
            elif "Case diameter:" in segment:
                diameter = segment.split("Case diameter: ")[-1].strip()
                # if next segment ends in "mm" then add it to diameter
                if case_details_segments[case_details_segments.index(segment) + 1].strip().endswith('mm'):
                    diameter += '.' + case_details_segments[case_details_segments.index(segment) + 1].strip()
                break
            elif "Diameter :" in segment:
                diameter = segment.split("Diameter : ")[-1].strip()
                # if next segment ends in "mm" then add it to diameter
                if case_details_segments[case_details_segments.index(segment) + 1].strip().endswith('mm'):
                    diameter += '.' + case_details_segments[case_details_segments.index(segment) + 1].strip()
                break
            elif "Case diameter (10-4 o'clock): " in segment:
                diameter = segment.split("Case diameter (10-4 o'clock): ")[-1].strip()
                # if next segment ends in "mm" then add it to diameter
                if case_details_segments[case_details_segments.index(segment) + 1].strip().endswith('mm'):
                    diameter += '.' + case_details_segments[case_details_segments.index(segment) + 1].strip()
                break
            elif "Diameter (10-4 o’clock): " in segment:
                diameter = segment.split("Diameter (10-4 o’clock): ")[-1].strip()
                # if next segment ends in "mm" then add it to diameter
                if case_details_segments[case_details_segments.index(segment) + 1].strip().endswith('mm'):
                    diameter += '.' + case_details_segments[case_details_segments.index(segment) + 1].strip()
                break
            elif "Case diameter (10 – 4 o’clock): " in segment:
                diameter = segment.split("Case diameter (10 – 4 o’clock): ")[-1].strip()
                # if next segment ends in "mm" then add it to diameter
                if case_details_segments[case_details_segments.index(segment) + 1].strip().endswith('mm'):
                    diameter += '.' + case_details_segments[case_details_segments.index(segment) + 1].strip()
                break
            elif "Diameter (10 - 4 o’clock): " in segment:
                diameter = segment.split("Diameter (10 - 4 o’clock): ")[-1].strip()
                # if next segment ends in "mm" then add it to diameter
                if case_details_segments[case_details_segments.index(segment) + 1].strip().endswith('mm'):
                    diameter += '.' + case_details_segments[case_details_segments.index(segment) + 1].strip()
                break
            elif "Case diameter (10-4 o’clock):" in segment:
                diameter = segment.split("Case diameter (10-4 o’clock): ")[-1].strip()
                # if next segment ends in "mm" then add it to diameter
                if case_details_segments[case_details_segments.index(segment) + 1].strip().endswith('mm'):
                    diameter += '.' + case_details_segments[case_details_segments.index(segment) + 1].strip()
                break
            elif "Case dimensions: " in segment:
                # take last two characters of segment and add them to diameter
                diameter = segment.split("Case dimensions: ")[-1].strip()[-2:]
                # if next segment ends in "mm" then add it to diameter
                if case_details_segments[case_details_segments.index(segment) + 1].strip().endswith('mm'):
                    diameter += '.' + case_details_segments[case_details_segments.index(segment) + 1].strip()
            elif "Diameter (10 4 oclock):" in segment:
                diameter = segment.split("Diameter (10 4 oclock): ")[-1].strip()
                # if next segment ends in "mm" then add it to diameter
                if case_details_segments[case_details_segments.index(segment) + 1].strip().endswith('mm'):
                    diameter += '.' + case_details_segments[case_details_segments.index(segment) + 1].strip()
                break


        # If ".Height" in diameter then split it by ".Height" and assign the first element to diameter
        if ".Height" in diameter:
            diameter = diameter.split(".Height")[0]
        
        # If 'mm' is found in diameter and it is attached to a number then add a space between the number and 'mm'
        if 'mm' in diameter:
            if diameter[-3].isdigit():
                diameter = diameter[:-2] + ' ' + diameter[-2:]
        # print(f"diameter is: {diameter}")
        item['diameter'] = diameter

        # Join the last two segments of case_details_segments into a single string while adding a "." in between them
        last_two_segments = '.'.join(case_details_segments[-2:])
        # print(f"last_two_segments is: {last_two_segments}")
        case_thickness = " "
        # Check content of last_two_segments
        # If last_two_segments contains "Height: " then proceed
        if "Height: " in last_two_segments:
            # Split the last_two_segments string by "Height: "
            last_two_segments = last_two_segments.split("Height: ")
            # Extract the second element of the last_two_segments and assign it to thickness
            case_thickness = last_two_segments[1]
            # if ',' is found in case_thickness then replace it with '.'
            if ',' in case_thickness:
                case_thickness = case_thickness.replace(',', '.')

        elif "Thickness: " in last_two_segments:
            # Split the last_two_segments string by "Thickness: "
            last_two_segments = last_two_segments.split("Thickness: ")
            # Extract the second element of the last_two_segments and assign it to thickness
            case_thickness = last_two_segments[1]

        elif "Height : " in last_two_segments:
            # Split the last_two_segments string by "Height : "
            last_two_segments = last_two_segments.split("Height : ")
            # Extract the second element of the last_two_segments and assign it to thickness
            case_thickness = last_two_segments[1]

        elif "Thickness : " in last_two_segments:
            # Split the last_two_segments string by "Thickness : "
            last_two_segments = last_two_segments.split("Thickness : ")
            # Extract the second element of the last_two_segments and assign it to thickness
            case_thickness = last_two_segments[1]
        
        
        # If 'mm' is found in case_thickness and it is attached to a number then add a space between the number and 'mm'
        if case_thickness:
            # print(f"case_thickness is: {case_thickness}")
            if 'mm' in case_thickness:
                if case_thickness[-3].isdigit():
                    case_thickness = case_thickness[:-2] + ' ' + case_thickness[-2:]
            item['case_thickness'] = case_thickness
        else:
            item['case_thickness'] = ' '

        # Get crystal information
        # Extract the segment that includes "crystal" and assign it to crystal
        crystal = "Sapphire"
        item['crystal'] = crystal

        # Get water resistance
        # Find the segment containing "Water-resistant to " and extract the value after it
        water_resistance = " "
        for segment in case_details_segments:
            if "Water-resistant to " in segment:
                # print("water_resistance segment is: " + segment)
                water_resistance = segment.split(" ")[-2].strip()
                # print(f"water_resistance pre-cleaning is: {water_resistance}")
                water_resistance = str(int(water_resistance) / 10)
                # print(f"water_resistance post-division is: {water_resistance}")
                # if result is "#.0 ATM" then change it to "# ATM"
                if water_resistance[-2:] == '.0':
                    water_resistance = water_resistance[:-2] + ' ' + 'ATM'
                    # print(f"water_resistance post-removing .0 is: {water_resistance}")
                    item['water_resistance'] = water_resistance
                    break

            elif "not water resistant" in segment:
                water_resistance = "Not water resistant"
                item['water_resistance'] = water_resistance
                break      

        # Get dial color
        dial_color = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/text()').get().replace('\r\n', '').strip().split(',')[0]
        if 'Dial:' in dial_color:
            dial_color = dial_color.split('Dial:')[1].strip().capitalize()
        elif 'Dial :' in dial_color:
            dial_color = dial_color.split('Dial :')[1].strip().capitalize()
        item['dial_color'] = dial_color
        
        # Get numerals
        numerals_check = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/text()').get().replace('\r\n', '').strip().split('.')
        # print(f"numerals_check is {numerals_check}")

        # Find and capture the part containing 'numerals'
        for segment in numerals_check:
            if 'numerals' in segment:
                # print(f"numerals is: {segment}")
                if ',' in segment:
                    item['numerals'] = segment.strip().split(',')[1].strip().capitalize()
                    # print(f"numerals is: {item['numerals']}")
                else:
                    item['numerals'] = segment.strip().capitalize()
                    # print(f"numerals is: {item['numerals']}")
                break  # Stop searching after finding the first occurrence
            else:
                item['numerals'] = ' '


        # Confirm if section header is 'gemsetting' or 'strap'
        # If section header is 'gemsetting' then get bracelet material, bracelet color and clasp type from div[5]
        # If section header is 'strap' then get bracelet material, bracelet color and clasp type from div[4]
        section_header = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[4]/div[1]/text()').get()
        if section_header != None:
            section_header = section_header.strip().lower()
        # print(f"section_header is: {section_header}")

        bracelet_color = ' '
        bracelet_material = ' '
        clasp_type = ' '
        bracelet_details = ' '

        if section_header == 'gemsetting':
             # Get bracelet material
            
            if response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[5]/div[2]/text()').get():
                bracelet_details = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[5]/div[2]/text()').get().replace('\r\n', '').strip().split('.')[0]
                if bracelet_details != None:
                    bracelet_material = bracelet_details.strip()
                else:
                    bracelet_material = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[4]/div[2]/text()').get().replace('\r\n', '').strip().split('.')[0]
            item['bracelet_material'] = bracelet_material

            # Get bracelet color
            # Find the index of the last comma in the string
            last_comma_index = bracelet_details.rfind(',')
            if last_comma_index != -1:
                # Extract the substring after the last comma and strip any leading/trailing whitespace
                
                bracelet_color = bracelet_details[last_comma_index + 1:].strip()
                


            # Get clasp type
            if response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[5]/div[2]/text()').get():
                clasp_type = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[5]/div[2]/text()').get().replace('\r\n', '').strip().split('.')[1].strip()
            
        elif section_header == 'strap':
            # Get bracelet material
            bracelet_details = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[4]/div[2]/text()').get().replace('\r\n', '').strip().split('.')[0]
            bracelet_material = bracelet_details.strip()
            

            # Get bracelet color
            # Find the index of the last comma in the string
            last_comma_index = bracelet_details.rfind(',')
            if last_comma_index != -1:
                # Extract the substring after the last comma and strip any leading/trailing whitespace
                
                bracelet_color = bracelet_details[last_comma_index + 1:].strip()
                


            # Get clasp type
            if response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[4]/div[2]/text()').get():
                clasp_type = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[4]/div[2]/text()').get().replace('\r\n', '').strip().split('.')[1].strip()
            
        elif section_header == 'bracelet':
            # Get bracelet material
            if response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[5]/div[2]/text()').get():
                bracelet_details = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[5]/div[2]/text()').get().replace('\r\n', '').strip().split('.')[0]
                if bracelet_details != None:
                    bracelet_material = bracelet_details.strip()
                else:
                    bracelet_material = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[4]/div[2]/text()').get().replace('\r\n', '').strip().split('.')[0]
                

            # Get bracelet color
            # Find the index of the last comma in the string
            last_comma_index = bracelet_details.rfind(',')
            if last_comma_index != -1:
                # Extract the substring after the last comma and strip any leading/trailing whitespace
                
                bracelet_color = bracelet_details[last_comma_index + 1:].strip()
                
            # Get clasp type
            if response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[5]/div[2]/text()').get():
                clasp_type = response.xpath('/html/body/div[3]/article/section[2]/div[2]/div[2]/div/div[2]/div[5]/div[2]/text()').get().replace('\r\n', '').strip().split('.')[1].strip()
                

        item['bracelet_color'] = bracelet_color
        item['bracelet_material'] = bracelet_material
        item['clasp_type'] = clasp_type

        # print(f"'bracelet_material' is: {bracelet_material}")
        # print(f"'bracelet_color' is: {bracelet_color}")
        # print(f"'clasp_type' is: {clasp_type}")


        # Get movement
        # check if the movement is located in /html/body/div[3]/section[2]/div/div[2]/h1/span[2]/ or /html/body/div[3]/section[2]/div/div[2]/h1/
        movement = response.xpath('//html/body/div[3]/article/section[2]/div[1]/h1/span[4]/text()').get()
        # print(f"movement is: {movement}")

        if movement == None:
            movement = response.xpath('/html/body/div[3]/article/section[3]/div[1]/h1/span[4]/text()').get()
            if movement == None:
                movement = response.xpath('/html/body/div[3]/article/section[4]/div[1]/h1/span[4]/text()').get()
        # print (f"movement is: {movement}")
        if movement:
            movement = movement.title()

        # # if movement is type None then extract it from /html/body/div[3]/section[2]/div/div[2]/h1/
        # if movement == None:
        #     movement = response.xpath('/html/body/div[3]/section[2]/div/div[2]/h1/span[2]/text()').get()
        
        if movement:
            if movement.lower() == 'self-winding':
                movement = 'Automatic'
            elif movement.lower() == 'manual winding':
                movement = 'Manual winding'

        item['movement'] = movement

        # Get caliber
        caliber = response.xpath('/html/body/div[3]/section[2]/div/div[3]/div/h1/span[1]/text()').get()
        if caliber == None:
            caliber = response.xpath('/html/body/div[3]/section[1]/div/div[2]/h1/span[1]/text()').get()
        item['caliber'] = caliber

        # Define a function to unescape HTML entities
        def unescape_html(text):
            return html.unescape(text)
    
        # Extract caliber data headers and details to get power reserve, frequency, and jewels
        caliber_data = []
        # append "Description" to caliber_data[0] since it is not included
        # print(f"parent_model is: {parent_model}")
        if 'pocket' not in parent_model.lower():
            caliber_data.append("Description")

        # Check if /html/body/div[3]/section[1]/div/div[3]/div/p or /html/body/div[3]/section[2]/div/div[3]/div/p have data and pick one
        if response.xpath('/html/body/div[3]/section[1]/div/div[3]/div/p/strong[1]/text()').get():
            # /html/body/div[3]/section[1]/div/div[3]/div/p has data
            for i in range(1, 15):
                xpath_expression = f"/html/body/div[3]/section[1]/div/div[3]/div/p/strong[{i}]"
                header_element = response.xpath(xpath_expression).get()
                if header_element:
                    header_text = header_element.strip()  # Extract text and strip any leading/trailing whitespace
                    caliber_data.append(header_text)

                caliber_data_2_elements = response.xpath('/html/body/div[3]/section[1]/div/div[3]/div/p/text()')
        else:
            # /html/body/div[3]/section[2]/div/div[3]/div/p has data
            for i in range(1, 15):
                xpath_expression = f"/html/body/div[3]/section[2]/div/div[3]/div/p/strong[{i}]"
                header_element = response.xpath(xpath_expression).get()
                if header_element:
                    header_text = header_element.strip()  # Extract text and strip any leading/trailing whitespace
                    caliber_data.append(header_text)

                caliber_data_2_elements = response.xpath('/html/body/div[3]/section[2]/div/div[3]/div/p/text()')

        # Extract text from elements and remove <sup> tags
        caliber_data_2 = []
        for element in caliber_data_2_elements:
            text = element.get().strip()  # Extract text and strip any leading/trailing whitespace
            text = text.replace('\r\n', '')  # Remove newline characters
            text = re.sub(r'<sup[^>]*>.*?</sup>', '', text)  # Remove <sup> tags and their content
            caliber_data_2.append(text)

        # Clean the headers in caliber_data by removing <strong> tags
        caliber_data = [re.sub(r'<[^>]*>', '', header) for header in caliber_data]

        # print(f"caliber_data is {caliber_data}")
        # print(f"caliber_data_2 is {caliber_data_2}")


        # Process caliber_data_2 to remove unwanted symbols and handle special symbols
        cleaned_data = [unescape_html(data.strip()) for data in caliber_data_2 if data.strip()]
        # remove ":  " from each element
        cleaned_data = [data.split(':  ')[-1] for data in cleaned_data]
        # remove last . from each element if found
        cleaned_data = [data[:-1] if data.endswith('.') else data for data in cleaned_data]
        # Remove empty entries
        cleaned_data = [data for data in cleaned_data if data]

        # If cleaned_data starts with a number, then remove the first index in cleaned_data
        if cleaned_data[0][0].isdigit():
                cleaned_data.pop(0)


        # Combine cleaned_data and caliber_data
        joined_data = []
        # current_header = ""

        for data, header in zip(cleaned_data, caliber_data):
            if data and header:
                joined_data.append(f"{header}: {data}")


        # print(f"cleaned_data is: {cleaned_data}")
        # print(f"joined_data is {joined_data}")

        # Get power reserve from joined_data
        power_reserve = ' '
        if "Power reserve" in caliber_data:
            # Find the index of "Power Reserve" in caliber_data
            index = caliber_data.index("Power reserve")
            if index < len(joined_data):
                # Assign the value from joined_data to item['power_reserve']
                power_reserve = joined_data[index].split(': ')[1]
                # print(f"power_reserve before split is: {power_reserve}")
                if 'max.' in power_reserve:
                    power_reserve = power_reserve.split('max.')[1].strip()
                elif 'min.' in power_reserve:
                    power_reserve = power_reserve.split('min.')[1].strip()
                    if 'max.' in power_reserve:
                        power_reserve = power_reserve.split('max.')[0].strip()
                elif 'Min.' in power_reserve:
                    power_reserve = power_reserve.split('Min.')[1].strip()
                # print(f"power_reserve after split is: {power_reserve}")
                if "hours" in power_reserve:
                    power_reserve = power_reserve.split('hours')[0].strip()
                    # re-add hours to power_reserve
                    power_reserve += ' hours'
                # print(f"power_reserve after hours split and re-add is: {power_reserve}")
                item['power_reserve'] = power_reserve


        # Get frequency from joined_data
        frequency = ' '
        if "Vibrations/hour" in caliber_data:
            # Find the index of "Vibrations/hour" in caliber_data
            index = caliber_data.index("Vibrations/hour")
            if index < len(joined_data):
                # Assign the value from joined_data to item['frequency']
                # frequency = joined_data[index].split(': ')[1]
                frequency = re.sub(r'(\d) (\d)', r'\1\2', joined_data[index].split(': ')[1])
                frequency = frequency.replace(',','')
                item['frequency'] = frequency
                
        elif "Frequency" in caliber_data:
            # Find the index of "Frequency" in caliber_data
            index = caliber_data.index("Frequency")
            if index < len(joined_data):
                # Assign the value from joined_data to item['frequency']
                # frequency = joined_data[index].split(': ')[1]
                frequency = re.sub(r'(\d) (\d)', r'\1\2', joined_data[index].split(': ')[1])
                frequency = frequency.replace(',','')
                item['frequency'] = frequency

        # print(f"frequency is {frequency}")

        # Get jewels from joined_data
        jewels = ' '
        if "Jewels" in caliber_data:
            # Find the index of "Jewels" in caliber_data
            index = caliber_data.index("Jewels")
            if index < len(joined_data):
                # Assign the value from joined_data to item['Jewels']
                jewels = joined_data[index].split(': ')[1]
                item['jewels'] = jewels

        # print(f"jewels is {jewels}")

        # If quartz then run this section
        check_quartz = response.xpath('/html/body/div[3]/section[2]/div/div[3]/div/h1/span[2]/text()').get()
        if check_quartz == 'Quartz':
            jewels = response.xpath('/html/body/div[3]/section[2]/div/div[3]/div/p/text()[4]').get().replace(":","").strip().replace('.','')
            item['jewels'] = jewels
            frequency = response.xpath('/html/body/div[3]/section[2]/div/div[3]/div/p/text()[5]').get().replace(":","").strip().replace('.','')
            item['frequency'] = frequency

        # Get marketing_name
        marketing_name = " "
        item['marketing_name'] = marketing_name

        # Get weight
        weight = " "
        item['weight'] = weight

        # Get features
        # Features are the list of features from caliber
        if response.xpath('/html/body/div[3]/section[2]/div/div[3]/div/p/text()[1]').get():
            features = response.xpath('/html/body/div[3]/section[2]/div/div[3]/div/p/text()[1]').get().replace('\r\n', '').strip()
        else:
            features = ' '
        item['features'] = features

        # Get nickname
        nickname = ' '

        # Check if the XPath selector has results and if the desired index exists
        nickname_elements = response.xpath('/html/body/div[3]/article/section[1]/div/div[1]/text()').getall()
        if len(nickname_elements) > 2:
            nickname = nickname_elements[2].replace('\r\n', '').strip()

        #if nickname ends with '.' then remove it
        if nickname.endswith('.'):
            nickname = nickname[:-1]
        item['nickname'] = nickname

        # Get price
        # price = response.xpath('//*[@id="product_price"]/text()').get()
        price = " "
        item['price'] = price

        # Get curency
        currency = 'USD'
        item['currency'] = currency

        # Get case_finish:
        case_finish = ' '
        item['case_finish'] = case_finish

        # Get between_lugs
        between_lugs = ' '
        item['between_lugs'] = between_lugs

        # Get lug_to_lug
        lug_to_lug = ' '
        item['lug_to_lug'] = lug_to_lug

        # Get bezel_material
        bezel_material = ' '
        item['bezel_material'] = bezel_material

        # Get bezel_color
        bezel_color = ' '
        item['bezel_color'] = bezel_color

        # Get year_introduced
        year_introduced = ' '
        item['year_introduced'] = year_introduced

        # Get image_url
        # image_url = response.xpath('/html/body/div[3]/article/section[2]/div[3]/div[3]/div/div/div[3]/div/picture/img/@src')
        # to be copied from files that have them
        image_url = ' '
        item['image_url'] = image_url

        # Get style
        style = ' '
        item['style'] = style

        # Get made_in
        made_in = 'Switzerland'
        item['made_in'] = made_in

        # Get case_shape
        case_shape = ' '
        item['case_shape'] = case_shape

        # 

        # Get type
        type = ' '
        # if reference_number starts with '7300' or '4910' then type is 'Women's Watches'
        if item['reference_number'].startswith('7300') or item['reference_number'].startswith('4910'):
            type = "Women's Watches"
        # else if reference_number starts with '98' or '97' then type is 'Pocket Watches'
        elif item['reference_number'].startswith('98') or item['reference_number'].startswith('97'):
            type = "Pocket Watches"
        # else type is Men's Watches:
        else:
            type = "Men's Watches"
        item['type'] = type

        # Get short_description
        short_description = description.split('.')[0]
        item['short_description'] = short_description

        yield item

# # IMAGE SCRAPING CONTINUES

#         yield scrapy.Request(url=self.get_image_url(item['nickname']), callback=self.parse_image, meta={'item': item})

#     def get_image_url(self, nickname):
#         # Function to construct the image URL based on the model number
#         base_image_url = 'https://static.patek.com/images/articles/face_white/350/'
#         image_url = f'{nickname.upper().replace("-", "_")}_1@2x.jpg'
#         return urljoin(base_image_url, image_url)

#     def parse_image(self, response):
#         # Extract the item object from the meta
#         item = response.meta['item']
#         # Get the image URL from the response
#         image_url = response.url
#         # Save the image URL in the item
#         item['image_urls'] = image_url
#         yield item    
