from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
'''
Lena Bibbo 
48248104
Partners: Amelia Nam and Charlotte Foley
lbibbo@umich.edu

WRITTEN REFLECTION AT BOTTOM

'''

def get_listings_from_search_results(html_file):
    """
    Write a function that creates a BeautifulSoup object on html_file. Parse
    through the object and return a list of tuples containing:
     a string of the title of the listing,
     an int of the cost to rent for one night,
     and a string of the listing id number
    in the format given below. Make sure to turn costs into ints.

    The listing id is found in the url of a listing. For example, for
        https://www.airbnb.com/rooms/1944564
    the listing id is 1944564.
.

    [
        ('Title of Listing 1', 'Cost 1', 'Listing ID 1'),  # format
        ('Loft in Mission District', 210, '1944564'),  # example
    ]
    """
    listing_title_list = []
    cost_list = []
    listing_id = []
    listing_id_list = []
 
    base_path = os.path.abspath(os.path.dirname(__file__))
    fullpath = os.path.join(base_path, html_file)
    file = open(fullpath, 'r')
    f = file.read()
    file.close()
    soup = BeautifulSoup(f, 'html.parser')

    listing_title = soup.find_all('div', class_ = 't1jojoys dir dir-ltr')
    for ti in listing_title:
        listing_title_list.append(ti.text)

    cost = soup.find_all('span', class_= '_tyxjp1')
    for co in cost:
        cost_list.append(int(co.text.strip('$')))
    #remove the $ and make it an int

    for listing in listing_title:
        listing_id.append(listing.get('id')[6:])
        #get rid of the weird _title
       
    for x in range(len(cost_list)):
        listing_id_list.append((listing_title_list[x], cost_list[x], listing_id[x]))

    return listing_id_list


def get_listing_information(listing_id):
    """
    Write a function to return relevant information in a tuple from an Airbnb listing id.
    NOTE: Use the static files in the html_files folder, do NOT send requests to the actual website.
    Information we're interested in:
        string - Policy number: either a string of the policy number, "Pending", or "Exempt"
            This field can be found in the section about the host.
            Note that this is a text field the lister enters, this could be a policy number, or the word
            "pending" or "exempt" or many others. Look at the raw data, decide how to categorize them into
            the three categories.
        string - Place type: either "Entire Room", "Private Room", or "Shared Room"
            Note that this data field is not explicitly given from this page. Use the
            following to categorize the data into these three fields.
                "Private Room": the listing subtitle has the word "private" in it
                "Shared Room": the listing subtitle has the word "shared" in it
                "Entire Room": the listing subtitle has neither the word "private" nor "shared" in it
        int - Number of bedrooms
.
    (
        policy number,
        place type,
        number of bedrooms
    )
    """
    base_path = os.path.abspath(os.path.dirname(__file__))
    fullpath = os.path.join(base_path, f'html_files/listing_{listing_id}.html')
    file = open(fullpath, 'r')
    f = file.read()
    file.close()

    # read_listing = 'listing_' + listing_id + '.html'
    # with open(read_listing) as f:
    #     contents = f.read()
    soup = BeautifulSoup(f, 'html.parser')
 
    policy_list = []
    type_list = []
    bedroom_list = []
    get_list = []


    policy_numbers = soup.find('ul', class_='fhhmddr dir dir-ltr')
    policy_numbers = policy_numbers.find_all('span')[0]
    for policy in policy_numbers: 
        policy_num = policy.text
        if 'pending' in policy_num.lower():
            policy_num = 'Pending'
        elif 'exempt' in policy_num.lower():
            policy_num = 'Exempt'



    type_place = soup.find('h2', class_ = '_14i3z6h')
    place1 = type_place.text
    words_list = place1.split()
    if words_list[0].lower() == "private":
        place_type = 'Private Room'
    elif words_list[0].lower() == 'shared':
        place_type = 'Shared Room'
    else:
        place_type = "Entire Room"

    bedroom = soup.find('ol', class_ = 'lgx66tx dir dir-ltr')
    bedroom = bedroom.find_all('span')[5]
    for bed in bedroom:
        bed_str = bed.text
        if bed_str.lower() == 'studio':
            bedroom_num = 1
        else:
            bed_str.split()
            bedroom_num = int(bed_str[0])
    
    tup = (policy_num, place_type, bedroom_num)
    return tup



