from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import json


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('lang=en')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver


driver = set_chrome_driver()

# driver = webdriver.Chrome('./chromedriver')

links = ["https://www.amazon.com/s?k=CJ&crid=3KMLLRL4GZ5VC&sprefix=c%2Caps%2C285&ref=nb_sb_noss_2",
         "https://www.amazon.com/s?k=CJ&page=2&crid=3G7D2OX9OTPSK&qid=1677542356&sprefix=c%2Caps%2C472&ref=sr_pg_2",
         "https://www.amazon.com/s?k=CJ&page=3&crid=3G7D2OX9OTPSK&qid=1677550545&sprefix=c%2Caps%2C472&ref=sr_pg_3",
         "https://www.amazon.com/s?k=CJ&page=4&crid=3G7D2OX9OTPSK&qid=1677550547&sprefix=c%2Caps%2C472&ref=sr_pg_4",
         "https://www.amazon.com/s?k=CJ&page=5&crid=3G7D2OX9OTPSK&qid=1677550653&sprefix=c%2Caps%2C472&ref=sr_pg_5",
         "https://www.amazon.com/s?k=CJ&page=6&crid=3G7D2OX9OTPSK&qid=1677550669&sprefix=c%2Caps%2C472&ref=sr_pg_6",
         "https://www.amazon.com/s?k=CJ&page=7&crid=3G7D2OX9OTPSK&qid=1677550684&sprefix=c%2Caps%2C472&ref=sr_pg_7",
         "https://www.amazon.com/s?k=cj+foods&crid=14BQ3WO6G2JA5&sprefix=cj+food%2Caps%2C260&ref=nb_sb_noss_1",
         "https://www.amazon.com/s?k=bibigo&crid=7R9PY4WQBV4I&sprefix=bibi%2Caps%2C255&ref=nb_sb_noss_1",
         "https://www.amazon.com/s?k=Bibigo&page=2&crid=1526QVGP3FKNM&qid=1677550738&sprefix=bibigo%2Caps%2C269&ref=sr_pg_2",
         "https://www.amazon.com/s?k=Bibigo&page=3&crid=1526QVGP3FKNM&qid=1677550741&sprefix=bibigo%2Caps%2C269&ref=sr_pg_3",
         "https://www.amazon.com/s?k=햇반&crid=21KIY9I0J5W1D&sprefix=햇바%2Caps%2C262&ref=nb_sb_noss_1",
         "https://www.amazon.com/s?k=다시다&crid=VXNCHJ2UGWSF&sprefix=다싣%2Caps%2C252&ref=nb_sb_noss",
         "https://www.amazon.com/s?k=해찬들&crid=2VCBJY86P3PNX&sprefix=해찬%2Caps%2C257&ref=nb_sb_noss_1",
         "https://www.amazon.com/s?k=cheiljedang&crid=AIY0GVG65ZID&sprefix=cheiljeda%2Caps%2C399&ref=nb_sb_noss_2",
         "https://www.amazon.com/s?k=cheiljedang&page=2&crid=AIY0GVG65ZID&qid=1678781859&sprefix=cheiljeda%2Caps%2C399&ref=sr_pg_2"]

brands = ['CJ', 'CJ Foods', 'Bibigo', 'Yasik', 'Haechandle', 'cj', 'bibigo', 'yasik', 'haechandle', 'Bulk',
          'Cheiljedang', 'cheiljedang']


def get_info(url):
    matching_list = []
    driver.get(url)
    # Loop through each search result and extract the link of the matching products
    for result in driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]'):
        name = result.find_element(By.XPATH, './/h2/a/span').text
        name_list = name.lower().split()
        is_name_in_brands = False
        for name_ in name_list:
            if name_ in brands:
                is_name_in_brands = True
                break
        if is_name_in_brands:
            try:
                price_whole = result.find_element(By.CSS_SELECTOR, '.a-price-whole').text
                price_fraction = result.find_element(By.CSS_SELECTOR, '.a-price-fraction').text
                price = '$' + price_whole + '.' + price_fraction
            except:
                price = ""
            try:
                rating_element = result.find_element(By.CSS_SELECTOR, 'div.a-row.a-size-small span.a-icon-alt')
                rating = rating_element.get_attribute('innerHTML').split()[0]
            except:
                rating = ""

            link = result.find_element(By.XPATH, './/h2/a').get_attribute('href')
            product_dict = {"name": name, "price": price, "rating": rating, "link": link}
            matching_list.append(product_dict)
    return matching_list


