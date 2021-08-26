# Testing

## Table of Contents

1. [Code Validation](#code-validation)

    - [HTML](#html)

    - [CSS](#css)

    - [JS](#js)

    - [PEP8](#pep8)

2. [Lighthouse in Chrome DevTools](#lighthouse-in-chrome-devtools) 

3. [Browser compatibility and responsiveness](#browser-compatibility-and-responsiveness)

    - [Testing on Different Browsers](#testing-on-different-browsers)

    - [Testing on Different Devices](#testing-on-different-devices)

4. [Testing User Stories](#testing-user-stories)

5. [Manual testing](#manual-testing)

6. [Bugs and Fixes](#bugs-and-fixes)

-----

- ### Code Validation  

    - #### HTML 
    
        HTML checked was done with [The W3C Markup Validation Service](https://validator.w3.org/)
        
         - All Pages 
         
            ![](readme_file/html-validation.jpg)

        NOTE: All pages that didn't required login was test with direct url and those that required login the code was that from ```View Page Source```. 

    - #### CSS 
    
        CSS checked was done with [The W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)
    
        - CSS - base.css
        
            ![](readme_file/base-css-validation.jpg)

            - The warnings were for:

                The variables is an unknown vendor extension

                The value break-word is deprecated.

                Same color for background-color and border-color on:
                
                - btn-outline-white:focus

                - allauth inputs and buttons

                - custom-checkbox for images on edit products page

                And the rest for unknown vendor extension

                NOTE: Due to a [bug in W3C CSS Validator]( https://github.com/w3c/css-validator/issues/305) the variables has been replace from inside calc() function as was given 4 errors in the base.css validations

        - CSS - profile.css

            ![](readme_file/profile-css-validation.jpg)

            - The warnings were for:

                All for Unknown vendor extension

        - CSS - checkout.css

            ![](readme_file/checkout-css-validation.jpg)

            - The warnings were for:

                All for Unknown vendor extension
        
    - #### JS 
    
        JS checked was done with [JSHint, a JavaScript Code Quality Tool](https://jshint.com/)
        - base.js

            ![](readme_file/base-js-jshint.jpg)

            - One undefined variable:
            
                $ - jquery function.

        - owl.initializer.js

            ![](readme_file/owl.initializer-js-jshint.jpg)

            - One undefined variable:
            
                $ - jquery function.

        - reviews.js

            ![](readme_file/reviews-js-jshint.jpg)

            - One undefined variable:
            
                $ - jquery function.

        - countryfield.js

            ![](readme_file/countryfield-js-jshint.jpg)

            - One undefined variable:
            
                $ - jquery function.

        - products.js

            ![](readme_file/products-js-jshint.jpg)

            - One undefined variable:
            
                $ - jquery function.

        - image.widget.js

            ![](readme_file/image.widget-js-jshint.jpg)

            - One warning:

                - 'template literal syntax' is only available in ES6 (use 'esversion: 6').

            - One undefined variable:
            
                $ - jquery function.

        - quantity_input_script.html

            ![](readme_file/quantity_input_script-js-jshint.jpg)

            - Three warnings:

                - 'template literal syntax' is only available in ES6 (use 'esversion: 6').

            - One undefined variable:
            
                $ - jquery function.

        - stripe_elements.js 


            ![](readme_file/stripe_elements-js-jshint.jpg)

            - Two warnings:

                - 'template literal syntax' is only available in ES6 (use 'esversion: 6').

            - Two undefined variable:
            
                $ - jquery function.

                Stripe - instance of the Stripe object

        - bag.js

            ![](readme_file/bag-js-jshint.jpg)

            - One warning:

                - 'template literal syntax' is only available in ES6 (use 'esversion: 6').

            - One undefined variable:
            
                $ - jquery function.

    - #### PEP8 
    
        [PEP8 Validator](http://pep8online.com/) was used to validate Python code

        - All files pass.

            ![](readme_file/pep8-online.jpg)




[Back to Top](#table-of-contents)
-----

- ### Lighthouse in Chrome DevTools 

    - Desktop test

        | Pages                                | Performance | Accessibility | Best Practices | SEO |
        | :----------------------------------- | :---------: | :-----------: | :------------: | :-: |
        | Home Page                            |     63      |       93      |        93      |  90 |
        | Products Page                        |     94      |       90      |        93      |  90 |
        | Product Detail Page                  |     88      |       73      |        93      |  90 |
        | Wishlist Page                        |     98      |       89      |        93      |  90 |
        | Review Page                          |     91      |       92      |        93      |  90 |
        | Register Page                        |     98      |       89      |        93      |  90 |
        | Login Page                           |     98      |       89      |        93      |  90 |
        | Profile Page                         |     89      |       78      |        93      |  90 |
        | Product Management Page              |     97      |       81      |        93      |  90 |
        | Edit Product Page                    |     97      |       81      |        93      |  90 |
        | Shopping Bag Page                    |     92      |       80      |        93      |  90 |
        | Checkout Page                        |     81      |       88      |        93      |  90 |
        | Checkout Success Page                |     90      |       89      |        93      |  90 |
        | Contact Page                         |     98      |       92      |        93      |  90 |

    - Mobile test

        | Pages                                | Performance | Accessibility | Best Practices | SEO |
        | :----------------------------------- | :---------: | :-----------: | :------------: | :-: |
        | Home Page                            |     62      |       91      |        93      |  90 |
        | Products Page                        |     73      |       95      |        87      |  89 |
        | Product Detail Page                  |     56      |       70      |        87      |  92 |
        | Wishlist Page                        |     76      |       98      |        87      |  90 |
        | Review Page                          |     77      |       95      |        87      |  92 |
        | Register Page                        |     83      |       95      |        93      |  91 |
        | Login Page                           |     79      |       95      |        93      |  89 |
        | Profile Page                         |     69      |       83      |        93      |  91 |
        | Product Management Page              |     79      |       88      |        93      |  91 |
        | Edit Product Page                    |     79      |       88      |        93      |  92 |
        | Shopping Bag Page                    |     79      |       76      |        87      |  90 |
        | Checkout Page                        |     58      |       96      |        87      |  92 |
        | Checkout Success Page                |     74      |       97      |        93      |  91 |
        | Contact Page                         |     83      |       97      |        93      |  91 |


[Back to Top](#table-of-contents)
-----

- ### Browser compatibility and responsiveness

  - #### Testing on Different Browsers

    - The following web browsers were used for testing the browser compatibility and responsiveness (System: Windows 10 64-bit).

        1. Chrome - Version 92.0.4515.159 (Official Build) (64-bit)

        2. Firefox - 91.0.1 (64-bit)

        3. Edge - Version 92.0.902.78 (Official build) (64-bit)

        4. Opera - Version:78.0.4093.147

        All test was good. 

        Note: No test was performed for Internet Explorer.

  - #### Testing on Different Devices

    1. iPhone 11 - IOS 14.0.1

    2. Ipad Mini 2 - IOS 12.4.8 

    3. Huawei P Smart

  - A large amount of testing was done to ensure that all pages were linked correctly.

[Back to Top](#table-of-contents)
-----

- ### Testing User Stories

    I.	First Time Visitor Goals:

    - To be able to quickly understand the purpose of the website. 

        - Immediatly after the home page loads the user quickly understands the purpose of the website from the welcome text, call to action button and even the hero image 

    - To be able to quickly identify new products and sales.

        - On the home page, there are two carousels one with New Arrival products and one with Now on Sale. Also on the navigation menu on special offers, users can find New arrival or Sale products

    - To be able to know if there is a free delivery

        - Under the navigations menu there is a banner that informs the users about the free delivery

    - To be able to know if there is a free return

        - Under the navigations menu there is a banner that informs the users about the free return

    - To be able to view a specific category of products and use filters inside that category.

        - On the navigation menu, there are many categories from which the user can choose. Once they navigate to a specific category the user can use the ```sort menu``` the filter the products

    - To be able to view product details and reviews from other customers.

        - Once the user clicks on a product it will be redirect to product detail page where they can find the product description, and from the tab menu the user can choose to read the product reviews

    - To be able to adjust the product quantity from shopping bag

        - There is implemented functionality so that users can adjust the quantity of each product from the shopping bag

    - To be able to remove a product from shopping bag

        - There is implemented functionality so that users can remove each product from the shopping bag

    - To be able to receive confirmation after purchase a product.

        - After the user complete the secure checkout successuful an confimation email with user detail and order detail is send to the email that was used on complete purchase form

    - To be able to contact the company and subscribe to newsletter to receive the latest offers

        - On the footer of each page the user can subscribe the our newsletter and can use the link to contact page for any query

    II.	Returning User Goals:

    - To be able to register for an account and receive confirmations after.

        - The website has the functionality for the user to register for an account and they will receive and email for confirmation. Once they will confirm the email the account will be ready to use.

    - To be able to easy loggin, logout and easily recover my password

        - The user can loggin very easy and quickly with no hassle and they can use the ```Forget Password``` link from login page to reset their password

    - To have a user profile where I keep track of my orders, my query and update personal information

        - Once the user register for an account they will have a profile page from where they can update the personal details, view order history(if any) and view all the queries that they send thru contact form(if any)

    - To be able to create a wishlist so I can review it later

        - Once the user register for an account they can now add products to their wishlist

    - To be able to leave reveiw for specific product, and be able to edit or delete the review

    III.	Site Owner Goals:

    - To be able to add, edit and delete products

        - The site owner, once he is login, can add product from the product management page, they can edit each product either by pressing the edit button on the products page or from product detail page. They also can delete a product from the products page or product detail page once they can confirm the delete.

    - To be able to add, edit and delete categories.

        - The site owner can add, edit or delete categories only from the admin dashboard.

    - Be able to have access to admin section

        - The site owner will have access to the admin dashboard, but some features will be read-only like the order number, order price and few more

    - Have a secure online payment

        - The secure checkout payment is build with Stripe Payments which is a payment processing platform

    - Send confirmation order for each purchase with order and customer details

        - After each purchase an confirmation email it's send with user and order details
    

[Back to Top](#table-of-contents)
-----

- ### Manual testing

    - Testing all links from the navigation bar

        - Expected: Once each link is pressed it has to redirect to each specific page. Logo to redirect the home page.

        - Result: All links were working correctly.

    - Testing all call to actions links from the ```Home``` page

        - Expected: Each link that is pressed it has to redirect to each specific page.

        - Result: All call to actions links are working correctly.

    - Testing product links from each carousel

        - Expected: Each product that is pressed has to redirect to his specific product detail page.

        - Result: As expected the product redirects to his specific product detail page.

    - Testing sort on all products page

        - Expected: The products are to be sorted by each filter accordingly and in the direction that the user has choosing, ascending or descending

        - Result: As expected the sorting filter, either by name, category, brand, or price, and the direction chosen by users are displayed correctly

    - Testing search form

        - Expected: Return all products that contain the query word in: product brand, name or description 

        - Result: The query result is as expected

    - Testing sort on search query

        - Expected: Sort the query result without loosing the search query

        - Result: The sort is working as expected

    - Testing pagination with sort on search query

        - Expected: Have the same query search with the sort filter use the paginations with loosing the search query or sort filter

        - Result: The paginations is working as expected without loosing any search or sort parameter

    - Testing all links from the breadcrumb

        - Expected: Once each link is pressed from the navigational hierarchy it has to redirect to each specific page

        - Result: All links were working correctly.

    - Testing ```Keep shopping``` and ```Add to bag``` buttons from product detail page

        - Expected 1: The ```Keep shopping``` button should redirect to products page

        - Expected 2: The ```Add to bag``` button should add the product to shopping bag

        - Result: As expected the ```Keep shopping``` and ```Add to bag``` buttons are working correctly.

    - Testing adjust quantity from product detail and shopping bag page

        - Expected: The product quantity should increase/decrease in quantity when user uses the increase/decrease buttons

        - Result: As expected the increase/decrease buttons on both pages are working correctly.

    - Testing review sections for unregister users:

        - Expected: The unregister users can see all the reviews that other users write for a particular product, but then can write any reviews until they sign in. Two links will be display the unregister users: ```sign in``` or ```sign up```

        - Result: As expected the unregister users can see only the reviews for the specific product and the two links for ```sign in``` or ```sign up```, the button for write a review is not display.

        ![](readme_file/product-detail-review-unregister-user.jpg)

    - Testing wishlist page and wishlist buttons from products page and product detail page for unregister users:

        - Expected: All button for Add to wishlist from product page and product detail page are not display for unregister user, and on wishlist page the two links for ```sign in``` or ```sign up``` will be displayed.

        - Result: As expected the unregister users can see only the add to sihlist buttons and on the wishlist page the two links for ```sign in``` or ```sign up``` are displayed.

        ![](readme_file/wishlist-unregister-user.jpg)

    - Testing update quantity on shopping bag

        - Expected 1: Once the quantity on product is increase/decrease and the update button is pressed the subtotal and total price on the shopping bag should reflect the price base on the new quantity

        - Expected 2: If the user wants to add to the bag a product that already is in the bag the quantity is increasing accordingly

        - Result: As expected the update quantity on shopping bag page are working correctly.

    - Testing remove specific product from shopping bag

        - Expected: Once the remove button from a specific product is press that product will be remove from shopping bag

        - Result: As expected when remove button is press the right product is remove from the bag

    - Testing Complete order for unregister users

        - Expected: Once the order is complete and it's successuful an success message will be show to the user that an email cofirmation it's send to the email address provided on the checkout form.

        - Result: As expected an message will confirm to the user that the order complete and the email it's send to the address provided
    
        ![](readme_file/order-confirmation.jpg)
        
        ![](readme_file/email-confirmation.jpg)

        ![](readme_file/stripe-payment-intent.succeeded.jpg)

        ![](readme_file/order-confirmation-admin-dashboard.jpg)
        

    - Testing register to website

        - Expected: When a user is registered to the website a message with the confirmation that the verification email has been sending to his address will be shown on the screen and an email sent to his address

        - Result: As expected after filling the sign up form a message pop up on the screen with the confirmation that the email for verify has been send to my address

        ![](readme_file/register-verify-email-address.jpg)

        ![](readme_file/register-email-address.jpg)
        

    - Testing show the wishlist buttons

        - Expected: Once the user is sign in on the products and product detail page show the wishlist button, and the links to sign in and sign up from wishlist are now hidden and the user can start create his wishlist

        - Result: As expected after user sign in the button are visible for the user to create his wishist

        ![](readme_file/wishlist-btn-products-page.jpg)
        
        ![](readme_file/wishlist-btn-product-detail.jpg)

        ![](readme_file/wishlist-new-user.jpg)

    - Testing adding to wishlist

        - Expected: Once the user adds a product to wishlist a confirmation message is show on the screen and the wishlist icon is displaying how many products he has in the list

        - Result: As expected the confirmation message is shown and on the icon is display the numbers of product in his wishlist

        ![](readme_file/wishlist-add-product.jpg)

        ![](readme_file/wishlist-page.jpg)

    - Testing removing from wishlist

        - Expected: The user can remove products from wishlist from: products page, product detail and wishlist page by pressing the wishlist button and on the screen is show a message that the product has been remove

        - Result: As expected the confirmation message is shown that the product has been removed, and the wishlist and display number on the wishlist icon reflects that

        ![](readme_file/wishlist-remove-product.jpg)


    - Testing order history in user profile

        - Expected: After the user purchase a product, a confirmation message on the screen it shown, an email it send and the order is save on the user profile for his history

        - Result: As expected everything is working correctly message are been display and email send and the profile order history is reflecting the purchase order.

        ![](readme_file/profile-order-history.jpg)

    - Testing link to order detail from order history

        - Expected: When user click on the order detail it will redirect to the specific order detail page and a message is display that this is a past confirmation

        - Result: Everything is working as expected

    - Testing adding review for login users

        - Expected: After user is login he can leave a review for each specific product from product detail page from the review tab. After review is submited a message is show that a review has been added to that product, user can go back using back to product button, and now he can see his review on the tab reviews with the functionality to edit or delete the review.

        - Result: Everything is working as expected

        ![](readme_file/product-add-review.jpg)

    - Testing editing other users review

        - Expected: When the user is trying to edit other users review and error message is show on the screen and the request is stopped immediatly.

        - Testing: Login on different brower with the user gmayer2021 and taken the edit link from the first review 

        - Result: After paste in the link into initial browser an error message is show on the screen and the request is stopped immediatly.

        ![](readme_file/product-edit-other-user-review.jpg)


    - Testing deleting other users review

        - Expected: When the user is trying to delete other users review and error message is show on the screen and the request is stopped immediatly.

        - Testing: Login on different brower with the user gmayer2021 and taken the delete link from the first review 

        - Result: After paste in the link into initial browser an error message is show on the screen and the request is stopped immediatly.

        ![](readme_file/product-delete-other-user-review.jpg)

        - Testing user editing his own review

        - Expected: When the user press the edit link on his review he his redirect to edit review page and a alert message on the screen that his edditing a review is shown. After submitting is successufull the user is redirect back to product detail page where he can see his review and a confirmation message is show on the screen also

        - Result: Everything is working as expected

        ![](readme_file/product-edit-own-review.jpg)

        ![](readme_file/product-update-own-review.jpg)


    - Testing user deleting his own review

        - Expected: When the user is trying to delete other users review and error message is show on the screen and the request is stopped immediatly.

        - Testing: Login on different brower with the user gmayer2021 and taken the delete link from the first review 

        - Result: After paste in the link into initial browser an error message is show on the screen and the request is stopped immediatly.

        ![](readme_file/product-delete-own-review-confirmation.jpg)

        ![](readme_file/product-delete-own-review-success.jpg)

    - Testing admin add product

        - Expected: After the admin fills the add product form with all requirements details, the product should appear in products page, on search and on the category the was selected and be able to see the product detail page.

        - Result: As expected the product was uploaded successufull

        ![](readme_file/admin-add-product.jpg)

        ![](readme_file/admin-add-product-search.jpg)

    - Testing admin edit product

        - Expected 1: Change the price of the product to more then 6 digits and click update product. The form should raise an error 

        - Expected 2: Change the price of the product to more less than initial price and update product. The form should validate

        - Result: As expected in both cases the result is working correctly.

        ![](readme_file/admin-edit-product-error.jpg)

        ![](readme_file/admin-edit-product-success.jpg)

    - Testing admin delete product

        - Expected 1: When the admin wants to delete a product a modal is shown and ask for confirmation before actially deleting the product

        - Expected 2: After the admin confirm the delete product the product should delete from our database and the page should redirect to products page

        - Result: As expected in both cases the result is working correctly.

        ![](readme_file/admin-delete-product-confirmation-box.jpg)

        ![](readme_file/admin-delete-product-message.jpg)

        ![](readme_file/admin-delete-product-search-box.jpg)

    - Testing stripe payment with [Stripe testing cards](https://stripe.com/docs/testing)

        - Expected 1: First we choose not to autheticate and the payment should faild

        - Expected 2: Now we authenticate and the payment should not be process due to insuficient funds

        - Result: As expected the payment faild

        Fail authentication

        ![](readme_file/stripe-payment-fail-authentication.jpg)

        ![](readme_file/stripe-payment_intent.payment_failed.jpg)

        ![](readme_file/stripe-no-authenticate.jpg)

        Complete authentication

        ![](readme_file/stripe-charge-faild.jpg)

        ![](readme_file/stripe-insuficient-funds.jpg)


[Back to Top](#table-of-contents)
-----

- ### Bugs and Fixes

    - During the set up of the project for deploy to heroku after I set up the ```DATABASE_URL``` in ```settings.py``` I got an error on the terminal: 

        ```
        django.db.utils.OperationalError: FATAL:  role "" does not exist on heroku postgres
        ```

        - To fix: After I did few reasearh on the SLACK Community I found that in the Full Template, from Code Institute, there is a PGHOSTADDR local variable that has been added to accommodate for the new SQLAlchemy lessons. In order to run showmigrations and migrate after we need to run the terminal this command:

        ```
        unset PGHOSTADDR
        ```

        - After that I could complete set up the Heroku Postgres

    - After I deploy to heroku I got an application error from heroku check your logs

         After I check the logs and see the build I see that the Procfile was not set up correctly and was an error on the Procfile itself: 

        ```
        web: gunicorn gentleman_mayer.wsgi.application
        ```

        - To Fix: It sems that was a typo in Procfile as before application suppose to be ```:``` and not a dot ```.```

        ```
        web: gunicorn gentleman_mayer.wsgi:application
        ```


    - After deploy to Heroku I got error 400 when open the application

        - To fix: I set up the Debug to True on the Heroku Config Vars and restart the application. It semse that the error was from base.js script as it had a trailling slash in front of the path. 

        - After I remove the slash the aplication was working fine

    - During Development after creating the Contact and Newsletter app after few test and set up, when I change the DATABASE_URL for Heroku Postgres to run the migrations with if statemenet I got an error when trying to run ```showmigrations```:

        ```
        django.core.exceptions.ImproperlyConfigured: settings.DATABASES is improperly configured. Please supply the NAME value.
        ```

        - The site was loading fine on Gitpod with SQLite3 but would start with DATABASE_URL variable to connect to heroku.

            - After I did few reasearh on the SLACK Community it simce that if I run 
        
        ```
        echo $DATABASE_URL
        ```
        in the terminal we get back an response that gitpod already set the 
        
        ```
        postgresql://gitpod@localhost
        ```

        and was given an error because was not a Postgres URL

        - To fix: run in the terminal

            ```
            unset DATABASE_URL
            ```

    - After set up the Gmail account to send email I receive two email at once every times when was doing the test

        - ![](readme_file/double-emails-error.jpg)

        - It seems that in the Heroku website I had the same variable names in Config Vars on two apps.

        To Fix: I have change all the variable name from the current project to make sure there is no conflict and after I test send emails again

        As expected I receive only one email from the current project

    - After making few more test on the reviews page I notice that was a flaw in my UX design and the design it breaking apart

        As you can see my initial UX design was not quite fully tested and I was happy how it looks

        - ![](readme_file/reviews-page-initial-design.jpg)

        After user is login the UX design it starts to break

        - ![](readme_file/reviews-page-flow-in-ux-design-2.jpg)

        And if I added a long review to the product it breaks apart

        - ![](readme_file/reviews-page-flow-in-ux-design.jpg)

        To Fix: After the main col that was render by the forloop I have added another div with display flex so I can make some elements within the colunm streach to take the parent full height:

        - First I added:
        ```
        <div class="position-relative d-flex flex-column border-0 rounded-0 h-100">
        ```
        - Second I wrapped the row that hold the description, user and date into another div:

        ```
        <div class="card-body p-0">
        ```
        - Third I have added to the row that was wrapped by card-body the class h-100

        ```
        <div class="row h-100
        ```
       - ![](readme_file/review-page-ux-fix.jpg) 

       NOTE: Basically, it is the same approach that a card has but the reason that I used the ```position-relative d-flex flex-column``` classes instead of the ```card``` class which basically contains all three plus more, is because of  ```word-wrap: break-word;``` which basically break the stars design, and that was taken from see credit, and to fix I suppose to add another class with property   ```word-wrap: inherit;``` to override the one on the card, which was too much

    - Stars from the review not showing the correct rating on tablets and phone

        As you can see on the desktop the stars are showing with no flaw what so ever, but on tablet and phone the design starts to break as the tip of the stars on top and bottom does not show and the color of rating is not showing the correct star rating

        Desktop/laptop

        - ![](readme_file/rating-stars-desktop.jpg)

        Tablet

        - ![](readme_file/rating-stars-tablet.jpg)

        Phone

        - ![](readme_file/rating-stars-phone.jpg)

        To Fix: I have remove from base.css on the class .star-ratings-css the following

        ```
            height: 25px;
            width: 100px;
            line-height: 0.8;
        ```

        and added instead 

        ```
            width: -webkit-min-content;
            width: -moz-min-content;
            width: min-content;
        ```

        To keep the stars in the same line with the title review I have added ```pt-2``` class to the title review column

        NOTE: To keep the star design clean and match with the site I have remove ```text-shadow: 0px 1px 0 #a2a2a2;``` from .star-ratings-css as well
  
    
> NOTE: No other bugs that I'm aware of were left unsolved.

Return to [README.md](README.md)