def get_detailed_listing_database(html_file):
    """
    Write a function that calls the above two functions in order to return
    the complete listing information using the functions you???ve created.
    This function takes in a variable representing the location of the search results html file.
    The return value should be in this format:


    [
        (Listing Title 1,Cost 1,Listing ID 1,Policy Number 1,Place Type 1,Number of Bedrooms 1),
        (Listing Title 2,Cost 2,Listing ID 2,Policy Number 2,Place Type 2,Number of Bedrooms 2),
        ...
    ]
    """

    listing_database_list = []
    tup = ()
    listing_id_list = get_listings_from_search_results(html_file)

    for listing_id in listing_id_list:
        listing_info = get_listing_information(listing_id[2])
        tup = listing_id + listing_info
        listing_database_list.append(tup)

    return listing_database_list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_detailed_listing_database()), sorts the tuples in
    ascending order by cost, writes the data to a csv file, and saves it
    to the passed filename. The first row of the csv should contain
    "Listing Title", "Cost", "Listing ID", "Policy Number", "Place Type", "Number of Bedrooms",
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Listing Title,Cost,Listing ID,Policy Number,Place Type,Number of Bedrooms
    title1,cost1,id1,policy_number1,place_type1,num_bedrooms1
    title2,cost2,id2,policy_number2,place_type2,num_bedrooms2
    title3,cost3,id3,policy_number3,place_type3,num_bedrooms3
    ...

    In order of least cost to most cost.

    This function should not return anything.
    """
    with open(filename, 'w', newline = '') as f:
        f.write('Listing Title,Cost,Listing ID,Policy Number,Place Type,Number of Bedrooms\n')
        data_s = sorted(data, key=lambda x:x[1])
        writer = csv.writer(f)
        writer.writerows(data_s)

def check_policy_numbers(data):
    """
    Write a function that takes in a list of tuples called data, (i.e. the one that is returned by
    get_detailed_listing_database()), and parses through the policy number of each, validating the
    policy number matches the policy number format. Ignore any pending or exempt listings.
    Return the listing numbers with respective policy numbers that do not match the correct format.
        Policy numbers are a reference to the business license San Francisco requires to operate a
        short-term rental. These come in two forms, where # is a number from [0-9]:
            20##-00####STR
            STR-000####
    .
    Return value should look like this:
    [
        listing id 1,
        listing id 2,
        ...
    ]

    """
    id_list = []
    pattern = r'20[0-9]{2}-00[0-9]{4}STR|STR-000[0-9]{4}|Pending|License not needed per OSTR'
    for tup in data:
        found = re.findall(pattern, tup[3])
        if len(found) == 0:
            id_list.append(tup[2])
    
    return id_list


def extra_credit(listing_id):
    """
    There are few exceptions to the requirement of listers obtaining licenses
    before listing their property for short term leases. One specific exception
    is if the lister rents the room for less than 90 days of a year.

    Write a function that takes in a listing id, scrapes the 'reviews' page
    of the listing id for the months and years of each review (you can find two examples
    in the html_files folder), and counts the number of reviews the apartment had each year.
    If for any year, the number of reviews is greater than 90 (assuming very generously that
    every reviewer only stayed for one day), return False, indicating the lister has
    gone over their 90 day limit, else return True, indicating the lister has
    never gone over their limit.
    """
    base_path = os.path.abspath(os.path.dirname(__file__))
    fullpath = os.path.join(base_path, f'html_files/listing_{listing_id}_reviews.html')
    file = open(fullpath, 'r')
    f = file.read()
    file.close()

    soup = BeautifulSoup(f, 'html.parser')

    dates_dict = {}
    dates = soup.find_all('li', class_ = '_1f1oir5')
    for date in dates:
        date = date.text.split()
        dates_dict[date[1]] = dates_dict.get(date[1], 0) + 1
    for num in dates_dict.values():
        if num > 90:
            return False
        else:
            return True


class TestCases(unittest.TestCase):

    def test_get_listings_from_search_results(self):
        # call get_listings_from_search_results("html_files/mission_district_search_results.html")
        # and save to a local variable
        listings = get_listings_from_search_results("html_files/mission_district_search_results.html")
        # check that the number of listings extracted is correct (20 listings)
        self.assertEqual(len(listings), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(listings), list)
        # check that each item in the list is a tuple
        for listing in listings:
            self.assertEqual(type(listing), tuple)
        # check that the first title, cost, and listing id tuple is correct (open the search results html and find it)
        self.assertEqual(listings[0][0], 'Loft in Mission District')
        self.assertEqual(listings[0][1], 210)
        self.assertEqual(listings[0][2], '1944564')
        # check that the last title is correct (open the search results html and find it)
        self.assertEqual(listings[-1][0], 'Guest suite in Mission District')
        

    def test_get_listing_information(self):
        html_list = ["1623609",
                     "1944564",
                     "1550913",
                     "4616596",
                     "6600081",
                     ]
        # call get_listing_information for i in html_list:
        listing_informations = [get_listing_information(id) for id in html_list]
        # check that the number of listing information is correct (5)
        self.assertEqual(len(listing_informations), 5)
        for listing_information in listing_informations:
            # check that each item in the list is a tuple
            self.assertEqual(type(listing_information), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(listing_information), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(listing_information[0]), str)
            self.assertEqual(type(listing_information[1]), str)
            # check that the third element in the tuple is an int
            self.assertEqual(type(listing_information[2]), int)
        # check that the first listing in the html_list has policy number 'STR-0001541'
        self.assertEqual(listing_informations[0][0],'STR-0001541' )
        # check that the last listing in the html_list is a "Private Room"
        self.assertEqual(listing_informations[-1][1], 'Private Room')
        # check that the third listing has one bedroom
        self.assertEqual(listing_informations[2][2], 1)
        

    def test_get_detailed_listing_database(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save it to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # check that we have the right number of listings (20)
        self.assertEqual(len(detailed_database), 20)
        for item in detailed_database:
            # assert each item in the list of listings is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 6
            self.assertEqual(len(item), 6)

        # check that the first tuple is made up of the following:
        # 'Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1
        self.assertEqual(detailed_database[0], ('Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1))

        # check that the last tuple is made up of the following:
        # 'Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1
        self.assertEqual(detailed_database[-1], ('Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1))
        

    def test_write_csv(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call write csv on the variable you saved
        write_csv(detailed_database, "test.csv")
        # read in the csv that you wrote
        csv_lines = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for i in csv_reader:
                csv_lines.append(i)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Listing Title','Cost','Listing ID','Policy Number','Place Type','Number of Bedrooms'])
        # check that the next row is Private room in Mission District,82,51027324,Pending,Private Room,1
        self.assertEqual(csv_lines[1], ['Private room in Mission District', '82', '51027324', 'Pending', 'Private Room', '1'])
        # check that the last row is Apartment in Mission District,399,28668414,Pending,Entire Room,2
        self.assertEqual(csv_lines[-1], ['Apartment in Mission District','399','28668414','Pending','Entire Room','2'])
        

    def test_check_policy_numbers(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call check_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = check_policy_numbers(detailed_database)
        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)
        # check that there is exactly one element in the string
        self.assertEqual(len(invalid_listings), 1)
        # check that the element in the list is a string
        self.assertEqual(type(invalid_listings[0]), str)
        # check that the first element in the list is '16204265'
        self.assertEqual(invalid_listings[0], '16204265')


if __name__ == '__main__':
    database = get_detailed_listing_database("html_files/mission_district_search_results.html")
    write_csv(database, "airbnb_dataset.csv")
    check_policy_numbers(database)
    unittest.main(verbosity=2)


'''
One very effective way of showing users that an Airbnb is properly validated, would be to allow users to see the documents proving the Airbnb???s 
business license is valid. To do so, there should be some sort of system that allows you to have access to the business name, tax number, business 
address, license number, and business activity. Once you have access to all this information, you would be able to verify one???s business license. 
This system is similar to this project because we were able to take data from part of a website and then utilize that public information in our desired 
way. While this seems logical and would ensure to users that the short term rental they are staying at is safe and successfully validated, there are many 
cons to this idea. For example, businesses and short term rental owners may be uncomfortable with the fact that third party companies will have access 
to their personal information. Another complaint that would make people against adopting this system would be that it is too time-consuming. Many people 
may say that users will lose interest in figuring out whether the short term rental???s business license is valid or not because it requires a lot of 
information and time. 

One question I could explore would be, does the cost of housing (specifically Airbnbs) relate positively or negatively to the average income for 
Americans in the United States? Another question this data could help me explore could be, how does the level of safety for housing locations relate 
to housing cost? The answer to these questions could tell potential buyers and renters that there is a lack of or substantial amount of housing security. 
As a data scientist working with a housing activist organization to fight against housing security, if the answers to these questions reflect poorly 
against housing security it would help our organization build a case.  		 	 	 		
			
I think one important factor to consider is constitutional rights, specifically the First Amendment right to free speech. If you are discussing the 
legality of web scraping in relation to terms of service violations, people's rights still need to remain protected. Preventing someone from violating 
the terms of service in order to access data or share information should not violate their individual rights. It is also important to consider what is 
categorized as an infringement on personal property and whether or not a computer system is considered public or personal. This is important because the 
legality of web scraping and data accessing can differ based on whether the system is considered to be personal property. 

This situation reminds me of the Microsoft versus Google situation. There is a really fine line between deciding what is too much information versus what 
is the appropriate amount of information. Some guidelines should be enforced to help reduce this uncomfortableness. For example, we need to make sure that
 we are looking at the impact levels of all the information that is being processed. One guideline that we should consider is what would be the adverse effect 
 on the individual or business? If the answer to that question is, catastrophic effects then that should tell us we should not be putting this information out 
 to the public. Another guideline that we should consider is whether the information is a breach of privacy or a contract/regulation. If the data that we are 
 currently assessing breaches any sort of agreements that could result in legal issues, then that should determine that we should not be using this data publicly. 
			
		

'''