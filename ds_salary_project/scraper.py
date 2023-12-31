import selenium
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    print(selenium.__version__)
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    # driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="

    # url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="
    # url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element_by_css_selector('[alt="Close"]').click()  # clicking to the X.
            # print(' x out worked')
        except NoSuchElementException:
            # print(' x out failed')
            pass

        # Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("react-job-listing")  # jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:
            time.sleep(.1)

            try:
                driver.find_element_by_css_selector('[alt="Close"]').click()  # clicking to the X.
                # print(' x out worked')
            except NoSuchElementException:
                # print(' x out failed')
                pass
            # print(job_button.text)
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            job_button.click()  # You might
            time.sleep(1)
            collected_successfully = False

            while not collected_successfully:
                try:

                    # Wait for the location element to be visible
                    # location_element = WebDriverWait(driver, 10).until(
                    #     EC.visibility_of_element_located((By.XPATH, './/div[@class="location"]'))
                    # )
                    # location = location_element.text
                    # location_element = driver.find_element_by_xpath('.//div[contains(@class, "job-title")]/following-sibling::div[@class="location"]')
                    location = job_button.find_element_by_css_selector('.location').text
                    # location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_title = job_button.find_element_by_css_selector('.job-title').text
                    # company_name = driver.find_element_by_css_selector('.ml-xsm').text
                    company_name = job_button.find_element_by_xpath('.//div[starts-with(@class, "ml-xsm")]').text
                    # company_name = driver.find_element_by_xpath('.//div[starts-with(@class, "ml-xsm") and contains(@class, "job-search-")]').text
                    # job_description = driver.find_element_by_css_selector('.jobDescriptionContent desc').text
                    # job_description = job_button.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    # job_description = job_button.find_element_by_xpath('.//div[contains(@class, "jobDescriptionContent") and contains(@class, "desc")]').text
                    # job_description = job_button.find_element_by_css_selector('.jobDescriptionContent').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text

                    # print(job_description)
                    collected_successfully = True
                    # print(location)
                except Exception as e:
                    print("Failed:", e)
                    traceback.print_exc()
                    time.sleep(5)

            try:
                # salary_estimate = driver.find_element_by_xpath('.//span[@class="gray salary"]').text
                salary_estimate = job_button.find_element_by_css_selector('.salary-estimate').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                # rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
                # rating = job_button.find_element_by_xpath('.//span[@class="job-search-rnnx2x"]').text
                # rating = job_button.find_element_by_xpath('.//span[@class="css-rnnx2x"]').text
                rating = job_button.find_element_by_xpath(".//span[contains(@class, 'job-search-rnnx2x') or contains(@class, 'css-rnnx2x')]").text
                # print(rating)
                # css-rnnx2x
                # rating = job_button.find_element_by_xpath('.//*[@id = "MainCol"]/div[1]/ul/li[2]/div/div/a/div[1]/div[1]/div[2]/span[2]').text
                # // *[ @ id = "MainCol"] / div[1] / ul / li[2] / div / div / a / div[1] / div[1] / div[2] / span[2]
            #     job-search-rnnx2x
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
                # Printing for debugging
            if verbose:
                    print("Job Title: {}".format(job_title))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Job Description: {}".format(job_description[:500]))
                    print("Rating: {}".format(rating))
                    print("Company Name: {}".format(company_name))
                    print("Location: {}".format(location))

                # Going to the Company tab...
                # clicking on this:
                # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                # job_button.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()
                # driver.find_element_by_xpath('.//div[@class="css-t3xrds e856ufb4"]').click()
                # print("bbb")
                # job_button.find_element_by_css_selector('.css-t3xrds').click()
                # job_button.find_element_by_css_selector('.//div[contains(@class, "css-t3xrds")]').click()
                job_button.find_element_by_css_selector('.SVGInline-svg').click()
                time.sleep(3)
                # print("aaaa")
                # css-t3xrds e856ufb4
                try:
                    # <div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    # </div>
                    headquarters = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    # size = driver.find_element_by_xpath(
                    #     './/div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                    # size = driver.find_element_by_xpath('.//div[@class="css-1taruhi"]//label[text()="Size"]//following-sibling::*').text
                    # size=driver.find_element_by_xpath('//span[contains(text(), "Size")]/following-sibling::span[1]').text
                    size = driver.find_element_by_xpath('//div[@id="EmpBasicInfo"]//div[contains(span[@class="css-1taruhi e1pvx6aw1"], "Size")]/span[@class="css-i9gxme e1pvx6aw2"]').text
                    # print(size)
                except NoSuchElementException:
                    size = -1

                try:
                    # founded = driver.find_element_by_xpath(
                    #     './/div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                    founded = driver.find_element_by_xpath('//div[@id="EmpBasicInfo"]//div[contains(span[@class="css-1taruhi e1pvx6aw1"], "Founded")]/span[@class="css-i9gxme e1pvx6aw2"]').text
                except NoSuchElementException:
                    founded = -1

                try:
                    # type_of_ownership = driver.find_element_by_xpath(
                    #     './/div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                    type_of_ownership = driver.find_element_by_xpath('//div[@id="EmpBasicInfo"]//div[contains(span[@class="css-1taruhi e1pvx6aw1"], "Type")]/span[@class="css-i9gxme e1pvx6aw2"]').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    # industry = driver.find_element_by_xpath(
                    #     './/div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                    industry = driver.find_element_by_xpath('//div[@id="EmpBasicInfo"]//div[contains(span[@class="css-1taruhi e1pvx6aw1"], "Industry")]/span[@class="css-i9gxme e1pvx6aw2"]').text
                except NoSuchElementException:
                    industry = -1

                try:
                    # sector = driver.find_element_by_xpath(
                    #     './/div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                    sector = driver.find_element_by_xpath('//div[@id="EmpBasicInfo"]//div[contains(span[@class="css-1taruhi e1pvx6aw1"], "Sector")]/span[@class="css-i9gxme e1pvx6aw2"]').text
                except NoSuchElementException:
                    sector = -1

                try:
                    # revenue = driver.find_element_by_xpath(
                    #     './/div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                    revenue = driver.find_element_by_xpath('//div[@id="EmpBasicInfo"]//div[contains(span[@class="css-1taruhi e1pvx6aw1"], "Revenue")]/span[@class="css-i9gxme e1pvx6aw2"]').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    # competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                    competitors = driver.find_element_by_xpath('//div[@id="EmpBasicInfo"]//div[contains(span[@class="css-1taruhi e1pvx6aw1"], "Competitors")]/span[@class="css-i9gxme e1pvx6aw2"]').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                print("No such element")
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Headquarters": headquarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "Competitors": competitors})
            # add job to jobs

            # Clicking on the "next page" button
        try:
                # driver.find_element_by_xpath('.//li[@class="next"]//a').click()
                # print("Next")
                try:
                    driver.find_element_by_css_selector('[alt="Close"]').click()  # clicking to the X.
                    # print(' x out worked')
                except NoSuchElementException:
                    # print(' x out failed')
                    pass
                # driver.find_element_by_xpath('.//button[@class="nextButton"]').click()
                # time.sleep(.1)
                # driver.find_element_by_css_selector('.navIcon-svg').click()
                driver.find_element_by_xpath('.//*[@id = "MainCol"]/div[2]/div/div[1]/button[7]').click()
                # driver.find_element_by_xpath('.//svg[@class="SVGInline-svg navIcon-svg job-search-vuulpw-svg e13qs2070-svg"]').click()

        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                         len(jobs)))
            break
    print(jobs)
    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.