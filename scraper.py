# VitolizeÂ® for Men
# VitolizeÂ® for Men
# Forever ImmuBlend®
# Vitâ™€lizeÂ® For Women
# Vitâ™€lizeÂ® For Women


from scrapy.selector import Selector
import csv
import time
import datetime
import sys
import os
import re


from selenium import webdriver
# =============================================================================
# from selenium.webdriver import ActionChains
# =============================================================================

from selenium.webdriver.common.keys import Keys
from shutil import which
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.action_chains import ActionChains

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# process = Popen('cmd /K "C: & cd C:\Program Files\Google\Chrome\Application & chrome.exe --remote-debugging-port=8980 --user-data-dir="C:/Users/drkap/Desktop/amazon_affiliate/visa_profile""',shell=True)
# time.sleep(10)

# process = Popen('cmd /K "C: & cd C:\Program Files\Google\Chrome\Application & chrome.exe --remote-debugging-port=8983 --user-data-dir="D:/cpt/visa_profile/amazon_profile""',shell=True)

# # input('click to go next')
# ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
# time.sleep(3)


# if links are already collected and you dont want to recollect comment this section then
links = [
    # =============================================================================
    'https://shopnow.foreverliving.com/usa/en-us/best-sellers',
    'https://shopnow.foreverliving.com/can/en-ca/best-sellers',
    'https://shopnow.foreverliving.com/aus/en-au/best-sellers',
    'https://shopnow.foreverliving.com/gbr/en-gb/best-sellers',
    # 'https://shopnow.foreverliving.com/can/fr-ca/best-sellers',
    # 'https://shopnow.foreverliving.com/usa/es-us/best-sellers',


]
with open('forever_links1.csv', 'w') as fw:
    write = csv.writer(fw)
    fw.close()
filename = datetime.datetime.now().strftime('%d')

date_started = datetime.datetime.now().strftime('%d')

chrome_path = which("chromedriver")
co = Options()
co.add_argument("--start-maximized")
# ChromeOptions options = new ChromeOptions();
# co.DebuggerAddress = "127.0.0.1:9222"
# co.add_argument("no-sandbox")
# co.add_argument("user-data-dir=D:\cpt\walmart_profile1")
# --user-data-dir=
# co.add_argument("user-data-dir=C:\environments\selenium")
# co.add_experimental_option("debuggerAddress","localhost:8983")
driver = webdriver.Chrome(executable_path=chrome_path, options=co)

for link in links:
    driver.get(link)
    driver.implicitly_wait(5)
    time.sleep(5)
    try:

        driver.find_element_by_xpath(
            '//button[@data-cookiefirst-action="reject"]').click()
        time.sleep(2)
    except:
        pass
# =============================================================================
#     try:
#
#         driver.find_element_by_xpath('//button[@class="header-logo-container btn-aria"]').click()
#         time.sleep(4)
#     except:pass
#     driver.execute_script("document.body.style.zoom='50%'")
# =============================================================================

    if '/en-us/' in link:
        link_country = 'en_us'

    elif '/es-us/' in link:
        link_country = 'es_us'
    elif '/en-ca/' in link:
        link_country = 'en_ca'
    elif '/fr-ca/' in link:
        link_country = 'fr_ca'
    elif '/en-gb/' in link:
        link_country = 'en_gb'
    elif '/en-au/' in link:
        link_country = 'en_au'
    else:
        link_country = ""

    category_links = driver.find_elements_by_xpath(
        '//ul[@id="categoriesMenu-js"]/li/button')
    response = Selector(text=driver.page_source)
    all_categories = response.xpath(
        '//ul[@id="categoriesMenu-js"]/li/button/span/text()').getall()
    for i, category in enumerate(category_links):
        try:
            actions = ActionChains(driver)
            actions.move_to_element(category).perform()
            time.sleep(3)
            try:
                category.click()
            except:
                time.sleep(3)
                try:
                    actions.move_to_element(category).perform()
                    time.sleep(3)
                    category.click()
                except:
                    try:
                        category.click()
                    except:
                        driver.refresh()
                        driver.implicitly_wait(5)
                        time.sleep(6)
                        actions.move_to_element(category).perform()
                        time.sleep(3)
                        category.click()
        except:
            try:
                actions = ActionChains(driver)
                cat_name = all_categories[i]
                em_to_move = driver.find_element_by_xpath(
                    '//ul[@id="categoriesMenu-js"]/li/button/span[normalize-space()="'+str(cat_name)+'"]')
                actions.move_to_element(em_to_move).perform()
                time.sleep(3)
                em_to_move.click()