def get_details():
    details_dict = {}
    time.sleep(2)
    driver.maximize_window()

    # ingredients, about this item
    try:
        expander_btns = driver.find_elements(By.XPATH, '//i[@class="a-icon a-icon-section-expand"]')
        for btn in expander_btns:
            btn.click()
    except:
        pass

    # diet type
    try:
        diet_type_list = []
        diet_type_tags = driver.find_elements(By.XPATH,
                                              '//span[@class="a-size-base a-color-base _cse-nutritional-info-and-ingredient-card_style_dilText__1iIqY"]')
        for tag in diet_type_tags:
            diet_type_list.append(tag.text)
    except:
        diet_type_list = "None"
    details_dict["diet_type"] = diet_type_list

    # ingredients
    try:
        ingredients = driver.find_element(By.XPATH, '//div[@id="nic-ingredients-content"]/span').text
    except:
        ingredients = "None"

    details_dict["ingredient"] = ingredients

    # features_see_more
    try:
        see_more_c1 = driver.find_element(By.XPATH, '//div[@id="productOverview_feature_div"]')
        see_more_c2 = see_more_c1.find_element(By.XPATH, '//div[@id="poExpander"]')
        see_more_c3 = see_more_c2.find_element(By.XPATH, '//div[@id="poToggleButton"]')
        see_more = see_more_c3.find_element(By.XPATH, '//span[text() = "See more"]')
        driver.execute_script("arguments[0].click();", see_more)
    except:
        pass

    time.sleep(2)

    # features
    try:
        feature_dict = {}
        feature_table = driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]')
        feature_tbody = feature_table.find_element(By.TAG_NAME, 'tbody')
        feature_trs = feature_tbody.find_elements(By.TAG_NAME, 'tr')
        for tr in feature_trs:
            feature_tds = tr.find_elements(By.TAG_NAME, 'td')
            for i in range(2):
                td = feature_tds[i]
                span = td.find_element(By.TAG_NAME, 'span').text
                if i == 0:
                    feature_type = span
                else:
                    feature_content = span
            feature_dict[feature_type] = feature_content
    except:
        feature_dict = "None"
    details_dict["product_details"] = feature_dict

    # About this Item

    try:
        ati_list = []
        try:
            ati_container = driver.find_element(By.XPATH, '//div[@id="featurebullets_feature_div"]')
            ati_inner_container = ati_container.find_element(By.XPATH, '//div[@id="feature-bullets"]')
        except:
            ati_inner_container = driver.find_element(By.XPATH, '//div[@id="feature-bullets"]')
        ati_ul = ati_inner_container.find_element(By.TAG_NAME, 'ul')
        ati_lis = ati_ul.find_elements(By.TAG_NAME, 'li')
        for li in ati_lis:
            span = li.find_element(By.TAG_NAME, 'span').text
            ati_list.append(span)
    except:
        ati_list = "None"

    details_dict["about_this_item"] = ati_list

    return details_dict


