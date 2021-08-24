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
        

    - Testing 

        - Expected:

        - Result:

[Back to Top](#table-of-contents)
-----

- ### Bugs and Fixes

    - 

        - To fix: 

    
    > NOTE: No other bugs that I'm aware of were left unsolved.

Return to [README.md](README.md)