#                                                      #[contains(.="'+str(cat_name)+'")]')
            except:
                actions = ActionChains(driver)
                em_to_move = driver.find_element_by_xpath(
                    '//ul[@id="categoriesMenu-js"]/li/button["'+str(i)+'"]')
                actions.move_to_element(em_to_move).perform()
                time.sleep(3)
                em_to_move.click()

        time.sleep(7)
        response_cat = Selector(text=driver.page_source)

        cat_link = driver.current_url

        category_name = driver.find_element_by_xpath(
            '//ul[@id="categoriesMenu-js"]/li/button[@class="btn-aria active-category" or @class="btn-aria active-category ipad-active"]/span').text
        country_name = driver.find_element_by_xpath(
            '//button[@id="country-language-js"]/span[@class="header-country d-none d-md-inline ng-tns-c55-1"]').text
        country_lang = driver.find_element_by_xpath(
            '//button[@id="country-language-js"]/span[@class="header-country pl-2 ng-tns-c55-1"]').text
        for i in range(5):
            # driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(5)
        products_links = driver.find_elements_by_xpath(
            '//a[@class="product__image-container"]')
        for product in products_links:
            product_a = product.get_attribute('href')
            print('link is ', product_a)

            if link_country == 'en_us':
                aff_link = product_a+'?store=US&distribID=200002416566&language=en'
            elif link_country == 'es_us':
                aff_link = product_a+'?store=US&distribID=200002416566&language=es'

            elif link_country == 'en_ca':
                aff_link = product_a+'?store=CAN&distribID=200002416566&language=en'

            elif link_country == 'fr_ca':
                aff_link = product_a+'?store=CAN&distribID=200002416566&language=fr'

            elif link_country == 'en_gb':
                aff_link = product_a+'?store=GBR&distribID=200002416566&language=en'

            elif link_country == 'en_au':
                aff_link = product_a+'?store=AUS&distribID=200002416566&language=en'

            try:
                with open('forever_links1.csv', '+a', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(
                        [category_name, product_a, link_country, aff_link])
            except:
                with open('forever_links1.csv', '+a', newline='', encoding='utf-8') as f:
                    write = csv.writer(f)
                    write.writerow(
                        [category_name, product_a, link_country, aff_link])

        cat_description = response_cat.xpath(
            '//div[@class="col-12 col-md category-banner__description ng-star-inserted"]/p/text()').getall()
        category_complete_desc = ''
        for cat in cat_description:
            category_complete_desc += cat
        cat_img = response_cat.xpath(
            '(//source[@class="desktop-banner"])[5]/@srcset').get()
        category_name = response_cat.xpath(
            '//h1[@class="category-banner__name col-12 col-md-auto d-flex flex-column justify-content-center text-md-right mb-3 mb-md-0 ng-star-inserted"]/text()').get()
        try:
            category_name = category_name.strip()
        except:
            pass
        try:
            with open('forever_category_data.csv', '+a', newline='') as fw:
                write = csv.writer(fw)
                write.writerow([link, cat_link, category_name,
                               category_complete_desc, cat_img])
        except:
            with open('forever_category_data.csv', '+a', newline='', encoding='utf-8') as fw:
                write = csv.writer(fw)
                write.writerow([link, cat_link, category_name,
                               category_complete_desc, cat_img])

            # try:
            #     with open('forever_links_{0}_{1}.csv'.format(country_name,country_lang),'+a',newline='') as f:
            #         write=csv.writer(f)
            #         write.writerow([category_name,product_a])
            # except:
            #     with open('forever_links_{0}_{1}.csv'.format(country_name,country_lang),'+a',newline='',encoding='utf-8') as f:
            #         write=csv.writer(f)
            #         write.writerow([category_name,product_a])


try:
    driver.close()
    time.sleep(3)
except:
    pass


# link collection portion end


# process = Popen('cmd /K "C: & cd C:\Program Files\Google\Chrome\Application & chrome.exe --remote-debugging-port=8989 --user-data-dir="D:/cpt/amazon_affiliate/foreever_profile""',shell=True)

out_of_stock_products = True
chrome_path = which("chromedriver")
co = Options()
co.add_argument("--start-maximized")
# ChromeOptions options = new ChromeOptions();
# co.DebuggerAddress = "127.0.0.1:9222"
# co.add_argument("no-sandbox")
# co.add_argument("user-data-dir=D:\cpt\walmart_profile1")
# --user-data-dir=
# co.add_argument("user-data-dir=C:\environments\selenium")
# co.add_experimental_option("debuggerAddress","localhost:8989")
driver = webdriver.Chrome(executable_path=chrome_path, options=co)


#x=input('add extension and hit enter')

all_products_done = []
countries_done = []
files_written = []
previous_link_country = ""
on_start = 0
with open('forever_links1.csv', 'r') as fr:
    reader = csv.reader(fr)
    for row in reader:
        category = row[0]
        link = row[1]

        link_country = row[2]
        # if you dont want to collect products for specific country ,uncomment the below code and change en_us/es_us with country code
        # if link_country=='en_us' or link_country=='es_us':
        #     continue

        if on_start == 0:
            countries_done.append(link_country)
            on_start = 1

        if link_country in countries_done:
            pass
        else:
            all_products_done = []
            countries_done.append(link_country)

        # if previous_link_country=="":
        #    previous_link_country=link_country
        # else:

        # if link_country=='en_gb':
        #     pass
        # else:continue
        if link_country == 'en_us' or link_country == 'es_us':
            country = 'United States,US,USA'
            country_cat = 'usa_categories'

        elif link_country == 'en_ca' or link_country == 'fr_ca':
            country = 'Canada,CAN,CN'
            country_cat = 'canada_categories'

        elif link_country == 'en_gb':
            country = 'United Kinddom,UK,GBR, GB'
            country_cat = 'uk_categories'
        elif link_country == 'en_au':
            country = 'Australia,AUS'
            country_cat = 'austraila_categories'

        aff_link = row[3]
        driver.get(link)
        driver.implicitly_wait(7)
        time.sleep(6)
        try:

            driver.find_element_by_xpath(
                '//button[@data-cookiefirst-action="reject"]').click()
            time.sleep(2)
        except:
            pass

        suggest = ['Original URL', 'post_title', 'SKU', 'short_description', 'Price', 'quantities', country_cat, 'Description', 'Usage',
                   'Image', 'affiliate_link', 'total_reviews', 'review_stars', 'Ingredients', 'Tags', 'youtube_video_link', 'Out Of Stock']

        file_name_done = 'forever_products_{0}'.format(link_country)
        if file_name_done in files_written:
            pass
        else:
            with open('forever_products_{0}.csv'.format(link_country), 'w') as fw:

                write = csv.writer(fw)
                fw.close()
                time.sleep(2)
            try:
                with open('forever_products_{0}.csv'.format(link_country), '+a', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(suggest)
            except:
                with open('forever_products_{0}.csv'.format(link_country), '+a', newline='', encoding='utf-8') as f:
                    write = csv.writer(f)
                    write.writerow(suggest)

            # suggest=[link,main_name1,item_no,short_desc,price,quantity,"All Products",complete_description_c,img,video_src,aff_link,total_rating,avg_rating,ingredients,complete_tag]
            suggest = ['Original URL', 'post_title', 'SKU', 'short_description', 'Price', 'quantities', country_cat, 'Description',
                       'Image', 'affiliate_link', 'total_reviews', 'review_stars', 'Ingredients', 'Tags', 'youtube_video_link', 'Out Of Stock']
            with open('forever_products_{0}_1.csv'.format(link_country), 'w') as fw:

                write = csv.writer(fw)
                fw.close()
                time.sleep(2)
            try:
                with open('forever_products_{0}_1.csv'.format(link_country), '+a', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(suggest)
            except:
                with open('forever_products_{0}_1.csv'.format(link_country), '+a', newline='', encoding='utf-8') as f:
                    write = csv.writer(f)
                    write.writerow(suggest)

            files_written.append(file_name_done)

        def collect_data():
            try:
                out_of_stock_check = driver.find_element_by_xpath(
                    "//a[contains(text(),' Out of Stock ') or @class='btn btn-secondary d-block d-sm-inline-block disable-span']")
                out_of_stock = 'Y'
            except:
                out_of_stock = 'N'

            if out_of_stock_products == False and out_of_stock == 'Y':
                return

            else:
                pass
            url_check = driver.current_url
            url_check1 = url_check.split('/')[-1]

            try:
                name = driver.find_element_by_xpath(
                    '//h1[@class="product-title mb-1"]').text
                main_name = driver.find_element_by_xpath(
                    '//h1[@class="product-title mb-1"]').text
                main_name1 = driver.find_element_by_xpath(
                    '//h1[@class="product-title mb-1"]').text
                try:
                    main_name1 = main_name1.replace("™", '')
                except:
                    pass
                if '375-Vitolize-For-Women' in url_check1:
                    main_name1 = "Vitolize® for Women"
                    name = main_name1
                    main_name = main_name1
                if '374-Vitolize-For-Men' in url_check1:
                    main_name1 = "Vitolize® for Men"
                    name = main_name1
                    main_name = main_name1

                # try:
                #     driver.find_element_by_xpath("//h1[contains(text(),'Vit♂lize® for Men')]")
                #     main_name1="Vitolize® for Men"
                #     name=main_name1
                #     main_name=main_name1

                # except:
                #     try:
                #         driver.find_element_by_xpath("//h1[contains(text(),'Vit♂lize® for Women')]")
                #         main_name1="Vitolize® for Women"
                #         name=main_name1
                #         main_name=main_name1
                #         pass
                #     except:
                #         pass
            except:
                # continue
                return
            short_desc = driver.find_element_by_xpath(
                '//div[@id="product-detail-description"]').text
            try:
                short_desc = short_desc.replace('Description du produit', '')
            except:
                pass

            try:
                short_desc = short_desc.replace('Product description', '')
            except:
                pass

            try:
                short_desc = short_desc.replace('Descripción del producto', '')
            except:
                pass

            try:
                short_desc = short_desc.strip()
            except:
                pass

            item_no = driver.find_element_by_xpath(
                '//div[@class="item-number"]/span[2]').text
            try:
                item_no = 'Item# '+item_no
            except:
                pass

            price = driver.find_element_by_xpath(
                '//span[@class="price ng-star-inserted"]').text
            try:
                quantity = driver.find_element_by_xpath(
                    '//span[@class="item-quantity"]/p').text
            except:
                quantity = ""
            try:
                usage = driver.find_element_by_xpath(
                    '//div[@id="ProductUsage"]//div[@class="desc-container"]').text
            except:
                usage = ""
            description = driver.find_elements_by_xpath(
                "//h2[contains(text(),'Description')]/following-sibling::div/p")
            if description:

                complete_description = ""
                for d in description:
                    desc = d.text
                    complete_description += desc
            else:
                description = driver.find_elements_by_xpath(
                    '//div[@id="product-detail-long-descption"]/p')
                complete_description = ""
                for d in description:
                    desc = d.text
                    complete_description += desc

            try:
                img = driver.find_element_by_xpath(
                    '//img[@class="img--main--responsive img--main ng-star-inserted"]').get_attribute('src')
            except:
                img = ""

            # try:
            #     video_src=driver.find_element_by_xpath('//iframe[@allowfullscreen or @crossorigin]').get_attribute('src')
            # except:
            #     video_src=""
            try:
                em = driver.find_element_by_xpath(
                    '//em[@class="video-icon fa fa-play-circle"]')
                actions = ActionChains(driver)
                actions.move_to_element(em)
                time.sleep(3)
                driver.find_element_by_xpath(
                    '//em[@class="video-icon fa fa-play-circle"]').click()
                # /ancestor::div[@class="swiper-slide text-center pointer ng-star-inserted swiper-slide-next"]

                # em.click()
                # except:
                #     print('not clickable')

                time.sleep(3)
                driver.find_element_by_xpath(
                    '//div[@class="swiper-slide text-center ng-star-inserted swiper-slide-active"]//img[@alt="Play Icon" and @class="video-icon"]').click()
                time.sleep(5)
                try:
                    video_src = driver.find_element_by_xpath(
                        '//iframe[@allowfullscreen or @crossorigin]').get_attribute('src')
                except:
                    video_src = ""
                print('this is video link', video_src)
                time.sleep(2)
                driver.find_element_by_xpath(
                    '//button[@id="dismissModal"  and @aria-label="common.Close"]').click()
                time.sleep(2)
            # aff_link=link+'?store=US&distribID=200002416566&language=en'

            except:
                video_src = ""
            # aff_link=link+'?store=US&distribID=200002416566&language=en'

            try:
                total_rating = driver.find_element_by_xpath(
                    '//div[@class="reviews review-count d-none d-sm-block"]/a').text
                # total_rating=total_rating.split(')')[0].replace('(')
            except:
                total_rating = ""
            try:
                avg_rating = driver.find_element_by_xpath(
                    '//div[@id="averageRating"]/span').text
            except:
                avg_rating = ""

            try:
                ingredients = driver.find_element_by_xpath(
                    "//div[@class='additional-content']").text
            except:
                ingredients = "Product ingredients detail is not available"

            category1 = category.replace(' ', '')

            tag_ = name.replace(' ', "")
            try:
                tag_ = tag_.strip()
            except:
                pass

            tag_ = tag_.replace("™", '').replace(
                '-', '').replace('*', '').replace('®', '')
            name = name.replace('Forever Aloe vera', 'Forever Aloe')
            tag_ = name.replace("™", '').replace(
                '-', '').replace('*', '').replace('®', '')
            name1 = tag_.replace(' ', '')

            main_name = main_name.replace("™", '').replace(
                '-', '').replace('*', '').replace('®', '')

            complete_combination = name1

            if 'Aloe' in main_name:
                name1 = main_name.replace('Aloe', 'Aloevera')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1
            if 'Forever' in main_name and 'Forever Aloe' not in main_name:
                name1 = main_name.replace('Forever', 'ForeverLiving')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

            if 'Forever Aloe' in main_name and 'Forever Aloe vera' not in main_name:
                name1 = main_name.replace('Forever Aloe', 'ForeverLiving Aloe')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

                name1 = main_name.replace(
                    'Forever Aloe', 'ForeverLiving Aloevera')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

                name1 = main_name.replace('Forever Aloe', 'Aloevera')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

                name1 = main_name.replace('Forever Aloe', 'Aloe')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

                name1 = main_name.replace('Forever Aloe', 'ForeverLiving')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

                name1 = main_name.replace('Forever Aloe', 'Forever')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

            if 'Forever Aloe vera' in main_name:
                name = main_name.replace('Forever Aloe vera', 'Forever Aloe')
                name1 = name.replace('Forever Aloe', 'ForeverLiving Aloe')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

                name1 = main_name.replace(
                    'Forever Aloe', 'ForeverLiving Aloevera')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

                name1 = main_name.replace('Forever Aloe', 'Aloevera')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

                name1 = main_name.replace('Forever Aloe', 'Aloe')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

                name1 = main_name.replace('Forever Aloe', 'ForeverLiving')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

                name1 = main_name.replace('Forever Aloe', 'Forever')
                name1 = name1.replace(' ', '')
                complete_combination += ','+name1

            complete_tag = complete_combination+','+category1+',FLP'+','+country + \
                ',ForeverLivingProducts,BuyAloeProducts,BuyAloeProducts.com,AloeVera,AloeVeraProducts,Healthy,Health'

            all_description_c = complete_description.replace('\n', 'splitit.')

            a = re.sub('[^a-zA-Z0-9.?]', ' ', all_description_c)
            a = a.replace('  ', ' ').lstrip().rstrip()
            a = a.split('splitit.')
            complete_description_c = ""
            for desc in a:
                try:
                    desc = desc.strip()
                except:
                    desc = desc
                complete_description_c += desc+'\n\n'
            #print(complete_description_short)#

            a_link = driver.current_url
            slug = a_link.split('/')[-1]
            print('Slug is ', slug)

            suggest = [link, main_name1, item_no, short_desc, price, quantity, category, complete_description_c,
                       usage, img, aff_link, total_rating, avg_rating, ingredients, complete_tag, video_src, out_of_stock]
            print(suggest)
            try:
                with open('forever_products_{0}.csv'.format(link_country), '+a', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(suggest)
            except:
                with open('forever_products_{0}.csv'.format(link_country), '+a', newline='', encoding='utf-8') as f:
                    write = csv.writer(f)
                    write.writerow(suggest)

            # all products entry
            if slug in all_products_done:
                print('Slug exist in ', all_products_done)
                pass
            else:

                suggest = [link, main_name1, item_no, short_desc, price, quantity, "All Products", complete_description_c,
                           usage, img, aff_link, total_rating, avg_rating, ingredients, complete_tag, video_src, out_of_stock]
                print(suggest)
                try:
                    with open('forever_products_{0}.csv'.format(link_country), '+a', newline='') as f:
                        write = csv.writer(f)
                        write.writerow(suggest)
                except:
                    with open('forever_products_{0}.csv'.format(link_country), '+a', newline='', encoding='utf-8') as f:
                        write = csv.writer(f)
                        write.writerow(suggest)

            if usage:
                complete_description_c = complete_description+'<h1>'+usage+'</h1>'
            suggest = [link, main_name1, item_no, short_desc, price, quantity, category, complete_description_c,
                       img, aff_link, total_rating, avg_rating, ingredients, complete_tag, video_src, out_of_stock]
            print(suggest)
            try:
                with open('forever_products_{0}_1.csv'.format(link_country), '+a', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(suggest)
            except:
                with open('forever_products_{0}_1.csv'.format(link_country), '+a', newline='', encoding='utf-8') as f:
                    write = csv.writer(f)
                    write.writerow(suggest)

            if slug in all_products_done:
                print('Slug exist in ', all_products_done)
                pass
            else:
                suggest = [link, main_name1, item_no, short_desc, price, quantity, "All Products", complete_description_c,
                           img, aff_link, total_rating, avg_rating, ingredients, complete_tag, video_src, out_of_stock]
                print(suggest)
                try:
                    with open('forever_products_{0}_1.csv'.format(link_country), '+a', newline='') as f:
                        write = csv.writer(f)
                        write.writerow(suggest)
                except:
                    with open('forever_products_{0}_1.csv'.format(link_country), '+a', newline='', encoding='utf-8') as f:
                        write = csv.writer(f)
                        write.writerow(suggest)

            all_products_done.append(slug)

        try:
            print('here')
            varition_checks = driver.find_elements_by_xpath(
                '//div[@class="variations m-0 ng-star-inserted"]/div/div//input[@name="radio"]/parent::label[@role="radio"]')
            print('here again')
            if varition_checks:
                for variation in varition_checks:
                    variation.click()
                    time.sleep(4)
                    # try:
                    #
                    # except:pass
                    collect_data()
            else:
                print('calling function')
                collect_data()

        except:
            print('calling function')
            collect_data()