def get_reviews():
    reviews_dict = {}

    # driver.get(url)
    driver.execute_script('window.scrollTo(0,6000)')
    time.sleep(2)

    review_container = driver.find_element(By.XPATH, '//div[@id="reviewsMedley"]')

    try:
        total_ratings = review_container.find_element(By.XPATH, '//div[@data-hook="total-review-count"]/span').text
        # print(total_ratings)
    except:
        total_ratings = "None"

    reviews_dict["total_ratings"] = total_ratings

    if total_ratings != "None":

        # 1~5
        star_count = 5
        star_dict = {}
        customer_review_stars = review_container.find_elements(By.CSS_SELECTOR, '.a-histogram-row')
        for star in customer_review_stars:
            try:
                td = star.find_element(By.CSS_SELECTOR, '.a-text-right')
                percent = td.find_element(By.XPATH, './/a[@class="a-link-normal"]').text
                # print(percent)
            except:
                percent = "None"
            if star_count == 5:
                star_dict["5_star"] = percent
            elif star_count == 4:
                star_dict["4_star"] = percent
            elif star_count == 3:
                star_dict["3_star"] = percent
            elif star_count == 2:
                star_dict["2_star"] = percent
            else:
                star_dict["1_star"] = percent
            star_count = star_count - 1
        reviews_dict["rating_percent(1~5)"] = star_dict

        # By Feature
        try:
            features_container = review_container.find_element(By.XPATH,
                                                               './/div[@id="cr-summarization-attributes-list"]')
            try:
                see_more = features_container.find_element(By.XPATH, './/div[4]/a').click()
            except:
                pass
            features = features_container.find_elements(By.XPATH, './/div[@data-hook="cr-summarization-attribute"]')
        except:
            features = "None"
        # see_more_feature = features_container.find_element(By.XPATH, './/div[@data-hook="cr-summarization-attributes-see-more"]')
        # features.append(see_more_feature)

        if features != "None":
            feature_dict = {}
            for feature in features:
                feature_for = feature.find_element(By.XPATH, './/div[@class="a-row"]/span').text
                feature_rate = feature.find_element(By.CSS_SELECTOR, '.a-size-base.a-color-tertiary').text
                # print(feature_for, ":", feature_rate)
                feature_dict[feature_for] = feature_rate
            reviews_dict["by_feature"] = feature_dict
        else:
            # By features
            reviews_dict["by_feature"] = features

        # Read Reviews That Mention

        try:
            tag = review_container.find_element(By.XPATH, '//span[@data-cr-trigger-on-view]')
            lighthouse_terms = json.loads(tag.get_attribute('data-cr-trigger-on-view'))['ajaxParamsMap'][
                'lighthouseTerms']
            tag_list = lighthouse_terms.split('/')
            reviews_dict["read_reviews_that_mention"] = tag_list
        except:
            reviews_dict["read_reviews_that_mention"] = "None"

        # Top Reviews From the United States

        try:
            us_reviews = review_container.find_element(By.CSS_SELECTOR, '#cm-cr-dp-review-list')
            cards = us_reviews.find_elements(By.CSS_SELECTOR, '.a-section.review.aok-relative')
            sentence_review_list = []
            for card in cards:
                sentence_review_dict = {}
                star_rate = card.find_element(By.XPATH, './/a[@class="a-link-normal"]').get_attribute("title").split()[
                    0]
                sentence_review_dict["rating"] = star_rate

                sentence_title = card.find_element(By.XPATH, './/a[@data-hook="review-title"]/span').text
                sentence_review_dict["title"] = sentence_title

                sentence = card.find_element(By.XPATH, './/div[@data-hook="review-collapsed"]/span').text
                sentence_review_dict["content"] = sentence

                sentence_review_list.append(sentence_review_dict)
            reviews_dict["top_reviews_from_the_united_states"] = sentence_review_list
        except:
            reviews_dict["top_reviews_from_the_united_states"] = "None"

        # Top positive / critical review

        try:
            see_all_reviews_link = review_container.find_element(By.XPATH,
                                                                 './/a[@data-hook="see-all-reviews-link-foot"]').click()
            time.sleep(2)
            positive_container = driver.find_element(By.CSS_SELECTOR,
                                                     '.a-column.a-span6.view-point-review.positive-review')
            critical_container = driver.find_element(By.CSS_SELECTOR,
                                                     '.a-column.a-span6.view-point-review.critical-review')
            positive_review = positive_container.find_element(By.CSS_SELECTOR,
                                                              'div.a-row.a-spacing-top-mini > span').text
            critical_review = critical_container.find_element(By.CSS_SELECTOR,
                                                              'div.a-row.a-spacing-top-mini > span').text
            reviews_dict["top_positive_review"] = positive_review
            reviews_dict["top_critical_review"] = critical_review
        except:
            reviews_dict["top_positive_review"] = "None"
            reviews_dict["top_critical_review"] = "None"

    return reviews_dict


product_list_raw = []

for link in links:
    tmp_list = get_info(link)
    product_list_raw.append(tmp_list)

product_list_CJ = []
product_name_list = []
for i in range(len(links)):
    page = product_list_raw[i]
    for dictionary in page:
        url = dictionary['link']
        driver.get(url)
        try:
            brand = driver.find_element(By.XPATH, '//a[@id="bylineInfo"]')
            brand_name = brand.text
        except:
            brand_name = "none"

        brand_split = brand_name.split()

        if len(brand_split) >= 2:
            if brand_split[1] == "the":
                brand = brand_split[2]
            else:
                brand = brand_split[1]
        else:
            brand = brand_name

        if brand in brands:
            if dictionary["name"] not in product_name_list:
                product_name_list.append(dictionary["name"])
                detail_dict = get_details()
                review_dict = get_reviews()
                dictionary["details"] = detail_dict
                dictionary["review"] = review_dict
                product_list_CJ.append(dictionary)

# Quit the driver
driver.quit()

json_data = json.dumps(product_list_CJ, indent=6)

with open('CJ_Amazon.json', 'w') as file:
    file.write(json_data)